from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user_api.models import UserModel
from user_api.serializers import UserSerializer, UserCreateSerializer, LoginSerializer, LoginResultSerializer


class UserView(APIView):
    """
    View for all users
    """

    def get(self, request):
        """
        GET - All users list
        :param request: http request
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
            new_user_serializer.create(validated_data=request.data)
            return Response(new_user_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(new_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """
    View for single user
    """

    def _get_object(self, user_id):
        try:
            return UserModel.objects.get(user_id=user_id)
        except UserModel.DoesNotExist:
            raise Http404

    def get(self, request, user_id):
        """
        GET - Single user detail
        :param request: http request
        :param user_id: user id of object
        :return: json object containing single user detail
        """
        user_model = self._get_object(user_id=user_id)
        user_serializer = UserSerializer(user_model)
        return Response(user_serializer.data)


class LoginView(APIView):
    """
    View for login result
    """

    def post(self, request):
        """
        POST - Login method
        :param request: http request
        :return: user's uuid if successful, http 400 if error
        """

        request_serializer = LoginSerializer(data=request.data)
        if request_serializer.is_valid() is False:
            return Response(request_serializer.errors, status.HTTP_400_BAD_REQUEST)

        matching_models = UserModel.objects.filter(
            name=request.data['name']).filter(password=request.data['password'])
        if len(matching_models) == 0:
            return Response({'error': 'ID or password is incorrect'}, status.HTTP_400_BAD_REQUEST)

        for model in matching_models:
            compare_serializer = LoginSerializer(model)
            if request_serializer.data == compare_serializer.data:
                return Response(LoginResultSerializer(model).data, status.HTTP_200_OK)

        return Response({'error': 'ID or password is incorrect'}, status.HTTP_400_BAD_REQUEST)
