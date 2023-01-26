from django.db import models

class Relation(models.Model):
	alias = models.CharField('Alias', max_length=128, unique=True, default='')
	webhook_url = models.CharField('WebHook Url', max_length=512, default='')

	def __str__(self):
		return f'{self.alias} - {self.webhook_url}'

class ClickRecord(models.Model):
	alias = models.CharField('Alias', max_length=128, default='')
	url_for_redirect = models.CharField('Url For Redirect', max_length=512, default='')
	email = models.CharField('Email', max_length=128, default='')
	status_code = models.IntegerField('Status Code', default=200)
	email_number = models.IntegerField('Email Number in Siquence', default=1)
	email_type = models.CharField('Email tyepe in Siquence', default='A', max_length=3, help_text='A/B Test')

	def __str__(self):
		return f'{self.alias} - {self.email} - {self.email_number}/{self.email_type}'
