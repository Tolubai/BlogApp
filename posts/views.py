from django.contrib import auth
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Post, Comment, PostLike
from .serializers import PostSerializer, CommentSerializer, CommentValidateSerializer, PostValidateSerializer, \
    UserLoginValidateSerializer, UserRegisterValidateSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_list_view(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def post_detail_view(request, pk):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        raise NotFound('Пост не найден')

    if request.method == 'GET':
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        PostLike.objects.create(
            post=post,
            user=request.user
        )
        return Response(data={'message': 'Added your Liked Post'})



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def post_comment_view(request, pk):

    if request.method == 'GET':
        try:
            comments = Comment.objects.filter(post=pk)
        except Comment.DoesNotExist:
            raise NotFound('Комментарии не найден')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommentValidateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    'message': 'ERROR',
                    'error': serializer.errors
                }
            )
        comment = Comment.objects.create(
            post_id=pk,
            text=serializer.validated_data['text'],
            author=request.user
        )
        comment.save()
        return Response(data={'commented'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create_view(request):
    serializer = PostValidateSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            status=status.HTTP_406_NOT_ACCEPTABLE,
            data={
                'message': 'ERROR',
                'error': serializer.errors
            }
        )
    post = Post.objects.create(
        title=serializer.validated_data['title'],
        text=serializer.validated_data['text'],
        author=request.user
    )
    post.save()
    return Response(data={'Post created'})


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = UserLoginValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    'message': 'ERROR',
                    'error': serializer.errors
                }
            )
    username = request.data['username']
    password = request.data['password']
    user = auth.authenticate(username=username, password=password)
    if user:
        try:
            token = Token.objects.get(user=user)
        except:
            token = Token.objects.create(user=user)
        return Response(data={'key': token.key})
    else:
        return Response(data={'massage': 'User not found'})

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserRegisterValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    'message': 'ERROR',
                    'error': serializer.errors
                }
            )
    User.objects.create_user(
        username=request.data['username'],
        email='a@n.ru',
        password=request.data['password'],
        )
    return Response(data={'massage': 'User created'})
