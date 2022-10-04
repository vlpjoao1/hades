from django.urls import path
from core.erp.views.category.views import category_list, CategoryList, CategoryCreateView, CategoryUpdateView, \
    CategoryDeleteView, CategoryFormView

urlpatterns = [
    path('category/list/',CategoryList.as_view(),name='category_listview' ),
    path('category/Create/', CategoryCreateView.as_view(), name='category_createview'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_updateview'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_deleteview'),
    path('category/form/', CategoryFormView.as_view(), name='category_formview'),
]
