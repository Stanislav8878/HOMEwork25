from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
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

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.views = (self.object.views or 0) + 1
        self.object.save(update_fields=['views'])
        return response

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'slug', 'content', 'image', 'is_published']
    template_name = 'blogs/post_form.html'

class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'slug', 'content', 'image', 'is_published']
    template_name = 'blogs/post_form.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blogs:post_list')
    template_name = 'blogs/post_confirm_delete.html'
