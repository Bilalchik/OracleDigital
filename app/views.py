import re
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView
from django.db.models import Q
from django.conf import settings
from .models import Student
from .forms import UserRegistrationForm, UserAuthenticationForm, StudentForm


def index(request):
    return render(request, 'app/index.html')


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'app/registration.html', {'form': form})
    form = UserRegistrationForm()
    return render(request, 'app/registration.html', {'form': form})


def authentication_view(request):
    if request.method == "POST":
        form = UserAuthenticationForm(data=request.POST)
        if form.is_valid():
            user_phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            user = authenticate(username=user_phone_number, password=password)
            if user != None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Неверный номер телефона или пароль')
                return render(request, 'app/authentication.html', {'form': form})
    form = UserAuthenticationForm()
    return render(request, 'app/authentication.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')


class StudentListView(ListView):
    queryset = Student.objects.all().order_by('-id')
    template_name = 'app/student_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')

        if search_query:
            queryset = queryset.filter(Q(full_name__icontains=search_query) |
                                       Q(full_name__iregex=r'\b{}\b'.format(re.escape(search_query))))

        return queryset


def student_delete(request, pk):

    student = Student.objects.get(id=pk)
    student.delete()

    return HttpResponseRedirect(reverse('student_list'))


def student_add(request):
    if request.method == 'POST':
        form = StudentForm(data=request.POST)
        if form.is_valid():
            student = form.save()
            return redirect('student_list')
        messages.error(request, 'Повторите попытку, убедитесь что поля заполнены в правильном формате')
    form = StudentForm()
    return render(request, template_name='app/student_add.html', context={'form': form})


def student_detail(request, pk):
    student = get_object_or_404(Student, id=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
        messages.error(request, 'Повторите попытку, убедитесь что поля заполнены в правильном формате')
    else:
        form = StudentForm(instance=student)

    return render(request, template_name='app/student_detail.html', context={'student': student, 'form': form})


def send_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        recipients = Student.objects.values_list('mail', flat=True)  # Получение адресов электронной почты всех учеников

        # Отправка сообщения по электронной почте
        subject = 'Сообщение для учеников'
        send_mail(subject, message, 'bilal.kubatbekov.04@mail.ru', recipients)

        return redirect('index')

    return render(request, 'app/send_message.html')


@receiver(post_save, sender=Student)
def send_student_notification(sender, instance, created, **kwargs):
    if created:
        email = instance.mail
        subject = 'Добро пожаловать!'
        message = f'Привет, {instance.full_name}! Вы успешно зарегистрированы на нашей платформе.'
        send_mail(subject, message, settings.ADMIN_EMAIL, [email])

