from django.urls import path
from core.user.views import UserListView, UserCreateView

app_name = 'user'

urlpatterns = [
    #user
    path('list/', UserListView.as_view(), name='user_listview'),
    path('create/', UserCreateView.as_view(), name='user_createview'),
]
