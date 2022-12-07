
from django.urls import path

from core.login.views import *

urlpatterns = [
    path('', LoginFormView.as_view(), name='login'),
    #from django
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    #path('logout2/', LogoutRedirectView.as_view(), name='logout'),
    path('reset/password/', ResetPasswordView.as_view(), name='reset_password'),
]