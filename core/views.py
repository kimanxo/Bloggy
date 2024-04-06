from pydoc import HTMLRepr
from django.http import HttpResponse, HttpResponse as HttpResponse
from django.views.generic import ListView, TemplateView
from django.views.generic import View
from .models import Category, Author, Article, Contact, Testimonial, Comment, Subscriber

from django.views.generic.edit import CreateView
from .forms import ContactForm
from django_htmx.http import (
    retarget,
)  # target swap locations in the DOM from the server
from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# Views


class IndexView(View):
    def get(self, request):
        categories = Category.objects.all()  # getting all the categories
        authors = Author.objects.prefetch_related().all()
        latest = (
            Article.objects.order_by("-created_at").prefetch_related().first()
        )  # getting the latest post
        featured = Article.objects.order_by("?").prefetch_related().first()
        articles = Article.objects.prefetch_related().all().order_by("-created_at")[:4]

        # getting the testimonials in a decending order (latest first)
        testimonials = Testimonial.objects.prefetch_related().order_by("-created_at")

        # paginating the testimonials by one testimonial per page
        paginator = Paginator(testimonials, 1)

        # specifying the get request parameter to fetch the next / previous instance
        page_number = self.request.GET.get("page", 1)
        testimonials_page = paginator.get_page(page_number)
        testimonials = testimonials_page

        # checking if the request is htmx originated, if yes return only the right testimonial instance
        if request.htmx:
            return render(
                request,
                "landing/testimonials.html",
                context={
                    "testimonials": testimonials,
                },
            )

        # if it's not htmx originated, then  return the whole page content
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
                    "testimonials": testimonials,
                },
            )

    def post(self, request):
        if request.htmx and request.header.get("src") == "newsletter":
            try:

                if (
                    Subscriber.objects.prefetch_related().all()
                    and Subscriber.objects.prefetch_related().get(
                        email=request.POST.get("email")
                    )
                ):
                    return render(
                        request,
                        "partials/subscribed.html",
                        {"message": "you're already subscribed"},
                    )

            except Subscriber.DoesNotExist:
                Subscriber.objects.create(email=request.POST.get("email"))
                return render(
                    request,
                    "partials/subscribed.html",
                    {"message": "Congrats!, you're subscribed now"},
                )
        else:
            return HttpResponse("")


# using django generic class based view ListView to render  a template that contains a list of elements for the same db tabl
class BlogView(ListView):
    template_name = (
        "blog/index.html"  # specifying the name of the template that should be rendered
    )
    model = Article  # specifying the corresponding db table
    context_object_name = "articles"  # ovverifying the context object name
    paginate_by = 5  # number of articles per page

    # returning the right page if the request is htmx originated , else return the wole page
    def get_template_names(self) -> list[str]:
        super().get_template_names()
        if self.request.htmx:
            return "blog/posts.html"
        return "blog/index.html"

    # overriding the default context to add the latest post into it
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest"] = (
            Article.objects.prefetch_related().order_by("-created_at").first()
        )
        return context


# static template page for the privacy policy page
class PrivacyPolicyView(TemplateView):
    template_name = "privacy_policy/index.html"


# contact form logic
class ContactView(CreateView):
    form_class = (
        ContactForm  # specify the form class we created earlier in the forms.py file
    )
    model = Contact  # specifying the concerned db tabel
    template_name = "contact/index.html"  # specifying the template to be rendered
    success_url = "/contact"  # where the user should be redirected if the submission was successful, "/contact" means we"re keeping the user in the same page
    context_object_name = "form"  # here we are just ovverriding the context object name to "form" to make it more relevant

    def form_valid(self, form):  # if the form is valid
        form.save()  # we should save data to the form
        response = HttpResponse(
            """ 
        <div class="success_container">
            <p>
            Your message have been successfully submitted to the admin, expect a reply within a maximum duration of a 24 hours
            </p>
            <a class="send_again" href=""> Send another message  </a>
        </div>
            """
        )  # this is the html response that will be displayed to the user after successful submission
        return retarget(
            response, "form"
        )  # here we use htmx retarget method to inject the response into the html element with the class of "form"


# static template page for the about page
class AboutView(TemplateView):
    template_name = "about/index.html"


# this view is responsible for rendering a template that  displays the posts written by  a specific author
class AuthorPostsView(TemplateView):
    template_name = "author_posts/index.html"

    # as always, we need to ovveride the context data to add our own context data
    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author"] = Author.objects.prefetch_related().get(
            pk=pk
        )  # fetching the author
        context["articles"] = (
            Article.objects.prefetch_related().filter(author=pk).order_by("-created_at")
        )  # fetching the articles written by  the specified author
        return context


# this view is responsible for rendering a template that  displays the posts under a specific category
class CategoryPostsView(TemplateView):
    template_name = "category_posts/index.html"  # the template to be rendered

    # as always, we need to ovveride the context data to add our own context data
    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.prefetch_related().get(
            pk=pk
        )  # fetching the category name
        context["articles"] = (
            Article.objects.prefetch_related()
            .filter(category=pk)
            .order_by("-created_at")
        )  # fetching the articles under the specified category
        context["count"] = (
            Article.objects.prefetch_related().filter(category=pk).count()
        )  # just counting how many posts we have in the category

        return context


# this view is responsible for rendering a template that  displays  aspeicific post with crud functionality
class ArticleView(View):
    def get(self, request, pk):
        article = Article.objects.prefetch_related().get(pk=pk)  # fetching the article
        commentos = (
            Comment.objects.prefetch_related()
            .filter(article=article)
            .order_by("-created_at")
        )  # fetching the comments
        paginator = Paginator(commentos, 5)  # paginating the comments
        page_number = self.request.GET.get("page", 1)
        comments_page = paginator.get_page(page_number)
        comments = comments_page

        if request.htmx:  # if the request is htmx originated
            return render(
                request,
                "article/cmts.html",  # render the comments section
                context={
                    "comments": comments,
                },  # with the comments as context
            )
        else:
            return render(
                request,
                "article/index.html",  # render the whole page
                context={
                    "article": article,
                    "comments": comments,
                    "count": commentos.count(),
                },
            )

    def post(self, request, pk, *args, **kwargs):  # if the request is POST
        if (
            request.htmx and request.headers.get("src") == "comment"
        ):  # and if it's from htmx
            Comment.objects.create(
                user=request.user,
                article=Article.objects.get(pk=pk),
                content=request.POST["comment"],
            )  # save the comment
            # refetch the comments
            comments = Comment.objects.filter(
                article=Article.objects.get(pk=pk)
            ).order_by("-created_at")
            paginator = Paginator(comments, 5)
            page_number = self.request.GET.get("page", 1)
            comments_page = paginator.get_page(page_number)
            comments = comments_page
            return render(request, "article/cmts.html", context={"comments": comments})
        elif request.htmx and (
            request.headers.get("src") == "up" or request.headers.get("src") == "down"
        ):
            article = Article.objects.get(pk=pk)
            if request.headers.get("src") == "up":
                article.upvote += 1
                article.save()
            else:
                article.downvote += 1
                article.save()

            return render(request, "partials/ratings.html", {"article": article})

    def delete(self, request, pk, *args, **kwargs):  # if the request is Delete
        comments = Comment.objects.filter(article=Article.objects.get(pk=pk)).order_by(
            "-created_at"
        )
        paginator = Paginator(comments, 5)
        page_number = self.request.GET.get("page", 1)
        comments_page = paginator.get_page(page_number)
        comments = comments_page
        if request.htmx:  # and from htmx
            Comment.objects.get(
                pk=request.headers.get("comment")
            ).delete()  # delete the comment
            return render(
                request, "article/cmts.html", context={"comments": comments}
            )  # render the comments

        return render(request, "article/cmts.html", context={"comments": comments})


class SettingsView(TemplateView):
    template_name = "settings/index.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ReadingListView(TemplateView):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    #
    template_name = "reading_list/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            articles = (
                self.request.user.readings.prefetch_related().first().articles.all()
            )
        except AttributeError:
            articles = None
        context["articles"] = articles
        return context


class SavedPostsView(TemplateView):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    #
    template_name = "saved_posts/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            articles = self.request.user.saved.prefetch_related().first().articles.all()
        except AttributeError:
            articles = None
        context["articles"] = articles
        return context
