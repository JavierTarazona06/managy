# Generated by Django 5.1.2 on 2024-11-03 04:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='amenity',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amenity', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bookingamenity',
            name='amenities',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_obj', to='api.amenity'),
        ),
        migrations.AddField(
            model_name='bookingamenity',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_amenity', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='events',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='eventselection',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_selection', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='eventselection',
            name='eventRef',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventsRef', to='api.events'),
        ),
        migrations.AddField(
            model_name='eventselection',
            name='membersRegistered',
            field=models.ManyToManyField(related_name='event_selection_members', to='users.member'),
        ),
        migrations.AddField(
            model_name='note',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to=settings.AUTH_USER_MODEL),
        ),
    ]