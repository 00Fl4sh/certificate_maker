from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView  # Import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('certificates/', include('certificates.urls')),
    path('', TemplateView.as_view(template_name='nav.html'), name='nav'),  # Add this line
    path('', TemplateView.as_view(template_name='create_certificate.html'), name='create'),  # Add this line
    path('', TemplateView.as_view(template_name='verify_certificate.html'), name='verification'),  # Add this line
]
