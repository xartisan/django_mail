import uuid

from django.contrib.auth import get_user_model
from django.db import models
# Create your models here.
from django.urls import reverse

from mailinglist import tasks

User = get_user_model()


class MailingList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('mailinglist:manage_mailinglist', kwargs={'pk': self.id})

    def user_can_use_mailing_list(self, user):
        return user == self.owner


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mailing_list = models.ForeignKey(to=MailingList, on_delete=models.CASCADE)
    subject = models.CharField(max_length=150)
    body = models.TextField()
    started = models.DateTimeField(default=None, null=True)
    finished = models.DateTimeField(default=None, null=True)

    def save(self,
             force_insert=False,
             force_update=False,
             using=None,
             update_fields=None):
        is_new = self._state.adding or force_insert
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields)
        if is_new:
            # self.send_confirmation_email()
            tasks.build_subscriber_message_for_message.delay(self.id)
            print('hj')


class SubscriberManager(models.Manager):

    def confirmed_subscribers_for_mailing_list(self, mailing_list):
        qs = self.get_queryset()
        qs = qs.filter(confirmed=True)
        qs = qs.filter(mailing_list=mailing_list)
        return qs


class Subscriber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    confirmed = models.BooleanField(default=False)
    mailing_list = models.ForeignKey(to=MailingList, on_delete=models.CASCADE)
    objects = SubscriberManager()

    class Meta:
        unique_together = ['email', 'mailing_list']

    def send_confirmation_email(self):
        tasks.send_confirmation_email_to_subscriber.delay(self.id)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        is_new = self._state.adding or force_insert
        super().save(force_insert=force_insert, force_update=force_update,
                     using=using, update_fields=update_fields)
        if is_new and not self.confirmed:
            self.send_confirmation_email()


class SubscriberMessageManager(models.Manager):

    def create_from_message(self, message):
        confirmed_subs = Subscriber.objects.confirmed_subscribers_for_mailing_list(
            message.mailing_list)
        return [
            self.create(message=message, subscriber=sub)
            for sub in confirmed_subs
        ]


class SubscriberMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(to=Message, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(to=Subscriber, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    sent = models.DateTimeField(default=None, null=True)
    last_attempt = models.DateTimeField(default=None, null=True)

    objects = SubscriberMessageManager()

    def save(self,
             force_insert=False,
             force_update=False,
             using=None,
             update_fields=None):
        print('fdasfsadfsadf**********', self.id)
        is_new = self._state.adding or force_insert
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields)
        if is_new:
            self.send()

    def send(self):
        tasks.send_subscriber_message.delay(self.id)
