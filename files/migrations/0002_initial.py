# Generated by Django 4.2.5 on 2023-11-06 08:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('spaces', '0001_initial'),
        ('files', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='createdBy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='file',
            name='space',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spaces.space'),
        ),
        migrations.AddField(
            model_name='file',
            name='users',
            field=models.ManyToManyField(related_name='allowed_user_for_file', to=settings.AUTH_USER_MODEL),
        ),
    ]
