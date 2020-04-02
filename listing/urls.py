from django.urls import path
from . import views

urlpatterns = [
    path('', views.listing_list, name='listing_list'),
    path('listing/create', views.create_listing, name='create_listing'),
    path('listing/edit/<int:listing_id>', views.edit_listing, name='edit_listing')
]