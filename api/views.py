from sunlightapi.api.models import ApiUser, ApiUserForm

from locksmith.auth import ApiAuth

class ApiViews(ApiAuth):
    api_name = 'sunlightapi'
    signing_key = '***REMOVED***'
    api_hub_url = 'http://localhost:8000/locksmith'
    key_model = ApiUser
    key_model_form = ApiUserForm
