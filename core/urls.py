from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import ProfileCreateAPIView, LoginView, RefreshTokenView, PasswordChangeView, SearchLieuView


urlpatterns = [

    ### Home
    path('register/', ProfileCreateAPIView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh_token/', RefreshTokenView.as_view(), name='refresh_token'),
    path('change_password/', PasswordChangeView.as_view(), name='change_password'),
    path('suggest/', SearchLieuView.as_view(), name='suggest'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)