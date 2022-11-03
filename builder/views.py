from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .forms import ComponentForm


def index(request):
    """The starting page. The user chooses the cpu's brand."""

    choices = [('AMD', 'AMD'), ('Intel', 'Intel')]
    label = "To start, select a socket-brand for your CPU and Motherboard:"

    if request.method != 'POST':
        form = ComponentForm(choices, label)    
    else:
        form = ComponentForm(choices, label, request.POST)
        if form.is_valid():
            order = Order()
            order.cpu_brand = form.cleaned_data['comp']
            order.save()
            return HttpResponseRedirect(reverse('builder:cpu',
                args=(order.id,)))

    context = {'form': form}
    return render(request, 'builder/index.html', context)
        

def cpu(request, order_id):
    """The user chooses the CPU."""

    # Get the order object and the available components (compatible ones)
    order = Order.objects.get(id=order_id)
    available_comps = CPU.objects.filter(socket=order.cpu_brand)
    
    choices = get_choices(available_comps)
    label = "Select a CPU:"

    if request.method != 'POST':
        form = ComponentForm(choices, label)
    else:
        form = ComponentForm(choices, label, request.POST)
        if form.is_valid():
            order.cpu = form.cleaned_data['comp']
            order.save()
            return HttpResponseRedirect(reverse('builder:motherboard',
                args=(order_id,)))
    
    context = {'form': form, 'order_id': order_id}
    return render(request, 'builder/cpu.html', context)


def motherboard(request, order_id):
    """The user chooses the motherboard."""

    # Get the order object and the available components (compatible ones)
    order = Order.objects.get(id=order_id)
    available_comps = Motherboard.objects.filter(socket=order.cpu_brand)

    choices = get_choices(available_comps)
    label = "Select a Motherboard:"

    if request.method != 'POST':
        form = ComponentForm(choices, label)
    else:
        form = ComponentForm(choices, label, request.POST)
        if form.is_valid():
            order.mb = form.cleaned_data['comp']
            order.save()
            return HttpResponseRedirect(reverse('builder:gpu',
                args=(order_id,)))
    
    context = {'form': form, 'order_id': order_id}
    return render(request, 'builder/motherboard.html', context)


def gpu(request, order_id):
    """The user chooses the GPU."""

    # Get the order object and the available components (compatible ones)
    order = Order.objects.get(id=order_id)
    available_comps = GPU.objects.all()

    choices = get_choices(available_comps)
    label = "Select a GPU:"

    if request.method != 'POST':
        form = ComponentForm(choices, label)
    else:
        form = ComponentForm(choices, label, request.POST)
        if form.is_valid():   
            order.gpu = form.cleaned_data['comp']
            order.save()
            return HttpResponseRedirect(reverse('builder:ram',
                args=(order_id,)))
    
    context = {'form':form , 'order_id': order_id}
    return render(request, 'builder/gpu.html', context)


def ram(request, order_id):
    """The user chooses the ram."""

    # Get the order object and the available components (compatible ones)
    order = Order.objects.get(id=order_id)
    available_comps = RAM.objects.all()

    choices = get_choices(available_comps)
    label = "Select the RAM:"

    if request.method != 'POST':
        form = ComponentForm(choices, label)
    else:
        form = ComponentForm(choices, label, request.POST)
        if form.is_valid():
            order.ram = form.cleaned_data['comp']
            order.save()
            return HttpResponseRedirect(reverse('builder:order_review',
                args=(order_id,)))
    
    context = {'form': form, 'order_id': order_id}
    return render(request, 'builder/ram.html', context)


def order_review(request, order_id):
    order = Order.objects.get(id=order_id)
    components = {'CPU Brand': order.cpu_brand, 'Motherboard': order.mb,
        'CPU': order.cpu, 'GPU': order.gpu, 'RAM': order.ram,
        'Ref. System': order.rf, 'Case': order.cs, 'Power Supply': order.ps}

    for k, comp in components.items():
        
        if comp and k != "CPU Brand":
            components[k] = Component.objects.get(id=comp)
    
    print(components)

    context = {'order': order, 'components': components}
    return render(request, 'builder/order_review.html', context)


def get_choices(components):
    """Creates and returns a choices-type list from a given list of components"""
    choices = []
    for comp in components:
        choices.append((comp.id, comp))  
    return choices