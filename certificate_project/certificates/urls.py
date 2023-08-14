from django.urls import path
from . import views

urlpatterns = [
    path('create_certificate/', views.create_certificate, name='create_certificate'),
    path('customize_certificate/', views.customize_certificate, name='customize_certificate'),
    path('certificate_detail/<int:certificate_id>/', views.certificate_detail, name='certificate_detail'),
    path('home/', views.home, name='home'),
    path('verify_certificate/', views.verify_certificate, name='verify_certificate'),
    path('verify_with_token/<int:certificate_id>/<str:token>/', views.verify_with_token, name='verify_with_token'),
    path('certificate_detail/<int:certificate_id>/download/', views.DownloadCertificateView.as_view(), name='download_certificate'),

    
    
    # Other URL patterns
]
