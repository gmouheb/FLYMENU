from django.db import models

# Create your models here.
class Category(models.Model):

    Name = models.CharField(max_length=255)
    Description = models.TextField(blank=True)


    def __str__(self):
        return self.Name

    class Meta:
        verbose_name_plural = "Categories"