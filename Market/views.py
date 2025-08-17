from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.decorators.cache import cache_page
from .forms import NewUserForm, BookForm, ProductForm, ProductInlineFormSet, CategoryFormSet, RatingForm
from datetime import datetime
from django.http import HttpResponse, HttpResponseNotFound
from django.core.paginator import Paginator
from .models import Book, Category, Rating, Post, Product


def index(request):
    return render(request, 'index.html')


def test(request):
    return render(request, 'test.html')


def current_time(request):
    now = datetime.now()
    html = f'''<html>
    <body>
    current time is {now}
    </body>
    </html>'''

    return HttpResponse(html)


def some_test(request):
    is_true = False
    if is_true:
        return HttpResponse(f'''<html>
    <body>
    good
    </body>
    </html>''')
    else:
        return HttpResponseNotFound("<h1>Page not found</h1>")


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Register successful')
            return redirect('market_index')
        messages.error(request, 'Unsuccessful register')
    else:
        form = NewUserForm()
    return render(request, 'register.html', {'register_form': form})


def login_p(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.info(request, 'login successful')
                return redirect('market_index')
        messages.error(request, 'Unsuccessful login')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'login_form': form})


def logout_p(request):
    logout(request)
    messages.success(request, 'You have been logout')
    return redirect('market_index')


def create_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            messages.error(request, 'Invalid Form')
            return redirect('create_book')
    else:
        form = BookForm()
    return render(request, 'book_form.html', {'form': form})


# def some_test(request, name, surname, age):
#     sm_prs = Person.objects.create(name=name, surname=surname, age=age)
#     sm_prs.save()

#.../books?page=2&pages=1
def book_list(request):
    qs = Book.objects.all().order_by('id')

    q = request.GET.get('search', '').strip()
    if q:
        qs = qs.filter(title__icontains=q)

    pages = request.GET.get('pages', '').strip()
    if pages in ['true', '1', 'yes', 'on']:
        qs = qs.order_by('pages')

    is_p = request.GET.get('is_published', '').lower()

    if is_p in ['true', '1', 'yes', 'on']:
        qs = qs.filter(is_published=True)
    elif is_p in ['false', '0', 'no', 'off']:
        qs = qs.filter(is_published=False)

    paginator = Paginator(qs, 2)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    return render(request, 'books.html', {
        'page': page,
        'search': q,
        'pages': pages,
        'is_published': is_p
    })


def create_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'product_form.html', {'form': form})


def manage_category(request):
    formset = CategoryFormSet(request.POST or None, queryset=Category.objects.all())
    if formset.is_valid():
        formset.save()
        return redirect('manage_category')
    return render(request, 'category_list.html', {'formset': formset})


def edit_category_products(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    formset = ProductInlineFormSet(request.POST or None, instance=category)
    if formset.is_valid():
        formset.save()
        return redirect('edit_category_products', category_id=category_id)
    return render(request, 'product_inline.html', {'category': category, 'formset': formset})


@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)

    user_rating = Rating.objects.filter(book=book, user=request.user).first()

    if request.method == "POST":
        form = RatingForm(request.POST, instance=user_rating)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.book = book
            rating.user = request.user
            rating.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = RatingForm(instance=user_rating)

    return render(request, 'book_detail.html', {'book': book, 'form': form, 'user_rating': user_rating})


@cache_page(10)
def post_list(request):
    posts = Post.objects.order_by('-views')[:20]
    return render(request, 'post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    post.views += 1
    post.save(update_fields=['views'])
    return render(request, 'post_detail.html', {'post': post})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart_view')


def cart_view(request):
    cart = request.session.get('cart', {})
    products_ids = [int(i) for i in cart.keys() ]
    products = Product.objects.filter(pk__in=products_ids)
    items = []
    total = 0
    for p in products:
        qty = cart.get(str(p.pk), 0)
        items.append({"product": p, "qty": qty, 'sum': qty * p.price })
        total += qty * p.price
    return render(request, 'cart.html', {'items': items, "total": total})

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('product_list')
    admin_email = 'jetcraker@ukr.net'
    send_mail(
        'Нове замовлення',
        f'замовлення: {cart}',
        admin_email,
        [admin_email],
        fail_silently=False
    )
    request.session['cart'] = {}
    request.session.modified = True
    return render(request, 'checkout_done.html')