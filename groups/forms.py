from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django import forms
from django.contrib.auth import get_user_model
from django.forms import Form, ModelForm
from django.utils.translation import gettext_lazy as _

from core.forms import RightColumn, SkipUnchangedFileFieldsModelFormMixin
from emoticons.forms import EmoticonPicker

from .models import ForumPost, Group, GroupInvitation

User = get_user_model()


class GroupCreateForm(ModelForm):
    class Meta:
        model = Group
        fields = ["name", "description", "is_private"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("name"),
            Field("description"),
            EmoticonPicker("description"),
            Field("is_private"),
            RightColumn(Submit("submit", _("Create new group"))),
        )


class GroupForm(SkipUnchangedFileFieldsModelFormMixin, ModelForm):
    class Meta:
        model = Group
        fields = ["name", "image", "description", "has_forum", "is_private", "admins"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("name"),
            Field("image"),
            Field("description"),
            EmoticonPicker("description"),
            Field("has_forum"),
            Field("is_private"),
            Field("admins"),
            RightColumn(Submit("submit", _("Update the group"))),
        )

        self.fields["admins"].queryset = User.objects.filter(
            groups_member__in=[self.instance]
        )


class GroupInviteForm(ModelForm):
    class Meta:
        model = GroupInvitation
        fields = ["to_user"]

    def __init__(self, to_user_queryset, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["to_user"].queryset = to_user_queryset

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("to_user"),
            RightColumn(Submit("submit", _("Send invitation"))),
        )


class ForumThreadCreateForm(Form):
    topic = forms.CharField(label=_("Topic"))
    post = forms.CharField(widget=forms.Textarea, label=_("Post"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("topic"),
            Field("post"),
            EmoticonPicker("post"),
            RightColumn(Submit("submit", _("Create thread"))),
        )


class ForumPostForm(ModelForm):
    class Meta:
        model = ForumPost
        fields = ["post"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("post"),
            EmoticonPicker("post"),
            RightColumn(Submit("submit", _("Create post"))),
        )
