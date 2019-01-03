from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .mixins import CsrfExemptMixin
from .utils import Mailchimp
from .forms import MarketingPreferenceForm
from .models import MarketingPreference
from django.views.generic import UpdateView, View

class MarketingPreferenceUpdateView(SuccessMessageMixin, UpdateView):
    form_class = MarketingPreferenceForm # required and built in
    template_name = 'base/forms.html' # yeah create this
    success_url = '/settings/email/'
    success_message = 'your email preferences has have been updated. Thank You'

    # the success_message is build in variable when you import SuccessMessageMixin - there is also a form for this message exist in the documentation


    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated():
            return redirect("/login/?next=/settings/email/")#HttpResponse("not Allowed", status=400)
        return super(MarketingPreferenceUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MarketingPreferenceUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Email Preferences'
        return context
        # without the Part above of the get_context_data the title will not appear in the form

        # get_context_data and dispatch is built in method you can customize as you want
        # in this example when we go to the get_object to subscribe or unsubscribe the Email it will give error if the user is not authenticated
        # dispatch will let us do something before we reach the actual get_object method

    def get_object(self):
        user = self.request.user
        obj, created = MarketingPreference.objects.get_or_create(user=user) # get_absolute_url
        return obj




"""

POST METHOD
data[email]: noubar@gmail.com

data[email_type]: html

data[merges][FNAME]:

data[merges][BIRTHDAY]:

fired_at: 2018-10-24 12:03:03

data[reason]: manual

data[merges][EMAIL]: noubar@gmail.com

data[web_id]: 39148937

data[merges][LNAME]:

data[merges][PHONE]:

data[list_id]: ce0e9dc684

data[ip_opt]: 5.107.56.24

data[action]: unsub

data[merges][ADDRESS]:

data[id]: 9be3bdaf2e

type: unsubscribe

"""

class MailchimpWebhookView(CsrfExemptMixin, View):
    # with adding the CsrfExemptMixin now mailchimp can post data to us , without it it cannot
    # because any post need to have csrf then we need to create mixin.py check the code inside
    # def get(self,request, *args, **kwargs):
    #     return HttpResponse('thank you', status=200)
    def post(self,request, *args, **kwargs):
        data = request.POST
        list_id = data.get('data[list_id]')
        if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
            hook_type = data.get("type")
            email = data.get('data[email]')
            response_status, response = Mailchimp().check_subscription_status(email)
            sub_status = response['status']
            is_subbed = None
            mailchimp_subbed = None
            if sub_status=="subscribed":
                is_subbed, mailchimp_subbed = (True, True)
            elif sub_status=="unsubscribed":
                is_subbed, mailchimp_subbed = (False, False)
            if is_subbed is not None and mailchimp_subbed is not None:
                qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(subscribed=is_subbed,
                            mailchimp_subscribe=mailchimp_subbed,
                            mailchimp_msg=str(data)
                            )

        return HttpResponse("Thank you", status=200)

# def mailchimp_webhook_view(request):
#     data = request.POST
#     list_id = data.get('data[list_id]')
#     if str(list_id) = str(MAILCHIMP_EMAIL_LIST_ID):
#         hook_type = data.get("type")
#         email = data.get('data[email]')
#         response_status, response = Mailchimp().check_subscription_status(email)
#         sub_status = response['status']
#         if sub_status == "subscribed":
#             qs = MarketingPreference.objects.filter(user__email__iexact=email)
#             if qs.exists():
#                 qs.update(subscribed=True,mailchimp_subscribe=True, mailchimp_msg=str(data))
#         elif sub_status == "unsubscribed":
#             qs = MarketingPreference.objects.filter(user__email__iexact=email)
#             if qs.exists():
#                 qs.update(subscribed=False, mailchimp_subscribe=False, mailchimp_msg=str(data))
#
#     return HttpResponse("Thank you", status=200)
