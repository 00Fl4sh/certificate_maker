# certificates/models.py

from django.db import models
import hashlib
import jwt
from datetime import datetime, timedelta
from django.conf import settings

class Certificate(models.Model):
    title = models.CharField(max_length=200)
    recipient_name = models.CharField(max_length=200)
    course = models.CharField(max_length=200)  # New field for the course
    issue_date = models.DateField()
    def get_absolute_url(self):
        return reverse('certificate_detail', args=[str(self.pk)])

class Verification(models.Model):
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=100, unique=True)

class Customization(models.Model):
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)
    font = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    layout = models.CharField(max_length=50)

def generate_verification_code(certificate_id):
    verification_code = hashlib.sha256(str(certificate_id).encode()).hexdigest()[:8]
    return verification_code

def generate_jwt_token(certificate_id):
    expiration = datetime.utcnow() + timedelta(days=1)
    token_payload = {
        'certificate_id': certificate_id,
        'exp': expiration
    }
    token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm='HS256')
    return token
