from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (ProfileCreateView, LoginView, PasswordChangeView, ResetPasswordView, ChangeInfosView,
                SearchLieuView, ProfileChangeView, ForgotPasswordView)


urlpatterns = [

    ### Home
    path('register/', ProfileCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    path('change_password/', PasswordChangeView.as_view(), name='change_password'),
    path('change_profile/', ProfileChangeView.as_view(), name='change_profile'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('suggest/', SearchLieuView.as_view(), name='suggest'),
    path('update/', ChangeInfosView.as_view(), name='update'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)