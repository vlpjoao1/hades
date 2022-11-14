from django.urls import path
from core.user.views import UserListView

app_name = 'user'

urlpatterns = [
    #user
    path('list/', UserListView.as_view(), name='user_listview'),
]
