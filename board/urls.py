from django.urls import path
from . import views


urlpatterns = [
    path('', views.ad_list, name='ad_list'),
    path('create/', views.ad_create, name='ad_create'),
    path('<int:pk>/', views.ad_detail, name='ad_detail'),
    path('<int:pk>/update/', views.ad_update, name='ad_update'),
    path('<int:pk>/delete/', views.ad_delete, name='ad_delete'),

    path('func/', views.func, name='func'),
    path('load_temp/', views.load_temp, name='load_temp'),
    path('select_temp/', views.select_temp, name='select_temp'),
    # path('rend_t_str/', views.rend_t_str, name='rend_t_str')
    path('req_methods/', views.req_methods, name='req_methods'),
    path('save_item/', views.save_item, name='save_item'),
    path('site_moved/', views.site_moved, name='site_moved'),
    path('gz/', views.gz, name='gz'),
    path('n/', views.DBList.as_view(), name='n')
]
