from django.contrib import admin
from .models import Entries
# Register your models here.


class EntriesAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


admin.site.register(Entries, EntriesAdmin)