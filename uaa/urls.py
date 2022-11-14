from django.urls import path
from . import views

#paths for account app.
urlpatterns = [
    path('',views.LoginView, name='login_url'),
    path('logout',views.LogoutView, name='logout_url'),
    path('registrationNoView',views.RegistrationNoView, name='registrationNoView_url'),
    path('addRegNo',views.AddRegNoView, name='addRegNo_url'),
    path('register/',views.RegisterView, name="register_url"),
    path('addUser/',views.AddUserView, name='addUser_url'), 
    path('updateUserView/<str:pk>',views.UpdateUserView, name='updateUserView_url'),
    path('dashboard/',views.DashboardView, name='dashboard_url'),
    
    path('profile/',views.ProfileView, name='profile_url'),
    path('update_profile/',views.UpdateProfileView, name='update_profile_url'),
    path('allUsers/',views.AllUsersView, name='allUsers_url'), 
    path('updatePasswordView/',views.UpdatePasswordView, name='updatePasswordView_url'),
    path('forgotPasswordView/',views.ForgotPasswordView, name='forgotPasswordView_url'),
    path('resetPasswordView/',views.ResetPasswordView, name='resetPasswordView_url'),
    path('userStatusView/',views.UserStatusView, name='userStatusView_url'),  
    path('tipButtonView/',views.TipButtonView, name='tipButtonView_url'),
    path('tipView/',views.TipView, name='tipView_url'), 
    path('manageTip/', views.ManageTipsView, name="manageTip_url"),
    path('deleteTips/<str:pk>', views.DelateTipsView, name="deleteTips_url"),
]