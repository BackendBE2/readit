from django.shortcuts import render, redirect
from .models import Article, Tags, Category
from apps.comments.forms import CommentForm


def index(request):
    object_list = Article.objects.all().order_by('-id')

    context = {
        'object_list': object_list
    }

    return render(request, 'index.html', context)


def views_up(request, pk):
    article = Article.objects.get(id=pk)
    article.views += 1
    article.save()
    return redirect('articles:single', article.pk)


def article_single(request, pk):
    article = Article.objects.get(id=pk)
    categories = Category.objects.all()
    recent_articles = Article.objects.all().order_by('-id')[:3]
    tags = Tags.objects.all()
    form = CommentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.article_id = pk
        obj.save()
        return redirect(f'/blog-detail/{pk}#article-comments')
    context = {
        'object': article,
        'categories': categories,
        'recent_articles': recent_articles,
        'tags': tags,
        'form': form,
    }
    return render(request, 'blog-single.html', context)
