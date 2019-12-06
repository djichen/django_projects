from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template.loader import render_to_string

from boats.models import Boat, Type

class BoatList(LoginRequiredMixin, View) :
    def get(self, request):
        mc = Type.objects.all().count();
        al = Boat.objects.all();
        ctx = { 'type_count': mc, 'boat_list': al };
        return render(request, 'boats/boat_list.html', ctx)

class TypeView(LoginRequiredMixin,View) :
    def get(self, request):
        ml = Type.objects.all();
        ctx = { 'type_list': ml };
        return render(request, 'boats/type_list.html', ctx)

class TypeCreate(LoginRequiredMixin,CreateView):
    model = Type
    fields = '__all__'
    success_url = reverse_lazy('boats:all')

class TypeUpdate(LoginRequiredMixin, UpdateView):
    model = Type
    fields = '__all__'
    success_url = reverse_lazy('boats:all')

class TypeDelete(LoginRequiredMixin, DeleteView):
    model = Type
    fields = '__all__'
    success_url = reverse_lazy('boats:all')

class BoatCreate(LoginRequiredMixin,CreateView):
    model = Boat
    fields = '__all__'
    success_url = reverse_lazy('boats:all')

class BoatUpdate(LoginRequiredMixin, UpdateView):
    model = Boat
    fields = '__all__'
    success_url = reverse_lazy('boats:all')

class BoatDelete(LoginRequiredMixin, DeleteView):
    model = Boat
    fields = '__all__'
    success_url = reverse_lazy('boats:all')