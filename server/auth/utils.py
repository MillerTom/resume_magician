import jwt, time
from functools import wraps
from django.http import JsonResponse
from django.conf import settings


def validate_access_token(token, tenant_id, client_id):
    # Decode and validate the token
    allowed_issuers = [
        f"https://sts.windows.net/{tenant_id}/",
        f"https://login.microsoftonline.com/{tenant_id}/v2.0"
    ]
    
    decoded = jwt.decode(token, options={'verify_signature': False})
    if decoded['iss'] in allowed_issuers:
        if int(time.time()) < decoded['exp']:
            return True
    raise Exception('Invalid token')


def is_authenticated(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        # Get the access token from the Authorization header
        auth_header = self.request.headers.get("Authorization", None)
        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse({"error": "Authorization header missing or invalid."}, status=401)
        
        token = auth_header.split(" ")[1]  # Extract the token part
        
        try:
            # Validate the token
            tenant_id = settings.AZURE_AD_OAUTH2_TENANT_ID
            client_id = settings.AZURE_AD_OAUTH2_KEY
            claims = validate_access_token(token, tenant_id, client_id)

            # # Attach claims to the request for further processing (optional)
            # request.user_claims = claims

        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=401)
        
        # Token is valid, proceed with the view
        return view_func(self, request, *args, **kwargs)
    
    return wrapper