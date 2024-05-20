from django_filters import FilterSet
from .models import PostReply


class ReplyFilter(FilterSet):

    class Meta:
        model = PostReply
        fields = ['announce']
