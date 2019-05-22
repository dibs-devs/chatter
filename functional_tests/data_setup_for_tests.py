from tenants.models import Client, Domain
from django.contrib.auth import get_user_model

def set_up_data():
    # create your public tenant
    tenant = Client(schema_name='public',
                  name='Schemas Inc.')
    tenant.save()

    # Add one or more domains for the tenant
    domain = Domain()
    domain.domain = 'localhost' # don't add your port or www here! on a local server you'll want to use localhost here
    domain.tenant = tenant
    domain.is_primary = True
    domain.save()

    user = get_user_model().objects.create(username="user0")
    user.set_password("dummypassword")
    user.save()
