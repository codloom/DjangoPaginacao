# Django Paginação (Simples)

Documentação Oficial do Django [Link](https://docs.djangoproject.com/en/4.1/ref/paginator/)

Vídeo Tutorial [Link](https://www.youtube.com/watch?v=kcXPT06LnLQ)

 *myapp/models.py*
``` python
from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name
 ``` 
 
 *myapp/admin.py*
```python
from django.contrib import admin

from myapp.models import Product

# Register your models here.
admin.site.register(Product)
```

Rodar
```python
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser # para criar um usuario administrador para acessar django admin
```

---

Vamos criar nossa view para listar os produtos.
```python
from django.core.paginator import Paginator
from django.shortcuts import render
from myapp.models import Product

def product_list(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 3) # mostra 3 produtos por pagina
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'page_obj': page_obj})
```

*myapp/urls.py*
```python
from django.urls import path 
from myapp import views

urlpatterns = [
    path('', views.product_list, name='product-list'), 
]
```

Criar um template para listar os produtos que cadastramos.
*myapp/templates/list.html*
```html
{% extends 'base.html' %}
{% block title %}index 1{% endblock %}
{% block content %}
<h1>Produtos</h1>
<div class="container"> 
    <table class="table"> 
        <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Nome</th>
                <th scope="col">Preço</th>
                <th scope="col">Descrição</th>
            </tr>
        </thead> 
        <tbody>
            {% for product in page_obj %}
            <tr>
                <th scope="row">{{ product.id }}</th>
                <th scope="row">{{ product.name|upper }}</th>
                <th scope="row">{{ product.price }}</th>
                <th scope="row">{{ product.description }}</th>
            </tr>
            {% endfor %}
        </tbody>
    </table> 
    {% include 'pagination.html' %} 
</div> 
{% endblock %}
```

*myapp/templates/pagination.html*
```html
{% if page_obj.has_other_pages %}
<div class="btn-group" role="group" aria-label="Item pagination">
    {% if page_obj.has_previous %}
        <a href="?page={{ page_obj.previous_page_number }}" class="btn btn-outline-primary">&laquo;</a>
    {% endif %}

    {% for page_number in page_obj.paginator.page_range %}
        {% if page_obj.number == page_number %}
            <button class="btn btn-outline-primary active">
                <span>{{ page_number }} <span class="sr-only">(Atual)</span></span>
            </button>
        {% else %}
            <a href="?page={{ page_number }}" class="btn btn-outline-primary">
                {{ page_number }}
            </a>
        {% endif %}
    {% endfor %}

    {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}" class="btn btn-outline-primary">&raquo;</a>
    {% endif %}
</div>
{% endif %}
```


