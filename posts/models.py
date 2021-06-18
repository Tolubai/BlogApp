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
    post = models.ForeignKey(Post, verbose_name='пост', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='техт')
    commented_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), verbose_name='Автор', on_delete=models.CASCADE)

