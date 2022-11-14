from .models import Component, CPU, Motherboard

def get_available_comps(comp, order):
    """Returns a list of components that are available in the DB, by their type
            and socket."""

    if comp == 'cpu':
        available_comps = CPU.objects.filter(socket=order.cpu_brand)
    elif comp == 'motherboard':
        available_comps = Motherboard.objects.filter(socket=order.cpu_brand)
    else:
        available_comps = Component.objects.filter(c_type=comp)

    return available_comps


def get_previous_next(comp_keys, comp):
    """Returns the previous and the next keywords of the given keyword,
        by a sequence list."""

    if comp == 'cpu':
        previous = 'index'
    else:
        previous = comp_keys[comp_keys.index(comp) - 1]

    if comp == 'power_supply':
        next = None
    else:
        next = comp_keys[comp_keys.index(comp) + 1]

    return previous, next


def get_max_amount(order):
    """Returns a max amount of compatible ram sticks, by a motherboard's max or
        a default (4)."""

    if order.motherboard: 
        mother = Motherboard.objects.get(c_type='motherboard', id=order.motherboard)
        max_amount = mother.ram_slots     
    else:
        max_amount = 4
    
    return max_amount