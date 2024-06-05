from django.contrib import admin
from django.urls import path, include
from account.views import user_list

urlpatterns = [
    path('admin/user-list/', user_list, name='user_list'),
    path('admin/', admin.site.urls),
    path('api/user/', include('account.urls')),
]
