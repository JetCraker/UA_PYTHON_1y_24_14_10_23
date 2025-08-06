from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Ad, Rubric
from .forms import AdForm
from django.http import HttpResponse, JsonResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.template.loader import get_template, select_template, render_to_string
from django.template import Template

from django.views.decorators.http import require_http_methods, require_GET, require_POST, require_safe
from django.views.decorators.gzip import gzip_page

from django.views.generic import ListView, CreateView, View


@require_GET
def ad_list(request):
    ads = Ad.objects.select_related('rubric').order_by('-created_at')
    return render(request, 'ad_list.html', {'ads': ads})


def ad_create(request):
    if request.method == "POST":
        form = AdForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = AdForm()
    return render(request, 'ad_form.html', {'form': form})


def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    return render(request, 'ad_detail.html', {'ad': ad})

@require_GET
def ad_update(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if request.method == "POST":
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad_detail', pk=pk)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ad_form.html', {'form': form})


def ad_delete(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if request.method == "POST":
        ad.delete()
        return redirect('ad_list')
    return render(request, 'ad_confirm_delete.html', {'ad': ad})


def func(request):
    resp = HttpResponse(content='This is main page', content_type='text/plain; charset=UTF-8', status=200)

    resp['keyword'] = 'Python'

    resp.write('123123')
    resp.writelines(['456', '678'])

    return resp


def load_temp(request):
    template = get_template('base.html')
    html = template.render()
    return HttpResponse(html)


def select_temp(request):
    template = select_template(['ad_confirm.html', 'base.html'])
    return HttpResponse(template.render())

# def rend_t_str(request):
#     email = render_to_string('email.html', context={'name': "Alice", 'name2':'ROman'})
#     send_email(email)
#     return HttpResponse(status=200, content='Відправлено успішно')


def req_methods(request):
    data = {
    "host":request.get_host(),
    "port":request.get_port(),
    "path":request.get_full_path(),
    "secure": request.is_secure(),
    "mega": request.build_absolute_uri()
    }
    return JsonResponse(data)


def save_item(request):
    # якась логіка збереження
    url = reverse('ad_list')

    return HttpResponse(url)

def site_moved(request):
    url = reverse('ad_create')
    return HttpResponsePermanentRedirect(url)


@gzip_page
def gz(request):
    text = '...' * 10000

    return HttpResponse(text)


class DBList(ListView):
    model = Ad
    template_name = 'ad_list.html'

