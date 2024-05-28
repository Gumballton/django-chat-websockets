from django.urls import path, reverse_lazy

from django.contrib.auth.views import PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('add-member/<str:room_name>', views.AddMemberView.as_view(), name='add_member'),
    path('leave_chat/<int:room_id>/', views.leave_chat, name='leave_chat'),

    path('change-password/', views.ChangeUserPassword.as_view(), name='change_user_password'),
    path('change-password/done/', PasswordChangeDoneView.as_view(
        template_name='users/change_password_done.html'), name='change_user_password_done'),


    path('password-reset/', PasswordResetView.as_view(
         template_name='users/password_reset_from.html',
         email_template_name='users/reset_email_form.html',
         success_url=reverse_lazy('users:password_reset_done')),
         name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(
         template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url=reverse_lazy('users:password_reset_complete')), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'),
        name='password_reset_complete')
]