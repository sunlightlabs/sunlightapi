from sunlightapi.api.models import ApiUser, ApiUserForm

from locksmith.auth import ApiAuth

class ApiViews(ApiAuth):
    api_name = 'sunlightapi'
    signing_key = '***REMOVED***'
    api_hub_url = 'http://localhost:8000/locksmith'

    key_model = ApiUser

    require_confirmation = True
    registration_email_subject = 'Sunlight Labs API Registration'

site = ApiViews()
