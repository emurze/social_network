from .forms import PostForm, ReplyForm


class AddReplyFormMixin:
    def get_context_data(self, *args, **kwargs):
        kwargs['reply_form'] = ReplyForm()
        return super().get_context_data(*args, **kwargs)


class AddPostForm:
    def get_context_data(self, *args, **kwargs):
        kwargs['post_form'] = PostForm()
        return super().get_context_data(*args, **kwargs)
