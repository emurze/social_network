from django.contrib import admin


from apps.post.models import Post, LikeContract, Reply

admin.site.register(Post)
admin.site.register(LikeContract)
admin.site.register(Reply)
