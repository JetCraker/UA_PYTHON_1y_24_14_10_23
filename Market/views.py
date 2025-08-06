from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import NewUserForm, BookForm
from datetime import datetime
from django.http import HttpResponse, HttpResponseNotFound
from django.core.paginator import Paginator
from .models import Book


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