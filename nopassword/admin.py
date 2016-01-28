from django.contrib import admin

from .models import LoginCode

class LoginCodeAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'code', 'timestamp', 'next',)
    search_fields = ('user',)

admin.site.register(LoginCode, LoginCodeAdmin)
