from django import forms
from django.forms import ModelForm, ValidationError
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

    def clean_username(self):
        """Reject usernames that differ only in case."""
        username = self.cleaned_data.get("username")
        if (
            username
            and self._meta.model.objects.filter(username__iexact=username).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "username": self.instance.unique_error_message(
                            self._meta.model, ["username"]
                        )
                    }
                )
            )
        if len(username) < 6 or len(username) > 12:
            self._update_errors(
                ValidationError(
                    {
                        "username": "Username must be between 6 and 12 characters"
                    }
                )
            )
    
        return username


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ['host', 'participants']

class Userform(ModelForm):

    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']
        