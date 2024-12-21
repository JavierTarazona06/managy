from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework import serializers
from .models import Note, Amenity, Events, BookingAmenity, EventSelection, RecreationalVenue
from .models import Image, ExcelFile
from users.models import Member


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        # No one can read the password
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        #print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "author"]
        extra_kwargs = {"author": {"read_only": True}}


class AmenitySerializer(serializers.ModelSerializer):
    #name = serializers.CharField(max_length=50)
    #description = serializers.CharField()
    #capacity = serializers.IntegerField(default=1, validators=[MinValueValidator(1)])
    occupied = serializers.BooleanField(default=False, read_only=True)
    member_user = serializers.CharField(read_only=True)

    #image = serializers.CharField()
    class Meta:
        model = Amenity
        fields = ["id", "name", "description", "capacity", "occupied", "image", "member_user", "created_at", "author"]
        extra_kwargs = {"author": {"read_only": True}, "member_user": {"read_only": True}}

    def update_amenity(self, instance, validated_data):
        member_user = validated_data.get('member_user', instance.member_user)
        status = validated_data.get('occupied', instance.member_user)

        if 'member_user' in validated_data:
            #if instance.canRegister():
            instance.member_user = str(member_user)
            instance.occupied = status
            #print("Success")
            #else:
            #    print("Can't register")
        instance.save()
        return instance


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ["id", "eventName", "eventDescription",
                  "eventLocation", "eventCapacity",
                  "eventTime", "eventDate",
                  "created_at", "author"]
        extra_kwargs = {"author": {"read_only": True}}


class BookingAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingAmenity
        fields = ['amenities', 'time', 'date',
                  'amenity_details', 'amenity_capacity',
                  'author', 'id', 'created_at']
        extra_kwargs = {"author": {"read_only": True}}

    def create(self, validated_data):
        amenity = validated_data.pop('amenities', None)
        booking_amenity = BookingAmenity(
            amenities=amenity,
            amenity_name=amenity.getName(),
            time=validated_data['time'],
            date=validated_data['date'],
            amenity_details=validated_data['amenity_details'],
            amenity_capacity=validated_data['amenity_capacity'],
            amenity_id=amenity.id,
            author=validated_data['author'],
        )
        booking_amenity.save()
        amenity_serial = AmenitySerializer()
        amenity_serial.update_amenity(amenity, {'member_user': str(booking_amenity.author), 'occupied': True})
        return booking_amenity


class BookingAmenityUpdate(serializers.ModelSerializer):
    class Meta:
        model = BookingAmenity
        fields = ['amenities', 'time', 'date',
                  'amenity_details', 'amenity_capacity',
                  'author', 'id', 'created_at']
        extra_kwargs = {
            "amenities": {"read_only": True},
            "author": {"read_only": True},
            "id": {"read_only": True},
            "created_at": {"read_only": True},
        }


class BookingAmenitySerializerView(serializers.ModelSerializer):
    class Meta:
        model = BookingAmenity
        fields = ['amenity_name', 'amenity_details',
                  'amenity_capacity', 'amenity_id',
                  'time', 'date', 'id']


class EventSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventSelection
        fields = ['eventRef', 'created_at', 'author', 'id']
        extra_kwargs = {"author": {"read_only": True}, "numRegistered": {"read_only": True},
                        "membersRegistered": {"read_only": True}}

    def create(self, validated_data):
        events = validated_data.pop('eventRef', None)

        eventSelection = EventSelection(
            eventRef=events,
            name=events.getName(),
            date=events.getDate(),
            time=events.getTime(),
            numRegistered=1,
            description=events.getDescription(),
            capacity=events.getCapacity(),
            author=validated_data['author']
        )
        eventSelection.save()
        return eventSelection


class EventSelectionSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = EventSelection
        fields = ['numRegistered', 'membersRegistered']
        extra_kwargs = {"numRegistered": {"read_only": True}, "membersRegistered": {"read_only": True}}

    def validate(self, value):
        member = self.context['request'].user
        event_selection = self.instance
        if (self.context.get('action') == 'register'):
            if event_selection.membersRegistered.filter(id=member.id).exists():
                raise serializers.ValidationError("You are already registered for this event.")
        elif (self.context.get('action') == 'cancel'):
            if not (event_selection.membersRegistered.filter(id=member.id).exists()):
                raise serializers.ValidationError("You are not registered for this event.")
        return value

    def update(self, instance, validated_data):
        #members = validated_data.pop('member', None)
        try:
            member_id = self.context['request'].user
            member = Member.objects.get(id=member_id.id)

        except Member.DoesNotExist:
            raise serializers.ValidationError("Member does not exist.")
        #print("Test")

        if (self.context.get('action') == 'register'):
            if member and not (instance.isFull()):
                instance.membersRegistered.add(member)
                instance.numRegistered += 1
        elif self.context.get('action') == 'cancel':
            if member and not (instance.isFull()):
                instance.membersRegistered.remove(member)
                instance.numRegistered -= 1
        instance.save()
        return instance


class EventSelectionSerializerView(serializers.ModelSerializer):
    class Meta:
        model = EventSelection
        fields = ['name', 'date', 'description', 'capacity', 'numRegistered', 'membersRegistered', 'created_at', 'id',
                  'author']


#-----------------------------------------------------------------------
#---------------- JAVIER - elr490 --------------------------------------
#-----------------------------------------------------------------------


class RecreationalVenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecreationalVenue
        fields = '__all__'


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image', 'title', 'url']
        extra_kwargs = {
            "url": {"read_only": True},
            "image": {"write_only": True},
            "title": {"write_only": True}
        }


class ExcelUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcelFile
        fields = ['file', 'title', 'url']
        extra_kwargs = {
            "url": {"read_only": True},
            "file": {"write_only": True},
            "title": {"write_only": True}
        }