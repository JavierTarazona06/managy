from django.test import TestCase
from api.models import Amenity, Events, BookingAmenity, EventSelection, RecreationalVenue
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import requests
from rest_framework import status
from rest_framework.response import Response
from django.urls import reverse
from datetime import date
from users.models import Member, Worker, Admin
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase
import json


# Create your tests here.
class AmenityTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = get_user_model().objects.create_user(
            username='testuser',
            email='meme@sas.sm',
            password='testpass'
        )

        cls.amenity = Amenity.objects.create(
            name="Cool place",
            description="Nice place to vibe",
            capacity=10,
            occupied=False,
            author=cls.test_user
        )

    def test_amenity_creation(self):
        """Test that the Amenity instance is created correctly."""
        amenity = self.amenity
        self.assertEqual(self.amenity.name, "Cool place")
        self.assertEqual(self.amenity.description, "Nice place to vibe")
        self.assertEqual(self.amenity.capacity, 10)
        self.assertEqual(self.amenity.occupied, False)
        print(
            "Amenity Created: name=" + self.amenity.name + ",description=" + self.amenity.description + ",capacity:" + str(
                self.amenity.capacity) + "")

    def test_str_method(self):
        """Test the string representation of the Amenity."""
        self.assertEqual(str(self.amenity), "Cool place")  # Assuming __str__ method returns the name
        print("Testing str:" + str(self.amenity))

    def test_capacity_positive(self):
        """Test that the capacity is a positive integer."""
        self.assertGreater(self.amenity.capacity, 0)
        print("Testing capacity:" + str(self.amenity.capacity))

    def test_update_amenity(self):
        """Test updating an Amenity instance."""
        self.amenity.name = "Updated place"
        self.amenity.save()
        updated_amenity = Amenity.objects.get(id=self.amenity.id)
        self.assertEqual(updated_amenity.name, "Updated place")
        print(
            "Amenity updated: name=" + self.amenity.name + ",description=" + self.amenity.description + ",capacity:" + str(
                self.amenity.capacity))

    def test_delete_amenity(self):
        """Test deleting an Amenity instance."""
        amenity_id = self.amenity.id
        self.amenity.delete()
        with self.assertRaises(Amenity.DoesNotExist):
            Amenity.objects.get(id=amenity_id)

class AmenityTestView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a RecreationalVenue instance for association
        cls.recreational_venue = RecreationalVenue.objects.create(
            name="Test Recreational Venue",
            address="123 Test Street",
            photo="1234567890"
        )

        cls.admin_user = Admin.create_admin(
            username="admin",
            password="adminpassword",
            email='admin@sas.sm',
            role="admin"
        )

        cls.token_admin = RefreshToken.for_user(cls.admin_user).access_token
        cls.admin_user.recreational_venue.add(cls.recreational_venue.id)
    def test_amenity_creation(self):
        """Test that the Amenity instance is created correctly."""
        data = {
            "name":"Cool place",
            "description":"Nice place to vibe",
            "capacity":10,
            "occupied":False,
            "image":"pepe",
            "author":self.admin_user
        }
        response = self.client.post('/api/amenity/create/', data, format='json',HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Amenity.objects.count(), 1)
        self.assertEqual(Amenity.objects.first().name, "Cool place")
        self.assertEqual(Amenity.objects.first().description,"Nice place to vibe")
        self.assertEqual(Amenity.objects.first().capacity, 10)
        self.assertEqual(Amenity.objects.first().occupied,False)
        #print("Amenity Created: name="+self.amenity.name+",description="+self.amenity.description+",capacity:"+str(self.amenity.capacity)+"")

    def test_list_amenity(self):
        """Test listing Events."""
        data = {
            "name":"Cool place",
            "description":"Nice place to vibe",
            "capacity":10,
            "occupied":False,
            "image":"pepe",
            "author":self.admin_user
        }
        response_creation = self.client.post('/api/amenity/create/', data, format='json',HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        response = self.client.get('/api/amenity/view/', HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0].get("name"), "Cool place")
        self.assertEqual(response.data[0].get("description"), "Nice place to vibe")
        self.assertEqual(response.data[0].get("occupied"), False)
        self.assertEqual(response.data[0].get("image"),"pepe")
        self.assertEqual(response.data[0].get("capacity"), 10)

    def test_update_amenity(self):
        """Test updating an Amenity instance."""
        data = {
            "name":"Cool place",
            "description":"Nice place to vibe",
            "capacity":10,
            "occupied":False,
            "image": "pepe",
            "author":self.admin_user
        }
        response_creation = self.client.post('/api/amenity/create/', data, format='json',HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        self.assertEqual(response_creation.status_code, 201)

        #print("Response:"+str(response_creation.content))
        data = {
            "name":"Updated place",
            "description":"Nice place to vibe",
            "capacity": 10,
            "occupied": False,
            "image": "pepe",
        }
        #print("data:"+str(response_creation.data.get("id")))
        response = self.client.put(f'/api/amenity/update/{response_creation.data.get('id')}/', data, content_type="application/json", HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Amenity.objects.count(), 1)
        self.assertEqual(Amenity.objects.first().name, "Updated place")
        self.assertEqual(Amenity.objects.first().description,"Nice place to vibe")
        self.assertEqual(Amenity.objects.first().capacity, 10)
        self.assertEqual(Amenity.objects.first().occupied,False)
    def test_delete_amenity(self):
        """Test deleting an Amenity instance."""
        data = {
            "name":"Cool place",
            "description":"Nice place to vibe",
            "capacity":10,
            "occupied":False,
            "image": "pepe",
            "author": self.admin_user
        }
        response_creation = self.client.post('/api/amenity/create/', data, format='json',HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        self.assertEqual(response_creation.status_code, 201)

        response = self.client.delete(f'/api/amenity/delete/{response_creation.data.get('id')}/',HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Amenity.DoesNotExist):
            Amenity.objects.get(id=response_creation.data.get("id"))


    def test_sort_amenity(self):
        """Test sort Events."""
        amenity_1 = {
            "name":"Cool place",
            "description":"Nice place to vibe",
            "capacity":10,
            "occupied":False,
            "image":"pepe",
            "author":self.admin_user
        }
        amenity_2 = {
            "name":"Pool",
            "description":"Warm",
            "capacity":10,
            "occupied":False,
            "image":"pasas",
            "author":self.admin_user
        }
        amenity_3 = {
            "name":"Cabin",
            "description":"Cozy",
            "capacity":4,
            "occupied":False,
            "image":"paasasasas",
            "author":self.admin_user
        }
        response_creation_1 = self.client.post('/api/amenity/create/', amenity_1, format='json',HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        self.assertEqual(response_creation_1.status_code, 201)

        response_creation_2 = self.client.post('/api/amenity/create/', amenity_2, format='json',HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        self.assertEqual(response_creation_2.status_code, 201)

        response_creation_3 = self.client.post('/api/amenity/create/', amenity_3, format='json',HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        self.assertEqual(response_creation_3.status_code, 201)

        #Ascending
        response_random = self.client.get(f'/api/amenity/get_amenity/0/', HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        self.assertEqual(response_random.status_code, 200)
        self.assertEqual(response_random.data[0].get("name"), "Cool place")
        self.assertEqual(response_random.data[1].get("name"), "Pool")
        self.assertEqual(response_random.data[2].get("name"), "Cabin")

        response_ascending = self.client.get(f'/api/amenity/get_amenity/1/', HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        self.assertEqual(response_ascending.data[0].get("name"), "Cabin")
        self.assertEqual(response_ascending.data[1].get("name"), "Cool place")
        self.assertEqual(response_ascending.data[2].get("name"), "Pool")

        response_descending = self.client.get(f'/api/amenity/get_amenity/2/', HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        self.assertEqual(response_descending.data[0].get("name"), "Pool")
        self.assertEqual(response_descending.data[1].get("name"), "Cool place")
        self.assertEqual(response_descending.data[2].get("name"), "Cabin")

    def test_search_amenity(self):
        """Test listing Events."""
        amenity_1 = {
            "name": "Cool place",
            "description": "Nice place to vibe",
            "capacity": 10,
            "occupied": False,
            "image": "pepe",
            "author": self.admin_user
        }
        amenity_2 = {
            "name": "Pool",
            "description": "Warm",
            "capacity": 10,
            "occupied": False,
            "image": "pasas",
            "author": self.admin_user
        }
        amenity_3 = {
            "name": "Cabin",
            "description": "Cozy",
            "capacity": 4,
            "occupied": False,
            "image": "paasasasas",
            "author": self.admin_user
        }
        response_creation_1 = self.client.post('/api/amenity/create/', amenity_1, format='json',HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        self.assertEqual(response_creation_1.status_code, 201)

        response_creation_2 = self.client.post('/api/amenity/create/', amenity_2, format='json',HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        self.assertEqual(response_creation_2.status_code, 201)

        response_creation_3 = self.client.post('/api/amenity/create/', amenity_3, format='json',HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        self.assertEqual(response_creation_3.status_code, 201)

        response_search_1 = self.client.get(f'/api/amenity/search/Cabin/', HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        self.assertEqual(response_search_1.status_code, 200)
        self.assertEqual(len(response_search_1.data),1)

        self.assertEqual(response_search_1.data[0].get("name"), "Cabin")

        response_search_2 = self.client.get(f'/api/amenity/search/C/', HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        self.assertEqual(response_search_2.status_code, 200)
        self.assertEqual(len(response_search_2.data),2)
        self.assertEqual(response_search_2.data[0].get("name"), "Cool place")
        self.assertEqual(response_search_2.data[1].get("name"), "Cabin")

        response_search_3 = self.client.get(f'/api/amenity/search/blaSajas/', HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        self.assertEqual(response_search_3.status_code, 200)
        self.assertEqual(len(response_search_3.data),0)


class EventTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = Admin.create_person(
            username='testuser',
            email='meme@sas.sm',
            role='worker',
            password='testpass'
        )
        cls.event = Events.objects.create(
            eventName="Yoga Class",
            eventDescription="A relaxing yoga class",
            eventLocation="Studio A",
            eventTime="10:00:00",
            eventDate="2024-11-20",
            eventCapacity=20,
            author=cls.test_user
        )

    def test_event_creation(self):
        """Test that the Event instance is created correctly."""
        event = self.event
        self.assertEqual(event.eventName, "Yoga Class")
        self.assertEqual(event.eventDescription, "A relaxing yoga class")
        self.assertEqual(event.eventLocation, "Studio A")
        self.assertEqual(event.eventTime, "10:00:00")
        self.assertEqual(event.eventDate, "2024-11-20")
        self.assertEqual(event.eventCapacity, 20)
        self.assertEqual(event.author.username, "meme@sas.sm")

    def test_str_method(self):
        """Test the string representation of the Events."""
        self.assertEqual(str(self.event), "Yoga Class")

    def test_get_event_details(self):
        """Test the getEventDetails method."""
        event_details = self.event.getEventDetails()
        expected_details = "Yoga Class A relaxing yoga class Studio A 10:00:00"
        self.assertEqual(event_details, expected_details)

    def test_is_event_today(self):
        """Test the isEventToday method."""
        event_today = Events.objects.create(
            eventName="Today’s Event",
            eventDescription="An event happening today",
            eventLocation="Studio B",
            eventTime="14:00:00",
            eventDate=date.today(),
            eventCapacity=10,
            author=self.test_user
        )
        self.assertTrue(event_today.isEventToday())

        event_not_today = Events.objects.create(
            eventName="Future Event",
            eventDescription="An event happening in the future",
            eventLocation="Studio C",
            eventTime="16:00:00",
            eventDate="2024-12-01",
            eventCapacity=10,
            author=self.test_user
        )
        self.assertFalse(event_not_today.isEventToday())

    def test_update_event(self):
        """Test updating an Event instance."""
        self.event.eventName = "Updated Yoga Class"
        self.event.save()
        updated_event = Events.objects.get(id=self.event.id)
        self.assertEqual(updated_event.eventName, "Updated Yoga Class")

    def test_delete_event(self):
        """Test deleting an Event instance."""
        event_id = self.event.id
        self.event.delete()
        with self.assertRaises(Events.DoesNotExist):
            Events.objects.get(id=event_id)


class EventViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """
        cls.test_user = get_user_model().objects.create_user(
            username='testuser',
            email='meme@sas.sm',
            password='testpass'
        )
        """
        # Create a RecreationalVenue instance for association
        cls.recreational_venue = RecreationalVenue.objects.create(
            name="Test Recreational Venue",
            address="123 Test Street",
            photo="1234567890"
        )

        cls.test_user = Admin.create_admin(
            username='testuser',
            email='meme@sas.sm',
            role='admin',
            password='testpass'
        )
        cls.test_user.recreational_venue.add(cls.recreational_venue.id)
        cls.token = RefreshToken.for_user(cls.test_user).access_token

        cls.event_data = {
            "eventName": "New Event",
            "eventDescription": "This is a test event",
            "eventLocation": "Test Location",
            "eventTime": "15:00:00",
            "eventDate": "2024-11-25",
            "eventCapacity": 30,
            "author": cls.test_user.id
        }

    def get_auth_headers(self):
        """Helper method to get the authorization headers with the JWT token."""
        return {'Authorization': f'Bearer {self.token}'}

    def test_create_event(self):
        """Test creating an Events."""
        #login = self.client.login(username='testuser', password='testpass')
        #print(login)
        response = self.client.post(reverse('create-event'), self.event_data, format='json', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 201)
        event = Events.objects.first()
        self.assertEqual(Events.objects.count(),1)
        self.assertEqual(event.eventDescription, "This is a test event")
        self.assertEqual(event.eventLocation, "Test Location")
        self.assertEqual(event.eventTime.strftime('%H:%M:%S'), "15:00:00")
        self.assertEqual(event.eventDate.strftime('%Y-%m-%d'),"2024-11-25")
        self.assertEqual(event.eventCapacity, 30)

    def test_event_list(self):
        """Test listing Events."""
        #self.client.login(username='testuser', password='testpass')
        response_creation = self.client.post(reverse('create-event'), self.event_data, format='json', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response_creation.status_code, 201)

        response = self.client.get(reverse('view-event'), HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data),1)
        self.assertEqual(response.data[0].get("eventName"), "New Event")
        self.assertEqual(response.data[0].get("eventDescription"), "This is a test event")
        self.assertEqual(response.data[0].get("eventLocation"), "Test Location")
        self.assertEqual(response.data[0].get("eventTime"), "15:00:00")
        self.assertEqual(response.data[0].get("eventDate"),"2024-11-25")
        self.assertEqual(response.data[0].get("eventCapacity"), 30)
        #print(response.content)

    def test_update_event(self):
        """Test updating an Events."""
        event = Events.objects.create(
            eventName="Yoga Class",
            eventDescription="A relaxing yoga class",
            eventLocation="Studio A",
            eventTime="10:00:00",
            eventDate="2024-11-20",
            eventCapacity=20,
            author=self.test_user
        )
        data = {
            "eventName": "Updated Yoga Class",
            "eventDescription": "An updated relaxing yoga class",
            "eventLocation": "Studio D",
            "eventTime": "11:00:00",
            "eventDate": "2024-11-21",
            "eventCapacity": 25
        }
        response = self.client.put(reverse('update-event', kwargs={'pk': event.id}), data, format='json', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        event.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(event.eventName, "Updated Yoga Class")
        self.assertEqual(event.eventLocation, "Studio D")


    def test_delete_event(self):
        """Test deleting an Events."""
        event = Events.objects.create(
            eventName="Yoga Class",
            eventDescription="A relaxing yoga class",
            eventLocation="Studio A",
            eventTime="10:00:00",
            eventDate="2024-11-20",
            eventCapacity=20,
            author=self.test_user
        )
        response = self.client.delete(reverse('delete-event', kwargs={'pk': event.id}), HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Events.DoesNotExist):
            Events.objects.get(id=event.id)

    def test_search_event_name(self):
        event_data_1 = {
            "eventName": "eew Event",
            "eventDescription": "This is a test event",
            "eventLocation": "Test Location",
            "eventTime": "15:00:00",
            "eventDate": "2027-11-25",
            "eventCapacity": 30,
            "author": self.test_user.id
        }
        event_data_2 = {
            "eventName": "zxasas",
            "eventDescription": "This is a test event2",
            "eventLocation": "Test Location2",
            "eventTime": "15:00:00",
            "eventDate": "2026-11-25",
            "eventCapacity": 30,
            "author": self.test_user.id
        }
        event_data_3 = {
            "eventName": "eppep",
            "eventDescription": "This is a test event",
            "eventLocation": "Test Location",
            "eventTime": "15:00:00",
            "eventDate": "2025-11-25",
            "eventCapacity": 30,
            "author": self.test_user.id
        }

        response_creation_1 = self.client.post(reverse('create-event'), event_data_1, format='json', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response_creation_1.status_code, 201)

        response_creation_2 = self.client.post(reverse('create-event'), event_data_2, format='json', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response_creation_2.status_code, 201)

        response_creation_3 = self.client.post(reverse('create-event'), event_data_3, format='json', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response_creation_3.status_code, 201)

        response_search_1 = self.client.get(f'/api/event/get_event_name/e/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response_search_1.status_code, 200)
        self.assertEqual(len(response_search_1.data),2)
        self.assertEqual(response_search_1.data[0].get("eventName"), "eew Event")
        self.assertEqual(response_search_1.data[1].get("eventName"), "eppep")

        response_search_2 = self.client.get(f'/api/event/get_event_name/zxasas/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response_search_2.status_code, 200)
        self.assertEqual(len(response_search_2.data),1)
        self.assertEqual(response_search_2.data[0].get("eventName"), "zxasas")

        response_search_3 = self.client.get(f'/api/event/get_event_name/zxFsas/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response_search_3.status_code, 200)
        self.assertEqual(len(response_search_3.data),0)


    def test_sort_event(self):
        event_data_1 = {
            "eventName": "eew Event",
            "eventDescription": "This is a test event",
            "eventLocation": "Test Location",
            "eventTime": "15:00:00",
            "eventDate": "2027-11-25",
            "eventCapacity": 30,
            "author": self.test_user.id
        }
        event_data_2 = {
            "eventName": "zxasas",
            "eventDescription": "This is a test event2",
            "eventLocation": "Test Location2",
            "eventTime": "15:00:00",
            "eventDate": "2026-11-25",
            "eventCapacity": 30,
            "author": self.test_user.id
        }
        event_data_3 = {
            "eventName": "eppep",
            "eventDescription": "This is a test event",
            "eventLocation": "Test Location",
            "eventTime": "15:00:00",
            "eventDate": "2025-11-25",
            "eventCapacity": 30,
            "author": self.test_user.id
        }

        response_creation_1 = self.client.post(reverse('create-event'), event_data_1, format='json', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response_creation_1.status_code, 201)

        response_creation_2 = self.client.post(reverse('create-event'), event_data_2, format='json', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response_creation_2.status_code, 201)

        response_creation_3 = self.client.post(reverse('create-event'), event_data_3, format='json', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response_creation_3.status_code, 201)

        response_sort_1 = self.client.get(f'/api/event/get_event/0/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response_sort_1.status_code, 200)
        self.assertEqual(len(response_sort_1.data),3)
        self.assertEqual(response_sort_1.data[0].get("eventDate"), "2027-11-25")
        self.assertEqual(response_sort_1.data[1].get("eventDate"), "2026-11-25")
        self.assertEqual(response_sort_1.data[2].get("eventDate"), "2025-11-25")

        response_sort_2 = self.client.get(f'/api/event/get_event/1/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response_sort_2.status_code, 200)
        self.assertEqual(len(response_sort_2.data),3)
        self.assertEqual(response_sort_2.data[0].get("eventDate"), "2025-11-25")
        self.assertEqual(response_sort_2.data[1].get("eventDate"), "2026-11-25")
        self.assertEqual(response_sort_2.data[2].get("eventDate"), "2027-11-25")

        response_sort_3 = self.client.get(f'/api/event/get_event/2/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response_sort_3.status_code, 200)
        self.assertEqual(len(response_sort_3.data),3)
        self.assertEqual(response_sort_3.data[0].get("eventDate"), "2027-11-25")
        self.assertEqual(response_sort_3.data[1].get("eventDate"), "2026-11-25")
        self.assertEqual(response_sort_3.data[2].get("eventDate"), "2025-11-25")
    def test_filter_event(self):
        event_data_1 = {
            "eventName": "eew Event",
            "eventDescription": "This is a test event",
            "eventLocation": "Test Location",
            "eventTime": "15:00:00",
            "eventDate": "2027-11-25",
            "eventCapacity": 30,
            "author": self.test_user.id
        }
        event_data_2 = {
            "eventName": "zxasas",
            "eventDescription": "This is a test event2",
            "eventLocation": "Test Location2",
            "eventTime": "15:00:00",
            "eventDate": "2026-11-25",
            "eventCapacity": 30,
            "author": self.test_user.id
        }
        event_data_3 = {
            "eventName": "eppep",
            "eventDescription": "This is a test event",
            "eventLocation": "Test Location",
            "eventTime": "15:00:00",
            "eventDate": "2025-11-25",
            "eventCapacity": 30,
            "author": self.test_user.id
        }

        response_creation_1 = self.client.post(reverse('create-event'), event_data_1, format='json', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response_creation_1.status_code, 201)

        response_creation_2 = self.client.post(reverse('create-event'), event_data_2, format='json', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response_creation_2.status_code, 201)

        response_creation_3 = self.client.post(reverse('create-event'), event_data_3, format='json', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response_creation_3.status_code, 201)

        response_sort_1 = self.client.get(f'/api/event/filter_event_date/2025-10-10/2027-12-10/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response_sort_1.status_code, 200)
        self.assertEqual(len(response_sort_1.data),3)
        self.assertEqual(response_sort_1.data[0].get("eventDate"), "2027-11-25")
        self.assertEqual(response_sort_1.data[1].get("eventDate"), "2026-11-25")
        self.assertEqual(response_sort_1.data[2].get("eventDate"), "2025-11-25")

        response_sort_2 = self.client.get(f'/api/event/filter_event_date/2025-10-10/2026-12-10/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response_sort_2.status_code, 200)
        self.assertEqual(len(response_sort_2.data),2)
        self.assertEqual(response_sort_2.data[0].get("eventDate"), "2026-11-25")
        self.assertEqual(response_sort_2.data[1].get("eventDate"), "2025-11-25")

        response_sort_3 = self.client.get(f'/api/event/filter_event_date/2025-10-10/2025-12-10/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response_sort_3.status_code, 200)
        self.assertEqual(len(response_sort_3.data),1)
        self.assertEqual(response_sort_3.data[0].get("eventDate"), "2025-11-25")

        response_sort_4 = self.client.get(f'/api/event/filter_event_date/2023-10-10/2024-12-10/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response_sort_4.status_code, 200)
        self.assertEqual(len(response_sort_4.data),0)


class BookingAmenityTestView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test users
        cls.worker_user = get_user_model().objects.create_user(
            username='workeruser',
            email='worker@sas.sm',
            password='testpass',
            role="worker"
        )
        cls.member_user = get_user_model().objects.create_user(
            username='memberuser',
            email='member@sas.sm',
            password='testpass',
            role="member"
        )

        # Create a RecreationalVenue instance for association
        cls.recreational_venue = RecreationalVenue.objects.create(
            name="Test Recreational Venue",
            address="123 Test Street",
            photo="1234567890"
        )

        cls.token_worker = RefreshToken.for_user(cls.worker_user).access_token
        cls.token_member = RefreshToken.for_user(cls.member_user).access_token
        cls.worker_user.recreational_venue.add(cls.recreational_venue.id)
        cls.member_user.recreational_venue.add(cls.recreational_venue.id)

        # Create test amenity
        cls.test_amenity = Amenity.objects.create(
            name="Cool place",
            description="Nice place to vibe",
            capacity=10,
            occupied=False,
            author=cls.worker_user
        )

    def test_create_booking(self):
        """Test creating a booking for an amenity (as a member)."""
        data = {
            "amenities": self.test_amenity.id,
            "date": "2024-11-24",
            "time": "15:00:00",
            "amenity_details": "pepe",
            "amenity_capacity": 5
        }
        response = self.client.post('/api/amenity/booking/create/', data, format='json',HTTP_AUTHORIZATION=f'Bearer {self.token_member}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BookingAmenity.objects.count(), 1)
        booking = BookingAmenity.objects.first()
        self.assertEqual(booking.amenities, self.test_amenity)
        self.assertEqual(booking.author, self.member_user)

    def test_create_booking_as_worker(self):
        """Test that a worker cannot create a booking (workers should not have booking rights)."""
        #self.client.login(username='workeruser', password='testpass')
        data = {
            "amenity": self.test_amenity.id,
        }
        response = self.client.post('/api/amenity/booking/create/', data, format='json',
                                    HTTP_AUTHORIZATION=f'Bearer {self.token_worker}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_bookings(self):
        """Test retrieving bookings for a user."""
        #Create a booking for the member user
        #self.client.login(username='memberuser', password='testpass')

        data = {
            "amenities": self.test_amenity.id,
            "date": "2025-11-24",
            "time": "15:00:00",
            "amenity_details": "pepe",
            "amenity_capacity": 5,
            "author": self.member_user.id
        }
        response_creation = self.client.post('/api/amenity/booking/create/', data, format='json',HTTP_AUTHORIZATION=f'Bearer {self.token_member}')
        self.assertEqual(response_creation.status_code, status.HTTP_201_CREATED)

        response = self.client.get('/api/amenity/booking/view/', HTTP_AUTHORIZATION=f'Bearer {self.token_member}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print("Test:"+str(response.data[0]))
        #print("Test:" + str(response.data))
        #self.assertEqual(len(response.data), 1)
        #self.assertEqual(response.data[0], self.test_amenity.id)
        #print("Test:"+str(response.content))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get("amenity_details"), data.get("amenity_details"))
        self.assertEqual(response.data[0].get("amenity_capacity"), data.get("amenity_capacity"))
        self.assertEqual(response.data[0].get("start_time_date"), data.get("start_time_date"))



    def test_cancel_booking(self):
        """Test canceling a booking."""
        # Create a booking for the member user
        #self.client.login(username='memberuser', password='testpass')
        booking = BookingAmenity.objects.create(
            amenities=self.test_amenity,
            date="2024-11-24",
            time="15:00:00",
            amenity_details="pepe",
            amenity_capacity=5,
            author=self.member_user,
        )
        response = self.client.delete(f'/api/amenity/booking/cancel/{booking.id}/',
                                      HTTP_AUTHORIZATION=f'Bearer {self.token_member}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Check that the booking is deleted
        with self.assertRaises(BookingAmenity.DoesNotExist):
            BookingAmenity.objects.get(id=booking.id)

    def test_cancel_booking_as_worker(self):
        """Test that a worker cannot cancel a booking they did not create."""
        # Create a booking for the member user
        #self.client.login(username='workeruser', password='testpass')
        booking = BookingAmenity.objects.create(
            amenities=self.test_amenity,
            date="2024-11-24",
            time="15:00:00",
            amenity_details="pepe",
            amenity_capacity=31,
            author=self.member_user,
        )
        response = self.client.delete(f'/api/amenity/booking/cancel/{booking.id}/',
                                      HTTP_AUTHORIZATION=f'Bearer {self.token_worker}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_booking_unauthorized(self):
        """Test that an unauthorized user cannot create a booking."""
        data = {
            "amenities": self.test_amenity.id,
        }
        response = self.client.post('/api/amenity/booking/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_bookings_unauthorized(self):
        """Test that an unauthorized user cannot view bookings."""
        response = self.client.get('/api/amenity/booking/view/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cancel_booking_unauthorized(self):
        """Test that an unauthorized user cannot cancel a booking."""
        booking = BookingAmenity.objects.create(
            amenities=self.test_amenity,
            date="2024-11-24",
            time="15:00:00",
            amenity_details="pepe",
            amenity_capacity=31,
            author=self.member_user,
        )
        response = self.client.delete(f'/api/amenity/booking/cancel/{booking.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permissions_for_non_member(self):
        """Test that only members (not workers) can make bookings."""
        #self.client.login(username='workeruser', password='testpass')
        data = {
            "amenities": self.test_amenity.id,
            "date": "2025-11-24",
            "time": "15:00:00",
            "amenity_details": "pepe",
            "amenity_capacity": 31
        }
        response = self.client.post('/api/amenity/booking/create/', data, format='json',
                                    HTTP_AUTHORIZATION=f'Bearer {self.token_worker}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_search_bookingAmenity(self):
        self.test_amenity_2 = Amenity.objects.create(
            name="Wonderous place",
            description="Nice place to vibe",
            capacity=10,
            occupied=False,
            author=self.worker_user
        )
        self.test_amenity_3 = Amenity.objects.create(
            name="Wonderful place",
            description="Nice place to vibe",
            capacity=10,
            occupied=False,
            author=self.worker_user
        )

        amenity_1 = {
            "amenities": self.test_amenity.id,
            "amenity_name":self.test_amenity.name,
            "date": "2026-11-24",
            "time": "15:30:00",
            "amenity_details":"pep3e",
            "amenity_capacity":4,
            "author":self.member_user
        }
        amenity_2 = {
            "amenities": self.test_amenity_2.id,
            "amenity_name": self.test_amenity_2.name,
            "date": "2026-11-24",
            "time": "15:30:00",
            "amenity_details":"pepe",
            "amenity_capacity":8,
            "author": self.member_user

        }
        amenity_3 = {
            "amenities": self.test_amenity_3.id,
            "amenity_name": self.test_amenity_3.name,
            "date": "2026-11-24",
            "time": "15:30:00",
            "amenity_details":"asas",
            "amenity_capacity":5,
            "author": self.member_user
        }

        response_creation_1 = self.client.post('/api/amenity/booking/create/',amenity_1, format='json',HTTP_AUTHORIZATION=f'Bearer {self.token_member}')
        self.assertEqual(response_creation_1.status_code, status.HTTP_201_CREATED)

        response_creation_2 = self.client.post('/api/amenity/booking/create/',amenity_2, format='json',HTTP_AUTHORIZATION=f'Bearer {self.token_member}')
        self.assertEqual(response_creation_2.status_code, status.HTTP_201_CREATED)

        response_creation_3 = self.client.post('/api/amenity/booking/create/',amenity_3, format='json',HTTP_AUTHORIZATION=f'Bearer {self.token_member}')
        self.assertEqual(response_creation_3.status_code, status.HTTP_201_CREATED)

        response_search_1 = self.client.get(f'/api/amenity/booking/search/Wond/1/', HTTP_AUTHORIZATION=f'Bearer {self.token_member}')
        self.assertEqual(response_search_1.status_code, 200)
        self.assertEqual(len(response_search_1.data),2)
        self.assertEqual(response_search_1.data[0].get("amenity_name"), "Wonderous place")
        self.assertEqual(response_search_1.data[1].get("amenity_name"), "Wonderful place")

        response_search_2 = self.client.get(f'/api/amenity/booking/search/Wondero/2/', HTTP_AUTHORIZATION=f'Bearer {self.token_member}')
        self.assertEqual(response_search_2.status_code, 200)
        self.assertEqual(len(response_search_2.data),1)
        self.assertEqual(response_search_2.data[0].get("amenity_name"), "Wonderous place")

        response_search_3 = self.client.get(f'/api/amenity/booking/search/Wasasas/60/', HTTP_AUTHORIZATION=f'Bearer {self.token_member}')
        self.assertEqual(response_search_3.status_code, 200)
        self.assertEqual(len(response_search_3.data),0)


class EventSelectionTestsView(TestCase):
    def setUp(self):
        # Create a RecreationalVenue instance for association
        self.recreational_venue = RecreationalVenue.objects.create(
            name="Test Recreational Venue",
            address="123 Test Street",
            photo="1234567890"
        )

        """Set up test environment with initial data."""
        # Create users
        self.member_user = Member.create_member(
            username="member",
            password="memberpassword",
            role='member',
            email="member@asl.sm"
        )

        self.admin_user = Admin.create_admin(
            username="admin",
            password="adminpassword",
            email='admin@sas.sm',
            role="admin"
        )

        # Create a member profile
        #self.member = Member.objects.create(user=self.member_user)

        # Create an event
        self.event = Events.objects.create(
            eventName="Yoga Class",
            eventDescription="A calming yoga session.",
            eventLocation="Yoga Studio",
            eventCapacity=20,
            eventTime="10:00:00",
            eventDate="2024-12-01",
            author=self.admin_user
        )

        self.token_member = RefreshToken.for_user(self.member_user).access_token
        self.token_admin = RefreshToken.for_user(self.admin_user).access_token

        # Authenticate the client
        #self.client.login(username="member", password="memberpassword")

        self.admin_user.recreational_venue.add(self.recreational_venue.id)
        self.member_user.recreational_venue.add(self.recreational_venue.id)

    def test_event_selection_creation(self):
        """Test that an event selection can be created."""
        url = "/api/event/selection/create/"
        data = {
            "eventRef": self.event.id,
            "author": self.admin_user.id
        }
        response = self.client.post(url, data, format="json", HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EventSelection.objects.count(), 1)
        self.assertEqual(EventSelection.objects.get().eventRef, self.event)

    def test_register_for_event(self):
        """Test that a user can register for an event."""
        # First, create an event selection
        event_selection = EventSelection.objects.create(
            eventRef=self.event,
            name=self.event.getName(),
            date=self.event.getDate(),
            time=self.event.getTime(),
            numRegistered=0,
            description=self.event.getDescription(),
            capacity=self.event.getCapacity(),
            author=self.admin_user
        )
        # Now try registering for the event
        url = f"/api/event/selection/register/{event_selection.id}/"
        response = self.client.put(url, {}, HTTP_AUTHORIZATION=f'Bearer {self.token_member}',content_type='application/json')

        # Print the response to understand the error
        #print(response.content)  # Print response to help debug
        #print(response.status_code)  # Ensure we are seeing the status code for clarity

        event_selection.refresh_from_db()
        # Check if the registration was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        event_selection.refresh_from_db()
        self.assertIn(self.member_user, event_selection.membersRegistered.all())
        self.assertEqual(event_selection.numRegistered, 1)

    def test_register_for_event_already_registered(self):
        """Test that a user cannot register twice for the same event."""
        # First, create an event selection and register the user
        self.event_selection = EventSelection.objects.create(
            eventRef=self.event,
            name=self.event.getName(),
            date=self.event.getDate(),
            time=self.event.getTime(),
            numRegistered=0,
            description=self.event.getDescription(),
            capacity=self.event.getCapacity(),
            author=self.member_user
        )

        # Register
        url = f"/api/event/selection/register/{self.event_selection.id}/"
        response_register = self.client.put(url, {}, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {self.token_member}')

        # Try registering again
        url = f"/api/event/selection/register/{self.event_selection.id}/"
        response = self.client.put(url, {}, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {self.token_member}')

        # Should raise a validation error because the user is already registered
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_registration(self):
        """Test that a user can cancel their registration for an event."""
        # First, create an event selection and register the user
        self.event_selection = EventSelection.objects.create(
            eventRef=self.event,
            name=self.event.getName(),
            date=self.event.getDate(),
            time=self.event.getTime(),
            numRegistered=0,
            description=self.event.getDescription(),
            capacity=self.event.getCapacity(),
            author=self.member_user
        )

        # Try registering again
        url = f"/api/event/selection/register/{self.event_selection.id}/"
        response_register = self.client.put(url, {}, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {self.token_member}')

        # Now, cancel the registration
        url = f"/api/event/selection/register/cancel/{self.event_selection.id}/"
        response = self.client.put(url, {}, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {self.token_member}')

        # Check if the cancellation was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event_selection.refresh_from_db()
        self.assertNotIn(self.member_user, self.event_selection.membersRegistered.all())
        self.assertEqual(self.event_selection.numRegistered, 0)

    def test_cancel_registration_not_registered(self):
        """Test that a user cannot cancel registration if they haven't registered."""
        # Create an event selection without registering the user
        self.event_selection = EventSelection.objects.create(
            eventRef=self.event,
            name=self.event.getName(),
            date=self.event.getDate(),
            time=self.event.getTime(),
            numRegistered=0,
            description=self.event.getDescription(),
            capacity=self.event.getCapacity(),
            author=self.member_user
        )

        # Try canceling the registration
        url = f"/api/event/selection/register/cancel/{self.event_selection.id}/"
        response = self.client.put(url, {}, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {self.token_member}')

        # Should return an error because the user isn't registered
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
