from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Component, Order
from .forms import *
from .functions import *


def index(request):
    """The starting page. The user chooses the cpu's brand."""

    choices = [('AMD', 'AMD'), ('Intel', 'Intel')]
    label = "To start, select a socket-brand for your CPU and Motherboard:"

    if request.method != 'POST':
        form = ComponentForm(choices, label, True)

    else:
        form = ComponentForm(choices, label, True, request.POST)
        if form.is_valid():
            order = Order()
            order.cpu_brand = form.cleaned_data['comp']
            order.save()
            return HttpResponseRedirect(reverse('builder:choose_component',
                args=(order.id, 'cpu')))

    context = {'form': form}
    return render(request, 'builder/index.html', context)


def choose_component(request, order_id, comp):
    """The user chooses a component"""
    
    ### Data and data access handling
    # Dict with common keywords and label suffixes.
    components = {'cpu':'CPU', 'motherboard':'Motherboard', 'gpu':'GPU',
        'ram':'RAM', 'ref_system':'Ref. System', 'case':'Case',
        'power_supply':'Power Supply'}
    
    order = Order.objects.get(id=order_id)

    # Create the list of compatible components by type and socket.
    available_comps = get_available_comps(comp, order)
    
    # Create the form's choices and label.
    choices = get_choices(available_comps)
    label = f'Select the {components[comp]}:'

    # Create the keyword of the previous and the next component to choose
    comp_keys = list(components.keys())
    previous, next = get_previous_next(comp_keys, comp)
    
    # Crate max amount variable
    max_amount = get_max_amount(order)
    

    ### Form handling
    # 'GET' - Send the data to frontend
    if request.method != 'POST':
        # If comp is ram create form blank form. Ram specified
        if comp == 'ram':
            form = RamForm(choices, label, max_amount)

        # If not comp is not ram, create a common Component Form
        else:
            form = ComponentForm(choices, label, False)

    # 'POST' - Process the data
    else:
        # Create a form bounded to the post data.
        if comp == 'ram':
            form = RamForm(choices, label, max_amount, request.POST)
        else:
            form = ComponentForm(choices, label, False, request.POST)

        # Validate the data. Then, update the order.
        if form.is_valid():
            if form.cleaned_data['comp'] == '':
                # Set order field to None if comp was skipped
                setattr(order, comp, None)
            elif comp == 'ram':
                # If comp is ram, set data to order's ram field format
                amount = form.cleaned_data['amount']
                order.ram = str(amount) + 'x' + str(form.cleaned_data['comp'])
            else:
                # Set order's field to forms data
                setattr(order, comp, form.cleaned_data['comp'])
            
            order.save()

            if comp == 'power_supply':
                return HttpResponseRedirect(reverse('builder:order_review',
                    args=(order_id,)))
            else:
                return HttpResponseRedirect(reverse('builder:choose_component',
                    args=(order_id, next)))
                    
    context = {'form': form, 'order_id': order_id, 'comp': comp,
        'previous':previous}
    return render(request, 'builder/choose_component.html', context)


def order_review(request, order_id):
    order = Order.objects.get(id=order_id)
    components = {'CPU Brand': order.cpu_brand, 'Motherboard': order.motherboard,
        'CPU': order.cpu, 'GPU': order.gpu, 'RAM': order.ram,
        'Ref. System': order.ref_system, 'Case': order.case,
        'Power Supply': order.power_supply}

    for k, comp in components.items():
        
        if comp and k != "CPU Brand" and k != 'RAM':
            components[k] = Component.objects.get(id=comp)
        elif comp and k == 'RAM':
            amount, id = comp.split("x")
            components[k] = (amount, Component.objects.get(id=id))
    

    context = {'order': order, 'components': components, 'previous': 'power_supply'}
    return render(request, 'builder/order_review.html', context)


def get_choices(components):
    """Creates and returns a choices-type list from a given list of components"""
    choices = []
    for comp in components:
        choices.append((comp.id, comp))  
    return choices