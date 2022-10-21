from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Component


def index(request):
    """The starting page. The user chooses the cpu's brand."""
    order = url_str() # An order with the components the user chooses.
    context = {'order': order}
    try:
        brand = request.POST['brand']
    except KeyError:
        return render(request, 'builder/index.html', context)
    else:
        order = url_str(order, f"brand:{brand}-")
        return HttpResponseRedirect(reverse('builder:cpu',
            args=(order,)))


def cpu(request, order):
    """The user chooses the CPU."""
    splitted_order = split_order(order)
    order = [tuple(order.split(":"))]
    available_comps = Component.objects.filter(c_type='CPU').filter(
        model__icontains=order[0][1])
    order = order_raw
    context = {'components': available_comps, 'order': order}

    try:
        chosen_cpu = available_comps.get(pk=request.POST['cpu'])
        chosen_cpu = request.POST['cpu']
    except  (KeyError, Component.DoesNotExist):
        return render(request, 'builder/cpu.html', context)
    else:
        order += "-cpu:" + chosen_cpu
        return HttpResponseRedirect(reverse('builder:motherboard',
            args=(order,)))
   

def motherboard(request, order):
    order_raw = order
    order_split = order.split("-")
    order = []
    for o in order_split:
        order.append(tuple(o.split(":")))
    context = {'order': order}
    return render(request, 'builder/motherboard.html', context)


def url_str(order=None, string=None):
    if order and string:
        order += string
        return order
    else:
        return 'order'


def split_order(order):
    fields = order.split("-")
    splitted_order = []
    for field in fields:
        splitted_order.append(tuple(field.split(":")))
    return splitted_order
    