import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from products.forms import ProductForm
from products.models import Product

DATA = {
    "p_sku": "SKU-1",
    "description": "Rice 5kg",
    "quantity": 10,
    "action": "Restock",
    "location": "Aisle 3",
}


@pytest.fixture
def admin(db):
    return User.objects.create_superuser("boss", "boss@example.com", "pw-12345-xyz")


@pytest.fixture
def staff(db):
    return User.objects.create_user("clerk", "clerk@example.com", "pw-12345-xyz")


@pytest.fixture
def product(db):
    return Product.objects.create(**DATA)


def test_index_shows_counts_and_total_units(client, db):
    Product.objects.create(**DATA)
    Product.objects.create(**{**DATA, "p_sku": "SKU-2", "quantity": 5})
    res = client.get(reverse("index"))
    assert res.status_code == 200
    assert res.context["product_count"] == 2 and res.context["total_units"] == 15


def test_index_with_no_products_reports_zero_units(client, db):
    assert client.get(reverse("index")).context["total_units"] == 0


def test_about_page(client, db):
    assert client.get(reverse("about")).status_code == 200


def test_products_are_listed_newest_first(db):
    first = Product.objects.create(**DATA)
    second = Product.objects.create(**{**DATA, "p_sku": "SKU-2"})
    assert list(Product.objects.all()) == [second, first]
    assert str(first) == "SKU-1"


@pytest.mark.parametrize(
    "name", ["product_add", "product_edit", "product_update", "product_delete"]
)
def test_management_views_reject_anonymous_and_non_superusers(client, staff, product, name):
    url = reverse(name, args=[product.pk]) if name != "product_add" else reverse(name)
    anon = client.post(url, DATA)
    assert anon.status_code == 302 and "login" in anon.url
    client.force_login(staff)
    assert client.post(url, DATA).status_code == 302  # redirected to login, not allowed
    assert Product.objects.count() == 1  # nothing created or deleted


def test_superuser_can_add_a_product(client, admin):
    client.force_login(admin)
    res = client.post(reverse("product_add"), DATA)
    assert res.status_code == 302 and res.url == reverse("index")
    assert Product.objects.get().p_sku == "SKU-1"


def test_add_form_rerenders_on_invalid_input(client, admin):
    client.force_login(admin)
    res = client.post(reverse("product_add"), {**DATA, "quantity": "abc"})
    assert res.status_code == 200 and Product.objects.count() == 0


def test_negative_quantity_is_rejected_by_the_server(client, admin):
    client.force_login(admin)
    res = client.post(reverse("product_add"), {**DATA, "quantity": -3})
    assert res.status_code == 200 and Product.objects.count() == 0
    assert "quantity" in res.context["form"].errors


def test_form_accepts_zero_quantity():
    assert ProductForm(data={**DATA, "quantity": 0}).is_valid()


def test_edit_page_renders_for_superuser(client, admin, product):
    client.force_login(admin)
    assert client.get(reverse("product_edit", args=[product.pk])).status_code == 200


def test_update_changes_the_product(client, admin, product):
    client.force_login(admin)
    res = client.post(reverse("product_update", args=[product.pk]), {**DATA, "quantity": 42})
    assert res.status_code == 302
    product.refresh_from_db()
    assert product.quantity == 42


def test_edit_and_update_404_for_unknown_product(client, admin):
    client.force_login(admin)
    assert client.get(reverse("product_edit", args=[999])).status_code == 404
    assert client.post(reverse("product_update", args=[999]), DATA).status_code == 404


def test_delete_requires_post(client, admin, product):
    client.force_login(admin)
    assert client.get(reverse("product_delete", args=[product.pk])).status_code == 405
    assert Product.objects.count() == 1
    assert client.post(reverse("product_delete", args=[product.pk])).status_code == 302
    assert Product.objects.count() == 0
