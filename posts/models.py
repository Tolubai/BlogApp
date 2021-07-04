from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model


class Post(models.Model):
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
    title = models.CharField(max_length=255, verbose_name='Название')
    text = models.TextField(verbose_name='Техт')
    created_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), verbose_name='Автор', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
    post = models.ForeignKey(Post, verbose_name='пост', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name='техт')
    commented_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), verbose_name='Автор', on_delete=models.CASCADE)


class PostLike(models.Model):
    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
    post = models.ForeignKey(Post, verbose_name='пост', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='пользователь', on_delete=models.CASCADE)

