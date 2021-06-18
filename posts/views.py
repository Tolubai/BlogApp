from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


@api_view(['GET'])
def post_list_view(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def post_detail_view(request, pk):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        raise NotFound('Пост не найден')
    serializer = PostSerializer(post)
    return Response(serializer.data)


@api_view(['GET'])
def post_comment_view(request, pk):
    try:
        comments = Comment.objects.filter(post=pk)
    except Comment.DoesNotExist:
        raise NotFound('Комментарии не найден')
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)
