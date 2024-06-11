# Generated by Django 4.0 on 2024-06-11 01:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cart', '0001_initial'),
        ('ads', '0004_alter_announcement_condition_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Itemcart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_item', to='ads.announcement')),
            ],
            options={
                'ordering': ('cart',),
            },
        ),
    ]
