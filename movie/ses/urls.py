from django.urls import path, reverse_lazy
from . import views

app_name='ses'
urlpatterns = [
    path('', views.hello_world, name = 'hello_world'),
    path('add/', views.hello_world, name = 'hello_world'),
]

# urlpatterns = [
#     path('', views.index, name='index'),
# ]