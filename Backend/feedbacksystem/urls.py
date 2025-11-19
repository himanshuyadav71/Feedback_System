from django.contrib import admin
from django.urls import path
from feedback_app import views as feedback_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tables/', feedback_views.list_tables, name='list_tables'),
    path('users/', feedback_views.list_users, name='list_users'),
]
