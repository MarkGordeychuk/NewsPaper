from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.cache import cache

from .models import Post, Author
from .filters import PostFilter
from .forms import PostForm, SubscribeCategoryForm


from pprint import pprint

# Decorator for different types
TYPES = {
    Post.NEWS: {'title': 'News', 'url': 'news/'},
    Post.PAPER: {'title': 'Papers', 'url': 'papers/'},
}


class PostTypeSetter:
    def __init__(self, types: dict):
        self._types = {p_type: {'context': cont, 'classes': dict()} for p_type, cont in types.items()}

    def register(self, url, name):
        def decorator(cls):
            for p_type, value in self._types.items():
                def class_creator():
                    cont = value['context']

                    class Wrapper(cls):
                        post_type = p_type

                        def get_queryset(self):
                            return super().get_queryset().filter(post_type=self.post_type)

                        def get_context_data(self, **kwargs):
                            context = super().get_context_data(**kwargs)
                            context.update(cont)
                            return context

                    return Wrapper

                self._types[p_type]['classes'][url] = {
                    'class': class_creator(),
                    'name': f"news_{p_type.lower()}_{name}",
                }

            return cls

        return decorator

    def get_urlpattern(self):
        for p_type, value in self._types.items():
            for cls_url, cls in value['classes'].items():
                kwargs = {'name': cls['name']}
                yield value['context']['url'] + cls_url, cls['class'], kwargs


ptype_views = PostTypeSetter(TYPES)


# Permission to change post for post author
class PostChanger(PermissionRequiredMixin):
    model = Post

    def has_permission(self):
        return True if self.request.user == self.get_object().author.user else super().has_permission()


# Basic Post Views
@ptype_views.register('', 'list')
class PostsList(ListView):
    model = Post
    ordering = '-date_in'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


@ptype_views.register('<int:pk>', 'detail')
class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


@ptype_views.register('create/', 'create')
class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user.author
        post.post_type = self.post_type
        return super().form_valid(form)


@ptype_views.register('<int:pk>/update/', 'update')
class PostUpdate(PostChanger, UpdateView):
    form_class = PostForm
    template_name = 'post_edit.html'
    permission_required = ('news.change_post',)


@ptype_views.register('<int:pk>/delete/', 'delete')
class PostDelete(PostChanger, DeleteView):
    template_name = 'post_delete.html'
    permission_required = ('news.delete_post',)

    def get_success_url(self):
        return self.object.get_list_url()


class IndexView(TemplateView):
    template_name = 'index.html'


@login_required
def become_author(request):
    user = request.user
    if request.method == 'POST':
        authors_group = Group.objects.get(name='authors')
        if not request.user.groups.filter(name='authors').exists():
            authors_group.user_set.add(user)
        if not hasattr(user, 'author'):
            Author.objects.create(user=user)
    return redirect(reverse('accounts', args=[user.pk]))


@login_required
def subscribe_category(request):
    user = request.user
    if request.method == 'POST':
        form = SubscribeCategoryForm(request.POST)
        if form.is_valid():
            user.categories_subscribed.set(form.cleaned_data['categories'])
            user.save()
    return redirect(reverse('accounts', args=[user.pk]))

