from django.contrib import admin


from apps.post.models import Post, LikeContract

admin.site.register(Post)
admin.site.register(LikeContract)
