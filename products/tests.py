from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Product


class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            p_sku="SKU-001",
            description="Test product",
            quantity=10,
            location="Aisle 1",
            action="None",
        )

    def test_str(self):
        self.assertEqual(str(self.product), "SKU-001")

    def test_default_ordering(self):
        p2 = Product.objects.create(
            p_sku="SKU-002", description="Another", quantity=5, location="Aisle 2", action="None"
        )
        products = list(Product.objects.all())
        self.assertEqual(products[0], p2)


class IndexViewTest(TestCase):
    def setUp(self):
        Product.objects.create(p_sku="A", description="desc", quantity=3, location="L", action="N")
        Product.objects.create(
            p_sku="B", description="desc2", quantity=7, location="L2", action="N"
        )

    def test_get_200(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_context_counts(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.context["product_count"], 2)
        self.assertEqual(response.context["total_units"], 10)

    def test_empty_inventory_total_units_zero(self):
        Product.objects.all().delete()
        response = self.client.get(reverse("index"))
        self.assertEqual(response.context["total_units"], 0)


class AboutViewTest(TestCase):
    def test_get_200(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)


class SuperuserRequiredViewsTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser("admin", "a@a.com", "pass")
        self.regular = User.objects.create_user("user", "u@u.com", "pass")
        self.product = Product.objects.create(
            p_sku="SKU-X", description="desc", quantity=1, location="L", action="N"
        )

    def test_addnew_redirects_anonymous(self):
        response = self.client.get(reverse("product_add"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response["Location"])

    def test_addnew_redirects_regular_user(self):
        self.client.login(username="user", password="pass")
        response = self.client.get(reverse("product_add"))
        self.assertEqual(response.status_code, 302)

    def test_addnew_get_superuser(self):
        self.client.login(username="admin", password="pass")
        response = self.client.get(reverse("product_add"))
        self.assertEqual(response.status_code, 200)

    def test_addnew_post_creates_product(self):
        self.client.login(username="admin", password="pass")
        count_before = Product.objects.count()
        response = self.client.post(
            reverse("product_add"),
            {
                "p_sku": "NEW",
                "description": "new prod",
                "quantity": 5,
                "location": "B2",
                "action": "N",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), count_before + 1)

    def test_edit_get_superuser(self):
        self.client.login(username="admin", password="pass")
        response = self.client.get(reverse("product_edit", args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_update_post_superuser(self):
        self.client.login(username="admin", password="pass")
        response = self.client.post(
            reverse("product_update", args=[self.product.id]),
            {
                "p_sku": "SKU-X",
                "description": "updated",
                "quantity": 99,
                "location": "L",
                "action": "N",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 99)

    def test_delete_post_superuser(self):
        self.client.login(username="admin", password="pass")
        pid = self.product.id
        response = self.client.post(reverse("product_delete", args=[pid]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(pk=pid).exists())

    def test_delete_get_not_allowed(self):
        self.client.login(username="admin", password="pass")
        response = self.client.get(reverse("product_delete", args=[self.product.id]))
        self.assertEqual(response.status_code, 405)
