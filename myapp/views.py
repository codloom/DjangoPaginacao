from django.core.paginator import Paginator
from django.shortcuts import render

from myapp.models import Product

def product_list(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 3) # mostra 3 produtos por pagina
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'list.html', {'page_obj': page_obj})