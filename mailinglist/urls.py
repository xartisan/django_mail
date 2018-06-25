from django.urls import path

from mailinglist.views import MailingListListView, CreateMailingListView, DeleteMailingListView, MailingListDetailView, \
    SubscribeToMailingListView, ThankYouForSubscribingView, ConfirmSubscriptionView, UnsubscribeView, CreateMessageView, \
    MessageDetailView

app_name = 'mailinglist'

urlpatterns = [
    path('', MailingListListView.as_view(), name='mailinglist_list'),
    path('new', CreateMailingListView.as_view(), name='create_mailinglist'),
    path(
        '<uuid:pk>/delete',
        DeleteMailingListView.as_view(),
        name='delete_mailinglist'),
    path(
        '<uuid:pk>/manage',
        MailingListDetailView.as_view(),
        name='manage_mailinglist'),
    path(
        '<uuid:mailinglist_pk>/subscribe',
        SubscribeToMailingListView.as_view(),
        name='subscribe'),
    path(
        '<uuid:pk>/thankyou',
        ThankYouForSubscribingView.as_view(),
        name='subscriber_thankyou'),
    path(
        'subscribe/confirmation/<uuid:pk>',
        ConfirmSubscriptionView.as_view(),
        name='confirm_subscription',
    ),
    path(
        'unsubscribe/<uuid:pk>',
        UnsubscribeView.as_view(),
        name='unsubscribe',
    ),
    path('<uuid:mailinglist_pk>/message/new',
         CreateMessageView.as_view(), name='create_message'),
    path('message/<uuid:pk>', MessageDetailView.as_view(), name='view_message'),

]
