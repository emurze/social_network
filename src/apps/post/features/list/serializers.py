from rest_framework import serializers

from apps.post.models import Reply


class ReplySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    photo = serializers.CharField(source='user.photo')

    class Meta:
        model = Reply
        fields = ('content', 'username', 'created', 'photo')
