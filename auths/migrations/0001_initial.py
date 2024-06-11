# Generated by Django 4.0 on 2024-06-02 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cep', models.CharField(default='00000-000', max_length=9)),
                ('public_place', models.CharField(max_length=255)),
                ('public_place_type', models.CharField(default='default_type', max_length=100)),
                ('neighborhood', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(default='BA', max_length=2)),
            ],
        ),
    ]