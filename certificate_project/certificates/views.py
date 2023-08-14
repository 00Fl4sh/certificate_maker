from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Certificate, Verification, Customization
from .forms import CertificateForm, CustomizationForm
from .utils import generate_verification_code, generate_jwt_token
from .models import Verification, generate_verification_code
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Certificate
from django.views import View
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def verify_with_token(request, certificate_id, token):
    verification = Verification.objects.filter(
        certificate_id=certificate_id).first()

    if verification:
        generated_token = generate_jwt_token(certificate_id)
        if token == generated_token:
            return render(request, 'certificates/verification_result.html', {'certificate_id': certificate_id, 'success_message': 'Certificate verified successfully.'})
        else:
            messages.error(request, 'Verification failed. Invalid token.')
    else:
        messages.error(request, 'Verification failed. Certificate not found.')

    return redirect(reverse('home'))


class DownloadCertificateView(View):
    def get(self, request, certificate_id):
        certificate = get_object_or_404(Certificate, pk=certificate_id)

        # Create a PDF document
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="certificate_{certificate_id}.pdf"'

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)

        # Set up the positions for text lines
        x = 100
        y = 750
        line_height = 30

        p.drawString(x, y, "Certificate")
        y -= line_height

        p.drawString(x, y, "This is to certify that")
        y -= line_height

        p.drawString(x, y, f"Recipient: {certificate.recipient_name}")
        y -= line_height

        p.drawString(x, y, "has successfully completed the course in")
        y -= line_height

        p.drawString(x, y, f"Course: {certificate.course}")
        y -= line_height

        p.drawString(x, y, f"Issue Date: {certificate.issue_date}")
        # Add more information here

        p.showPage()
        p.save()

        pdf = buffer.getvalue()
        buffer.close()

        response.write(pdf)
        return response

# Other views...


def create_certificate(request):
    if request.method == 'POST':
        form = CertificateForm(request.POST)
        if form.is_valid():
            certificate = form.save()

            verification_code = generate_verification_code(certificate.id)

            verification = Verification(
                certificate=certificate, verification_code=verification_code)
            verification.save()

            # Verification.objects.create(certificate=certificate, verification_code=verification_code)
            certificate.verification_code = verification_code
            certificate.save()
            return redirect('home')
    else:
        form = CertificateForm()
    return render(request, 'certificates/create_certificate.html', {'form': form})

def verify_certificate(request):
    certificate_id = None
    generated_token = None

    if request.method == 'POST':
        verification_token = request.POST.get('verification_token')
        try:
            verification = Verification.objects.get(verification_code=verification_token)
            certificate = verification.certificate
            generated_token = generate_verification_code(certificate.id)
            if verification_token == generated_token:
                return render(request, 'certificates/verification_result.html', {'certificate': certificate, 'generated_token': generated_token, 'success_message': 'Verification successful'})
            else:
                messages.error(request, 'Verification failed. Token mismatch.')
        except Verification.DoesNotExist:
            messages.error(request, 'Verification failed. Certificate not found.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    return render(request, 'certificates/verify_certificate.html', {'certificate_id': certificate_id, 'generated_token': generated_token})

def customize_certificate(request):
    # Your logic here
    return render(request, 'certificates/customize_certificate.html')

# def nav(request):
#     # Your logic here
#     return render(request, 'certificates/nav.html')


def home(request):
    return render(request, 'certificates/home.html')


def certificate_detail(request, certificate_id):
    certificate = get_object_or_404(Certificate, pk=certificate_id)
    verification = get_object_or_404(Verification, certificate=certificate)

    # context = {'certificate': certificate}

    # Generate the URL for certificate_detail view
    certificate_url = reverse('certificate_detail', args=[certificate_id])

    context = {
        'certificate': certificate,
        'certificate_url': certificate_url,
        # Add verification code to the context
        'verification_code': verification.verification_code,

    }

    return render(request, 'certificates/certificate_detail.html', context)
# certificates/views.py


def some_view(request):
    # Assuming you have a valid certificate_id
    certificate_id = 123
    certificate_url = reverse('certificate_detail', args=[certificate_id])

    context = {
        'certificate_url': certificate_url,
    }

    return render(request, 'your_template.html', context)
# views.py


def home(request):
    # Assuming you have a valid way to retrieve a certificate object
    recent_certificates = Certificate.objects.order_by('issue_date')[:5]
    return render(request, 'certificates/home.html', {'recent_certificates': recent_certificates})
