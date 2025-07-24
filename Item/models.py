from django.db import models

# Create your models here.

class Item(models.Model):

    Name = models.CharField(max_length=255)
    Category = models.ForeignKey('Category.Category', on_delete=models.CASCADE)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Image = models.ImageField(upload_to='images/', blank=True, null=True)
    Available = models.BooleanField(default=True)
    Description = models.TextField(blank=True)


    def __str__(self):
        return f"{self.Name, self.Category, self.Price, self.Available, self.Description}"

    class Meta:
        verbose_name_plural = "Items"