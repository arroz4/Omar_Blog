from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
from blog.models import Post,Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.forms import PostForm,CommentForm
from django.urls import reverse_lazy,reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class GalleryView(TemplateView):
    template_name = 'gallery.html'

class CvView(TemplateView):
    template_name = 'cv.html'


class DraftListView(LoginRequiredMixin,ListView):
    template_name = 'blog/post_draft_list.html'
    context_object_name = 'post_draft_list'
    login_url= '/login/'
    # redirect_field_name= 'blog/post_draft_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')
        ###NOT WORKIN
        ##filter is wrong is grabbing from another template

class PostListView(ListView):
    model = Post

    #Esta funcion organiza los post de la lista en orden ascendente por fecha
    ## __lte significa less than y se agrega al final de una funcion en un query para dar ordenes de busqueda se llama lookuptype a esto
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url='/login/'
    redirect_field_name= 'blog/post_detail.html'
    form_class= PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url='/login/'
    redirect_field_name= 'blog/post_detail.html'
    form_class= PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url= reverse_lazy('post_list')



###COMMENT views

def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment= form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk= comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)

##PUBLISH
@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)
