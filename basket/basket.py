from product.models import Product

import uuid


CART_SESION_ID="skey"

class Basket(object):
    """
    A base Basket class, providing some default behaviors that
    can be inherited or overrided, as necessary.

    """

    def __init__(self, request):
        # request.session.set_expiry(300) #expire after 5 minutes
        self.session = request.session
        self.user=request.user
        basket = self.session.get(CART_SESION_ID)
        if CART_SESION_ID not in request.session:
            basket = self.session[CART_SESION_ID] = {"id":str(uuid.uuid4()),"items":{}}
        self.basket = basket
    def add(self, product, qty=1):
        """
        Adding and updating the users basket session data
    
        """
        if qty<1:
            self.save()
            return
        product_slug = str(product.id)

        if product_slug in self.basket["items"]:
            self.basket["items"][product_slug]['qty'] += qty
            #set the ordered attribute to false
            self.basket["ordered"]=False
        else:
            self.basket["items"][product_slug]= {"qty":qty}
            self.basket["items"][product_slug]["product"]=product.title
            self.basket["items"][product_slug]["product_id"]=product_slug
        self.save()

    def __iter__(self):
        """
        Collect the product_slugs in the session data to query the database
        and return products
        """
        product_slugs = list(self.basket["items"].keys())
        # remove ordered and ordered dates
        if "ordered" in product_slugs:product_slugs.remove("ordered")
        if "ordered_date" in product_slugs:product_slugs.remove("ordered_date")
        products = Product.products.filter(id__in=product_slugs)
        basket = self.basket.copy()

        for product in products:
            basket["items"][str(product.id)]['price'] =int(product.price)

        for item in basket["items"].values():
            qty=0
            if item['qty']<0:pass
            else:qty=item['qty']
            item['total_price'] = int(item['price'] * qty)
            yield item

    def __len__(self):
        """
        Get the basket data and count the qty of items

        """
        return sum(item['qty'] for item in self.basket["items"].values())

    def update(self, productid, productqty):
        """
        Update values in session data

        """
        if productqty<0:productqty=0
        productid=str(productid)
        if productid in self.basket["items"]:
            self.basket["items"][productid]['qty'] = productqty
        self.save()

    def get_total_price(self):
        return int(sum([item['price'] * item['qty'] for item in self.basket["items"].values()]))

    def delete(self, productid):
        """
        Delete one quantity of an item from cart
        """
        product_id = str(productid)

        if product_id in self.basket["items"]:
            self.basket["items"][product_id]["qty"]-=1
        self.save()
    def checkout(self):
        self.save()     
        self.flush() 
    def flush(self):
        self.session.pop(CART_SESION_ID)

    def save(self):
        self.session.modified = True

class Summary(Basket):
    def __init__(self,request) -> None:
        super().__init__(request=request)
    def save(self):
        self.transaction_id=self.basket.get("id","None")
        self.items=list(i for i in self.__iter__() if i["qty"]>0)
        self.price=self.get_total_price()
        return super().save()
        
    def checkout(self):
        self.ordered=True
        # self.basket["ordered"]=True
        return super().checkout()