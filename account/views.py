from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from account.authentication import ExpiringTokenAuthentication
from account.models import ExpiringToken

from .serializer import LoginSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def LoginView(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    django_login(request, user)
    token, _ = ExpiringToken.objects.get_or_create(user=user)
    if token.expired():
        # If the token is expired, generate a new one.
        token.delete()
        token = ExpiringToken.objects.create(
            user=user
        )
    return Response({'token': token.key}, status=200)


@api_view(['POST'])
@authentication_classes([ExpiringTokenAuthentication, ])
@permission_classes([IsAuthenticated])
def LogoutView(request):
    content = {
        'user': request.user,
        'auth': request.auth,
    }
    print(content)
    try:
        request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
        pass
    django_logout(request)
    return Response('Successfully logged out.', status=204)
