from .models import Category, Product
def categories_processor(request):
    category = Category.objects.all()
    return({'category':category})
def products_processor(request):
    products = Product.objects.all()
    return({"product":products})