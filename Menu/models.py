from django.db import models

# Create your models here.
class Menu(models.Model):

    Title = models.CharField(max_length=255)
    Slug = models.SlugField(max_length=255,auto_created=True,unique=True,null=True)
    MenuItems = models.ManyToManyField('Item.Item')
    Table = models.IntegerField(null=True, blank=True)

    def __str__(self):

        return self.Title
