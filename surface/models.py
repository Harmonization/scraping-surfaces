from django.db import models

# Create your models here.
class ModelSurface(models.Model):
    name = models.CharField(max_length=100)
    latex_expr = models.CharField(max_length=400, default='')
    latex_img = models.CharField(max_length=400, default='')
    img = models.CharField(max_length=400, default='')
    text = models.TextField(default='')
    link = models.CharField(max_length=400, default='')

    # parameters = models.ExpressionList()

    def __str__(self):
        return f'{self.id} {self.name}'