from .models import Users, DownLink
from django.forms import ModelForm, TextInput, Textarea


class CommentForm(ModelForm):
    class Meta:
        model = Users
        fields = ["comment"]
        widgets = {
            'comment': Textarea(attrs={'placeholder': 'Введите комментарий', 'class': 'form-control-lg'})
        }


class LinkForm(ModelForm):
    class Meta:
        model = DownLink
        fields = ['old_link']
        widgets = {
            'old_link': TextInput(attrs={'type': "text", 'id': "link"})
        }

