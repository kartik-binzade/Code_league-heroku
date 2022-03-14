from django import forms
from .models import Group, Comment, Classes, TimeChoice, Questions, Topic, Edits



class CreateGroupForm(forms.ModelForm):
    name = forms.CharField(max_length=240, widget=forms.Textarea(attrs={'cols': 48, 'rows': 3}))
    description = forms.CharField(max_length=5000, widget=forms.Textarea(attrs={'cols': 48, 'rows': 8}))

    class Meta:
        model = Group
        fields = ("name", "description")


class PostComment(forms.ModelForm):
    text = forms.CharField(max_length=240, widget=forms.Textarea(attrs={'cols': 100, 'rows': 10}))

    class Meta:
        model = Comment
        fields = ('text',)


class CreateClassForm(forms.ModelForm):
    name = forms.CharField(max_length=240, widget=forms.Textarea(attrs={'cols': 48, 'rows': 3}))
    description = forms.CharField(max_length=5000, widget=forms.Textarea(attrs={'cols': 48, 'rows': 10}))

    class Meta:
        model = Classes
        fields = ('name', 'description')


class CreateTimeChoice(forms.ModelForm):
    start = forms.DateTimeField()
    duration = forms.IntegerField()

    class Meta:
        model = TimeChoice
        fields = ('start', 'duration')


class CreateQuestion(forms.ModelForm):
    question = forms.CharField(max_length=240, widget=forms.Textarea(attrs={'cols': 48, 'rows': 3}))
    description = forms.CharField(max_length=5000, widget=forms.Textarea(attrs={'cols': 48, 'rows': 10}))

    class Meta:
        model = Questions
        fields = ('question', 'description')

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}
 # entry
class EditsForm(forms.ModelForm):
    class Meta:
        model = Edits
        fields = ['text']
        labels = {'text': 'Edits'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}