from django.urls import path
from . import views


urlpatterns = [
    path('', views.show_brand_models, name='show_brand_models'),
    path('update_autoru_catalog/', views.update_brand_models, name='update_brand_models'),
]
