from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('rooms/', views.getRooms),
    path('rooms/<str:pk>', views.getRoom),
    path('users/<str:key>', views.getUsers),
    path('delete_user/<str:pk>/<str:key>', views.deleteUser)]