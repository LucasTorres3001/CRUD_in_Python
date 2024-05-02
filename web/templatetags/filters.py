
from atexit import register
from django import template
from web.models import Comment, Imagem, PersonalData

register = template.Library()

@register.filter(name='get_the_first_image')
def get_the_first_image(personal_data: PersonalData):
    image = Imagem.objects.filter(personal_data=personal_data).first()
    if image:
        return image.image.url
    else:
        return False
    
@register.filter(name='get_comment')
def get_comment(personal_data: PersonalData):
    comment = Comment.objects.get(personal_data=personal_data)
    if comment:
        return comment.comment
    else:
        return ''
    
@register.filter(name='get_user')
def get_user(personal_data: PersonalData):
    personal_data = PersonalData.objects.get(id=personal_data.id)
    user = personal_data.user
    if user:
        return user.username
    else:
        return 'User without supervisor'