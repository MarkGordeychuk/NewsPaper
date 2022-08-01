from django.contrib import admin
from .models import Author, Category, Post, Comment, PostCategory
from modeltranslation.admin import TranslationAdmin


class CategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = (CategoryInline, )


# class CategoryAdmin(TranslationAdmin):
#     model = Category


admin.site.register(Author)
admin.site.register(Category, TranslationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
