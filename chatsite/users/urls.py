from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('add-member/<str:room_name>', views.AddMemberView.as_view(), name='add_member'),
    path('leave_chat/<int:room_id>/', views.leave_chat, name='leave_chat'),
]