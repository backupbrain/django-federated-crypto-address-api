from rest_framework_api_key.permissions import BaseHasAPIKey
from .models import (
    AuthorizedApiKey
)


class HasAuthorizedApiKey(BaseHasAPIKey):
    """Permissions class that requires an AuthorizedApiKey."""

    model = AuthorizedApiKey
