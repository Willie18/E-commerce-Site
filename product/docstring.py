def list_products_api_docstring():
    return( """
     ``GET`` lists all relations where an ``Product`` is accessible by
     a ``User``.

    ``POST`` Generates a request to create a Product

     **Example request**:

    .. code-block:: http

    GET  /api/v1/products/ HTTP/1.1

    """)

def post_product_api_docstring():
    return(
    """
    Creates a request to create a new product in the inventory

    """)
def update_product_api():
    return( 
    """
    Creates a request to patch a product in the inventory with the passed details

    ***EXAMPLE REQUEST***

    .. code-block:: http

    /api/v1/products/{1}/ HTTP/1.1" 200 470
    
    """)
