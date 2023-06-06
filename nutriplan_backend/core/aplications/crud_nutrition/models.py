from django.db import models
from ..authentication.models import User


class Post_recipe(models.Model):
    # the author will be to use with a login user
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    ingredients = models.TextField(null=False, default='')
    description = models.TextField()
    image = models.ImageField(upload_to="files", null=True)
    likes = models.ManyToManyField(User, related_name='liked_posts')
    favorites = models.ManyToManyField(User, related_name='favorite_post')
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
