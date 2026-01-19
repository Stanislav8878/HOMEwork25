from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import F
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blogs/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(is_published=True).order_by('-created_at')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blogs/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Аккуратно увеличиваем счётчик просмотров
        Post.objects.filter(pk=obj.pk).update(views=F('views') + 1)
        obj.refresh_from_db(fields=['views'])
        return obj


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'slug', 'content', 'image', 'is_published']
    template_name = 'blogs/post_form.html'
    permission_required = 'blogs.add_post'
    raise_exception = True

    def get_success_url(self):
        return self.object.get_absolute_url()


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'slug', 'content', 'image', 'is_published']
    template_name = 'blogs/post_form.html'
    permission_required = 'blogs.change_post'
    raise_exception = True

    def get_success_url(self):
        return self.object.get_absolute_url()


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blogs:post_list')
    template_name = 'blogs/post_confirm_delete.html'
    permission_required = 'blogs.delete_post'
    raise_exception = True
