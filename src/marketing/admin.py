from django.contrib import admin
from .models import MarketingPreference


class MarketingPreferenceAdmin(admin.ModelAdmin):

    list_display = ['__str__', 'subscribed', 'update']
    # to list the Columns when you enter the model in admin 
    readonly_fields = ['mailchimp_msg','mailchimp_subscribe', 'timestamp' , 'update']
    class Meta:
        model = MarketingPreference
        fields = ['user' , 'subscribed', 'mailchimp_msg','mailchimp_subscribe', 'timestamp', 'update']

admin.site.register(MarketingPreference, MarketingPreferenceAdmin)
