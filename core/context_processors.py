from django.contrib.auth.models import User


def profile_context_processor(request):
    """
    This context processor adds the user's profile object to the context.

    Args:
        request: The current request object.

    Returns:
        A dictionary containing the user's profile object.
    """
    if request.user.is_authenticated:
        try:
            return {"profile": request.user.profile.first()}
        except User.profile.RelatedObjectDoesNotExist:
            return {}
    else:
        return {}
