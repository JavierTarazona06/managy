from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models import Q
from api.models import Events,Amenity


from .utils import RandomString


class PersonManager(BaseUserManager):
    def create_user(self, **extra_fields):
        extra_fields["email"] = self.normalize_email(extra_fields["email"])
        user = self.model(**extra_fields)
        user.set_password(extra_fields["password"])
        user.save(using=self._db)
        return user

    def create_superuser(self, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(**extra_fields)

    def delete_user(self, user):
        user.delete()


class Person(AbstractUser):
    ROLES = [
        ('member', 'Member'),
        ('worker', 'Worker'),
        ('admin', 'Admin')
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLES, default='member')
    dob = models.DateField(null=True)
    telephone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    recreational_venue = models.ManyToManyField('api.RecreationalVenue', related_name="persons")
    objects = PersonManager()

    def getInfo(self):
        return [str(self.user.id), str(self.name), str(self.last_name), str(self.email), str(self.dob),
                str(self.telephone), str(self.role)]

    def getId(self):
        return self.id

    #def delete(self):
    #def updateInfo(self):


class Member(Person):
    events = models.ManyToManyField('api.EventSelection', related_name="event_booking")
    amenities = models.ManyToManyField('api.BookingAmenity', related_name="booking_amenity")

    @classmethod
    def create_member(cls, **extra_fields):
        extra_fields.setdefault('role', 'member')
        return cls.objects.create_user(**extra_fields)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

    def getAmenity(self, id):
        try:
            amenity = Amenity.objects.get(id=id)
            return amenity
        except Exception as e:
            ValueError("Error Amenity doesn't exist: "+str(e))
            return None
    def getEventList(cls):
        return Events.objects.all()

    def getEvent(self,id):
        try:
            event=Events.objects.get(id=id)
            return event
        except self.models.DoesNotExist:
            ValueError("Error Amenity doesn't exist")
            return None

    #def cancelEvent(self,id):
    #def registerAmenity(self):


class Worker(Person):
    address = models.TextField()

    @classmethod
    def create_worker(cls, **extra_fields):
        extra_fields.setdefault('role', 'worker')
        extra_fields.setdefault('password', RandomString(20))
        return cls.objects.create_user(**extra_fields)

    @classmethod
    def viewEvents(cls):
        return Events.objects.all()

    def getAmenity(self,id):
        try:
            amenity = Amenity.objects.get(id=id)
            return amenity
        except self.models.DoesNotExist:
            ValueError("Amenity doesn't exist")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"


class Admin(Person):
    address = models.TextField()

    @classmethod
    def create_admin(cls, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields['username'] = extra_fields['email']
        return cls.objects.create_superuser(**extra_fields)

    def create_person(**extra_fields):
        extra_fields['username'] = extra_fields["email"]
        if (extra_fields["role"] == 'member'):
            extra_fields.setdefault('password', RandomString(20))
            return Member.create_member(**extra_fields)
        elif (extra_fields["role"] == 'worker'):
            extra_fields.setdefault('password', RandomString(20))
            return Worker.create_worker(**extra_fields)
        elif (extra_fields["role"] == 'admin'):
            return Admin.create_admin(extra_fields["email"], **extra_fields)
        else:
            pass

    def find_person(id=None, name=None, role=None, email=None):
        filters = Q()
        if id is not None and id != 0:
            filters |= Q(id=id)
        if name is not None and name != "Null":
            filters |= Q(first_name__icontains=name)
        if role is not None and role != "Null":
            filters |= Q(role__icontains=role)
        if email is not None and email != "Null":
            filters |= Q(email__icontains=email)
        return Person.objects.filter(filters)

    def getInfo(self):
        return super().getInfo() + [str(self.recreational_venue)]

    def delete_person(self, user_id):
        try:
            user = Person.objects.get(id=user_id)
            #self._delete_user(user)
            user.delete()
        except self.models.DoesNotExist:
            raise ValueError("User Not found")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"



class PasswordReset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)