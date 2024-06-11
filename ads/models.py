from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='book/%Y/%m/%d', blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales_user')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'name'),)

    def __str__(self):
        return self.name


class Announcement(models.Model):
    STATUS_CHOICES = (
        ('DISABLE', 'disable'),
        ('ACTIVATED', 'activated')
    )

    STATUS_CONDITION = (
        ('NOVO', 'Novo'),
        ('USADO', 'Usado'),
        ('DANIFICADO', 'Danificado'),
        ('SEMINOVO', 'Seminovo'),
        ('ANTIGO - RARO', 'Antigo - Raro'),
        ('ANTIGO - COLEÇÃO', 'Antigo - Coleção'),
        ('ENCADERNAÇÃO ESPECIAL', 'Encadernação Especial')
    )

    title = models.CharField(max_length=200, db_index=True)
    study_area = models.CharField(max_length=200, db_index=True)
    condition = models.CharField(max_length=30, choices=STATUS_CONDITION, default='')  # Alterado para acomodar a opção mais longa
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='announcements')  # Alterado related_name
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE, null=True, related_name='announcement_questions')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='disable')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'title'),)

    def __str__(self):
        return self.title