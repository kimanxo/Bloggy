from django.http import (
    HttpResponse,
    HttpResponse as HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
    HttpResponseNotFound,
)
from django.views.generic import ListView, TemplateView
from django.views.generic import View
from .models import (
    Category,
    Author,
    Article,
    Contact,
    ReadLater,
    Testimonial,
    Comment,
    Subscriber,
    Favourite,
    Vote,
)
from django.views.generic.edit import CreateView
from .forms import ContactForm
from django_htmx.http import (
    retarget,
)  # target swap locations in the DOM from the server
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


# Views


class IndexView(View):
    def get(self, request):
        categories = Category.objects.all()  # getting all the categories
        authors = Author.objects.prefetch_related(
            "articles"
        ).all()  # Adjust prefetching to include related articles
        latest = (
            Article.objects.order_by("-created_at")
            .select_related("author", "category")
            .first()  # getting the latest post
        )
        featured = (
            Article.objects.order_by("?").select_related("author", "category").first()
        )
        articles = Article.objects.select_related("author", "category").order_by(
            "-created_at"
        )[:4]

        # getting the testimonials in a descending order (latest first)
        testimonials = Testimonial.objects.order_by("-created_at")

        # paginating the testimonials by one testimonial per page
        paginator = Paginator(testimonials, 1)

        # specifying the get request parameter to fetch the next / previous instance
        page_number = request.GET.get("page", 1)
        testimonials_page = paginator.get_page(page_number)

        # checking if the request is htmx originated, if yes return only the right testimonial instance
        if request.htmx:
            return render(
                request,
                "landing/testimonials.html",
                context={
                    "testimonials": testimonials_page,
                },
            )

        # if it's not htmx originated, then return the whole page content
        else:
            return render(
                request,
                "landing/index.html",
                context={
                    "categories": categories,
                    "authors": authors,
                    "articles": articles,
                    "latest": latest,
                    "featured": featured,
                    "testimonials": testimonials_page,
                },
            )

    def post(self, request):
        if request.htmx and request.headers.get("src") == "newsletters":
            email = request.POST.get("email")
            if email:
                if Subscriber.objects.filter(email=email).exists():
                    return render(
                        request,
                        "partials/subscribed.html",
                        {"message": "You're already subscribed"},
                    )
                else:
                    Subscriber.objects.create(email=email)
                    return render(
                        request,
                        "partials/subscribed.html",
                        {"message": "Congrats! You're subscribed now"},
                    )
            else:
                return HttpResponseBadRequest("Invalid email address")

        return HttpResponseNotAllowed("GET")


# using django generic class based view ListView to render  a template that contains a list of elements for the same db tabl
class BlogView(ListView):
    template_name = (
        "blog/index.html"  # specifying the name of the template that should be rendered
    )
    model = Article  # specifying the corresponding db table
    context_object_name = "articles"  # overriding the context object name
    paginate_by = 5  # number of articles per page

    # returning the right page if the request is htmx originated, else return the whole page
    def get_template_names(self) -> list[str]:
        query = self.request.GET.get("query")
        if self.request.htmx and self.request.headers.get("src") == "search":
            return ["post.html", query]
        if self.request.htmx:
            return ["blog/posts.html"]
        return ["blog/index.html"]

    # overriding the default context to add the latest post into it
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest"] = (
            Article.objects.select_related("author", "category")
            .order_by("-created_at")
            .first()
        )
        query = self.request.GET.get("query")
        if query:
            context["results"] = Article.objects.select_related(
                "author", "category"
            ).filter(title__icontains=query)
        return context


# static template page for the privacy policy page
class PrivacyPolicyView(TemplateView):
    template_name = "privacy_policy/index.html"


# contact form logic
class ContactView(CreateView):
    """
    Handles the display and submission of the contact form.
    """

    form_class = (
        ContactForm  # specify the form class we created earlier in the forms.py file
    )
    model = Contact  # specifying the concerned db table
    template_name = "contact/index.html"  # specifying the template to be rendered
    success_url = "/contact"  # where the user should be redirected if the submission was successful, "/contact" means we're keeping the user on the same page
    context_object_name = "form"  # here we are just overriding the context object name to "form" to make it more relevant

    def form_valid(self, form):  # if the form is valid
        form.save()  # we should save data to the form
        response_html = """
        <div class="success_container">
            <p>
                Your message has been successfully submitted to the admin. Expect a reply within a maximum duration of 24 hours.
            </p>
            <a class="send_again" href="">Send another message</a>
        </div>
        """  # this is the HTML response that will be displayed to the user after successful submission
        response = HttpResponse(response_html)
        if self.request.htmx:
            return retarget(
                response, "form"
            )  # here we use htmx retarget method to inject the response into the HTML element with the class of "form"
        return super().form_valid(
            form
        )  # ensure the default behavior for non-HTMX requests


# static template page for the about page
class AboutView(TemplateView):
    template_name = "about/index.html"


# this view is responsible for rendering a template that  displays the posts written by  a specific author
class AuthorPostsView(TemplateView):
    template_name = "author_posts/index.html"

    # Override the context data to add our own context data
    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            author = Author.objects.select_related().get(pk=pk)  # fetching the author
            articles = (
                Article.objects.select_related("author", "category")
                .filter(author=pk)
                .order_by("-created_at")
            )  # fetching the articles written by the specified author
        except Author.DoesNotExist:
            author = None
            articles = Article.objects.none()

        context["author"] = author
        context["articles"] = articles
        return context


# this view is responsible for rendering a template that  displays the posts under a specific category
class CategoryPostsView(TemplateView):
    template_name = "category_posts/index.html"  # the template to be rendered

    # Override the context data to add our own context data
    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            category = Category.objects.select_related().get(
                pk=pk
            )  # fetching the category
            articles = (
                Article.objects.select_related("author", "category")
                .filter(category=pk)
                .order_by("-created_at")
            )  # fetching the articles under the specified category
            count = articles.count()  # counting how many posts we have in the category
        except Category.DoesNotExist:
            category = None
            articles = Article.objects.none()
            count = 0

        context["category"] = category
        context["articles"] = articles
        context["count"] = count

        return context


# this view is responsible for rendering a template that  displays  aspeicific post with crud functionalityclass ArticleView(View):
class ArticleView(View):
    def get(self, request, pk):
        try:
            article = Article.objects.select_related("author", "category").get(
                pk=pk
            )  # fetching the article
        except Article.DoesNotExist:
            return HttpResponseNotFound("Article not found")

        is_bookmarked = is_scheduled = upvoted = downvoted = False
        if request.user.is_authenticated:
            is_bookmarked = Favourite.objects.filter(
                user=request.user, post=article
            ).exists()
            is_scheduled = ReadLater.objects.filter(
                user=request.user, post=article
            ).exists()
            upvoted = Vote.objects.filter(
                user=request.user, article=article, vote_type="up"
            ).exists()
            downvoted = Vote.objects.filter(
                user=request.user, article=article, vote_type="down"
            ).exists()

        comments = (
            Comment.objects.select_related("user")
            .filter(article=article)
            .order_by("-created_at")
        )
        paginator = Paginator(comments, 5)
        page_number = self.request.GET.get("page", 1)
        comments_page = paginator.get_page(page_number)

        if request.htmx:
            return render(
                request, "article/cmts.html", context={"comments": comments_page}
            )

        related_articles = Article.objects.filter(category=article.category).exclude(
            pk=pk
        )
        return render(
            request,
            "article/index.html",
            context={
                "article": article,
                "comments": comments_page,
                "count": comments.count(),
                "articles": related_articles,
                "is_bookmarked": is_bookmarked,
                "is_scheduled": is_scheduled,
                "upvoted": upvoted,
                "downvoted": downvoted,
            },
        )

    def post(self, request, pk, *args, **kwargs):
        if request.htmx and request.headers.get("src") == "comment":
            article = get_object_or_404(Article, pk=pk)
            Comment.objects.create(
                user=request.user,
                article=article,
                content=request.POST.get("comment", ""),
            )
            comments = (
                Comment.objects.select_related("user")
                .filter(article=article)
                .order_by("-created_at")
            )
            paginator = Paginator(comments, 5)
            page_number = self.request.GET.get("page", 1)
            comments_page = paginator.get_page(page_number)
            return render(
                request, "article/cmts.html", context={"comments": comments_page}
            )

        elif request.htmx and request.headers.get("src") in ["up", "down"]:
            article = get_object_or_404(Article, pk=pk)
            src = request.headers.get("src")
            user_vote, created = Vote.objects.get_or_create(
                user=request.user, article=article, defaults={"vote_type": src}
            )

            if not created:
                if user_vote.vote_type != src:
                    if src == "up":
                        article.upvote += 1
                        article.downvote -= 1
                    else:
                        article.upvote -= 1
                        article.downvote += 1
                    user_vote.vote_type = src
                    user_vote.save()
            else:
                if src == "up":
                    article.upvote += 1
                else:
                    article.downvote += 1
            article.save()

            upvoted = Vote.objects.filter(
                user=request.user, article=article, vote_type="up"
            ).exists()
            downvoted = Vote.objects.filter(
                user=request.user, article=article, vote_type="down"
            ).exists()

            return render(
                request,
                "partials/ratings.html",
                {"article": article, "upvoted": upvoted, "downvoted": downvoted},
            )

        elif request.htmx and request.headers.get("src") in ["bookmark", "bookmarked"]:
            article = get_object_or_404(Article, pk=request.POST["article"])
            if request.headers.get("src") == "bookmark":
                Favourite.objects.get_or_create(user=request.user, post=article)
                return render(
                    request, "partials/bookmarked.html", context={"article": article}
                )
            else:
                Favourite.objects.filter(user=request.user, post=article).delete()
                return render(
                    request, "partials/bookmark.html", context={"article": article}
                )

        elif request.htmx and request.headers.get("src") in ["schedule", "scheduled"]:
            article = get_object_or_404(Article, pk=request.POST["article"])
            if request.headers.get("src") == "schedule":
                ReadLater.objects.get_or_create(user=request.user, post=article)
                return render(
                    request, "partials/scheduled.html", context={"article": article}
                )
            else:
                ReadLater.objects.filter(user=request.user, post=article).delete()
                return render(
                    request, "partials/schedule.html", context={"article": article}
                )

        return HttpResponseNotAllowed("POST")

    def delete(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if request.htmx:
            comment_pk = request.headers.get("comment")
            Comment.objects.filter(pk=comment_pk, article=article).delete()
            comments = (
                Comment.objects.select_related("user")
                .filter(article=article)
                .order_by("-created_at")
            )
            paginator = Paginator(comments, 5)
            page_number = self.request.GET.get("page", 1)
            comments_page = paginator.get_page(page_number)
            return render(
                request, "article/cmts.html", context={"comments": comments_page}
            )

        return HttpResponseNotAllowed("DELETE")


class SettingsView(TemplateView):
    template_name = "settings/index.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ReadingListView(TemplateView):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    template_name = "reading_list/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            items = ReadLater.objects.select_related("post").filter(
                user=self.request.user
            )
        except ReadLater.DoesNotExist:
            items = None

        context["items"] = items
        return context


class SavedPostsView(TemplateView):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    template_name = "saved_posts/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            items = Favourite.objects.select_related("post").filter(
                user=self.request.user
            )
        except Favourite.DoesNotExist:
            items = None

        context["items"] = items
        return context


class UpvotedPostsView(TemplateView):
    template_name = "upvoted_posts/index.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve upvoted articles by the current user
        items = Vote.objects.select_related("article").filter(
            user=self.request.user, vote_type="up"
        )

        context["items"] = items
        return context


class DownvotedPostsView(TemplateView):
    template_name = "downvoted_posts/index.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve upvoted articles by the current user
        items = Vote.objects.filter(user=self.request.user, vote_type="down")

        context["items"] = items
        return context
