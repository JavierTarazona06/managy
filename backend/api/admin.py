from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from users.models import Person
from django.contrib import admin
from users.models import Person, Member, Worker, Admin

class PersonAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'password', 'role', 'is_staff','id', 'is_superuser', 'created_at')
    list_filter = ('role', 'is_staff', 'is_superuser', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    fields = ('email', 'first_name','username', 'last_name', 'role', 'dob', 'telephone', 'is_staff', 'is_superuser', 'password')
    readonly_fields = ('created_at',)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:  # Editing an existing user
            return fieldsets
        return ((None, {'fields': (
        'email', 'first_name', 'last_name', 'role', 'dob', 'telephone', 'password', 'is_staff', 'is_superuser')}),)

    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new user
            obj.set_password(form.cleaned_data['password'])
        obj.save()
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = PersonAdmin.list_display
    search_fields = PersonAdmin.search_fields
@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = PersonAdmin.list_display + ('address',)
    search_fields = PersonAdmin.search_fields
@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = PersonAdmin.list_display + ('address',)
    search_fields = PersonAdmin.search_fields

admin.site.register(Person, PersonAdmin)

