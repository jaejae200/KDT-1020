from xml.etree.ElementTree import Comment
from django.shortcuts import render, redirect
from .models import Article, Comment as Comment_model
from .forms import ArticleForm, CommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    articles = Article.objects.order_by('-pk')
    
    context = {
        'articles': articles
    }

    return render(request, 'articles/index.html', context)

def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:index')

    else:
        form = ArticleForm()

    context = {
        'form' : form
    }
    return render(request, 'articles/form.html', context)

def detail(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm()

    context = {
        'article' : article,
        'comments' : article.comment_set.all(),
        'comment_form' : comment_form, 
    }
    return render(request, 'articles/detail.html', context)

@login_required
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user == article.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES, instance=article)
            if form.is_valid():
                form.save()
                return redirect('articles:detail', article.pk)
        else: 
            form = ArticleForm(instance=article)

        context = {
            'form' : form
        }
        return render(request, 'articles/form.html', context)
    else:
        return redirect('articles:detail', article.pk)

def delete(request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return redirect('articles:index')

@login_required
def comment_create(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment.save()
    return redirect('articles:detail', article.pk)


def comment_delete(request, article_pk, comment_pk):
    comment = Comment_model.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('articles:detail', article_pk)
    