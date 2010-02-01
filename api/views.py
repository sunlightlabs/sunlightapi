from sunlightapi.api.models import ApiKey, ApiKeyForm

from locksmith.auth import AuthViews

class ApiViews(AuthViews):
    api_name = 'sunlightapi'
    signing_key = '***REMOVED***'
    api_hub_url = 'http://localhost:8000/locksmith'

    key_model = ApiKey
    key_model_form = ApiKeyForm

    require_confirmation = True
    registration_email_subject = 'Sunlight Labs API Registration'

site = ApiViews()
