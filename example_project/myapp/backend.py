# import the User object
from django.contrib.auth.models import User
import myapp.ldap_auth

# Name my backend 'MyCustomBackend'
class MyCustomBackend:

    # Create an authentication method
    # This is called by the standard Django login procedure
    def authenticate(self, username=None, password=None):
        if not myapp.ldap_auth.authenticate(username, password):
            return None
        try:
            # Try to find a user matching your username
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            admin = username == 'dtenenba' # TODO don't hardcode
            user = User.objects.create_user(username,
                                            "{}@fredhutch.org".format(username),
                                            'passworddoesntmatter',
                                            is_superuser=admin,
                                            is_staff=admin)
        return user

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
