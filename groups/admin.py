from django.contrib import admin

from .models import ForumPost, ForumThread, Group, GroupInvitation


class ForumThreadInline(admin.TabularInline):
    model = ForumThread
    extra = 0
    ordering = ("-updated_at",)


class GroupAdmin(admin.ModelAdmin):
    inlines = [ForumThreadInline]


class ForumPostInline(admin.StackedInline):
    model = ForumPost
    extra = 0
    ordering = ("-created_at",)


class ForumThreadAdmin(admin.ModelAdmin):
    inlines = [ForumPostInline]
    readonly_fields = (
        "created_at",
        "updated_at",
    )


admin.site.register(Group, GroupAdmin)
admin.site.register(GroupInvitation)
admin.site.register(ForumThread, ForumThreadAdmin)
