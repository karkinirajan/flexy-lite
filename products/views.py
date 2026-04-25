from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ProductForm
from .models import Product


def is_superuser(user):
    return user.is_authenticated and user.is_superuser


def index(request):
    products = Product.objects.all()
    inventory_summary = products.aggregate(total_units=Sum("quantity"))
    context = {
        "products": products,
        "product_count": products.count(),
        "total_units": inventory_summary["total_units"] or 0,
    }
    return render(request, "index.html", context)


def about(request):
    return render(request, "about.html")


@user_passes_test(is_superuser)
def addnew(request):
    form = ProductForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Product created successfully.")
        return redirect("index")
    return render(
        request,
        "edit.html",
        {
            "form": form,
            "page_title": "Add product",
            "submit_label": "Create product",
        },
    )


@user_passes_test(is_superuser)
def edit(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(instance=product)
    return render(
        request,
        "edit.html",
        {
            "form": form,
            "product": product,
            "page_title": "Edit product",
            "submit_label": "Save changes",
        },
    )


@user_passes_test(is_superuser)
def update(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Product updated successfully.")
        return redirect("index")
    return render(
        request,
        "edit.html",
        {
            "form": form,
            "product": product,
            "page_title": "Edit product",
            "submit_label": "Save changes",
        },
    )


@user_passes_test(is_superuser)
@require_POST
def destroy(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    messages.success(request, "Product deleted.")
    return redirect("index")
