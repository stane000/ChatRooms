

from django.urls import path
from . import views

urlpatterns = [
    path("login_register/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerUser, name="register"),
    path("", views.home, name="home"),
    path("room/<str:pk>/", views.room , name="room"),
    path("profile/<str:pk>/", views.userProfile , name="user-profile"),
    path("create-room/", views.create_room , name="create-room"),
    path("update-room/<str:pk>/", views.update_room , name="update-room"),
    path("delete-room/<str:pk>/", views.delete_room , name="delete-room"),
    path("delete-message/<str:pk>/", views.delete_message , name="delete-message"),
    path("update-user/", views.updateUser , name="update-user"),
    path("delete-user/<str:pk>/", views.delete_user , name="delete-user"),
    path("topics/", views.topicsPage , name="topics"),
    path("activity/", views.activityPage , name="activity"),
    path("tic_toe/", views.ticToePage , name="tic_toe"),
]

