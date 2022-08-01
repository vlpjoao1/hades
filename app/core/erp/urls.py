from django.urls import path
from core.erp.views.category.views import category_list, CategoryList

urlpatterns = [
    #path('category/list/', category_list, name='category_list'),
    path('category/list/',CategoryList.as_view(),name='category_listview' )
]
