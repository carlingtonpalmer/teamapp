from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter #is use to handle viewsets
from reset_password import views as view_pass
from django.contrib.auth import views as auth_views


router = DefaultRouter()
# router.register('users', views.CreateUserView) #working just testing new createuserview below


urlpatterns = [
    # users
    path('login/', views.LoginUserApiView.as_view()),
    path('user/<int:pk>/', views.UserUpdateView.as_view()),
    path('register/', views.Register.as_view()),
    path('logout/', views.LogoutUserView.as_view()),
    path('users/', views.UserViewset.as_view()),

    # products
    path('product-cat/', views.ProductCategoryView.as_view()),
    path('product-sub/<slug:slug>/', views.ProductSubCategoryListSlugView.as_view(), name="prod_cat"), # working with slug
    path('product-sub/<slug:slug>/<int:pk>/', views.SingleProductView.as_view(), name="prod_cat"),
    
    # claim forms
    path('', include('claim_forms.urls')),
    
    # claims
    path('', include('claims.urls')),

    # reset password
    path('reset-password-sent/', view_pass.RestPasswordView.as_view()),
    path('reset-password/<uidb64>/<token>', view_pass.ResetPasswordConfirmView.as_view(template_name='../templates/registration/password_reset_form.html'),name='password_reset_confirm'),#
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='../templates/registration/password_reset_complete.html'),name='password_reset_complete'),
    
    # quotes
    path('', include('quotes.urls')),

    # email code confirmation
    path('send-confirm-code/', views.ConfirmEmailView.as_view()),
    path('confirm-code/', views.ConfirmEmailCodeView.as_view()),
    # path('resend-code/', views.ResendCode.as_view()),
]
