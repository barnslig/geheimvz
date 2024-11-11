from django_components import Component, register


@register("post")
class Post(Component):
    template_name = "post.html"

    def get_context_data(self, created_at, created_by, post):
        current_user = None

        request = self.outer_context.get("request")
        if request:
            current_user = request.user

        return {
            "can_send_messages": created_by.get_can_send_messages(current_user),
            "created_at": created_at,
            "created_by": created_by,
            "post": post,
        }
