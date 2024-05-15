import os, sys
from PIL import Image
from io import BytesIO
from hashlib import sha1
from .forms import FormTest
from datetime import datetime
from django.urls import reverse
from django.conf import settings
from django.http import HttpRequest
from django.contrib import auth, messages
from django.contrib.auth.models import User
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
        profession_name = request.POST.get('job')
        salary = request.POST.get('salary')
        try:
            if len(profession_name.strip()) < 4 or len(salary.strip()) < 1 or float(salary) < 1410:
                messages.add_message(request=request, level=messages.WARNING, message='Invalid profession.')
                return redirect(to=reverse(viewname='add_jobs'))
            else:
                job = Job(
                    profession_name=profession_name,
                    salary=float(salary)
                )
                job.save()
                messages.add_message(request=request, level=messages.SUCCESS, message='Job successfully registered.')
                return redirect(to=reverse(viewname='add_jobs'))
        except ValueError as ve:
            messages.add_message(request=request, level=messages.ERROR, message=f'Profession cannot be registered: {repr(ve)}')
            return redirect(to=reverse(viewname='add_jobs'))

def add_places(request: HttpRequest):
    if request.method == 'GET':
        return render(
            request=request,
            template_name='add_places.html'
        )
    elif request.method == 'POST':
        city = request.POST.get('city')
        uf = request.POST.get('uf')
        ddd = request.POST.get('ddd')
        region = request.POST.get('region')
        try:
            if len(city.strip()) < 3 or len(uf.strip()) < 2 or len(region.strip()) < 5 or ddd == None:
                messages.add_message(request=request, level=messages.WARNING, message='Invalid location.')
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
                messages.add_message(request=request, level=messages.SUCCESS, message='Location registered successfully.')
                return redirect(to=reverse(viewname='add_places'))
        except Exception as e:
            messages.add_message(request=request, level=messages.ERROR, message=f'Location cannot be registered: {repr(e)}')
            return redirect(to=reverse(viewname='add_places'))

def add_users(request: HttpRequest):
    if request.method == 'GET':
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
    elif request.method == 'POST':
        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        cpf = request.POST.get('cpf')
        gender = request.POST.get('gender')
        ethnicity = request.POST.get('ethnicity')
        try:
            date_of_birth = request.POST.get('date_of_birth')
            about_me = request.POST.get('comment')
            formatted_date = datetime.strptime(date_of_birth, '%Y-%m-%d')
            birthplace = int(request.POST.get('birthplace_id'))
            workplace = int(request.POST.get('workplace_id'))
            job = int(request.POST.get('job_id'))
            user = int(request.user.id)
            if len(name.strip()) < 3 or len(surname.strip()) < 3 or len(cpf.strip()) < 11:
                messages.add_message(request=request, level=messages.WARNING, message='Invalid username or CPF.')
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
                    user_id=user
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
                messages.add_message(request=request, level=messages.SUCCESS, message='Personal data registered successfully.')
                return redirect(to=reverse(viewname='add_users'))
        except ValueError as ve:
            messages.add_message(request=request, level=messages.ERROR, message=f'Personal data cannot be registered: {repr(ve)}')
            return redirect(to=reverse(viewname='add_users'))

def data_update_page(request: HttpRequest, slug: str):
    if request.session.get('user'):
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
        messages.add_message(request=request, level=messages.ERROR, message='User is not logged in.')
        return redirect(to=reverse(viewname='login'))

def home(request: HttpRequest):
    if request.session.get('user'):
        if request.method == 'GET':
            personal_data = PersonalData.objects.filter(user=request.session['user'])
            return render(
                request=request,
                template_name='home.html',
                context={
                    'personal_data': personal_data
                }
            )
        elif request.method == 'POST':
            cpf = request.POST.get('cpf')
            personal_data = PersonalData.objects.filter(user=request.session['user']).filter(cpf__icontains=cpf)
            return render(
                request=request,
                template_name='home.html',
                context={
                    'cpf': cpf,
                    'personal_data': personal_data
                }
            )
    else:
        messages.add_message(request=request, level=messages.ERROR, message='User is not logged in.')
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
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request=request, user=user)
            request.session['user'] = request.user.id
            return redirect(to=reverse(viewname='home'))
        else:
            messages.add_message(request=request, level=messages.WARNING, message='User not found.')
            return redirect(to=reverse(viewname='register_login'))

def professionals(request: HttpRequest):
    if request.session.get('user'):
        personal_data = PersonalData.objects.filter(user=request.session['user'])
        return render(
            request=request,
            template_name='professionals.html',
            context={
                'personal_data': personal_data
            }
        )
    else:
        messages.add_message(request=request, level=messages.ERROR, message='User is not logged in.')
        return redirect(to=reverse(viewname='login'))

def register_login(request: HttpRequest):
    if request.method == 'GET':
        return render(
            request=request,
            template_name='register_login.html'
        )
    elif request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username_email = request.POST.get('username')
        server = request.POST.get('server')
        email = f"{username_email}@{server}"
        password = request.POST.get('password')
        username = f'{first_name} {last_name}'
        user = User.objects.filter(username=username).filter(email=email).filter(password=password)
        try:
            if len(first_name.strip()) < 2 or len(last_name.strip()) < 3:
                messages.add_message(request=request, level=messages.WARNING, message='Invalid username.')
                return redirect(to=reverse(viewname='register_login'))
            elif len(username_email.strip()) < 3 or len(server.strip()) < 5:
                messages.add_message(request=request, level=messages.WARNING, message='Invalid email.')
                return redirect(to=reverse(viewname='register_login'))
            elif len(password.strip()) < 3:
                messages.add_message(request=request, level=messages.WARNING, message='Invalid password.')
                return redirect(to=reverse(viewname='register_login'))
            elif len(user) > 0:
                messages.add_message(request=request, level=messages.INFO, message='User already exists.')
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
                messages.add_message(request=request, level=messages.SUCCESS, message='User registered successfully.')
                return redirect(to=reverse(viewname='login'))
        except Exception as e:
            messages.add_message(request=request, level=messages.ERROR, message=f'User cannot be registered: {repr(e)}')
            return redirect(to=reverse(viewname='register_login'))

def show_data(request: HttpRequest, slug: str):
    if request.session.get('user'):
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
        messages.add_message(request=request, level=messages.ERROR, message='User is not logged in.')
        return redirect(to=reverse(viewname='login'))
    
def teste(request: HttpRequest):
    form = FormTest()
    return render(
        request=request,
        template_name='teste.html',
        context={
            'form': form
        }
    )

def to_go_out(request: HttpRequest):
    request.session.flush()
    auth.logout(request=request)
    return redirect(to=reverse(viewname='login'))

def update_data(request: HttpRequest):
    personal_data_slug = request.POST.get('pd_slug')
    new_workplace = int(request.POST.get('new_workplace_id'))
    new_images = request.FILES.getlist('new_images')
    new_comment = request.POST.get('new_comment')
    personal_data = PersonalData.objects.get(slug=personal_data_slug)
    personal_data.workplace_id = new_workplace
    personal_data.save()
    if new_images:
        for im in new_images:
            image_name = f'{datetime.today()}'
            encrypted_image = f"{sha1(image_name.encode('uft-8')).hexdigest()}.png"
            image = Image.open(im)
            image = image.convert('RGB')
            image = image.resize((389, 484))
            output = BytesIO()
            image.save(output, format='PNG', quality=100)
            output.seek(0)
            img = InMemoryUploadedFile(output, 'ImageField', encrypted_image, 'image/png', sys.getsizeof(output), None)
        imagem = Imagem.objects.get(personal_data=personal_data)
        imagem.image = img
        imagem.save()
    comment = Comment.objects.get(personal_data=personal_data)
    comment.comment = new_comment
    comment.save()
    messages.add_message(request=request, level=messages.SUCCESS, message='Personal data updated successfully.')
    return redirect(to=reverse(viewname='professionals'))

def user_delete(request: HttpRequest, id: int):
    personal_data = get_object_or_404(PersonalData, id=id)
    image = Imagem.objects.get(personal_data=personal_data)
    image = image.image.url
    image = image.replace('/', '\\')
    image_path = f'{settings.BASE_DIR}\{image}'
    os.remove(path=image_path)
    personal_data.delete()
    messages.add_message(request=request, level=messages.SUCCESS, message='Personal data successfully deleted.')
    return redirect(to=reverse(viewname='professionals'))