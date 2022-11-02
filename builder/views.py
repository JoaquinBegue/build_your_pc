from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .forms import *


def index(request):
    """The starting page. The user chooses the cpu's brand."""

    if request.method != 'POST':
        form = BrandForm()    
    else:
        form = BrandForm(request.POST)
        if form.is_valid():
            order = Order()
            order.cpu_brand = form.cleaned_data['brand']
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
    
    cpu_choices = []
    for comp in available_comps:
        cpu_choices.append((str(comp.id), str(comp)))

    if request.method != 'POST':
        form = CpuForm(cpu_choices)
    else:
        form = CpuForm(request.POST)
        if form.is_valid():
            order.cpu = form.cleaned_data['cpu']
            order.save()
            return HttpResponseRedirect(reverse('builder:order_review',
                args=(order_id,)))
    
    context = {'form': form, 'order_id': order_id}
    return render(request, 'builder/cpu.html', context)


def motherboard(request, order_id):
    """The user chooses the motherboard."""

    # Get the order object and the available components (compatible ones)
    order = Order.objects.get(id=order_id)
    available_comps = Motherboard.objects.filter(socket=order.cpu_brand)
    context = {'components': available_comps, 'order_id': order_id}

    if request.method == 'POST':
        order.mb = request.POST.get('mb', None)
        order.save()
        return HttpResponseRedirect(reverse('builder:gpu',
            args=(order_id,)))
    
    return render(request, 'builder/motherboard.html', context)


def gpu(request, order_id):
    """The user chooses the GPU."""

    # Get the order object and the available components (compatible ones)
    order = Order.objects.get(id=order_id)
    available_comps = GPU.objects.all()
    context = {'components': available_comps, 'order_id': order_id}

    if request.method == 'POST':
        order.gpu = request.POST.get('gpu', None)
        order.save()
        return HttpResponseRedirect(reverse('builder:ram',
            args=(order_id,)))
    
    return render(request, 'builder/gpu.html', context)


def ram(request, order_id):
    """The user chooses the ram."""

    # Get the order object and the available components (compatible ones)
    order = Order.objects.get(id=order_id)
    available_comps = RAM.objects.all()
    
    if order.mb:
        mb = Motherboard.objects.get(id=order.mb)
        max_ram_slots = mb.ram_slots
    else:
        max_ram_slots = 4

    context = {'components': available_comps, 'order_id': order_id,
        'max_ram_slots': max_ram_slots}

    if request.method == 'POST':
        ram_order = ""
        total_ram = 0
        for ram in available_comps:
            if request.POST.get(str(ram.id), "0") != "0":
                total_ram += int(request.POST.get(str(ram.id), "0"))
                ram_order += str(request.POST.get(str(ram.id), "0"))
                ram_order += "x" + str(ram.id) + "-"
        
        order.ram = ram_order[:-1]
        order.save()
        return HttpResponseRedirect(reverse('builder:order_review',
            args=(order_id,)))
    
    return render(request, 'builder/ram.html', context)


def order_review(request, order_id):
    order = Order.objects.get(id=order_id)
    components = {'CPU Brand': order.cpu_brand, 'Motherboard': order.mb,
        'CPU': order.cpu, 'GPU': order.gpu, 'RAM': order.ram,
        'Ref. System': order.rf, 'Case': order.cs, 'Power Supply': order.ps}

    for k, comp in components.items():
        
        if comp and k == "CPU Brand":
            pass

        elif comp and k != "RAM":
            components[k] = Component.objects.get(id=comp)

        elif comp and k == "RAM":
            ram_order = comp.split("-")
            order = dict()

            for ram in ram_order:
                amount, id = ram.split("x")
                order[amount] = Component.objects.get(id=id)
            
            components[k] = order

    context = {'order': order, 'components': components}
    return render(request, 'builder/order_review.html', context)


def check(request, arg):
    """Checks the previous page behavior."""

    context = {'arg':arg}
    return render(request, 'builder/check.html', context)