from django_components import Component, register


@register("post")
class Post(Component):
    template_name = "post.html"

    def get_context_data(
        self,
        created_at,
        created_by,
        post,
        id=None,
        attachment_height=None,
        attachment_url=None,
        attachment_width=None,
        attachment=None,
        show_send_message=True,
    ):
        current_user = None

        request = self.outer_context.get("request")
        if request:
            current_user = request.user

        return {
            "id": id,
            "can_send_messages": show_send_message
            and created_by
            and created_by.privacy_settings.get_can_send_messages(current_user),
            "created_at": created_at,
            "created_by": created_by,
            "post": post,
            "attachment_height": attachment_height,
            "attachment_url": attachment_url,
            "attachment_width": attachment_width,
            "attachment": attachment,
        }
