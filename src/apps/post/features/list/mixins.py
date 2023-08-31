class AddRepliesWithoutFirstMixin:
    def get_context_data(self, *args, **kwargs):
        posts = self.object_list

        for post in posts:
            replies = post.replies.all()

            post.replies_first = replies.first()
            post.replies_without_first = replies[1:]

        return super().get_context_data(*args, **kwargs)
