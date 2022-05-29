from news.models import *


user1 = User.objects.create_user('Ванька')
user2 = User.objects.create_user('Женька')

av1 = Author.objects.create(user=user1)
av2 = Author.objects.create(user=user2)

cat1 = Category.objects.create(name='Спорт')
cat2 = Category.objects.create(name='Политика')
cat3 = Category.objects.create(name='Образование')
cat4 = Category.objects.create(name='IT-индустрия')

new1 = Post.objects.create(author=av2, post_type=Post.PAPER, title='Что творится в мире?',
                           content='В мире вообще невесть что творится!')
new1.category.add(cat2)
new2 = Post.objects.create(author=av1, post_type=Post.NEWS, title='Ничего про спорт')
new2.category.add(cat1)
new3 = Post.objects.create(author=av2, post_type=Post.PAPER, title='Немного о модуле D2',
                           content='Как-то у вас там всё сумбурно, буд-то из разных мест накопипастили 😋')
new3.category.add(cat3, cat4)

com1 = Comment.objects.create(post=new2, author=user2, content='Лентяй!')
com2 = Comment.objects.create(post=new2, author=new2.author.user, content='Ну прости уж')
com3 = Comment.objects.create(post=new3, author=user1, content='Да, да. Я согласен.')
com4 = Comment.objects.create(post=new1, author=user1, content='😧')

new2.like(user2)
new2.dislike(user2)  # Тут Женька понял, что ошибся
new1.like(new1.author.user)
new3.like(user2)
new3.like(user1)

com1.like(com1.author)
com2.dislike(user2)
com3.like(user1)
com3.like(user2)
com4.like(user2)

av1.update_rating()
av2.update_rating()

best_author = Author.objects.order_by('-rating').first()
print(best_author.user.username, best_author.rating, '\n')

best_paper = Post.objects.filter(post_type=Post.PAPER).latest('rating')
print(f"({best_paper.date_in}) Автор: {best_paper.author.user.username}\n"
      + f"{best_paper.title}\n{best_paper.preview()}\n\u2764 {best_paper.rating}")

for com in best_paper.comment_set.all():
    print(f"({com.date_in}): {com.author.username}: {com.content} \u2764 {com.rating}")
