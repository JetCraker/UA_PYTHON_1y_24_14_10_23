from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'list.html'
    context_object_name = 'articles'
    queryset = Article.objects.filter(published=True)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'detail.html'
    context_object_name = 'article'


class ArticleCreateView(CreateView):
    model = Article
    template_name = 'form.html'
    fields = ['title', 'content', 'published']
    success_url = reverse_lazy('article_list')


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'form.html'
    fields = ['title', 'content', 'published']
    success_url = reverse_lazy('article_list')


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy("article_list")
