from django.db import models

# Create your models here.

class Message(models.Model):
    name = models.CharField(verbose_name=u'User name', max_length=255, blank=False, null=False)
    text = models.TextField(verbose_name=u'Message text', blank=False, null=False)
    created_at = models.DateTimeField(verbose_name=u'Created at', auto_now_add=True)

    def __unicode__(self):
        return u'At {}:{} {} said: {}'.format(self.created_at.hour, self.created_at.minute, self.name, self.text)

class Consultant(models.Model):
    name = models.CharField(verbose_name=u'User name', max_length=255, blank=False, null=False, unique=True)
    password = models.CharField(verbose_name=u'User pass', max_length=255, blank=False, null=False)
    google_id = models.TextField(verbose_name=u'GoogleID', blank=False, null=False)
    is_available = models.BooleanField(verbose_name=u"Is available?", default=False)