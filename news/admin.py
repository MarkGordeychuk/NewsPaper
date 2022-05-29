from django.contrib import admin
from .models import Author, Category, Post, Comment, PostCategory


class CategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = (CategoryInline, )


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
