from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        self.rating = sum(self.post_set.annotate(comment_rating=models.Sum('comment__rating'))
                          .aggregate(sum1=3*models.Sum('rating'), sum2=models.Sum('comment_rating')).values()) \
                      + self.user.comment_set.aggregate(sum3=models.Sum('rating'))['sum3']
        self.save()


class Category(models.Model):
    name = models.CharField(unique=True, max_length=255)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories_subscribed')

    def __str__(self):
        return self.name


class Post(models.Model):
    NEWS = 'NE'
    PAPER = 'PA'
    TYPES = {
        NEWS: 'Новость',
        PAPER: 'Статья',
    }

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=TYPES.items(), default=NEWS, db_column='type')
    date_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    rating = models.IntegerField(default=0)
    marks = models.ManyToManyField(User, through='PostMarks', related_name='post_marks')

    def __str__(self):
        return f"{self.get_post_type_display()}: (ID: {self.pk}, Time: {self.date_in}, Author: {self.author})"

    def like(self, user: User):
        mark_set = PostMarks.objects.filter(post=self, user=user)
        if mark_set.exists():
            mark = mark_set.first()
            if not mark.is_like:
                self.rating += 2
                mark.is_like = True
                mark.save()
        else:
            self.rating += 1
            self.marks.add(user)
        self.save()

    def dislike(self, user: User):
        mark_set = PostMarks.objects.filter(post=self, user=user)
        if mark_set.exists():
            mark = mark_set.first()
            if mark.is_like:
                self.rating -= 2
                mark.is_like = False
                mark.save()
        else:
            self.rating -= 1
            PostMarks.objects.create(post=self, user=user, is_like=False)
        self.save()

    def preview(self):
        return self.content[:124] + '...' if len(self.content) >= 127 else self.content

    def get_absolute_url(self):
        return reverse(f"news_{self.post_type.lower()}_detail", kwargs={'pk': self.pk})

    def get_list_url(self):
        return reverse(f"news_{self.post_type.lower()}_list")

    def get_update_url(self):
        return reverse(f"news_{self.post_type.lower()}_update", kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse(f"news_{self.post_type.lower()}_delete", kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_in = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)
    rating = models.IntegerField(default=0)
    marks = models.ManyToManyField(User, through='CommentMarks', related_name='comment_marks')

    def __str__(self):
        return f"Comment: (ID: {self.pk}, Time: {self.date_in}), Author: {self.author}) to {self.post}"

    def like(self, user: User):
        mark_set = CommentMarks.objects.filter(comment=self, user=user)
        if mark_set.exists():
            mark = mark_set.first()
            if not mark.is_like:
                self.rating += 2
                mark.is_like = True
                mark.save()
        else:
            self.rating += 1
            self.marks.add(user)
        self.save()

    def dislike(self, user: User):
        mark_set = CommentMarks.objects.filter(comment=self, user=user)
        if mark_set.exists():
            mark = mark_set.first()
            if mark.is_like:
                self.rating -= 2
                mark.is_like = False
                mark.save()
        else:
            self.rating -= 1
            CommentMarks.objects.create(comment=self, user=user, is_like=False)
        self.save()


class PostMarks(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)


class CommentMarks(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)
