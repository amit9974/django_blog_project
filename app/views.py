from email import message
from multiprocessing import reduction
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import render, get_list_or_404
from django.views.generic import ListView
from .models import Post, Comment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail

# Create your views here.
app_name = 'app'

def home(request):
    return render(request, "app/index.html")

    
# share the post via email 
def post_share(request, post_id):
    #retrive post by ID
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == "POST":
        # form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # ... send email   
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'pythongitcode@gmail.com', [cd['to']])
            sent = True
            return render(request, 'app/share.html', {'post':post, 'form':form, 'sent':sent})
    else:
        form = EmailPostForm()
        return render(request, 'app/share.html', {'post':post, 'form':form, 'sent':sent})


# all post list
def post_list(request):
    posts = Post.published.all()
    comment = Comment.objects.all()
    p= Paginator(posts, 3)
    page_number = request.GET.get('page')
    final = p.get_page(page_number)
    totalpage = final.paginator.num_pages
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    
    context = {'page_obj': page_obj,
                'lastpage':totalpage,
                'totalpagelist':[n+1 for n in range(totalpage)],
                'comment':comment,
                }

    return render(request,'app/list.html', context)



def post_details(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'app/details.html', {'post':post})


def comments(request, id):
    post = Post.objects.get(id=id)
    cmt = CommentForm(request.POST)
    if request.method == 'POST':
        if cmt.is_valid():
            cmt.save()
            return redirect('post_list')
    else:
        cmt = CommentForm()
    return render(request, "app/comment.html", {'cmt':cmt, 'post':post})





