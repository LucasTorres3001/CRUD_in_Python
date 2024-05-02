from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.

class Birthplace(models.Model):
    
    city_birth = models.CharField(max_length=75, blank=False, null=False)
    uf_birth = models.CharField(max_length=3, blank=False, null=False)
    ddd_birth = models.SmallIntegerField()
    region_birth = models.CharField(max_length=16, blank=False, null=False)
    
    def __str__(self) -> str:
        return self.city_birth
    
class Workplace(models.Model):
    
    city_work = models.CharField(max_length=75, blank=False, null=False)
    uf_work = models.CharField(max_length=3, blank=False, null=False)
    ddd_work = models.SmallIntegerField()
    region_work = models.CharField(max_length=16, blank=False, null=False)
    
    def __str__(self) -> str:
        return self.city_work
    
class Job(models.Model):
    
    profession_name = models.CharField(max_length=75, unique=True, blank=False, null=False)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    
    def __str__(self) -> str:
        return self.profession_name
    
class PersonalData(models.Model):
    
    name = models.CharField(max_length=19, blank=False, null=False)
    surname = models.CharField(max_length=36, blank=False, null=False)
    cpf = models.CharField(max_length=14, unique=True, blank=False, null=False)
    gender = models.CharField(max_length=6, blank=True, null=True)
    ethnicity = models.CharField(max_length=10, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    birthplace = models.ForeignKey(Birthplace, on_delete=models.DO_NOTHING)
    workplace = models.ForeignKey(Workplace, on_delete=models.DO_NOTHING)
    job = models.ForeignKey(Job, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    slug = models.SlugField(unique=True, blank=False, null=False)
    
    def __str__(self) -> str:
        return f'{self.name} {self.surname}'
    
    def save(self, *args, **kwargs):
        username: str = f'{self.name} {self.surname}'
        if not self.slug:
            self.slug = slugify(username)
        return super().save(args, kwargs)
    
class Imagem(models.Model):
    
    image = models.ImageField(upload_to='img')
    personal_data = models.ForeignKey(PersonalData, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.image
    
class Comment(models.Model):
    
    comment = models.TextField(blank=True, null=True)
    personal_data = models.ForeignKey(PersonalData, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.comment