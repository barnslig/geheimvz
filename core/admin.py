from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User

UserAdmin.fieldsets += (
    (
        _("General"),
        {
            "fields": (
                "image",
                "nickname",
                "pronouns",
                "birthday",
            )
        },
    ),
    (
        _("Personal"),
        {
            "fields": (
                "looking_for",
                "relationship",
                "hobbies",
                "what_i_like",
                "what_i_dont_like",
                "favourite_music",
                "favourite_movies",
                "favourite_books",
                "favourite_food",
                "i_am_good_at",
                "i_wish_for",
            )
        },
    ),
)

admin.site.register(User, UserAdmin)
