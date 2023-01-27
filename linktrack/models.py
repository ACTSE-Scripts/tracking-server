from django.db import models

class Relation(models.Model):
	alias = models.CharField('Alias', max_length=128, unique=True, default='')
	webhook_url = models.CharField('Webhook Url', max_length=512, default='')
	track_all_clicks = models.BooleanField('Track all clicks', default=False)
	unique_click_by_link = models.BooleanField('Unique click by link', default=False)

	def __str__(self):
		return f'{self.alias} - {self.webhook_url}'

class ClickRecord(models.Model):
	alias = models.CharField('Alias', max_length=128, default='')
	url_for_redirect = models.CharField('Url for Redirect', max_length=512, default='')
	email = models.CharField('Email', max_length=128, default='')
	status_code = models.IntegerField('Status Code', default=200)
	email_number = models.IntegerField('Email Number in Sequence', default=1)
	email_type = models.CharField('Email type in Sequence', default='A', max_length=3, help_text='A/B Test')

	def __str__(self):
		return f'{self.alias} - {self.email} - {self.email_number}/{self.email_type} - {self.status_code}'
