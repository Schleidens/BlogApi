from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, serializers, status, exceptions
from rest_framework.response import Response
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from random import randint

from knox.auth import TokenAuthentication


from .serializers import (
    getBlogSerializer,
    postBlogSerializer,
    getCommentSerializer,
    postCommentSerializer
)
from .models import blogPost, blogComment

# Create your views here.


class blogViewset(ModelViewSet):
    queryset = blogPost.objects.filter(draft=False).order_by("-created_date")

    # set different serializer for both post and get request
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return getBlogSerializer
        elif self.request.method == 'POST':
            return postBlogSerializer
        else:
            return getBlogSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    lookup_field = 'slug'

    def get_object(self):
        queryset = self.get_queryset()
        slug = self.kwargs['slug']

        try:
            obj = queryset.get(slug=slug)
        except blogPost.DoesNotExist:
            raise exceptions.NotFound("No blog match your request")
        return obj

    # override the save methods
    def perform_create(self, serializer):

        # set the  author field to the authenticated user
        serializer.validated_data['author'] = self.request.user

        # return error if a user try to send data as a non authenticated user
        user = self.request.user
        if serializer.validated_data['author'] != user:
            raise serializers.ValidationError(
                {"error": "User mismatch. The 'author' field must be the authenticated user."}
            )

        '''
            fill the slug field with the current title turn into a slug
            and add random number if the slug already exist to make it unique
        '''
        title = serializer.validated_data['title']
        slug = slugify(title)

        if blogPost.objects.filter(slug=slug).exists():
            slug = slug + "-" + str(randint(1000, 9999))
            serializer.validated_data['slug'] = slug
        else:
            serializer.validated_data['slug'] = slug
        serializer.save()

    # return error if non authenticated user try deleting data as other user
    def destroy(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed('DELETE')

    # return error if non authenticated user try modifying data as other user
    def update(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed('PUT')


'''
--------------------------------
views part for blog comment
--------------------------------
'''


class commentViewset(ModelViewSet):
    queryset = blogComment.objects.all().order_by("-created_date")

    # auth and permissions
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # set different serializer for both post and get request
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return getCommentSerializer
        elif self.request.method == 'POST':
            return postCommentSerializer
        else:
            return getCommentSerializer

    # filter comment list by blog post and return error if blog blog id requested doesn't exist
    def get_queryset(self):
        queryset = super().get_queryset()

        # get blog_id from url request
        slug = self.kwargs.get('slug')
        # get the single blog object  by passing the blog_slug
        blog = get_object_or_404(blogPost, slug=slug)

        if blog:
            queryset = queryset.filter(blog=blog)
        else:
            raise exceptions.NotFound("No blog match your request")

        return queryset

    # handle the request from save methods
    def perform_create(self, serializer):
        # set the  author field to the authenticated user
        serializer.validated_data['author'] = self.request.user

        # return error if a user try to send data as a non authenticated user
        user = self.request.user
        if serializer.validated_data['author'] != user:
            raise serializers.ValidationError(
                {"error": "User mismatch. The 'author' field must be the authenticated user."}
            )

        '''
            set the blog object for comment
        '''
        # get slug from url request
        slug = self.kwargs.get('slug')
        # get the single blog object  by passing the slug
        blog = get_object_or_404(blogPost, slug=slug)

        serializer.validated_data['blog'] = blog

        # perform the save action
        serializer.save()

    # handle delete request
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response(
                {"error": "You do not have permission to delete this comment."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # return error if non authenticated user try modifying data as other user
        if instance.author != request.user:
            return Response(
                {"error": "You do not have permission to update this comment."},
                status=status.HTTP_403_FORBIDDEN
            )

        # get slug from url request
        slug = self.kwargs.get('slug')
        # get the single blog object  by passing the slug as filter
        blog = get_object_or_404(blogPost, slug=slug)

        data = request.data.copy()
        data['blog'] = blog.id

        serializer = self.get_serializer(instance, data=data)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response(serializer.data)


'''
--------------------------------
Dashboard view for user post
--------------------------------
'''


class UserBlogViewset(ModelViewSet):
    queryset = blogPost.objects.all().order_by("-created_date")

    # auth and permissions
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # override lookup_field to use slug instead of pk
    lookup_field = 'slug'

    # set different serializer for both post and get request
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return getBlogSerializer
        elif self.request.method == 'POST':
            return postBlogSerializer
        else:
            return getBlogSerializer

    def get_queryset(self):
        # Retrieve the user from the request
        user = self.request.user

        # Modify the queryset based on the user
        queryset = super().get_queryset()

        # Filter the queryset based on the user
        queryset = queryset.filter(author=user)

        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        slug = self.kwargs['slug']

        try:
            obj = queryset.get(slug=slug)
        except blogPost.DoesNotExist:
            raise exceptions.NotFound("No blog match your request")
        return obj

    # prevent objects creation from this endpoint
    def create(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed('POST')

    # return error if non authenticated user try deleting data as other user
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response(
                {"error": "You do not have permission to delete this post."},
                status=status.HTTP_403_FORBIDDEN
            )
        super().destroy(request, *args, **kwargs)

        # Return a success message
        return Response({"message": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    # return error if non authenticated user try modifying data as other user
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response(
                {"error": "You do not have permission to update this post."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    # perform action for draft and undraft the blog post
    @action(detail=True, methods=['put'])
    def set_draft(self, request, slug):
        instance = self.get_object()

        # make sure the request is from the authenticated user and return error if not
        if instance.author != request.user:
            return Response(
                {"error": "You do not have permission to update this post."},
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            instance.draft = not instance.draft
            instance.save()

            # set different message base on current draft value
            if instance.draft:
                message = 'Post set to draft'
            else:
                message = 'post has been published successfully'
            return Response({'message': message}, status=status.HTTP_200_OK)
