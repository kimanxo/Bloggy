from django.contrib import admin
from .models import (
    Article,
    Author,
    Comment,
    Category,
    Contact,
    ReadLater,
    Testimonial,
    Profile,
    Newsletter,
    Subscriber,
    Favourite,
    Vote,
)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
    )  # Fields to display in list view
    list_filter = ("created_at",)  # Fields to filter by
    search_fields = ("name", "description")  # Fields to search within
    ordering = ("name", "created_at")  # Default sorting (ascending and descending)


admin.site.register(Category, CategoryAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)  # Fields to display in list view
    search_fields = (
        "name",
        "description",
    )  # Fields to search within
    ordering = ("name",)  # Default sorting (ascending and descending)


admin.site.register(Author, AuthorAdmin)


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("title",)
    }  # prepopulating the slug field from the title field

    list_display = (
        "title",
        "created_at",
        "category",
    )  # Fields to display in list view
    list_filter = (
        "created_at",
        "category",
    )  # Fields to filter by
    search_fields = (
        "title",
        "content",
    )  # Fields to search within
    ordering = (
        "title",
        "created_at",
        "category",
    )  # Default sorting (ascending and descending)


admin.site.register(Article, ArticleAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = "user", "created_at"  # Fields to display in list view
    search_fields = ("content", "user")  # Fields to search within
    ordering = ("created_at",)  # Default sorting (ascending and descending)


admin.site.register(Comment, CommentAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "subject",
        "email",
        "sent_at",
    )  # Fields to display in list view
    list_filter = ("sent_at",)  # Fields to filter by
    search_fields = ("name", "subject", "email")  # Fields to search within
    ordering = ("name", "sent_at")  # Default sorting (ascending and descending)


admin.site.register(Contact, ContactAdmin)


class TestimonialAdmin(admin.ModelAdmin):
    list_display = "name", "created_at"  # Fields to display in list view
    search_fields = ("content", "name")  # Fields to search within
    ordering = ("created_at",)  # Default sorting (ascending and descending)


admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(Profile)
admin.site.register(ReadLater)
admin.site.register(Newsletter)
admin.site.register(Subscriber)
admin.site.register(Favourite)
admin.site.register(Vote)
