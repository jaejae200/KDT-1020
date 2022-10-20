from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm, CommentForm

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
        'comments_form' : comment_form, 
    }
    return render(request, 'articles/detail.html', context)
