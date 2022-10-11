from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login_page'),
    path('user-page/', views.user_page, name='user_page'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('customer/<int:customer_id>/', views.customer, name='customer'),
    path('create-order/', views.create_order, name='create_order'),
    path('update-order/<int:order_id>/', views.update_order, name='update_order'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('account-settings/', views.account_settings, name='account_settings'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), name='password_reset_complete')
]
