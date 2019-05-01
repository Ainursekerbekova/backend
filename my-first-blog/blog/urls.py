from django.urls import path
from . import views

urlpatterns = [
    #Index
    path('', views.index, name='index'),

    #Search
    path('products/', views.search, name='search'),

    #All products
    path('products/<slug:type>/<slug:order>/', views.products, name="products"),

    #Product details
    path('products/<int:prod_id>/', views.detail, name='detail'),

    #Cart
    path('сart/', views.cart, name="cart"),

    #Delete
    path('cart/', views.delete, name="del"),

    #Change
    path('change/', views.change, name="change"),

    #Buy
    path('buy/', views.buy, name="buy"),

    #Register
    path('register/',views.UserFormView.as_view(), name='register'),

    #Profile
    path('profile/', views.profile, name='profile'),

    #Mail
    path('mail/', views.mail, name='mail'),

    #prod detail
    path('products/<int:prod_id>/<slug:order>/<slug:l>/', views.details, name='details_old'),
]