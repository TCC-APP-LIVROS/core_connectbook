# Generated by Django 4.0 on 2024-05-18 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=200)),
                ('study_area', models.CharField(db_index=True, max_length=200)),
                ('condition', models.CharField(choices=[('novo', 'Novo'), ('usado', 'Usado'), ('danificado', 'Danificado'), ('seminovo', 'Seminovo'), ('antigo - raro', 'Antigo - Raro'), ('antigo - coleção', 'Antigo - Coleção'), ('encadernação especial', 'Encadernação Especial')], default='', max_length=30)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('disable', 'Disabled'), ('activated', 'Activated')], default='disable', max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_client', models.TextField()),
                ('reply', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('announcement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='ads.announcement')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('description', models.TextField(blank=True)),
                ('author', models.CharField(db_index=True, max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='book/%Y/%m/%d')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_user', to='auth.user')),
            ],
            options={
                'ordering': ('name',),
                'index_together': {('id', 'name')},
            },
        ),
        migrations.AddField(
            model_name='announcement',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='announcements', to='ads.product'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='announcement_questions', to='ads.question'),
        ),
        migrations.AlterIndexTogether(
            name='announcement',
            index_together={('id', 'title')},
        ),
    ]
