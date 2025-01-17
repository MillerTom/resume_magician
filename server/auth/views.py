from rest_framework.response import Response
from rest_framework import generics, status as http_status
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
import requests
from auth.utils import is_authenticated
import jwt
from job.models import UserInfo

class GetTokenView(generics.GenericAPIView):
    @swagger_auto_schema(auto_schema=None)
    def post(self, request):
        data = request.data
        code = data['code']

        token_data = {
            'client_id': settings.AZURE_AD_OAUTH2_KEY,
            'client_secret': settings.AZURE_AD_OAUTH2_SECRET,
            'code': code,
            'redirect_uri': settings.LOGIN_REDIRECT_URL,
            'grant_type': 'authorization_code',
        }
        token_response = requests.post(settings.AZURE_AD_TOKEN_URL, data=token_data)
        if token_response.status_code != 200:
            return Response({'error': 'Failed to fetch tokens'}, status=400)

        tokens = token_response.json()
        access_token = tokens.get('access_token')
        id_token = tokens.get('id_token')

        decoded = jwt.decode(access_token, options={'verify_signature': False})
        name = decoded['name']

        return Response({'access_token': access_token, 'id_token': id_token, 'name': name}, status=http_status.HTTP_200_OK)


class GetUserView(generics.GenericAPIView):

    @swagger_auto_schema(auto_schema=None)
    @is_authenticated
    def get(self, request):
        auth_header = self.request.headers.get("Authorization", None)
        token = auth_header.split(" ")[1]
        decoded = jwt.decode(token, options={'verify_signature': False})
        email = decoded['unique_name']
        name = decoded['name']
        userinfo = UserInfo.objects.filter(email=email).first()
        if not userinfo:
            userinfo = UserInfo(
                email=email,
                name=name,
            )
            userinfo.save()
        name = decoded['name']
        return Response({'name': name, 'email': email}, status=http_status.HTTP_200_OK)
