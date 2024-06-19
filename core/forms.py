from django.forms import ModelForm
from .models import Contact


# contact form controll
class ContactForm(ModelForm):

    class Meta:
        model = Contact
        fields = ["email", "name", "subject", "message"]

        # specifying error messages for each field for each error
        error_messages = {
            "name": {
                "required": "you have to provide your name",
                "max_length": "please user a shorter name < 64",
            },
            "subject": {
                "required": "you have to provide the corresponding subject",
                "max_length": "please user a shorter subject name < 64",
            },
            "email": {
                "required": "you have to provide your email",
                "max_length": "please user a shorter email < 64",
            },
            "message": {
                "required": "you have to provide the corresponding message",
                "max_length": "please user a shorter message < 640",
            },
        }

    # adding placeholder text correspondingly
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            custom_attrs = {
                "placeholder": field  # each field will have a placeholder text based on the field name
            }
            self.fields[field].widget.attrs.update(custom_attrs)
