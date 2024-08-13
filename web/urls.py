from . import views
from django.urls import path

# Create your URLs here.

urlpatterns = [
    path('add_jobs/', views.add_jobs, name='add_jobs'),
    path('add_places/', views.add_places, name='add_places'),
    path('add_users', views.add_users, name='add_users'),
    path('data_update_page/<slug:slug>', views.data_update_page, name='data_update_page'),
    path('home/', views.home, name='home'),
    path('login/', views.log_in, name='login'),
    path('professionals/', views.professionals, name='professionals'),
    path('register_login/', views.register_login, name='register_login'),
    path('show_data/<slug:slug>', views.show_data, name='show_data'),
    path('test/', views.teste, name='test'),
    path('to_go_out/', views.to_go_out, name='to_go_out'),
    path('update_data/', views.update_data, name='update_data'),
    path('user_delete/<int:id>', views.user_delete, name='user_delete'),
]
