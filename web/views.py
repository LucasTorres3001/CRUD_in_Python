import os, sys
from PIL import Image
from io import BytesIO
from hashlib import sha1
from decimal import Decimal
from datetime import datetime
from .forms import ContactForm
from django.urls import reverse
from django.contrib import auth
from django.conf import settings
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.messages import add_message, constants
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect, get_object_or_404
from .models import Birthplace, Comment, Imagem, Job, PersonalData, Workplace

# Create your views here.

def add_jobs(request: HttpRequest):
    if request.method == 'GET':
        return render(
            request=request,
            template_name='add_jobs.html'
        )
    elif request.method == 'POST':
        profession_name = str(request.POST['job'])
        salary = request.POST['salary']
        try:
            if (len(profession_name.strip()) < 4) or (len(salary.strip()) < 1) or (float(salary) < 1411.9):
                add_message(request=request, level=constants.WARNING, message='Invalid profession.')
                return redirect(to=reverse(viewname='add_jobs'))
            else:
                job = Job(
                    profession_name=profession_name,
                    salary=Decimal(salary)
                )
                job.save()
                add_message(request=request, level=constants.SUCCESS, message='Job successfully registered.')
                return redirect(to=reverse(viewname='add_jobs'))
        except ValueError as ve:
            add_message(request=request, level=constants.ERROR, message=f'Profession cannot be registered: {repr(ve)}')
            return redirect(to=reverse(viewname='add_jobs'))

def add_places(request: HttpRequest):
    if request.method == 'GET':
        return render(
            request=request,
            template_name='add_places.html'
        )
    elif request.method == 'POST':
        city = request.POST['city']
        uf = request.POST['uf']
        ddd = request.POST['ddd']
        region = request.POST['region']
        try:
            if (len(city.strip()) < 3) or (len(uf.strip()) < 2) or (len(region.strip()) < 5) or (ddd == None):
                add_message(request=request, level=constants.WARNING, message='Invalid location.')
                return redirect(to=reverse(viewname='add_places'))
            else:
                birthplace = Birthplace(
                    city_birth=city,
                    uf_birth=uf,
                    ddd_birth=int(ddd),
                    region_birth=region
                )
                birthplace.save()
                workplace = Workplace(
                    city_work=city,
                    uf_work=uf,
                    ddd_work=int(ddd),
                    region_work=region
                )
                workplace.save()
                add_message(request=request, level=constants.SUCCESS, message='Location registered successfully.')
                return redirect(to=reverse(viewname='add_places'))
        except Exception as e:
            add_message(request=request, level=constants.ERROR, message=f'Location cannot be registered: {repr(e)}')
            return redirect(to=reverse(viewname='add_places'))

def add_users(request: HttpRequest):
    if request.method == 'GET':
        if request.user.is_authenticated:
            birthplace = Birthplace.objects.all()
            job = Job.objects.all()
            workplace = Workplace.objects.all()
            return render(
                request=request,
                template_name='add_users.html',
                context={
                    'birthplace': birthplace,
                    'job': job,
                    'workplace': workplace
                }
            )
        else:
            add_message(request=request, level=constants.INFO, message='User is not logged in.')
            return redirect(to=reverse(viewname='login'))
    elif request.method == 'POST':
        name = str(request.POST['first_name'])
        surname = str(request.POST['last_name'])
        cpf = str(request.POST['cpf'])
        gender = str(request.POST['gender'])
        ethnicity = str(request.POST['ethnicity'])
        try:
            date_of_birth = request.POST['date_of_birth']
            about_me = request.POST['comment']
            formatted_date = datetime.strptime(date_of_birth, '%Y-%m-%d')
            birthplace = int(request.POST['birthplace_id'])
            workplace = int(request.POST['workplace_id'])
            job = int(request.POST['job_id'])
            user = request.user
            if len(name.strip()) < 3 or len(surname.strip()) < 3 or len(cpf.strip()) < 11:
                add_message(request=request, level=constants.WARNING, message='Invalid username or CPF.')
                return redirect(to=reverse(viewname='add_users'))
            else:
                personal_data = PersonalData(
                    name=name,
                    surname=surname,
                    cpf=cpf,
                    gender=gender,
                    ethnicity=ethnicity,
                    date_of_birth=formatted_date,
                    birthplace_id=birthplace,
                    workplace_id=workplace,
                    job_id=job,
                    user=user
                )
                personal_data.save()
                for im in request.FILES.getlist('images'):
                    image_name = f'{datetime.today()}'
                    encrypted_image = f"{sha1(image_name.encode('utf-8')).hexdigest()}.png"
                    image = Image.open(im)
                    image = image.convert('RGB')
                    image = image.resize((389, 484))
                    output = BytesIO()
                    image.save(output, format='PNG', quality=100)
                    output.seek(0)
                    img = InMemoryUploadedFile(output, 'ImageField', encrypted_image, 'image/png', sys.getsizeof(output), None)
                    imagem = Imagem(
                        image=img,
                        personal_data=personal_data
                    )
                    imagem.save()
                comment = Comment(
                    comment=about_me,
                    personal_data=personal_data
                )
                comment.save()
                add_message(request=request, level=constants.SUCCESS, message='Personal data registered successfully.')
                return redirect(to=reverse(viewname='add_users'))
        except ValueError as ve:
            add_message(request=request, level=constants.ERROR, message=f'Personal data cannot be registered: {repr(ve)}')
            return redirect(to=reverse(viewname='add_users'))

def data_update_page(request: HttpRequest, slug: str):
    if request.user.is_authenticated:
        personal_data = PersonalData.objects.get(slug=slug)
        workplace = personal_data.workplace
        workplaces = Workplace.objects.all()
        return render(
            request=request,
            template_name='update_data.html',
            context={
                'personal_data': personal_data,
                'workplace': workplace,
                'workplaces': workplaces
            }
        )
    else:
        add_message(request=request, level=constants.ERROR, message='User is not logged in.')
        return redirect(to=reverse(viewname='login'))

def home(request: HttpRequest):
    if request.user.is_authenticated:
        if request.method == 'GET':
            personal_data = PersonalData.objects.filter(user=request.user)
            return render(
                request=request,
                template_name='home.html',
                context={
                    'personal_data': personal_data
                }
            )
        elif request.method == 'POST':
            cpf = str(request.POST['cpf'])
            personal_data = PersonalData.objects.filter(user=request.user).filter(cpf__icontains=cpf)
            return render(
                request=request,
                template_name='home.html',
                context={
                    'cpf': cpf,
                    'personal_data': personal_data
                }
            )
    else:
        add_message(request=request, level=constants.ERROR, message='User is not logged in.')
        return redirect(to=reverse(viewname='login'))

def login(request: HttpRequest):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(to=reverse(viewname='home'))
        return render(
            request=request,
            template_name='login.html'
        )
    elif request.method == 'POST':
        username = str(request.POST['username'])
        password = str(request.POST['password'])
        user = auth.authenticate(request=request, username=username, password=password)
        if user:
            auth.login(request=request, user=user)
            return redirect(to=reverse(viewname='home'))
        else:
            add_message(request=request, level=constants.WARNING, message='User not found.')
            return redirect(to=reverse(viewname='register_login'))

def professionals(request: HttpRequest):
    if request.user.is_authenticated:
        personal_data = PersonalData.objects.filter(user=request.user)
        return render(
            request=request,
            template_name='professionals.html',
            context={
                'personal_data': personal_data
            }
        )
    else:
        add_message(request=request, level=constants.ERROR, message='User is not logged in.')
        return redirect(to=reverse(viewname='login'))

def register_login(request: HttpRequest):
    if request.method == 'GET':
        return render(
            request=request,
            template_name='register_login.html'
        )
    elif request.method == 'POST':
        first_name = str(request.POST['first_name'])
        last_name = str(request.POST['last_name'])
        username_email = str(request.POST['username'])
        server = str(request.POST['server'])
        password = str(request.POST['password'])
        email = f"{username_email}@{server}"
        username = f'{first_name} {last_name}'
        user = User.objects.filter(username=username).filter(email=email).filter(password=password)
        try:
            if len(first_name.strip()) < 2 or len(last_name.strip()) < 3:
                add_message(request=request, level=constants.WARNING, message='Invalid username.')
                return redirect(to=reverse(viewname='register_login'))
            elif len(username_email.strip()) < 3 or len(server.strip()) < 5:
                add_message(request=request, level=constants.WARNING, message='Invalid email.')
                return redirect(to=reverse(viewname='register_login'))
            elif len(password.strip()) < 3:
                add_message(request=request, level=constants.WARNING, message='Invalid password.')
                return redirect(to=reverse(viewname='register_login'))
            elif len(user) > 0:
                add_message(request=request, level=constants.INFO, message='User already exists.')
                return redirect(to=reverse(viewname='register_login'))
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                user.save()
                add_message(request=request, level=constants.SUCCESS, message='User registered successfully.')
                return redirect(to=reverse(viewname='login'))
        except Exception as e:
            add_message(request=request, level=constants.ERROR, message=f'User cannot be registered: {repr(e)}')
            return redirect(to=reverse(viewname='register_login'))

def show_data(request: HttpRequest, slug: str):
    if request.user.is_authenticated:
        personal_data = PersonalData.objects.get(slug=slug)
        birthplace = personal_data.birthplace
        job = personal_data.job
        return render(
            request=request,
            template_name='show_data.html',
            context={
                'birthplace': birthplace,
                'job': job,
                'personal_data': personal_data
            }
        )
    else:
        add_message(request=request, level=constants.ERROR, message='User is not logged in.')
        return redirect(to=reverse(viewname='login'))
    
def teste(request: HttpRequest):
    form = ContactForm()
    return render(
        request=request,
        template_name='teste.html',
        context={
            'form': form
        }
    )

def to_go_out(request: HttpRequest):
    auth.logout(request=request)
    return redirect(to=reverse(viewname='login'))

def update_data(request: HttpRequest):
    new_workplace = int(request.POST['new_workplace_id'])
    new_images = request.FILES.getlist('new_images')
    new_comment = request.POST['new_comment']
    
    personal_data = get_object_or_404(PersonalData, slug=request.POST['pd_slug'])
    personal_data.workplace_id = new_workplace
    personal_data.save()
    if new_images:
        for im in new_images:
            image_name = f'{datetime.today()}'
            encrypted_image = f"{sha1(image_name.encode('utf-8')).hexdigest()}.png"
            image = Image.open(im)
            image = image.convert('RGB')
            image = image.resize((389, 484))
            output = BytesIO()
            image.save(output, format='PNG', quality=100)
            output.seek(0)
            img = InMemoryUploadedFile(output, 'ImageField', encrypted_image, 'image/png', sys.getsizeof(output), None)
        imagem = get_object_or_404(Imagem, personal_data=personal_data)
        imagem.image = img
        imagem.save()
    comment = get_object_or_404(Comment, personal_data=personal_data)
    comment.comment = new_comment
    comment.save()
    add_message(request=request, level=constants.SUCCESS, message='Personal data updated successfully.')
    return redirect(to=reverse(viewname='professionals'))

def user_delete(request: HttpRequest, id: int):
    personal_data = get_object_or_404(PersonalData, id=id)
    image = get_object_or_404(Imagem, personal_data=personal_data)
    image = image.image.url
    image = image.replace('/', '\\')
    image_path = f'{settings.BASE_DIR}\{image}'
    os.remove(path=image_path)
    personal_data.delete()
    add_message(request=request, level=constants.SUCCESS, message='Personal data successfully deleted.')
    return redirect(to=reverse(viewname='professionals'))