from django.urls import path
from store import views
urlpatterns = [
    path('', views.index.as_view(), name="index"),
    path('index/', views.index.as_view(), name="index"),
    path('login/', views.login, name="login"),
    path('validate_login/', views.validate_login, name="validate_login"),
    path('logout/', views.logout, name="logout"),
    path('signup/', views.signup, name="signup"),
    path('validate/', views.validate, name="validate"),
    path('search/<slug:slug>/', views.category_list, name='category_list'),
    path('<int:id>/', views.productdetails, name='product_detail'),
    path('cart/', views.cart.as_view(), name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),

]