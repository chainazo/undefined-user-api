from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from user_api.models import UserModel
from user_api.serializers import UserSerializer, UserCreateSerializer, LoginResultSerializer
from user_api.views import UserView, UserDetailView, LoginView


# Test for serializers
class UserSerializerTest(TestCase):
    """
    Test for user serializer(without uuid, password, phone number)
    """

    def setUp(self):
        self.test_model = UserModel(name='UserSerializer Test', email='ustest@test.com',
                                    password='testpwd111', phone_number='010-1234-5678',
                                    age=20, gender='W')
        self.test_model.save()
        self.test_serializer = UserSerializer(self.test_model).data

    def test_uuid_is_not_included(self):
        flag = False
        try:
            self.test_serializer['user_id']
        except KeyError:
            flag = True
        self.assertTrue(flag)

    def test_password_is_not_included(self):
        flag = False
        try:
            self.test_serializer['password']
        except KeyError:
            flag = True
        self.assertTrue(flag)

    def test_phone_number_is_not_included(self):
        flag = False
        try:
            self.test_serializer['phone_number']
        except KeyError:
            flag = True
        self.assertTrue(flag)

    def test_everything_else_is_added_correctly(self):
        self.assertEqual(self.test_model.name, self.test_serializer['name'])
        self.assertEqual(self.test_model.email, self.test_serializer['email'])
        self.assertEqual(self.test_model.age, self.test_serializer['age'])
        self.assertEqual(self.test_model.gender,
                         self.test_serializer['gender'])


class UserCreateSerializerTest(TestCase):
    """
    Test for user create serializer(with everything)
    """
    # TODO test with invalid data

    def setUp(self):
        self.test_model = UserModel(name='UserCreateSerializer Test', email='ucstest@test.com',
                                    password='testpwd222', phone_number='010-9012-3456',
                                    age=21, gender='M')
        self.test_model.save()
        self.test_serializer = UserCreateSerializer(self.test_model).data

    def test_is_serializer_generated_correctly(self):
        self.assertEqual(str(self.test_model.user_id),
                         self.test_serializer['user_id'])
        self.assertEqual(self.test_model.name, self.test_serializer['name'])
        self.assertEqual(self.test_model.email, self.test_serializer['email'])
        self.assertEqual(self.test_model.password,
                         self.test_serializer['password'])
        self.assertEqual(self.test_model.phone_number,
                         self.test_serializer['phone_number'])
        self.assertEqual(self.test_model.age, self.test_serializer['age'])
        self.assertEqual(self.test_model.gender,
                         self.test_serializer['gender'])


class LoginResultSerializerTest(TestCase):
    """
    Test for login result serializer(with uuid only)
    """

    def setUp(self):
        self.test_model = UserModel(name='LoginResultSerializer Test', email='lrstest@test.com',
                                    password='testpwd333', phone_number='010-7890-1234',
                                    age=22, gender='W')
        self.test_serializer = LoginResultSerializer(self.test_model).data

    def test_is_serializer_generated_correctly(self):
        self.assertEqual(str(self.test_model.user_id),
                         self.test_serializer['user_id'])


# Test for views
class UserViewGetTest(TestCase):
    """
    Test for UserView - get
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.request = self.factory.get('/users/')
        self.view = UserView.as_view()

    def test_get_without_auth(self):
        """
        Test case 1: no credentials provided
        Expected result: HTTP 401
        """
        response = self.view(self.request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_with_invalid_auth(self):
        """
        Test case 2: Invalid credentials provided
        Expected result: HTTP 401
        """
        self.request.user = AnonymousUser()
        response = self.view(self.request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_with_valid_auth(self):
        """
        Test case 3: Valid credentials provided
        Expected result: HTTP 200
        """
        force_authenticate(self.request, user=User)
        response = self.view(self.request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserViewPostTest(TestCase):
    """
    Test for UserView -post
    """
    pass


class UserDetailViewTest(TestCase):
    """
    Test for UserDetailView - get
    """
    pass


class LoginViewTest(TestCase):
    """
    Test for LoginView - post
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = LoginView.as_view()

        # saving sample models
        self.sample_model = UserModel(name='test', email='test@test.com',
                                      password='testpwd', phone_number='010-1234-5678',
                                      age=20, gender='M')
        self.sample_model.save()

    def test_without_auth(self):
        """
        Test case 1: No credentials provided
        Expected result: HTTP 401
        """
        request = self.factory.post(
            '/sessions/', {'name': 'test', 'password': 'testpwd'}, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_with_invalid_auth(self):
        """
        Test case 2: Invalid credentials provided
        Expected result: HTTP 401
        """
        request = self.factory.post(
            '/sessions/', {'name': 'test', 'password': 'testpwd'}, format='json')
        request.user = AnonymousUser()
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # From now on auth is always valid

    def test_with_incorrect_id(self):
        """
        Test case 3: ID is incorrect
        Expected result: HTTP 400
        """
        request = self.factory.post(
            '/sessions/', {'name': 'foo', 'password': 'testpwd'}, format='json')
        force_authenticate(request, user=User)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_with_incorrect_pw(self):
        """
        Test case 4: Password is incorrect
        Expected result: HTTP 400
        """
        request = self.factory.post(
            '/sessions/', {'name': 'test', 'password': 'bar'}, format='json')
        force_authenticate(request, user=User)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_with_valid_data(self):
        """
        Test case 5: Everything is valid
        Expected result: HTTP 200
        """
        request = self.factory.post(
            '/sessions/', {'name': 'test', 'password': 'testpwd'}, format='json')
        force_authenticate(request, user=User)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
