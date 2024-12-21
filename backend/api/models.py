import datetime

from django.db import models
from django.core.validators import MinValueValidator
from datetime import date


class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('users.Person', on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return self.title


class Amenity(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    capacity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    occupied = models.BooleanField(default=False)
    member_user = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('users.Person', on_delete=models.CASCADE, related_name="amenity")
    image = models.TextField()

    def __str__(self):
        return self.name

    def getName(self):
        return self.name

    def isOccupied(self):
        return self.occupied

    def getCapacity(self):
        return self.capacity

    def getId(self):
        return self.id

    def getDescription(self):
        return self.description

    def canRegister(self):
        return (self.member_user == "") and not (self.isOccupied())

    def register(self, member_us):
        if (self.canRegister()):
            self.occupied = True
            self.member_user = str(member_us)
            print("Success:" + str(member_us))
        else:
            print("Can't register for this amenity")

    def release(self):
        self.occupied = False
        self.member_user = ""
        self.save()


class Events(models.Model):
    eventName = models.CharField(max_length=50)
    eventDescription = models.TextField()
    eventLocation = models.TextField()
    eventTime = models.TimeField()
    eventDate = models.DateField()
    eventCapacity = models.IntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('users.Person', on_delete=models.CASCADE, related_name="event")

    def __str__(self):
        return self.eventName

    def getName(self):
        return self.eventName

    def getDescription(self):
        return self.eventDescription

    def getDate(self):
        return self.eventDate

    def getCapacity(self):
        return self.eventCapacity

    def getTime(self):
        return self.eventTime

    def getId(self):
        return self.id

    def getEventDetails(self):
        return f"{self.eventName} {self.eventDescription} {self.eventLocation} {self.eventTime}"

    def isEventToday(self):
        return (date.today() == self.eventDate)


class Booking(models.Model):
    #booked_status = models.BooleanField(default=False)
    #date = models.TextField(default=None)
    #time_slot = models.TextField(default=None)
    author = models.ForeignKey('users.Person', on_delete=models.CASCADE, related_name="Booking")
    created_at = models.DateTimeField(auto_now_add=True)

    #def __str__(self):
    #    return self

    def isBooked(self):
        return self.booked_status

    class Meta:
        abstract = True


class BookingAmenity(Booking):
    amenities = models.ForeignKey(Amenity, on_delete=models.CASCADE, related_name="booking_obj")
    amenity_name = models.TextField()
    date = models.DateField(default=datetime.date.today)
    time = models.TimeField(default=datetime.time(12, 0))  # Default to 12:00 PM (noon)
    amenity_details = models.TextField()
    amenity_capacity = models.IntegerField(default=0)
    amenity_id = models.IntegerField(default=0)
    author = models.ForeignKey('users.Person', on_delete=models.CASCADE, related_name="booking_amenity")
    created_at = models.DateTimeField(auto_now_add=True)


class EventSelection(Booking):
    name = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    eventRef = models.ForeignKey(Events, on_delete=models.CASCADE, related_name="eventsRef")
    numRegistered = models.IntegerField()
    membersRegistered = models.ManyToManyField('users.Member', related_name="event_selection_members")
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('users.Person', on_delete=models.CASCADE, related_name="event_selection")

    def getMembers(self):
        return self.membersRegistered

    def isFull(self):
        return (self.membersRegistered.count()) == (self.capacity)

#-----------------------------------------------------------------------
#---------------- JAVIER - elr490 --------------------------------------
#-----------------------------------------------------------------------

class RecreationalVenue(models.Model):
    name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=50)
    photo = models.CharField(max_length=256)

    def get_info(self):
        mydict = {
            "name": self.name,
            "address": self.address,
            "photo": self.photo
        }
        return mydict

    def __str__(self):
        mystr = "Recreational Venue: " + self.name + "\n\tAddress: " + self.address
        return mystr


class Image(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=255)
    url = models.CharField()


class ExcelFile(models.Model):
    file = models.FileField()
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True)
