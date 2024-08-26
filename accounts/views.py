from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import RegistrationForm, OTPForm, LoginForm
from .models import TempUser, User
import random
import requests

def send_otp(email, phone):
    email_otp = random.randint(100, 999)
    phone_otp = random.randint(100, 999)
    # Send OTPs to email and phone
    send_mail(
        'Your OTP for Registration',
        f'Your OTP: {email_otp}',
        'uppadagiridhar510@gmail.com',
        [email],
        fail_silently=False,
    )
    # Simulate sending SMS to phone (implement with an SMS gateway)
    response = requests.post(
        'https://textbelt.com/text',
        data={
            'phone': phone,
            'message': f'Your OTP is {phone_otp}',
            'key': 'textbelt'  # API key for free usage
        }
    )
    result = response.json()
    if result.get('success') != True:
        print('Failed to send SMS:', result.get('error'))
    return email_otp, phone_otp

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            email_otp, phone_otp = send_otp(email, phone)
            TempUser.objects.create(email=email, phone=phone, password=password, email_otp=email_otp, phone_otp=phone_otp)
            return redirect('validate_otp')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def validate_otp(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            combined_otp = form.cleaned_data['combined_otp']
            temp_user = TempUser.objects.latest('created_at')
            expected_otp = str(temp_user.email_otp) + str(temp_user.phone_otp)
            if combined_otp == expected_otp:
                User.objects.create(email=temp_user.email, phone=temp_user.phone, password=temp_user.password)
                # Send success message to email and phone
                send_mail('Registration Successful', 'You have successfully registered!', 'from@example.com', [temp_user.email])
                print(f'Sending registration success message to {temp_user.phone}')
                return redirect('registration_success')
            else:
                return render(request, 'validate_otp.html', {'form': form, 'error': 'Invalid OTP'})
    else:
        form = OTPForm()
    return render(request, 'validate_otp.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            password = form.cleaned_data['password']
            user = User.objects.filter(email=identifier).first() or User.objects.filter(phone=identifier).first()
            if user and user.password == password:
                return redirect('login_success')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Wrong password'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def registration_success(request):
    return render(request, 'registration_success.html')

def login_success(request):
    return render(request, 'login_success.html')
