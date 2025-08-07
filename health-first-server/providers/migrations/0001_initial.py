# Generated initial migration for providers app

import uuid
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClinicAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(help_text='Street address', max_length=200, validators=[django.core.validators.MinLengthValidator(1)])),
                ('city', models.CharField(help_text='City name', max_length=100, validators=[django.core.validators.MinLengthValidator(1)])),
                ('state', models.CharField(help_text='State or province', max_length=50, validators=[django.core.validators.MinLengthValidator(1)])),
                ('zip_code', models.CharField(help_text='Postal/ZIP code', max_length=20, validators=[django.core.validators.MinLengthValidator(3)])),
            ],
            options={
                'verbose_name': 'Clinic Address',
                'verbose_name_plural': 'Clinic Addresses',
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(help_text='First name (2-50 characters)', max_length=50, validators=[django.core.validators.MinLengthValidator(2), django.core.validators.MaxLengthValidator(50)])),
                ('last_name', models.CharField(help_text='Last name (2-50 characters)', max_length=50, validators=[django.core.validators.MinLengthValidator(2), django.core.validators.MaxLengthValidator(50)])),
                ('email', models.EmailField(help_text='Unique email address', max_length=254, unique=True)),
                ('phone_number', models.CharField(help_text='Unique phone number in international format', max_length=20, unique=True)),
                ('password', models.CharField(help_text='Hashed password', max_length=128)),
                ('specialization', models.CharField(choices=[('cardiology', 'Cardiology'), ('dermatology', 'Dermatology'), ('endocrinology', 'Endocrinology'), ('gastroenterology', 'Gastroenterology'), ('neurology', 'Neurology'), ('oncology', 'Oncology'), ('orthopedics', 'Orthopedics'), ('pediatrics', 'Pediatrics'), ('psychiatry', 'Psychiatry'), ('radiology', 'Radiology'), ('surgery', 'Surgery'), ('urology', 'Urology'), ('family_medicine', 'Family Medicine'), ('internal_medicine', 'Internal Medicine'), ('emergency_medicine', 'Emergency Medicine'), ('anesthesiology', 'Anesthesiology'), ('pathology', 'Pathology'), ('obstetrics_gynecology', 'Obstetrics & Gynecology'), ('ophthalmology', 'Ophthalmology'), ('otolaryngology', 'Otolaryngology'), ('other', 'Other')], help_text='Medical specialization (3-100 characters)', max_length=100, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(100)])),
                ('license_number', models.CharField(help_text='Unique alphanumeric license number', max_length=50, unique=True)),
                ('years_of_experience', models.PositiveIntegerField(help_text='Years of medical experience (0-50)')),
                ('verification_status', models.CharField(choices=[('pending', 'Pending'), ('verified', 'Verified'), ('rejected', 'Rejected')], default='pending', help_text='Account verification status', max_length=20)),
                ('license_document_url', models.URLField(blank=True, help_text='URL to uploaded license document', null=True)),
                ('is_active', models.BooleanField(default=True, help_text='Account active status')),
                ('email_verified', models.BooleanField(default=False, help_text='Email verification status')),
                ('email_verification_token', models.CharField(blank=True, help_text='Email verification token', max_length=255, null=True)),
                ('email_verification_expires', models.DateTimeField(blank=True, help_text='Email verification token expiration', null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('clinic_address', models.OneToOneField(help_text='Clinic address information', on_delete=django.db.models.deletion.CASCADE, related_name='provider', to='providers.clinicaddress')),
            ],
            options={
                'verbose_name': 'Provider',
                'verbose_name_plural': 'Providers',
                'indexes': [
                    models.Index(fields=['email'], name='providers_p_email_8c7e1c_idx'),
                    models.Index(fields=['phone_number'], name='providers_p_phone_n_8a29c5_idx'),
                    models.Index(fields=['license_number'], name='providers_p_license_c33a3f_idx'),
                    models.Index(fields=['verification_status'], name='providers_p_verific_d8e1b8_idx'),
                    models.Index(fields=['created_at'], name='providers_p_created_c2d8e5_idx'),
                ],
            },
        ),
        migrations.CreateModel(
            name='ProviderRegistrationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(help_text='IP address of registration attempt')),
                ('email', models.EmailField(help_text='Email used in registration attempt', max_length=254)),
                ('success', models.BooleanField(default=False, help_text='Whether registration was successful')),
                ('error_message', models.TextField(blank=True, help_text='Error message if registration failed', null=True)),
                ('user_agent', models.TextField(blank=True, help_text='User agent string', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Provider Registration Log',
                'verbose_name_plural': 'Provider Registration Logs',
                'indexes': [
                    models.Index(fields=['ip_address', 'created_at'], name='providers_p_ip_addr_f7c2b1_idx'),
                    models.Index(fields=['email', 'created_at'], name='providers_p_email_c7a8e4_idx'),
                ],
            },
        ),
    ] 