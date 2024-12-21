from datetime import datetime, timedelta, time
from datetime import date

from collections import defaultdict

from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.views import APIView
from django.core.files.storage import FileSystemStorage
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import UserSerializer, NoteSerializer, AmenitySerializer, BookingAmenityUpdate
from .serializers import EventSerializer, BookingAmenitySerializer, BookingAmenitySerializerView, \
    EventSelectionSerializer, EventSelectionSerializerView, EventSelectionSerializerUpdate, RecreationalVenueSerializer
from .serializers import ImageUploadSerializer, ExcelUploadSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note, Amenity, Events, BookingAmenity, EventSelection, RecreationalVenue
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from users.permissions import IsWorker, IsMember, IsAdmin
from datetime import date
from django.views.generic.edit import DeleteView
from rest_framework.response import Response
from rest_framework import status
from users.models import Worker

from data.utils import RandString
from data import gcp

import os
from django.conf import settings
from PIL import Image


class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)


class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)


class AmenityCreate(generics.CreateAPIView):
    serializer_class = AmenitySerializer
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsWorker]

    def get_queryset(self):
        user = self.request.user
        return Amenity.objects.filter(author=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)


class AmenityUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = AmenitySerializer
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsWorker]

    def get_queryset(self):
        user = self.request.user
        return Amenity.objects.filter(author=user)

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)


class AmenityList(generics.ListAPIView):
    serializer_class = AmenitySerializer
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        #user = self.request.user

        queryset = Amenity.objects.all()

        recreational_venue = self.request.user.recreational_venue.all()
        if recreational_venue:
            queryset = queryset.filter(author__recreational_venue__in=recreational_venue)
        return queryset
        #return Amenity.objects.filter(author=user)


class AmenityDelete(generics.RetrieveDestroyAPIView):
    serializer_class = AmenitySerializer
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsWorker]
    queryset = Amenity.objects.all()

    def get_queryset(self):
        return Amenity.objects.all()

    def perform_destroy(self, instance):
        instance.delete()


# Events
class EventCreate(generics.CreateAPIView):
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsWorker]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)


class EventList(generics.ListAPIView):
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Events.objects.all()


class EventUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsWorker]

    def get_queryset(self):
        return Events.objects.all()

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)


class EventDelete(generics.RetrieveDestroyAPIView):
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsWorker]

    def get_queryset(self):
        return Events.objects.all()

    def perform_destroy(self, instance):
        instance.delete()


class getEventName(generics.ListAPIView):
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.kwargs.get('query', '')
        queryset = Events.objects.filter(eventName__icontains=query)

        recreational_venue = self.request.user.recreational_venue.all()
        if recreational_venue:
            queryset = queryset.filter(author__recreational_venue__in=recreational_venue)

        today = datetime.now().date()
        queryset = queryset.filter(eventDate__gt=today)

        return queryset


class sortingEvents(generics.ListAPIView):
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        order = self.kwargs.get('pk', '')
        if order == 0:
            result = Events.objects.all()
        elif order == 1:
            result = Events.objects.all().order_by('eventDate').values()
        elif order == 2:
            result = Events.objects.all().order_by('-eventDate').values()
        else:
            result = Events.objects.all()

        recreational_venue = self.request.user.recreational_venue.all()
        if recreational_venue:
            result = result.filter(author__recreational_venue__in=recreational_venue)

        today = datetime.now().date()
        result = result.filter(eventDate__gt=today)

        return result


class searchEvents(generics.ListAPIView):
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        start = self.kwargs.get('start', '')
        end = self.kwargs.get('end', '')
        recreational_venue = self.request.user.recreational_venue.all()
        queryset = Events.objects.filter(eventDate__range=[start, end])

        if recreational_venue:
            queryset = queryset.filter(author__recreational_venue__in=recreational_venue)
        return queryset


class searchAmenitiesByName(generics.ListAPIView):
    serializer_class = AmenitySerializer
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        #authors=Amenity.objects.filter()
        #name = self.kwargs.get('name', '').strip()
        name = self.kwargs.get('name', None)
        recreational_venue = self.request.user.recreational_venue.all()

        queryset = Amenity.objects.all()

        if name:
            if recreational_venue:
                return Amenity.objects.filter(name__icontains=name,
                                              author__recreational_venue__in=recreational_venue)
        if recreational_venue:
            queryset = queryset.filter(author__recreational_venue__in=recreational_venue)

        return queryset

class sortingAmeneties(generics.ListAPIView):
    serializer_class = AmenitySerializer
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        order = self.kwargs.get('pk', '')
        if order == 0:
            result = Amenity.objects.all()
        elif order == 1:
            result = Amenity.objects.all().order_by('name').values()
        elif order == 2:
            result = Amenity.objects.all().order_by('-name').values()
        else:
            result = Amenity.objects.all()

        recreational_venue = self.request.user.recreational_venue.all()
        if recreational_venue:
            result = result.filter(author__recreational_venue__in=recreational_venue)

        return result


class createBooking(generics.CreateAPIView):
    serializer_class = BookingAmenitySerializer
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsMember]

    def post(self, request, *args, **kwargs):
        amenityID = request.data.get('amenities', None)
        toregister = int(request.data.get('amenity_capacity', None))
        cur_date = request.data.get('date', None)
        cur_time = request.data.get('time', None)

        # Parse the date
        try:
            date_field = datetime.strptime(cur_date, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return Response({"error": "Invalid date format. Send request "
                                      "again please"}, status=400)

        # Parse the time
        try:
            time_field = datetime.strptime(cur_time, "%H:%M:%S").time()
        except (ValueError, TypeError):
            return Response({"error": "Invalid time format"}, status=400)

        if not amenityID:
            return Response({'error': 'Amenity ID is required'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            amenityObj = Amenity.objects.get(pk=amenityID)
        except Amenity.DoesNotExist:
            return Response({'error': 'Amenity does not exist'},
                            status=status.HTTP_400_BAD_REQUEST)

        am_recVenue = amenityObj.author.recreational_venue.first()
        user_recVenue = self.request.user.recreational_venue.first()

        if am_recVenue.id != user_recVenue.id:
            return Response({'error': 'Amenity does not belong to this user'},
                            status=status.HTTP_400_BAD_REQUEST)

        #existing_booking = BookingAmenity.objects.filter(
            #amenities_id=amenityID,
            #date=cur_date,
            #time=cur_time
        #).exists()

        #if existing_booking:
            #return Response({'error': 'Amenity is already occupied'},
                            #status=status.HTTP_400_BAD_REQUEST)

        if not toregister:
            return Response({'error': 'Amenity Booking capacity cannot be null'},
                            status=status.HTTP_400_BAD_REQUEST)

        if toregister > amenityObj.capacity or toregister < 1:
            return Response({'error': f'Amenity capacity of {amenityObj.capacity} exceeded or invalid'},
                            status=status.HTTP_400_BAD_REQUEST)

        queryset1 = BookingAmenity.objects.filter(
            amenity_id = amenityID,
            date=cur_date,
            time=cur_time
        )
        total_registered1 = queryset1.aggregate(total=Sum('amenity_capacity'))['total']
        print(total_registered1)
        if total_registered1 and ((amenityObj.capacity - (total_registered1+toregister)) < 0):
            return Response(data={"error": f"This time slot is already full."}, status=status.HTTP_400_BAD_REQUEST)

        return super().post(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = 'register'
        return context

    def perform_create(self, serializer):
        book = serializer.save(author=self.request.user)
        return book

class getBooking(generics.ListAPIView):
    serializer_class = BookingAmenitySerializerView
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsMember]

    def get_queryset(self):
        user = self.request.user
        queryset = BookingAmenity.objects.filter(author=user)

        recreational_venue = self.request.user.recreational_venue.all()
        if recreational_venue:
            queryset = queryset.filter(author__recreational_venue__in=recreational_venue)

        today = datetime.now().date()
        current_time = timezone.now().time()
        print(queryset)
        print("+++")
        # Get all events for today and filter by time
        #today_queryset = queryset.filter(date=today, time__gte=current_time)
        print(today)
        today_queryset = queryset.filter(date=today)
        print(today_queryset)
        print("+++")

        # Get all events for future dates (no time check needed)
        future_queryset = queryset.filter(date__gte=today)
        print(future_queryset)
        print("+++")
        # Combine both querysets
        queryset = today_queryset | future_queryset
        queryset = queryset.distinct()

        queryset = queryset.filter(author__id=self.request.user.id)

        return queryset


class getAllBooking(generics.ListAPIView):
    serializer_class = BookingAmenitySerializerView
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsWorker]

    def get_queryset(self):
        return BookingAmenity.objects.all()


class cancelBooking(generics.RetrieveDestroyAPIView):
    serializer_class = BookingAmenitySerializer
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsMember]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = 'cancel'
        return context

    def get_queryset(self):
        user = self.request.user
        return BookingAmenity.objects.filter(author=user)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is None:
            return Response({'error': 'No primary key provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            booking = BookingAmenity.objects.get(pk=pk, author=request.user)
        except BookingAmenity.DoesNotExist:
            return Response({'error': 'Booking not found or unauthorized'}, status=status.HTTP_404_NOT_FOUND)

        return super().delete(request, *args, **kwargs)


class updateBooking(generics.UpdateAPIView):
    serializer_class = BookingAmenityUpdate
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsMember]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        return BookingAmenity.objects.filter(author=user)

    def put(self, request, *args, **kwargs):
        cur_booking = BookingAmenity.objects.get(pk=kwargs['pk'])

        toregister = request.data.get('amenity_capacity', None)
        cur_date = request.data.get('date', None)
        cur_time = request.data.get('time', None)

        amenityObj = Amenity.objects.get(pk=cur_booking.amenity_id)

        am_recVenue = amenityObj.author.recreational_venue.first()
        user_recVenue = self.request.user.recreational_venue.first()

        if am_recVenue.id != user_recVenue.id:
            return Response({'error': 'Amenity does not belong to this user RecrVenue'},
                            status=status.HTTP_400_BAD_REQUEST)

        if cur_booking.author.id != self.request.user.id:
            return Response({'error': 'Booking does not belong to this user'},
                            status=status.HTTP_400_BAD_REQUEST)

        existing_booking = BookingAmenity.objects.filter(
            amenities_id=amenityObj.id,
            date=cur_date,
            time=cur_time
        ).exists()

        if existing_booking:
            return Response({'error': 'Amenity is already occupied'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not toregister:
            return Response({'error': 'Amenity Booking capacity cannot be null'},
                            status=status.HTTP_400_BAD_REQUEST)
        if toregister > amenityObj.capacity or toregister < 1:
            return Response({'error': f'Amenity capacity of {amenityObj.capacity} exceeded or invalid'},
                            status=status.HTTP_400_BAD_REQUEST)

        return super().put(request, *args, **kwargs)

    def perform_update(self, serializer):
        booking = serializer.save(author=self.request.user)
        return booking


class searchBooking(generics.ListAPIView):
    serializer_class = BookingAmenitySerializerView
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        name = self.kwargs.get('name', '').strip()
        id = self.kwargs.get('id', '')
        if name:
            queryset = BookingAmenity.objects.filter(amenity_name__icontains=name)
        elif name and id:
            queryset = BookingAmenity.objects.filter(amenity_name__icontains=name, id__icontains=id)
        elif id:
            queryset = BookingAmenity.objects.filter(id__icontains=id)
        elif name:
            queryset = BookingAmenity.objects.filter(amenity_name__icontains=name)
        else:
            queryset = BookingAmenity.objects.all()

        recreational_venue = self.request.user.recreational_venue.all()
        if recreational_venue:
            queryset = queryset.filter(author__recreational_venue__in=recreational_venue)

        today = datetime.now().date()
        current_time = timezone.now().time()

        # Get all events for today and filter by time
        today_queryset = queryset.filter(date=today, time__gte=current_time)

        # Get all events for future dates (no time check needed)
        future_queryset = queryset.filter(date__gt=today)

        # Combine both querysets
        queryset = today_queryset | future_queryset
        queryset = queryset.distinct()

        queryset = queryset.filter(author__id=self.request.user.id)


        return queryset


class EventSelectionCreate(generics.CreateAPIView):
    serializer_class = EventSelectionSerializer
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsMember]

    def perform_create(self, serializer):
        eventSelect = serializer.save(author=self.request.user)
        return eventSelect

    def post(self, request, *args, **kwargs):
        event_data = request.data.get('eventRef')

        if not event_data:
            return Response(data={"error": "Event reference is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            event = Events.objects.get(id=event_data)
        except Events.DoesNotExist:
            return Response(data={"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        the_capacity = event.getCapacity()

        queryset1 = EventSelection.objects.filter(eventRef_id=event.getId())
        total_registered1 = queryset1.aggregate(total=Sum('numRegistered'))['total']
        total_registered2 = queryset1.count()
        #print(total_registered1)
        #print(total_registered2)

        if total_registered1 and not (the_capacity - total_registered1 > 0):
            return Response(data={"error": f"This event is already full."}, status=status.HTTP_400_BAD_REQUEST)

        if queryset1.filter(author_id=self.request.user.id).exists():
            return Response(data={"error": f"User already registered for the event"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Call the parent post method to perform the actual save
        return super().post(request, *args, **kwargs)


class EventSelectionView(generics.ListAPIView):
    serializer_class = EventSelectionSerializerView
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = EventSelection.objects.filter(author=user)

        queryset = EventSelection.objects.all()
        recreational_venue = self.request.user.recreational_venue.all()
        if recreational_venue:
            queryset = queryset.filter(author__recreational_venue__in=recreational_venue)

        current_date = now().date()
        queryset = queryset.filter(date__gte=current_date)

        queryset = queryset.filter(author_id=self.request.user.id)

        return queryset


class EventSelectionViewMember(generics.ListAPIView):
    serializer_class = EventSelectionSerializerView
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = EventSelection.objects.filter(author=user)

        recreational_venue = self.request.user.recreational_venue.all()
        if recreational_venue:
            queryset = queryset.filter(author__recreational_venue__in=recreational_venue)

        current_date = now().date()
        queryset = queryset.filter(date__gte=current_date)

        return queryset


class EventSelectionRegister(generics.UpdateAPIView):
    serializer_class = EventSelectionSerializerUpdate
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsMember]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = 'register'
        return context

    def get_queryset(self):
        return EventSelection.objects.all()
        #return EventSelection.objects.filter(date__gte=date.today())

    def perform_update(self, serializer):
        eventSelect = serializer.save()
        return eventSelect


class EventSelectionCancel(generics.DestroyAPIView):
    serializer_class = EventSelectionSerializerUpdate
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsMember]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = 'cancel'
        return context

    def get_queryset(self):
        return EventSelection.objects.all()

    def perform_update(self, serializer):
        eventSelect = serializer.save(member=self.request.user)
        return eventSelect

    def options(self, request, *args, **kwargs):
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        # Retrieve the object by ID
        event_selection_id = kwargs.get('pk')

        try:
            instance = EventSelection.objects.get(id=event_selection_id)
        except EventSelection.DoesNotExist:
            return Response({"error": "ID does not match an event selection."}, status=status.HTTP_404_NOT_FOUND)

        if not instance:
            return Response({"error": "ID does not match an event selection."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the current user is the author
        if instance.author_id != self.request.user.id:
            return Response({"error": "ID is not from an event of the user."}, status=status.HTTP_403_FORBIDDEN)

        # Delete the instance
        #instance.delete()

        #return Response({"message": "Event selection deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        return super().delete(request, *args, **kwargs)


class EventSelectionSearch(generics.ListAPIView):
    serializer_class = EventSelectionSerializerView
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        name = self.kwargs.get('name', '').strip()
        id = self.kwargs.get('id', '')
        user = self.request.user
        queryset = EventSelection.objects.filter(author=user)
        if name and id:
            queryset = queryset.filter(name__icontains=name, id__icontains=id)
        elif name:
            queryset = queryset.filter(name__icontains=name)

        recreational_venue = self.request.user.recreational_venue.all()
        if recreational_venue:
            queryset = queryset.filter(author__recreational_venue__in=[recreational_venue])

        current_date = now().date()
        queryset = queryset.filter(date__gte=current_date)

        return queryset


class Get_Recreational_venue(generics.ListAPIView):
    serializer_class = RecreationalVenueSerializer
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        recreational_venue = self.request.user.recreational_venue.all()
        return recreational_venue


#-----------------------------------------------------------------------
#---------- JAVIER - elr490 --------------------------------------------
#-----------------------------------------------------------------------

class RecreationalVenueView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RecreationalVenueSerializer

    def post(self, request, *args, **kwargs):
        serializer = RecreationalVenueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class uploadImageView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ImageUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            #serializer.save()
            image = validated_data.pop('image')
            title = validated_data.pop('title')

            img_name = f"{title}_{RandString(5)}.png"
            path = os.path.join('uploads/images', img_name)

            # Use FileSystemStorage to save the image
            fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'data'))
            filename = fs.save(path, image)
            file_url = fs.url(filename)  # Get the URL for the saved file

            # Optionally, upload to Google Cloud
            url = gcp.upload_to_gcp(os.path.join(settings.BASE_DIR, 'data', filename), "images/", img_name, 1)

            validated_data.update(url=url)
            return Response(validated_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class uploadExcelView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ExcelUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = ExcelUploadSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            file = validated_data.pop('file')
            title = validated_data.pop('title')

            fil_name = f"{title}_{RandString(5)}.xlsx"
            path = os.path.join('uploads/excel', fil_name)

            # Use FileSystemStorage to save the image
            fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'data'))
            filename = fs.save(path, file)
            file_url = fs.url(filename)  # Get the URL for the saved file

            # Optionally, upload to Google Cloud
            url = gcp.upload_to_gcp(os.path.join(settings.BASE_DIR, 'data', filename), "excel/", fil_name, 1)

            validated_data.update(url=url)
            return Response(validated_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DelRecreationalVenuesBatch(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = RecreationalVenueSerializer

    def delete(self, request, *args, **kwargs):
        # Filter users with IDs between 8 and 50
        to_delete = RecreationalVenue.objects.filter(id__gte=2, id__lte=50)

        if not to_delete.exists():
            return Response(
                {"detail": "No recreational venues found in the specified range."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Delete the users
        count, _ = to_delete.delete()

        return Response(
            {"detail": f"{count} recreational venues deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


class getBookingTimeSlots(generics.ListAPIView):
    authentication_classes = [JWTAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated, IsMember]

    def get(self, request, *args, **kwargs):
        amenity_id = kwargs.get('pk')

        current_date = datetime.now().date()

        days = [current_date + timedelta(days=i) for i in range(7)]

        # All 24:00:00
        all_times = [time(hour=h, minute=0) for h in range(24)]

        # Query existing bookings for the user within the next 7 days
        existing_bookings = BookingAmenity.objects.filter(
            amenity_id=amenity_id,
            date__gte=current_date,
            date__lte=days[-1]
        ).values('date', 'time')

        # Create a mapping of day to already booked times
        booked_slots = defaultdict(list)
        for booking in existing_bookings:
            booked_slots[booking['date']].append(booking['time'])

        # Create a structure for available slots
        available_slots = []
        for day in days:
            # Get available times by excluding booked times
            booked_times = booked_slots.get(day, [])
            available_times = [t for t in all_times if t not in booked_times]

            # Append the result for the current day
            available_slots.append({
                "day": day,
                "times": available_times
            })

        return Response(available_slots)