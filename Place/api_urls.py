from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Place API",
      default_version='version 1',
      description="Documentation de l'API de l'application de Referencement geographique, au Cameroun",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="parnelltchamba24@gmail"),
      license=openapi.License(name="BSD License"),
   ),
)



urlpatterns = [
    path('', include(('core.urls', 'core'))),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]