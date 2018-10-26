from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserAccount, TeamMod, UserInTeam
from django import forms


class ModelFormUser(forms.ModelForm):

    def save(self, commit=True):
        return super(ModelFormUser, self).save(commit=commit)

    class Meta:
        fields = '__all__'
        model = User


class CustomUserAdmin(UserAdmin):
    form = ModelFormUser

    list_display = ('username', 'last_name', 'first_name', 'middle_name', 'email', 'is_staff', 'is_superuser')

    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'first_name', 'last_name', 'middle_name',
                       'gender', 'date_birth', 'phone', 'country', 'city', 'avatar',
                       'bio')
        }),
    )

    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('username', 'email', 'password1', 'password2', 'is_stuff', 'is_superuser')
    #     })
    # )

    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserAccount)
admin.site.register(TeamMod)
admin.site.register(UserInTeam)
