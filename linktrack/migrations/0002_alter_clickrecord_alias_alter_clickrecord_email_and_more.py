# Generated by Django 4.1.4 on 2023-01-27 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linktrack', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clickrecord',
            name='alias',
            field=models.CharField(db_index=True, default='', max_length=128, verbose_name='Alias'),
        ),
        migrations.AlterField(
            model_name='clickrecord',
            name='email',
            field=models.CharField(db_index=True, default='', max_length=128, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='clickrecord',
            name='url_for_redirect',
            field=models.CharField(db_index=True, default='', max_length=512, verbose_name='Url for Redirect'),
        ),
    ]
