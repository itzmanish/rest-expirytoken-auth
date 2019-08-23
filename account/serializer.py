from django.contrib.auth import authenticate
from rest_framework import serializers, exceptions


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    msg = 'User is disabled.'
                    raise exceptions.ValidationError(msg)
            else:
                msg = 'Authentication failed'
                raise exceptions.ValidationError(msg)
        else:
            msg = 'Must provide username and username both'
            raise exceptions.ValidationError(msg)
        return data


class SignupSerializer(serializers.Serializer):
    pass
