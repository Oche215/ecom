from .models import Category, Product

def categories_processor(request):

    categories = Category.objects.all()
    products = Product.objects.filter(category=categories)
    return {'products': products, 'categories': categories}


