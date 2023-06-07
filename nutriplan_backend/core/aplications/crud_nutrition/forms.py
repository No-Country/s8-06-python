from django import forms
from .models import Post_recipe

#
class PublicationRecipeForm(forms.ModelForm):
    class Meta:
        model = Post_recipe
        fields = ['title', 'ingredients', 'description', 'image']

    imagen = forms.ImageField(label="Avatar", required=False, widget=forms.FileInput(attrs={'class':'form-control'}))
