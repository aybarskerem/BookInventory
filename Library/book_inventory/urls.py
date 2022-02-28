from django.urls import re_path
from book_inventory import views  
 
urlpatterns = [ 
    
    # API PAGES (drf)
    # re_path(r'^api/books/?$', views.book_inventory, name='book_inventory'),
    re_path(r'^api/books/?$', views.BookInventoryView.as_view(), name='book_inventory'),
    # re_path(r'^api/books/(?P<id>(\d+))/?$', views.book_details, name='book_details'),
    re_path(r'^api/books/(?P<id>(\d+))/?$', views.SelectedBookView.as_view(), name='book_details'),

    # REGULAR PAGES
    re_path(r'^books/(?P<id>(\d+))/?$', views.list_one, name='list_one'),
    # re_path(r'^(?:books)?/?$', views.list_all, name='list_all'),
    re_path(r'^books/?$', views.list_all, name='list_all'),
    re_path(r'^$',        views.list_all, name='list_all'),
]   
