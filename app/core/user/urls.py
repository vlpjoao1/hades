from django.urls import path
from core.user.views import UserListView, UserCreateView, UserUpdateView, UserDeleteView

app_name = 'user'

urlpatterns = [
    #user
    path('list/', UserListView.as_view(), name='user_listview'),
    path('create/', UserCreateView.as_view(), name='user_createview'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user_updateview'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user_deleteview'),
]
