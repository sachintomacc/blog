# Generated by Django 2.1.5 on 2020-05-09 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20200509_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postview',
            name='post',
        ),
        migrations.RemoveField(
            model_name='postview',
            name='user',
        ),
        migrations.DeleteModel(
            name='PostView',
        ),
    ]