# Generated by Django 4.1.4 on 2023-01-26 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linktrack', '0004_clickrecord_email_number_clickrecord_email_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='relation',
            name='track_all_clicks',
            field=models.BooleanField(default=False, verbose_name='Track All Clicks'),
        ),
        migrations.AlterField(
            model_name='clickrecord',
            name='email_number',
            field=models.IntegerField(default=1, verbose_name='Email Number in Sequence'),
        ),
        migrations.AlterField(
            model_name='clickrecord',
            name='email_type',
            field=models.CharField(default='A', help_text='A/B Test', max_length=3, verbose_name='Email type in Sequence'),
        ),
        migrations.AlterField(
            model_name='clickrecord',
            name='url_for_redirect',
            field=models.CharField(default='', max_length=512, verbose_name='Url for Redirect'),
        ),
        migrations.AlterField(
            model_name='relation',
            name='webhook_url',
            field=models.CharField(default='', max_length=512, verbose_name='Webhook Url'),
        ),
    ]