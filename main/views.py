from django.http import Http404
from django.shortcuts import render, redirect
from .models import Users, DownLink, Product, Cart, Order, \
    ResumeFile, DetailsOrder, Category, Picture, Size
from .forms import LinkForm, CommentForm
from .down_link import down_linker

from .telegram import send_message_in_telegram


def index(request):
    """
    Главная страница
    """
    return render(request, 'main/index.html', )

def download(request):
    """Скачать резюме"""
    resume = ResumeFile.objects.get(name='Тест')
    return redirect(resume.file.url)

def run(request):
    """
    Страница с сокращением ссылок
    """

    _new_link = ''
    links = LinkForm()
    usr = request.user
    if request.method == 'GET':
        links = LinkForm(request.GET)
        if links.is_valid():
            work_link = links.cleaned_data['old_link']
            DownLink.objects.get_or_create(old_link=work_link)
            database_link = DownLink.objects.get(old_link=work_link)
            database_link.new_link = down_linker(work_link)
            database_link.save()
            _new_link = database_link.new_link
            return render(request, 'main/down_link.html',
                              {"link": links, 'new_link': _new_link, 'usr': usr})
    return render(request, 'main/down_link.html', {"link": links, 'new_link': _new_link, 'usr': usr})


# <--------------------------------->
# Магазин, добавить в корзину, корзина:
# <--------------------------------->

def shop_page(request):
    """
    Основная страница интернет-магазина
    Активное: Добавление товара в корзину
    """

    product = Product.objects.all()
    usr = request.user
    if request.method == 'POST':
        if not request.user.is_authenticated:  # Если не авторизован - редиректит на авторизацию
            return redirect('/login')
        add_to_cart(request=request) # добавить продукт в корзину

    if request.method == 'GET' and 'category' in request.GET:
        context = change_category(request=request)
        return render(request, 'main/shop.html', context)

    context = {
        'pr': product,
        'usr': usr
    }
    return render(request, 'main/shop.html', context)


def change_category(request):
    """
    Выбор категории
    Возвращает context с теми товарами, категория которых выбрана
    """

    sneakers = Category.objects.get(category='Кроссовки')
    gumshoes = Category.objects.get(category='Кеды')
    shoes = Category.objects.get(category='Туфли')
    ankle_boot = Category.objects.get(category='Сапоги')
    product = Product.objects.all()
    usr = request.user
    if request.GET['category'] == 'Все':
        product = Product.objects.all()
    elif request.GET['category'] == 'Кроссовки':
        product = Product.objects.filter(category=sneakers)
    elif request.GET['category'] == 'Кеды':
        product = Product.objects.filter(category=gumshoes)
    elif request.GET['category'] == 'Туфли':
        product = Product.objects.filter(category=shoes)
    elif request.GET['category'] == 'Сапоги':
        product = Product.objects.filter(category=ankle_boot)

    context = {
        'pr': product,
        'usr': usr
    }

    return context


def add_to_cart(request):
    """
    Функция добавления продукта в корзину:
    Если продукт уже есть в корзине - добавляет новое количество к уже существующему.
    Если продукта в корзине нет - создаёт его там.
    """
    quantity = request.POST['count']
    product_name = request.POST['product']
    product = Product.objects.get(name=product_name)
    size = Size.objects.get(product=product, size=request.POST['size'])

    if Cart.objects.filter(product=product, owner=request.user, completed=False, size=size):
        exists_product = Cart.objects.get(product=product, owner=request.user, completed=False, size=size)
        old_quantity = exists_product.count #Старое количество
        new_count = int(old_quantity) + int(quantity) #считаем новое количество
        exists_product.total_unit_price = int(product.price) * new_count
        exists_product.count = new_count #меняем на новое количество
        exists_product.save() #сохраняем
    else:
        Cart.objects.create(product=product, count=quantity, owner=request.user, size=size)


def cart_page(request):
    """
    Страница Корзины.
    Активное: "Очистить корзину", "Удалить из корзины (1 ед. товара), "Заказать", "История заказов".
    """

    if not request.user.is_authenticated:  # Если не авторизован - редиректит на авторизацию
        return redirect('/login')

    cart_count = len(Cart.objects.filter(owner=request.user, completed=False)) # Количество товаров в корзине
    cart = Cart.objects.filter(owner=request.user)
    order = Order.objects.filter(owner=request.user)
    details_order = DetailsOrder.objects.filter(owner=request.user)
    full_sum = check_full_cumm_for_cart_page(request)
    usr = request.user

    context = {
        'cart': cart,
        'usr': usr,
        'order': order,
        'full_sum': full_sum,
        'cart_count': cart_count,
        'details_order': details_order
    }

    if request.method == 'GET': # Кнопка: "Очистить корзину"
        if 'destroy' in request.GET:
            Cart.objects.filter(owner=request.user, completed=False).update(completed=True)
            return redirect('/cart')
        elif 'delete' in request.GET: # Кнопка "Удалить из корзины"
            string = request.GET['delete']
            product, size = seek_elements(request=string)
            this_cart = Cart.objects.get(owner=request.user, product=product, size=size)
            this_cart.delete()
            return redirect('/cart')
        elif 'minus' in request.GET or 'plus' in request.GET:
            get_changed_product(request=request)
            return redirect('/cart')
        elif get_title_from_cart_form(request): # Кнопка "Заказать"

            new_details = DetailsOrder.objects.create(
                owner=request.user,
                first_name=request.GET['first_name'],
                last_name=request.GET['last_name'],
                email=request.GET['email'],
                number_phone=request.GET['number_phone'],
                comment=request.GET['comment'],
                payment_state=full_sum
            ) # добавляем в таблицу детали заказа

            for title in get_title_from_cart_form(request):
                nothing_, product_, size_ = title.split('%')
                product = Product.objects.get(name=product_)
                size = Size.objects.get(size=size_, product=product)
                count = request.GET[title]
                old_obj = Cart.objects.get(product=product, owner=request.user, completed=False, size=size)
                new_count = int(count)
                old_obj.count = new_count
                old_obj.total_unit_price = int(product.price) * new_count
                old_obj.completed = True
                old_obj.save()
                new_order = Order.objects.create(owner=request.user, products=old_obj,
                                                  price=old_obj.total_unit_price)
                new_order.details.add(new_details) # добавляем детали заказа к заказу

            tg_message = make_message_for_telegram(new_details) # Сформировать сообщение в телеграм
            send_message_in_telegram(tg_message) # Отправить сообщение в телеграм
            return redirect('/cart')

    return render(request, 'main/cart.html', context)


# <--------------------------------->
# Функции для корзины:
# <--------------------------------->




def get_changed_product(request):
    if 'minus' in request.GET:
        string = request.GET['minus']
        change_product, size = seek_elements(request=string)
        prod = Cart.objects.get(owner=request.user, product=change_product, completed=False, size=size)
        prod.count -= 1
        prod.save()
    elif 'plus' in request.GET:
        string = request.GET['plus']
        change_product, size = seek_elements(request=string)
        prod = Cart.objects.get(owner=request.user, product=change_product, completed=False, size=size)
        prod.count += 1
        prod.save()


def seek_elements(request):
    string = request
    size_, product_ = string.split('%')
    product = Product.objects.get(name=product_)
    size = Size.objects.get(product=product, size=size_)
    return product, size


def get_title_from_cart_form(request):
    """
    Получает загаловки с "count" из request запроса
    """
    name_list = []
    items = request.GET.items()
    for item in items:
        for it in item:
            if 'count' in it:
                name_list.append(it)
    return name_list


def check_full_cumm_for_cart_page(request):
    """
    Считает общую сумму в корзине
    """
    cart = Cart.objects.filter(owner=request.user, completed=False)
    full_price = 0
    for field in cart:
        full_price += (field.product.price * field.count)
    return full_price


# <--------------------------------->
# Страницы с товарами по отдельности:
# <--------------------------------->


def get_product_page(request, slug):
    product = Product.objects.get(slug__iexact=slug) # Получаем продукт из slug
    comment = CommentForm()
    sizes = Size.objects.filter(product=product)
    new_comment = Users.objects.filter(
        product=product).order_by('-id')  # Комментарии на странице, отсортированные от последнего
    prod_img = Picture.objects.filter(product=product)

    context = {
        'comment': comment,
        'new_comment': new_comment,
        'product': product,
        'prod_img': prod_img,
        'sizes': sizes
    }

    if request.method == 'GET':
        comment = CommentForm(request.GET)
        if comment.is_valid():
            Users.objects.create(product=product,
                                 comment=comment.cleaned_data["comment"],
                                 owner=request.user) # Сохранить новый комментарий
            return redirect(request.path)

    elif request.method == 'POST':
        if not request.user.is_authenticated:  # Если не авторизован - редиректит на авторизацию
            return redirect('/login')

        add_to_cart(request) # Добавить в корзину

    return render(request, 'main/product_page.html', context)


# <--------------------------------->
# Для телеграм-бота:
# <--------------------------------->


def make_message_for_telegram(details: DetailsOrder):
    """Формирует сообщение для телеграма"""
    order_products = []
    for order in details.orders.all():
        order_products.append(f'{order.products.product}, кол-во: {order.products.count} шт.')

    message = f'Пользователь: {details.owner} \n' \
              f'Имя: {details.first_name} \n' \
              f'Фамилия: {details.last_name} \n' \
              f'Email: {details.email} \n' \
              f'Телефон: {details.number_phone} \n' \
              f'Комментарий к заказу: {details.comment} \n\n' \
              f'Сделал на сайте следующий заказ' \
              f'на общую сумму: {details.payment_state} рублей.\n\n\n\n' \
              f'В заказе: \n\n' \
              f'{[prod for prod in order_products]}'

    return message
