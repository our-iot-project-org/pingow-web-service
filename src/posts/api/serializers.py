from rest_framework.serializers import ModelSerializer

from posts.models import Post

class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'publish',
        ]


class PostListSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'slug',
            'content',
            'publish',
            'timestamp',
        ]

class PostDetailSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'content',
            'publish',
            'timestamp',
        ]

# """
# data = {
#     "title": "Manual enter post",
#     "content": "This is a post entered manually via console",
#     "publish": "2017-2-2",
#     "slug":"manual-enter-post"
# }
# new_item = PostSerializer(data = data)
# if new_item.is_valid():
#     new_item.save()
# else:
#     print(new_item.errors)
# """"
