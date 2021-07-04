from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Post, Comment, PostLike


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    author = UserSerializer()

    class Meta:
        model = Post
        fields = 'id title text created_date author comments is_liked likes_count comments_count'.split()

    def get_is_liked(self, obj):
        if PostLike.objects.filter(post=obj, user=self.context['request'].user):
            return True
        return False

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_likes_count(self, obj):
        return PostLike.objects.filter(post=obj).count()


class CommentValidateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=1000)


class PostValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=255)
    text = serializers.CharField(min_length=10, max_length=2000)


class UserLoginValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class UserRegisterValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    password1 = serializers.CharField(max_length=255)

    def validate_username(self, username):
        if User.objects.filter(username=username).count() > 0:
            raise ValidationError('Пользователь уже существует')

    def validate(self, attrs):
        if attrs['password'] != attrs['password1']:
            raise ValidationError('Password did not match')
        return attrs


