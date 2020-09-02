from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.utils import timezone
from PIL import Image

User = get_user_model()


class DownLink(models.Model):
    old_link = models.TextField('Старая ссылка')
    new_link = models.TextField('Новая ссылка')

    def __str__(self):
        return self.old_link

    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'


class Category(models.Model):
    category = models.CharField('Категория', max_length=100, null=True)

    def __str__(self):
        return f'{self.category}'


class Product(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    img = models.ImageField(default='no-image.png', upload_to='product_image')
    slug = models.SlugField(max_length=150, unique=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('product_url', kwargs={'slug': self.slug})


class Size(models.Model):
    size = models.CharField('Размер', max_length=100, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.size} - {self.product}'


class Picture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    img = models.ImageField(default='no-image.png', upload_to='product_image')

    def __str__(self):
        return f'{self.product}'



class Cart(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
    total_unit_price = models.PositiveIntegerField(null=True)
    completed = models.BooleanField(default=False)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'owner: {self.owner}; product: {self.product}; count {self.count}'


class Order(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Заказчик')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    products = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Продукты')
    price = models.IntegerField(null=True, verbose_name='Общая сумма заказа')
    details = models.ManyToManyField('DetailsOrder', blank=True, related_name='orders')


    def __str__(self):
        return f'{self.owner} - {self.date} - {self.price}'


class Users(models.Model): #Комментарии на страницах продуктов
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    comment = models.TextField('Комментарий', null=True)
    comment_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.owner}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class ResumeFile(models.Model):

    name = models.CharField(verbose_name='Название файла', max_length=100)
    file = models.FileField(upload_to='product_image', verbose_name='Файл')
    is_active = models.BooleanField(default=True, verbose_name='Доступен')

    def __str__(self):
        return f'{self.name}'



class DetailsOrder(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    payment_state = models.CharField('Итоговая сумма', max_length=100)
    email = models.EmailField('Емеил', max_length=250)
    number_phone = models.CharField('Номер телефона', max_length=100)
    comment = models.TextField('Комментарий')
    date_order = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.owner} {self.date_order}'
