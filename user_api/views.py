from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user_api.models import UserModel
from user_api.serializers import UserSerializer, UserCreateSerializer


class UserView(APIView):
    """
    View for all users
    """
    def __str__(self):
        return 'API View for all users'

    def get(self, request, format=None):
        """
        GET - All users list
        :param request: http request
        :param format: html? json?
        :return: json object containing all user information
        """
        all_users = UserModel.objects.all()
        all_users_serializer = UserSerializer(all_users, many=True)
        return Response(all_users_serializer.data)

    def post(self, request):
        """
        POST - Create single user
        :param request: http request
        :return: json object containing created user info
        """
        new_user_serializer = UserCreateSerializer(data=request.data)
        if new_user_serializer.is_valid():
            new_user_serializer.save()
            return Response(new_user_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(new_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """
    View for single user
    """
    def __str__(self):
        return 'API View for single user'

    def _get_object(self, pk):
        try:
            return UserModel.objects.get(pk=pk)
        except UserModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        GET - Single user detail
        :param request: http request
        :param format: html? json?
        :param pk: primary key of object
        :return: json object containing single user detail
        """
        user_model = self._get_object(pk=pk)
        user_serializer = UserSerializer(user_model)
        return Response(user_serializer.data)
