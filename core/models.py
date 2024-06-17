from django.db import models
from ckeditor.fields import RichTextField
from allauth.account.auth_backends import get_user_model


# DB modles:


class Author(models.Model):
    username = models.CharField(
        primary_key=True, max_length=32, null=False, blank=False
    )
    name = models.CharField(max_length=64, null=False, blank=False)
    description = models.TextField(max_length=255, null=False, blank=False)
    image = models.ImageField(upload_to="authors_images")
    facebook = models.URLField(max_length=255, null=False, blank=True)
    instagram = models.URLField(max_length=255, null=False, blank=True)
    twitter = models.URLField(max_length=255, null=False, blank=True)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=32, null=False, blank=False, primary_key=True)
    description = models.CharField(max_length=128, null=False, blank=False)
    image = models.ImageField(upload_to="categories_images")
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"  # overriding the default verbose_name_plural for the category table


class Article(models.Model):
    slug = models.SlugField(max_length=256, null=False, blank=False, primary_key=True)
    title = models.CharField(max_length=256, null=False, blank=False)
    excert = models.TextField(max_length=512, null=False, blank=False)
    content = RichTextField(max_length=8192, null=False, blank=False)
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)
    image = models.ImageField(
        upload_to="articles_images", blank=True
    )  # media folder for this field = "articles_images"
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="articles",  # relationship reverse description
    )
    author = models.ForeignKey(
        Author,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="articles",
    )

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    content = models.TextField(max_length=2048, null=False, blank=False)
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="comments",
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    user = models.ForeignKey(
        get_user_model(),  # each comment belongs to one user
        blank=False,
        null=False,
        related_name="comments",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return (
            self.content[:10] + "..."
        )  # overrding comment content display on the admin panel


class Contact(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    email = models.EmailField(max_length=64, null=False, blank=False)
    subject = models.CharField(max_length=64, null=False, blank=False)
    message = models.TextField(max_length=640, null=False, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)


class Testimonial(models.Model):
    name = models.CharField(max_length=32, null=False, blank=False, primary_key=True)
    image = models.ImageField(upload_to="testimonials_images")
    description = models.CharField(max_length=128, null=False, blank=False)
    content = models.TextField(blank=False, max_length=200, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.ForeignKey(
        get_user_model(),  # each profile belongs to one user
        blank=False,
        null=False,
        related_name="profile",
        on_delete=models.CASCADE,
    )

    picture = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Favourite(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Article, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"


class ReadLater(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Article, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"


class Newsletter(models.Model):
    subject = models.CharField(max_length=255, blank=False, null=False)
    message = RichTextField(max_length=8192, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Subscriber(models.Model):
    email = models.EmailField(max_length=64, blank=False, null=False)
    subscribed_at = models.DateTimeField(auto_now_add=True)


class Vote(models.Model):
    VOTE_CHOICES = [("up", "Upvote"), ("down", "Downvote")]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=4, choices=VOTE_CHOICES)

    class Meta:
        unique_together = ("user", "article")
