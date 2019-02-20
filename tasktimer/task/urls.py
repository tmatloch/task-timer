from django.urls import include, path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('tasks/', views.task),
]