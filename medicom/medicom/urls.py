from django.contrib import admin
from django.urls import include, path
# Removing Authentication from admin panel
from django.contrib import admin
from django.contrib.auth.models import User, Group

#admin.site.unregister(User)
#admin.site.unregister(Group)


urlpatterns = [
    path('', include('online_pharmacy.urls')),
    path('admin/', admin.site.urls),

]
