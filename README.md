# Django Paginação com Filtro

Configurar paginação com filtro em Django

Repositório anteriror [Link](https://github.com/djangomy/pagination)

Vídeo Tutorial [Link](https://www.youtube.com/watch?v=0a0oaku1l34)

Documentação do Django (Paginator) [Link](https://docs.djangoproject.com/en/4.1/ref/paginator/)


Atualização na Views.py
```python
from django.core.paginator import Paginator
from django.shortcuts import render
from myapp.models import Product

def product_list(request):
    obj = request.GET.get('obj')
    print(obj)
    if obj:  
        product_list = Product.objects.filter(name__icontains=obj)  
    else:
        product_list = Product.objects.all()   
        
    paginator = Paginator(product_list, 3) # mostra 3 produtos por pagina
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'list.html', {'page_obj': page_obj})
```

Criar um template para listar os produtos que cadastramos.
*myapp/templates/list.html*
```html
{% extends 'base.html' %}
{% block title %}index 1{% endblock %}
{% block content %}
<h1>Produtos</h1>
<div class="container">
		# Adicionar form para pesquisar
    <form class="d-flex gap-3 mt-2" action="{% url 'product-list' %}" method="GET">          
        <span class="fw-bold">Pesquisar: </span>   
        <input name="obj" type="text" value="{{request.GET.obj}}" class="form-control" placeholder="pesquisar pelo nome do produto..."> 
        {% if request.GET.obj %}   
        <a class="btn btn-primary" href="{% url 'product-list' %}">Reset</a>                 
        {% endif %}  
        <button type="submit" class="btn btn-primary">Buscar</button> 
    </form> 
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

Essa parte vamos adicionar o objeto que vai vir do formulário de pesquisa na href da paginação. 
E vamos fazer uma validação simples if else. Existe varios jeito de fazer isso. Optei por fazer no mesmo template.

*myapp/templates/pagination.py*
```html
{% if page_obj.has_other_pages %}
<div class="btn-group" role="group" aria-label="Item pagination">

    {% if page_obj.has_previous %}

        {% if request.GET.obj %}
        <a href="?page={{ page_obj.previous_page_number }}&obj={{request.GET.obj}}" class="btn btn-outline-primary">&laquo;</a> 
        {% else %}
        <a href="?page={{ page_obj.previous_page_number }}" class="btn btn-outline-primary">&laquo;</a> 
        {% endif %} 

    {% endif %}

    {% for page_number in page_obj.paginator.page_range %}

        {% if request.GET.obj %}   
      
            {% if page_obj.number == page_number %}
                <button class="btn btn-outline-primary active">
                    <span>{{ page_number }} <span class="sr-only">(Atual)</span></span>
                </button>
            {% else %}
                <a href="?page={{ page_number }}&obj={{request.GET.obj}}" class="btn btn-outline-primary">
                    {{ page_number }}
                </a>
            {% endif %}

        {% else %}  

            {% if page_obj.number == page_number %}
            <button class="btn btn-outline-primary active">
                <span>{{ page_number }} <span class="sr-only">(Atual)</span></span>
            </button>
            {% else %}
                <a href="?page={{ page_number }}" class="btn btn-outline-primary">
                    {{ page_number }}
                </a>
            {% endif %}
        

        {% endif %}  

    {% endfor %}

    {% if page_obj.has_next %}
        {% if request.GET.obj %}
        <a href="?page={{ page_obj.next_page_number }}&obj={{request.GET.obj}}" class="btn btn-outline-primary">&raquo;</a>
        {% else %}
        <a href="?page={{ page_obj.next_page_number }}" class="btn btn-outline-primary">&raquo;</a>
        {% endif %}    
    {% endif %}

</div>
{% endif %}
``` 


