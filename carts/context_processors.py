from .models import Cart


def cart_count(request):
    count=5
    return dict(count=count)