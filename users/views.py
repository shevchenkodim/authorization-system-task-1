from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from .models import Department, User
import random

from django.contrib.auth.hashers import check_password

from .forms import UserRegisterForm, PhoneNumberForm, CollaboratorRegisterForm, \
    CollaboratorLoginForm, UserLoginForm

from .utils import check_user, check_collaborator, check_user_db


class IndexView(TemplateView):
    template_name = "base.html"
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PageGeneratingOTPView(TemplateView):
    template_name = "page_generating_otp_code.html"
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PhoneNumberForm()
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = PhoneNumberForm(request.POST)
            if form.is_valid():
                phone_number = form.cleaned_data.get('phone_number')

                otp_code = random.randint(1000, 9999)

                if not check_user(phone_number) and check_user_db():
                    form = UserRegisterForm()

                    print('OTP-code', str(otp_code))

                    response = render(request, 'signup_user.html', {
                                      'form': form, 'phone': phone_number})
                    response.set_cookie('OTP-code', value=otp_code, max_age=1000, expires=None,
                                        path='/', domain=None, secure=False, httponly=False, samesite=None)
                    return response

                elif not check_user(phone_number) and not check_user_db():
                    form = CollaboratorRegisterForm()

                    print('OTP-code', str(otp_code))

                    response = render(request, 'signup_collaborator.html', {
                                      'form': form, 'phone': phone_number})
                    response.set_cookie('OTP-code', value=otp_code, max_age=1000, expires=None,
                                        path='/', domain=None, secure=False, httponly=False, samesite=None)
                    return response

                elif check_user(phone_number) and check_collaborator(phone_number):
                    form = CollaboratorLoginForm()

                    print('OTP-code', str(otp_code))

                    response = render(request, 'signin_collaborator.html', {
                                      'form': form, 'phone': phone_number})
                    response.set_cookie('OTP-code', value=otp_code, max_age=1000, expires=None,
                                        path='/', domain=None, secure=False, httponly=False, samesite=None)
                    return response

                elif check_user(phone_number) and not check_collaborator(phone_number):
                    form = UserLoginForm()

                    print('OTP-code', str(otp_code))

                    response = render(request, 'signin_user.html', {
                                      'form': form, 'phone': phone_number})
                    response.set_cookie('OTP-code', value=otp_code, max_age=1000, expires=None,
                                        path='/', domain=None, secure=False, httponly=False, samesite=None)
                    return response

            else:
                messages.error(
                    request, 'Вы указали неверный номер телефона')

        return render(request, self.template_name, {'form': form})


class SignupUser(TemplateView):
    template_name = "signup_user.html"
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserRegisterForm()
        context['phone'] = self.kwargs['phone']
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                new_user = form.save(commit=False)
                new_user.username = form.cleaned_data.get(
                    'phone_number')
                new_user.phone_number = form.cleaned_data.get(
                    'phone_number')
                new_user.is_collaborator = False

                otp_code_form = form.cleaned_data.get('otp_code')
                otp_code = request.COOKIES.get('OTP-code')
                if int(otp_code_form) == int(otp_code):
                    new_user.save()

                    login(request, new_user,
                          backend='django.contrib.auth.backends.ModelBackend')

                    messages.success(
                        request, f'Добрый день, {new_user.last_name},{new_user.first_name}')
                    return redirect(reverse('index'))
                else:
                    messages.error(
                        request, 'OTP-пароль неверный!')

        return render(request, self.template_name, {'form': form, 'phone': self.kwargs['phone']})


class SignupCollaborator(TemplateView):
    template_name = "signup_collaborator.html"
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CollaboratorRegisterForm()
        context['phone'] = self.kwargs['phone']
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = CollaboratorRegisterForm(request.POST)
            if form.is_valid():
                new_user = form.save(commit=False)
                new_user.phone_number = form.cleaned_data.get(
                    'phone_number')
                new_user.is_collaborator = True
                new_user.department = Department.objects.all().first()

                otp_code_form = form.cleaned_data.get('otp_code')
                otp_code = request.COOKIES.get('OTP-code')

                password = form.cleaned_data.get('password')
                password2 = form.cleaned_data.get('password2')

                if int(otp_code_form) == int(otp_code) and password == password2:
                    new_user.save()
                    new_user.set_password(new_user.password)
                    new_user.save()

                    login(request, new_user,
                          backend='django.contrib.auth.backends.ModelBackend')

                    messages.success(
                        request, f'Добрый день, {new_user.last_name},{new_user.first_name}. Ваш отдел {new_user.department.name}')
                    return redirect(reverse('index'))
                else:
                    messages.error(
                        request, 'OTP-пароль или пароль неверный!')

        return render(request, self.template_name, {'form': form, 'phone': self.kwargs['phone']})


class SigninUser(TemplateView):
    template_name = "signin_user.html"
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserLoginForm()
        context['phone'] = self.kwargs['phone']
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = UserLoginForm(request.POST)
            if form.is_valid():
                phone_number = form.cleaned_data.get('phone_number')

                otp_code_form = form.cleaned_data.get('otp_code')
                otp_code = request.COOKIES.get('OTP-code')

                if int(otp_code_form) == int(otp_code):
                    user = User.objects.get(phone_number=phone_number)

                    login(request, user,
                          backend='django.contrib.auth.backends.ModelBackend')

                    messages.success(
                        request, f'Добрый день, {user.last_name},{user.first_name}.')
                    return redirect(reverse('index'))
                else:
                    messages.error(
                        request, 'OTP-пароль неверный!')

        return render(request, self.template_name, {'form': form, 'phone': self.kwargs['phone']})


class SigninCollaborator(TemplateView):
    template_name = "signin_collaborator.html"
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CollaboratorLoginForm()
        context['phone'] = self.kwargs['phone']
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = CollaboratorLoginForm(request.POST)
            if form.is_valid():
                phone_number = form.cleaned_data.get('phone_number')

                otp_code_form = form.cleaned_data.get('otp_code')
                otp_code = request.COOKIES.get('OTP-code')

                password = form.cleaned_data.get('password')

                if int(otp_code_form) == int(otp_code):
                    user = authenticate(
                        phone_number=phone_number, password=password)

                    login(request, user,
                          backend='django.contrib.auth.backends.ModelBackend')

                    messages.success(
                        request, f'Добрый день, {user.last_name},{user.first_name}. Ваш отдел {user.department.name}')
                    return redirect(reverse('index'))
                else:
                    messages.error(
                        request, 'OTP-пароль или пароль неверный!')

        return render(request, self.template_name, {'form': form, 'phone': self.kwargs['phone']})


def user_logout(request):
    logout(request)
    return redirect('/')
