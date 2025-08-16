from django.urls import path
from . import views


urlpatterns = [
    path('test/', views.test, name='test'),
    path('current_time/', views.current_time, name='current_time'),
    path('test2/', views.some_test, name='some_test'),

    path('', views.index, name='market_index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_p, name='login_p'),
    path('logout', views.logout_p, name='logout_p'),
    path('create_book/', views.create_book, name='create_book'),
    path('books/', views.book_list, name='books_list'),

    path('products/add', views.create_product, name='create_product'),
    path('products/', views.create_product, name='product_list'),
    path('categories/', views.manage_category, name='manage_category'),
    path('categories/<int:category_id>/products', views.edit_category_products, name='edit_category_products'),

    path('book/<int:pk>/', views.book_detail, name='book_detail')
]
