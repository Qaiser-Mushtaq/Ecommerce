from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)
    def __str__(self):
        return self.name
   
    
   
   
    class Meta: # data about data more instructions about our table
        verbose_name_plural = 'categories' 
    def get_absolute_url(self):
        return reverse('category_list', args=[self.slug])
    
    
    
class Product(models.Model):
    name = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(max_length=200, default=' ')
    image = models.ImageField(upload_to='images/')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    slug = models.SlugField(max_length=10)

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id])

    def __str__(self):
        return self.name
    
    @staticmethod
    def get_product_by_id(ids):
        return Product.objects.filter(id__in = ids)
       
    
class Customer(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 50)
    phone = models.CharField(max_length = 15)
    email = models.EmailField()
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.first_name
    
    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True
        return False
    @staticmethod
    def get_customer_by_email(email):
        try:
            if Customer.objects.get(email=email):
                return True
        except:
                return False



class Orders(models.Model):
    product = models.ForeignKey(Product,  on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    date = models.DateTimeField()
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.customer.first_name
    
    def placeorder(self):
        self.save()