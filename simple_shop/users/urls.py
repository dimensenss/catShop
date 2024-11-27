app_name ='users'

from django.urls import path
from users.views import *

urlpatterns = [
    path('signup/', SignUpUserView.as_view(), name='signup'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
]