from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .forms import *


def index(request):
    """The starting page. The user chooses the cpu's brand."""

    choices = [('AMD', 'AMD'), ('Intel', 'Intel')]
    label = "To start, select a socket-brand for your CPU and Motherboard:"

    if request.method != 'POST':
        form = ComponentForm(choices, label, False)

    else:
        form = ComponentForm(choices, label, False, request.POST)
        print('post')
        if form.is_valid():
            print('valid')
            order = Order()
            order.cpu_brand = form.cleaned_data['comp']
            order.save()
            return HttpResponseRedirect(reverse('builder:choose_cpu',
                args=(order.id, 'cpu')))
        else:
            return HttpResponse()
        

    context = {'form': form}
    return render(request, 'builder/index.html', context)


def choose_component(request, order_id, comp):
    """The user chooses a component"""
    
    order = Order.objects.get(id=order_id) # Get the Order object

    # Create a dict with items that will be used later
    comp_items = {
        'cpu': (CPU, 'CPU', order.cpu),
        'motherboard': (Motherboard, 'Motherboard', order.mb),
        'gpu': (GPU, 'GPU', order.gpu),
        'ram': (RAM, 'RAM', order.ram),
        'ref_system': (RefSystem, 'Refrigeration System', order.rf),
        'case': (Case, 'Case', order.cs),
        'power_supply': (PowerSupply, 'Power Supply', order.ps)
        }

    label = f'Select the {comp_items[comp][1]}:' # Create the custom label
    
    # Create the list of compatible comp_items
    if comp == 'cpu' or comp == 'motherboard':
        available_comps = comp_items[comp][0].objects.filter(socket=order.cpu_brand)
    else:
        available_comps = comp_items[comp][0].objects.all()
    
    choices = get_choices(available_comps) # Create the choices of the form's ChoiceField

    # Create the keyword of the previous and the next component to choose
    if comp == 'cpu':
        previous = 'index'
    else:
        previous = comp_items.keys()[comp_items.keys().index(comp) - 1]

    if comp == 'power_supply':
        next = 'order_review'
    else:
        next = comp_items.keys()[comp_items.keys().index(comp) + 1]

    # Crate max amount variable
    if order.mb: 
        mb = Motherboard.objects.get(id=order.mb)
        max_amount = mb.ram_slots     
    else:
        max_amount = 4

    # 'GET' - Send the data to frontend
    if request.method != 'POST':
        # If comp is ram create form blank form. Ram specified
        if comp == 'ram':
            form = ComponentForm(choices, label, True, max_amount)

        # If not comp is not ram, create a common Component Form
        else:
            form = ComponentForm(choices, label, False)

    # 'POST' - Process the data
    else:
        # Instantiate the form filled with post data.
        if comp == 'ram':
            form = ComponentForm(choices, label, True, max_amount,
                request.POST)
        else:
            form = ComponentForm(choices, label, False, request.POST)

        # Validate the data. Then, update the order.
        if form.is_valid():
            if comp == 'ram': # Set the data to order's ram format.
                ram = form.cleaned_data['comp']
                amount = form.cleaned_data['amount']
                order.ram = str(amount) + 'x' + str(ram)
            else:
                comp_items[comp][2] = form.cleaned_data[comp]

            order.save()
            return HttpResponseRedirect(reverse(f'builder:choose_{comp}',
                args=(order_id, next)))
    context = {'form': form, 'order_id': order_id, 'comp': comp,
        'previous':previous}
    return render(request, 'builder/choose_component.html', context)


def order_review(request, order_id):
    order = Order.objects.get(id=order_id)
    components = {'CPU Brand': order.cpu_brand, 'Motherboard': order.mb,
        'CPU': order.cpu, 'GPU': order.gpu, 'RAM': order.ram,
        'Ref. System': order.rf, 'Case': order.cs, 'Power Supply': order.ps}

    for k, comp in components.items():
        
        if comp and k != "CPU Brand" and k != 'RAM':
            components[k] = Component.objects.get(id=comp)
        elif comp and k == 'RAM':
            amount, id = comp.split("x")
            components[k] = (amount, Component.objects.get(id=id))
    

    context = {'order': order, 'components': components}
    return render(request, 'builder/order_review.html', context)


def get_choices(components):
    """Creates and returns a choices-type list from a given list of components"""
    choices = []
    for comp in components:
        choices.append((comp.id, comp))  
    return choices