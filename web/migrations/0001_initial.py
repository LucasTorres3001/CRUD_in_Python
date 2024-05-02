# Generated by Django 4.2.11 on 2024-05-01 00:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Birthplace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_birth', models.CharField(max_length=75)),
                ('uf_birth', models.CharField(max_length=3)),
                ('ddd_birth', models.SmallIntegerField()),
                ('region_birth', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profession_name', models.CharField(max_length=75, unique=True)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Workplace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_work', models.CharField(max_length=75)),
                ('uf_work', models.CharField(max_length=3)),
                ('ddd_work', models.SmallIntegerField()),
                ('region_work', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=19)),
                ('surname', models.CharField(max_length=36)),
                ('cpf', models.CharField(max_length=14, unique=True)),
                ('gender', models.CharField(blank=True, max_length=6, null=True)),
                ('ethnicity', models.CharField(blank=True, max_length=10, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('slug', models.SlugField(unique=True)),
                ('birthplace', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='web.birthplace')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='web.job')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('workplace', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='web.workplace')),
            ],
        ),
        migrations.CreateModel(
            name='Imagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='img')),
                ('personal_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.personaldata')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True)),
                ('personal_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.personaldata')),
            ],
        ),
    ]