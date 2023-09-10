from apps.post.features.create.forms import PostForm
from apps.post.features.list.forms import ReplyForm


class AddReplyFormMixin:
    def get_context_data(self, *args, **kwargs):
        kwargs['reply_form'] = ReplyForm()
        return super().get_context_data(*args, **kwargs)


class AddPostForm:
    def get_context_data(self, *args, **kwargs):
        kwargs['post_form'] = PostForm()
        return super().get_context_data(*args, **kwargs)
