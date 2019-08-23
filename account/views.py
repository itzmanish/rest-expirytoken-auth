from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication
from account.models import ExpiringToken
from account.authentication import ExpiringTokenAuthentication
from .serializer import LoginSerializer


@api_view(['post'])
@permission_classes([AllowAny])
def LoginView(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    django_login(request, user)
    token, created = ExpiringToken.objects.get_or_create(user=user)
    if token.expired():
        # If the token is expired, generate a new one.
        token.delete()
        token = ExpiringToken.objects.create(
            user=user
        )
    return Response({'token': token.key}, status=200)


@api_view(['post'])
@authentication_classes([ExpiringTokenAuthentication, SessionAuthentication])
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
