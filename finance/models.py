# finance/models.py

from django.db import models

class BaseModel(models.Model):
    objects = models.Manager()
    class Meta:
        abstract = True



class Source(BaseModel):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name



class Category(BaseModel):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name



class Transactions(BaseModel):

    source = models.ForeignKey(Source, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateField(auto_now=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.description}, {self.date}: {self.amount}"