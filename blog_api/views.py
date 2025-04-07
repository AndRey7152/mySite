from rest_framework import generics, filters, permissions
from blog.models import Post
from .serializer import PostSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .permissions import IsAuthorOrReadOnly

# Create your views here.
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10

class PostList(generics.ListCreateAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.object.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['body', 'author__profile__bio']
    ordering_fields = ['autor__id', 'publish']
    ordering = ['body']
    pagination_class = StandardResultsSetPagination

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.object.all()
    serializer_class = PostSerializer


class UserPostList(generics.ListAPIView):
    queryset = Post.object.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.kwargs['username']
        return Post.object.filter(author=user)

class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_parms.get('title_only'):
            return ['title']
        return super().get_search_fields(view, request)


