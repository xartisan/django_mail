from django.core.exceptions import PermissionDenied, FieldDoesNotExist

from mailinglist.models import MailingList


class UserCanUseMailingListMixin:

    def get_object(self, queryset=None):
        user = self.request.user
        obj = super().get_object(queryset)
        if not isinstance(obj, MailingList):
            obj = getattr(obj, 'mailing_list', None)
        if isinstance(obj, MailingList):
            if obj.user_can_use_mailing_list(user):
                return obj
            raise PermissionDenied()
        raise FieldDoesNotExist('view does not know how to get mailing list.')
