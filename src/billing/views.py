from django.conf import settings
from django.shortcuts import render , redirect
from django.http import JsonResponse, HttpResponse
from django.utils.http import is_safe_url
import stripe

from .models import BillingProfile, Card

STRIP_SECRET_KEY = getattr(settings, "STRIP_SECRET_KEY",'sk_test_dcQwZSOCpgPbOkLHaStIMRIs')
STRIPE_PUB_KEY= getattr(settings, "STRIPE_PUB_KEY",'pk_test_dIXXyNLLFIHbCRidgDWEiSOL')
stripe.api_key = STRIP_SECRET_KEY

def payment_method_view(request):
    #next_url
    # if request.user.is_authenticated:
    #     billing_profile = request.user.billingprofile
    #     my_customer_id = billing_profile.customer_id

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect('/cart/')
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'billing/payment-method.html',{"publish_key":STRIPE_PUB_KEY, 'next_url':next_url})


def payment_method_createview(request):
    if request.method=="POST" and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({"message":"Cannot find this user"},status_code=401)
        # if we didn't know what the data comming from the POST so just print(request.POST)
        token = request.POST.get("token")
        # token is coming from the POST , need to check
        if token is not None:
            new_card_obj = Card.objects.add_new(billing_profile, token)
            # to see how to store our card in our database too
        return JsonResponse({"message":"Success , your card is added!"})
    return HttpResponse("error",status_code=401)
