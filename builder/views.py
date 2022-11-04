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
            return HttpResponseRedirect(reverse('builder:case',
                args=(order_id,)))
    
    context = {'form': form, 'order_id': order_id}
    return render(request, 'builder/ram.html', context)


def case(request, order_id):
    """The user chooses the case."""

    # Get the order object and the available components (compatible ones)
    order = Order.objects.get(id=order_id)
    available_comps = Case.objects.all()

    choices = get_choices(available_comps)
    label = "Select the Case:"

    if request.method != 'POST':
        form = ComponentForm(choices, label)
    else:
        form = ComponentForm(choices, label, request.POST)
        if form.is_valid():
            order.cs = form.cleaned_data['comp']
            order.save()
            return HttpResponseRedirect(reverse('builder:ref_system',
                args=(order_id,)))
    
    context = {'form': form, 'order_id': order_id}
    return render(request, 'builder/case.html', context)


def ref_system(request, order_id):
    """The user chooses the ref system."""

    # Get the order object and the available components (compatible ones)
    order = Order.objects.get(id=order_id)
    available_comps = RefSystem.objects.all()

    choices = get_choices(available_comps)
    label = "Select the Refrigeration System:"

    if request.method != 'POST':
        form = ComponentForm(choices, label)
    else:
        form = ComponentForm(choices, label, request.POST)
        if form.is_valid():
            order.rf = form.cleaned_data['comp']
            order.save()
            return HttpResponseRedirect(reverse('builder:power_supply',
                args=(order_id,)))
    
    context = {'form': form, 'order_id': order_id}
    return render(request, 'builder/ref_system.html', context)




def power_supply(request, order_id):
    """The user chooses the power supply."""

    # Get the order object and the available components (compatible ones)
    order = Order.objects.get(id=order_id)
    available_comps = PowerSupply.objects.all()

    choices = get_choices(available_comps)
    label = "Select the Power Supply:"

    if request.method != 'POST':
        form = ComponentForm(choices, label)
    else:
        form = ComponentForm(choices, label, request.POST)
        if form.is_valid():
            order.ps = form.cleaned_data['comp']
            order.save()
            return HttpResponseRedirect(reverse('builder:order_review',
                args=(order_id,)))
    
    context = {'form': form, 'order_id': order_id}
    return render(request, 'builder/power_supply.html', context)


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


def choose_component(request, order_id, comp, socket=''):
    """The user chooses a component"""
    # Get the order object and the available components (compatible ones)
    components = {
        'cpu': (
            CPU,
            'CPU',
            ),
        'motherboard': (Motherboard, 'Motherboard'),
        'gpu': (GPU, 'GPU'),
        'ram': (RAM, 'RAM'),
        'ref_system': (RefSystem, 'Refrigeration System'),
        'case': (Case, 'Case'),
        'power_supply': (PowerSupply, 'Power Supply')
        }

    label = f'Select the {components[comp][1]}:'

    if socket == '':
        components = components[comp][0].objects.all()
    else:
        components = components[comp][0].objects.filter(socket=socket)
    
    choices = get_choices(components)

    order = Order.objects.get(id=order_id)

    if request.method != 'POST':
        form = ComponentForm(choices, label)
    else:
        form = ComponentForm(choices, label, request.POST)
        if form.is_valid():
            order.cpu = form.cleaned_data[comp]
            order.save()
            next_comp = components.keys()[components.keys().index(comp) + 1]
            return HttpResponseRedirect(reverse(f'builder:{comp}',
                args=(order_id,)))
    url = "{% url 'builder:" + comp + "' " + order_id + comp + socket + " %}"
    context = {'form': form, 'order_id': order_id}
    return render(request, 'builder/cpu.html', context)