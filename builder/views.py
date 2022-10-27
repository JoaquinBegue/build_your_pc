from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Component, Order


def index(request):
    """The starting page. The user chooses the cpu's brand."""

    if request.method == 'POST':
        order = Order(cpu_brand=request.POST['brand'])
        order.save()
        return HttpResponseRedirect(reverse('builder:cpu',
            args=(order.id,)))

    return render(request, 'builder/index.html')
        

def cpu(request, order_id):
    """The user chooses the CPU."""

    # Get the order object and the available components (compatible ones)
    order = Order.objects.get(id=order_id)
    available_comps = Component.objects.filter(c_type='CPU').filter(
        socket=order.cpu_brand)
    context = {'components': available_comps, 'order_id': order_id}

    if request.method == 'POST':
        order.cpu = request.POST.get('cpu', None)
        order.save()
        return HttpResponseRedirect(reverse('builder:motherboard',
            args=(order_id,)))
    
    return render(request, 'builder/cpu.html', context)


def motherboard(request, order_id):
    """The user chooses the motherboard."""

    # Get the order object and the available components (compatible ones)
    order = Order.objects.get(id=order_id)
    available_comps = Component.objects.filter(c_type='MB').filter(
        socket=order.cpu_brand)
    context = {'components': available_comps, 'order_id': order_id}

    if request.method == 'POST':
        order.mb = request.POST.get('mb', None)
        order.save()
        return HttpResponseRedirect(reverse('builder:gpu',
            args=(order_id,)))
    
    return render(request, 'builder/motherboard.html', context)


def gpu(request, order_id):
    """The user chooses the motherboard."""

    # Get the order object and the available components (compatible ones)
    order = Order.objects.get(id=order_id)
    available_comps = Component.objects.filter(c_type='GPU')
    context = {'components': available_comps, 'order_id': order_id}

    if request.method == 'POST':
        order.gpu = request.POST.get('gpu', None)
        order.save()
        return HttpResponseRedirect(reverse('builder:order_review',
            args=(order_id,)))
    
    return render(request, 'builder/gpu.html', context)

def order_review(request, order_id):
    order = Order.objects.get(id=order_id)
    components = {'Motherboard': order.mb, 'CPU': order.cpu,
        'GPU': order.gpu, 'RAM': order.ram, 'Ref. System': order.rf,
        'Case': order.cs, 'Power Supply': order.ps}

    for k, comp in components.items():
        if comp:
            components[k] = Component.objects.get(id=comp)

    print(components)
    context = {'order': order, 'components': components}
    return render(request, 'builder/order_review.html', context)