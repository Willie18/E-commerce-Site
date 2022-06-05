from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.

class UserAccountTests(TestCase):
    
    def test_new_superuser(self):
        db=get_user_model()
        superuser=db.objects.create_superuser(
            "test@superuser.com","testsuperuser","password"
        )
        self.assertEqual(superuser.email,"test@superuser.com")
        self.assertEqual(superuser.username,"testsuperuser")
        self.assertEqual(str(superuser),"testsuperuser")
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_active)
        
        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email="test@superuser.com",username="testsuperuser",password="password",is_superuser=False
            )
        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email="test@superuser.com",username="testsuperuser",password="password",is_staff=False
            )
    def test_new_user(self):
        db=get_user_model()
        user=db.objects.create_user(
            "test@user.com","testuser","password"
        )
        self.assertEqual(user.email,"test@user.com")
        self.assertEqual(user.username,"testuser")
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        
        with self.assertRaises(ValueError):
            db.objects.create_user(
                email="",password="password",username="username"
            )

