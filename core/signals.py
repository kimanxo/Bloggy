from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .models import Profile, Newsletter
from django.db.models.signals import post_save


@receiver(user_signed_up)
def create_user_profile(sender, user, **kwargs):
    sociallogin = kwargs.get("sociallogin")
    if sociallogin:
        picture_url = None
        if sociallogin.account.provider == "google":
            picture_url = sociallogin.account.extra_data.get("picture")
        elif sociallogin.account.provider == "github":
            picture_url = sociallogin.account.extra_data.get("avatar_url")
        Profile.objects.create(user=user, picture=picture_url)



@receiver(post_save, sender=Newsletter)
def sendLetter(sender, instance, created, *args, **kwargs):
    print(instance.message)
    # TODO: send a notification  to the user