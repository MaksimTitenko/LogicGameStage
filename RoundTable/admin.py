from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, TeamMod, UserInTeam, Invite, Question, ListOffset, QuestionTopic, GameSession
from django import forms


class ModelFormUser(forms.ModelForm):

    def save(self, commit=True):
        return super(ModelFormUser, self).save(commit=commit)

    class Meta:
        fields = '__all__'
        model = User


class QuestionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class CustomUserAdmin(UserAdmin):
    form = ModelFormUser

    list_display = ('username', 'last_name', 'first_name', 'middle_name', 'email', 'is_staff', 'is_superuser')

    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'first_name', 'last_name', 'middle_name',
                       'gender', 'date_birth', 'phone', 'avatar',
                       'bio')
        }),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(User, CustomUserAdmin)
admin.site.register(ListOffset)
admin.site.register(QuestionTopic)
admin.site.register(Question, QuestionAdmin)
admin.site.register(TeamMod)
admin.site.register(UserInTeam)
admin.site.register(Invite)
admin.site.register(GameSession)