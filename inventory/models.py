# inventory\models.py
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    objects = models.Manager()
    class Meta:
        abstract = True


def upload_to(instance, filename):
    return 'UPC/{filename}'.format(filename=filename)


class UpcDetail(BaseModel):
    id = models.CharField(primary_key=True, max_length=200, unique=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    details = models.TextField(max_length=10000, null=True, blank=True, default=None)
    category = models.CharField(max_length=1000, null=True, blank=True)
    grams = models.FloatField(max_length=1000, null=True, blank=True, default=None)
    image = models.ImageField(_("Image"), upload_to="UPC/", default='UPC/default.png', null=True, blank=True)

    def __str__(self):
        return f"{self.id}: {self.description}"


class Scans(BaseModel):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    UPC = models.ForeignKey(UpcDetail, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    delta = models.IntegerField()


class Recipes(BaseModel):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='Title')
    servings = models.IntegerField(null=True, blank=True, default=None, verbose_name='Servings')
    preptimeminutes = models.IntegerField(null=True, blank=True, default=None, verbose_name='Prep Time (Minutes)')
    description = models.TextField(max_length=10000, null=True, blank=True, default=None, verbose_name='Instructions')

    def get_absolute_url(self):
        return reverse('inventory-recipesdetail', kwargs={'pk': self.id})

    def __str__(self):
        return self.title


class Ingredients(BaseModel):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE, related_name='recipe_ingredient')
    category = models.CharField(max_length=255, null=False, blank=False, verbose_name='Item')
    grams = models.FloatField(max_length=10000, null=True, blank=True, default=None, verbose_name='Grams')
