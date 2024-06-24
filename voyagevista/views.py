from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Post, Category, Comment
from django.core.paginator import Paginator
from .forms import CommentForm
from django.http import JsonResponse
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator



def category_view(request, category_slug=None):
    """
    View for displaying posts filtered by category.
    """
    category = None
    categories = Category.objects.all()
    posts = Post.objects.filter(status=1).order_by('-created_on')

    if category_slug:
        category = Category.objects.get(slug=category_slug)
        posts = posts.filter(category=category)

    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'categories': categories,
        'page_obj': page_obj,
    }

    return render(request, 'index.html', context)


class PostDetailView(View):
    def get(self, request, slug):
        selected_post = get_object_or_404(Post, slug=slug)
        selected_post.number_of_views += 1  # Increment the number of views
        selected_post.save()
        
        approved_comments = selected_post.comments.filter(approved=True)
        pending_comments = []

        if request.user.is_authenticated:
            pending_comments = selected_post.comments.filter(approved=False, author=request.user)

        is_liked = selected_post.likes.filter(id=request.user.id).exists()

        comments_with_info = []
        for comment in approved_comments:
            is_owner = comment.author.username.lower() == request.user.username.lower()
            comments_with_info.append({"mycomment": comment, "is_owner": is_owner})

        comment_form_instance = CommentForm()
        return render(request, 'post_detail.html', {
            'post': selected_post,
            'comments': comments_with_info,
            'awaiting_comments': pending_comments,
            'comment_form': comment_form_instance,
            'liked': is_liked,
            'is_post_user': (request.user.id == selected_post.author.id),
        })

    def post(self, request, slug):
        selected_post = get_object_or_404(Post, slug=slug)
        approved_comments = selected_post.comments.filter(approved=True)

        if 'edit_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            selected_comment = get_object_or_404(Comment, id=comment_id)
            comment_form_instance = CommentForm(request.POST, instance=selected_comment)
            if comment_form_instance.is_valid():
                comment_form_instance.save()
                messages.success(request, 'Comment updated successfully.')
            else:
                messages.error(request, 'Error updating comment.')

        elif 'delete_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            selected_comment = get_object_or_404(Comment, id=comment_id)
            selected_comment.delete()
            messages.success(request, 'Comment deleted successfully.')

        else:
            comment_form_instance = CommentForm(request.POST)
            if comment_form_instance.is_valid():
                comment = comment_form_instance.save(commit=False)
                comment.author = request.user
                comment.post = selected_post
                comment.save()
                messages.success(request, 'Your comment has been submitted for approval.')
                return HttpResponseRedirect(reverse('post_detail', args=[slug]))

        comments_with_info = []
        for comment in approved_comments:
            is_owner = comment.author.username.lower() == request.user.username.lower()
            comments_with_info.append({"mycomment": comment, "is_owner": is_owner})

        is_liked = selected_post.likes.filter(id=request.user.id).exists()

        return render(request, 'post_detail.html', {
            'post': selected_post,
            'comments': comments_with_info,
            'comment_form': comment_form_instance,
            'liked': is_liked,
            'is_post_user': (request.user.id == selected_post.author.id),
        })

def edit_comment(request, id):
    comment = get_object_or_404(Comment, id=id, author=request.user)
    post = comment.post
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            comment_form.save()
            messages.add_message(request, messages.SUCCESS, 'Your comment has been updated.')
            return redirect('post_detail', slug=post.slug)
    else:
        comment_form = CommentForm(instance=comment)
    
    return render(request, 'edit_comment.html', {
        'comment_form': comment_form,
        'post': post
    })

def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id, author=request.user)
    post = comment.post
    if request.method == 'POST':
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Your comment has been deleted.')
        return redirect('post_detail', slug=post.slug)
    
    return render(request, 'delete_comment.html', {'comment': comment, 'post': post})