import string

from django.http import Http404

from api.models import RecreationalVenue

from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import PersonSerializer, WorkerSerializer, MemberSerializer, AdminSerializer, UserBatchSrl
from .serializers import UserFromAdminSerl, UserFromAdminBatchSerl
from .serializers import ResetPasswordRequestSerializer, ResetPasswordSerializer
from .models import Person, Worker, Member, Admin
from .models import PasswordReset
from .permissions import IsMember, IsAdmin, IsWorker
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from api.models import RecreationalVenue

from .requests import send_post_request_createBatch
from data.email_helpers import send_token_password

import pandas as pd
import random


class UserListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = PersonSerializer

    def get_queryset(self):
        return Person.objects.all()


'''Searches by id'''


class UserSearchView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = PersonSerializer

    def get_queryset(self):
        order = self.kwargs.get('pk', '')
        return Person.objects.all()


'''Searches multiple parameters'''


class UserSearchViewMultiple(generics.ListAPIView):
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = PersonSerializer

    def get_queryset(self):
        # Users set
        user_ids = set()

        name = self.request.query_params.get('name', None)
        email = self.request.query_params.get('email', None)
        id = self.request.query_params.get('id', None)
        role = self.request.query_params.get('role', None)

        admin_id = self.request.user.id
        admin = Admin.objects.get(id=admin_id)

        for recr_venue in admin.recreational_venue.all():
            # Add Ids
            user_ids.update(recr_venue.persons.values_list('id', flat=True))

        # Filtrar y devolver un queryset de usuarios únicos
        query_set = Person.objects.filter(id__in=user_ids).distinct()

        filters = {}
        if name:
            filters['first_name__icontains'] = name  # Case-insensitive match
        if email:
            filters['email'] = email
        if id:
            filters['id'] = id
        if role:
            filters['role'] = role

        return query_set.filter(**filters)


class UserGetView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PersonSerializer

    def get_object(self):
        # Retrieve the email parameter
        email = self.request.query_params.get('email', None)

        if email is None:
            raise ValidationError('Email is required')

        try:
            return Person.objects.get(email__iexact=email)
        except Person.DoesNotExist:
            raise ValidationError('Person with this email does not exist')


class UserDeleteView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = PersonSerializer

    def perform_destroy(self, instance):
        instance.delete()

    def get_queryset(self):
        return Person.objects.all()


class CreateUserView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = PersonSerializer

    def RandomString(self, n):
        chars = string.ascii_letters + string.digits
        return "".join(random.choice(chars) for _ in range(n))

    def perform_create(self, serializer):
        role = self.request.data.get('role')
        email = self.request.data.get('email')
        name = self.request.data.get('first_name')
        admin = self.request.user

        temp_username = "Tempuser-" + str(name) + "-" + str(email) + "-" + str(role)
        random_pass = self.RandomString(20)
        random_int = random.randint(0, 99999)

        temp_username = f"temp_user_{email.split('@')[0]}"
        #user = serializer.save(username=temp_username,role=role,email=email)
        Admin.create_person(self, username=temp_username, name=name, role=role, email=email)

        user = serializer.save(username=temp_username, password=random_pass, role=role, email=email,
                               person_id=random_int)
        user.recreational_venue.add(*admin.recreational_venue.all())
        return user


class CreateUserWorkerView(generics.CreateAPIView):
    serializer_class = WorkerSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        worker = serializer.save()
        return worker


class CreateUserMemberView(generics.CreateAPIView):
    serializer_class = MemberSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        member = serializer.save()
        return member


#-----------------------------------------------------------------------
#---------------- JAVIER - elr490 --------------------------------------
#-----------------------------------------------------------------------


class CreateUserAdminView(generics.CreateAPIView):
    serializer_class = AdminSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Person.objects.all()

    def perform_create(self, serializer):
        recreational_id = self.request.data.get('recreational_venue_id')
        if not recreational_id:
            raise ValidationError("Recreational venue ID must be provided.")
        try:
            recreational_venue = RecreationalVenue.objects.get(id=recreational_id)
            admin = serializer.save()
            admin.recreational_venue.add(recreational_venue)
        except RecreationalVenue.DoesNotExist:
            raise ValidationError("Recreational venue doesn't exist")
        return admin


class UserFromAdminView(generics.CreateAPIView):
    serializer_class = UserFromAdminSerl
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def perform_create(self, serializer):
        admin_id = self.request.user.id
        serializer.save(admin_id=admin_id)


class DelUserFromAdminView(generics.DestroyAPIView):
    queryset = Person.objects.all()
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = UserFromAdminSerl

    def delete(self, request, *args, **kwargs):
        try:
            # Get the instance or raise a 404
            instance = self.get_object()

            # Check if the instance and the current user have associated recreational venues
            if not instance.recreational_venue.exists() or not request.user.recreational_venue.exists():
                return Response({"error": "User or instance is not associated with any recreational venue"},
                                status=status.HTTP_400_BAD_REQUEST)

            # Check if both users belong to the same venue
            instance_venue = instance.recreational_venue.first()
            user_venue = request.user.recreational_venue.first()

            if instance_venue.id != user_venue.id:
                return Response({"error": "User not from your recreational venue"},
                                status=status.HTTP_403_FORBIDDEN)

            # Call the parent's delete method
            return super().delete(request, *args, **kwargs)
        except Http404:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)


class DelUserAdminBatch(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = UserBatchSrl

    def delete(self, request, *args, **kwargs):
        # Filter users with IDs between 8 and 50
        users_to_delete = Person.objects.filter(id__gte=141, id__lte=250)

        if not users_to_delete.exists():
            return Response(
                {"detail": "No users found in the specified range."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Delete the users
        count, _ = users_to_delete.delete()

        return Response(
            {"detail": f"{count} users deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


class UserFromAdminBatchView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = UserFromAdminBatchSerl

    def create(self, request, *args, **kwargs):
        admin_id = request.user.id
        print("Admin id is.   ", admin_id)
        admin = Admin.objects.get(id=admin_id)
        recreational_venue = admin.recreational_venue.first()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        role = validated_data.pop("role")
        excel_file = validated_data.pop('excel_link')
        ''''excel_file = ("https://storage.googleapis.com/download/storage/"
                      "v1/b/managy_bucket/o/admin_excel%2Ftestbatchcreation.xlsx?"
                      "generation=1730534493063868&alt=media")'''

        file_path = excel_file
        # df = pd.read_excel(file_path)
        df = pd.read_excel(file_path, engine='openpyxl')
        done_isd = []

        try:
            for index, row in df.iterrows():
                name = row['name']
                email = row['email']

                data = {
                    "first_name": name,
                    "email": email,
                    "role": role,
                    "recreational_venue_id": int(recreational_venue.id)
                }
                done_isd.append(send_post_request_createBatch(data))

        except Exception as e:
            for idi in done_isd:
                instance = Person.objects.get(pk=idi)
                instance.delete()
            return Response(data={"error": "Due to error: " + str(e) + "\nUsers "
                                                                         "created were rolled back: " + str(
                done_isd)}, status=status.HTTP_400_BAD_REQUEST)
            #raise AttributeError({"message": "Due to error: " + str(e) + "\nUsers "
            #                                                             "created were rolled back: " + str(
            #    done_isd)})

        return Response({"message": "Users Successfully Created"}, status=status.HTTP_201_CREATED)

    '''def perform_create(self, serializer):
        serializer.save()
        return {"message": "Users Successfully Created"}'''


class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        person = Person.objects.filter(email__iexact=email).first()

        if person:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(person)
            reset = PasswordReset(email=email, token=token)
            reset.save()

            send_token_password(email, token)

            #reset_url = f"{os.environ['PASSWORD_RESET_BASE_URL']}/{token}"
            # Sending reset link via email (commented out for clarity)
            # ... (email sending code)

            return Response({'success': 'We have sent you the token to reset your password'}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User with credentials not found"}, status=status.HTTP_404_NOT_FOUND)


class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = []

    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        new_password = data['new_password']
        confirm_password = data['confirm_password']

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=400)

        reset_obj = PasswordReset.objects.filter(token=token).first()

        if not reset_obj:
            return Response({'error': 'Invalid token'}, status=400)

        person = Person.objects.filter(email=reset_obj.email).first()

        if person:
            person.set_password(request.data['new_password'])
            person.save()

            reset_obj.delete()

            return Response({'success': 'Password updated'})
        else:
            return Response({'error': 'No user found'}, status=404)
