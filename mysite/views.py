from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from mysite.models import Post,Comment,Profile
from .forms import PostForm,CommentForm,UserCreateForm,ProfileForm,UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

def post_list(request):
    posts = Post.objects.filter(published_date__lte = timezone.now()).order_by('published_date')
    comment_and_posts = []
    for post in posts:
        comment_and_posts.append([post,len(Comment.objects.filter(post_id = post.id))])
    return render(request,'mysite/post_list.html',{'comment_and_posts':comment_and_posts})

def post_detail(request,pk):
	post = get_object_or_404(Post,pk=pk)
	return render(request,'mysite/post_detail.html',{'post':post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'mysite/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if(request.user != post.author):
        return redirect('post_detail',pk=post.pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'mysite/post_edit.html', {'form': form})

@login_required
def post_draft_list(request,username):
    posts = Post.objects.filter(published_date__isnull=True).filter(author__username=username).order_by('created_date')
    return render(request, 'mysite/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk = pk)
    post.publish()
    return redirect('post_detail',pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if(request.user != post.author):
        return redirect('post_detail',pk=post.pk)
    post.delete()
    return redirect('post_list')

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'mysite/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


def SignUp(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=raw_password)
            login(request,user)
            return redirect('post_list')
    else:
        form = UserCreateForm()
    return render(request, 'registration/signup.html', {'form': form})



@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST,instance=request.user)
        profile_form = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # messages.success(request, _('Your profile was successfully updated!'))
            return redirect('profile_edit')
        else:
            pass
            # messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile_edit.html', {
        'form': user_form,
        'profile_form': profile_form
    })

@login_required
def profile_view(request,username):
    user = User.objects.get(username=username)
    return render(request, 'profiles/Profile.html', {'user':user})