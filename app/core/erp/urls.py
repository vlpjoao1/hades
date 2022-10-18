from django.urls import path
from core.erp.views.category.views import category_list, CategoryList, CategoryCreateView, CategoryUpdateView, \
    CategoryDeleteView, CategoryFormView
from core.erp.views.dashborad.views import DashboardView
from core.erp.views.product.views import ProductList, ProductCreateView, ProductUpdateView, ProductDeleteView

urlpatterns = [
    path('category/list/', CategoryList.as_view(), name='category_listview'),
    path('category/Create/', CategoryCreateView.as_view(), name='category_createview'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_updateview'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_deleteview'),
    path('category/form/', CategoryFormView.as_view(), name='category_formview'),
    #product
    path('product/list/', ProductList.as_view(), name='product_listview'),
    path('product/Create/', ProductCreateView.as_view(), name='product_createview'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_updateview'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_deleteview'),
    #dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
