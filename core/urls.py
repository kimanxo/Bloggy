from django.urls import path
from .views import (
    IndexView,
    BlogView,
    CategoryPostsView,
    AuthorPostsView,
    ArticleView,
    PrivacyPolicyView,
    ContactView,
    AboutView,
    SettingsView,
    ReadingListView,
)


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("blog/", BlogView.as_view(), name="blog"),
    path("blog/category/<str:pk>", CategoryPostsView.as_view(), name="category_posts"),
    path("blog/author/<str:pk>", AuthorPostsView.as_view(), name="author_posts"),
    path("blog/article/<slug:pk>", ArticleView.as_view(), name="article"),
    path("privacy_policy", PrivacyPolicyView.as_view(), name="privacy_policy"),
    path("contact", ContactView.as_view(), name="contact"),
    path("about", AboutView.as_view(), name="about"),
    path("accounts/settings", SettingsView.as_view(), name="settings"),
    path("accounts/reading_list", ReadingListView.as_view(), name="reading_list"),
    
    # path(
    #     "post/<int:post_id>/remove_from_favourites/",
    #     RemoveFromFavourites.as_view(),
    #     name="remove_from_favourites",
    # ),
]
