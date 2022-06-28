# Third party imports
from django.contrib.auth.mixins import UserPassesTestMixin


class SuperuserRequiredMixin(UserPassesTestMixin):
    """
    Mixin for checking if user is superuser.
    """
    def test_func(self) -> bool:
        return self.request.user.is_superuser
