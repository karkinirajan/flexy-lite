from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("addnew/", views.addnew, name="product_add"),
    path("edit/<int:id>/", views.edit, name="product_edit"),
    path("update/<int:id>/", views.update, name="product_update"),
    path("delete/<int:id>/", views.destroy, name="product_delete"),
]
