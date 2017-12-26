from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from user_api.models import UserModel
from user_api.serializers import UserSerializer, UserCreateSerializer, LoginResultSerializer
from user_api.views import UserView, UserDetailView, LoginView


class UserCreateSerializerTest(TestCase):
    """
    Test for user create serializer(with everything)
    """

    def setUp(self):
        self.data = {
            'name': 'Test',
            'email': 'test@test.com',
            'password': 'Test1234',
            'phone_number': '010-1234-5678',
            'age': 20,
            'gender': 'M'
        }

    def test_invalid_password_length(self):
        self.data['password'] = 'Asdf123'
        test_serializer = UserCreateSerializer(data=self.data)
        self.assertFalse(test_serializer.is_valid())

    def test_invalid_password_no_number(self):
        self.data['password'] = 'Asdfasdf'
        test_serializer = UserCreateSerializer(data=self.data)
        self.assertFalse(test_serializer.is_valid())

    def test_invalid_password_no_uppercase(self):
        self.data['password'] = 'asdf1234'
        test_serializer = UserCreateSerializer(data=self.data)
        self.assertFalse(test_serializer.is_valid())

    def test_not_a_phone_number(self):
        self.data['phone_number'] = '12345678'
        test_serializer = UserCreateSerializer(data=self.data)
        self.assertFalse(test_serializer.is_valid())

    def test_invalid_phone_number_invalid_prefix(self):
        self.data['phone_number'] = '011-1234-5678'
        test_serializer = UserCreateSerializer(data=self.data)
        self.assertFalse(test_serializer.is_valid())

    def test_invalid_phone_number_invalid_length(self):
        self.data['phone_number'] = '011-234-5678'
        test_serializer = UserCreateSerializer(data=self.data)
        self.assertFalse(test_serializer.is_valid())

    def test_invalid_gender(self):
        self.data['gender'] = 'X'
        test_serializer = UserCreateSerializer(data=self.data)
        self.assertFalse(test_serializer.is_valid())

    def test_valid_create(self):
        test_serializer = UserCreateSerializer(data=self.data)
        self.assertTrue(test_serializer.is_valid())
        self.assertEqual(test_serializer.data, self.data)


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
    def setUp(self):
        self.factory = APIRequestFactory()
        self.data = {
            'name': 'Test',
            'email': 'test@test.com',
            'password': 'Test1234',
            'phone_number': '010-1234-5678',
            'age': 20,
            'gender': 'M'
        }
        self.view = UserView.as_view()

    def test_post_without_auth(self):
        """
        Test case 1: no credentials provided
        Expected result: HTTP 401
        """
        request = self.factory.post('/users/', data=self.data)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_with_invalid_auth(self):
        """
        Test case 2: Invalid credentials provided
        Expected result: HTTP 401
        """
        request = self.factory.post('/users/', data=self.data)
        request.user = AnonymousUser()
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_with_insufficient_args(self):
        """
        Test case 3: Arguments not totally filled
        Expected result: HTTP 400
        """
        invalid_data = {}
        request = self.factory.post('/users/', data=invalid_data)
        force_authenticate(request, user=User)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_with_invalid_args(self):
        """
        Test case 4: Arguments are invalid
        Expected result: HTTP 400
        """
        self.data['password'] = 'abc123'
        self.data['phone_number'] = '011-2345-6789'
        request = self.factory.post('/users/', data=self.data)
        force_authenticate(request, user=User)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_wth_valid_args(self):
        """
        Test case 5: Everything is valid
        Expected result: HTTP 201
        """
        request = self.factory.post('/users/', data=self.data)
        force_authenticate(request, user=User)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginViewTest(TestCase):
    """
    Test for LoginView - post
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = LoginView.as_view()

        # saving sample models
        self.sample_model = UserModel(name='test', email='test@test.com',
                                      password='Testpwd!999', phone_number='010-1234-5678',
                                      age=20, gender='M')
        self.sample_model.save()

    def test_without_auth(self):
        """
        Test case 1: No credentials provided
        Expected result: HTTP 401
        """
        request = self.factory.post(
            '/sessions/', {'name': 'test', 'password': 'Testpwd!999'})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_with_invalid_auth(self):
        """
        Test case 2: Invalid credentials provided
        Expected result: HTTP 401
        """
        request = self.factory.post(
            '/sessions/', {'name': 'test', 'password': 'Testpwd!999'})
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
            '/sessions/', {'name': 'foo', 'password': 'Testpwd!999'})
        force_authenticate(request, user=User)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_with_incorrect_pw(self):
        """
        Test case 4: Password is incorrect
        Expected result: HTTP 400
        """
        request = self.factory.post(
            '/sessions/', {'name': 'test', 'password': 'bar'})
        force_authenticate(request, user=User)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_with_valid_data(self):
        """
        Test case 5: Everything is valid
        Expected result: HTTP 200
        """
        request = self.factory.post(
            '/sessions/', {'name': 'test', 'password': 'Testpwd!999'})
        force_authenticate(request, user=User)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
