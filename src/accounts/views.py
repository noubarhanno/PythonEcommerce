from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login,get_user_model
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView
from django.http import HttpResponse
from django.shortcuts import render , redirect
from .forms import LoginForm , RegisterForm , GuestForm, ReactivateEmailForm, UserDetailChangeForm
from django.views.generic.edit import FormMixin
from django.utils.http import is_safe_url
from accounts.models import GuestEmail, EmailActivation
from .signals import user_logged_in
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from PythonEcommerceProject.mixins import NextUrlMixin, RequestFormAttachMixin
# Create your views here.

# the login required below is a function baased view

# automatically goes to /accounts/login/?next=/some/path
# @login_required
# def account_home_view(request):
#     return render(request, 'accounts/home.html', {})

# class LoginRequiredMixin(object):
#         @method_decorator(login_required)
#         def dispatch(self, *args, **kwargs):
#             return super(LoginRequiredMixin,self).dispatch(self, *args, **kwargs)

class AccountHomeView(LoginRequiredMixin,DetailView):
    template_name= 'accounts/home.html'
    def get_object(self):
        return self.request.user

class AccountEmailActivationView(FormMixin,View):
    success_url = '/login/'
    form_class = ReactivateEmailForm
    key = None
    def get(self,request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirmed_qs = qs.confirmable()
            if confirmed_qs.count() == 1:
                obj = confirmed_qs.first()
                obj.activate()
                messages.success(request, "your mail has been confirmed please login")
                return redirect('login')
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse('password_reset')
                    msg="""Your Email is already activated
                    do you want to <a href='{link}'>reset your password?</a>
                    """.format(link=reset_link)
                    messages.success(request, mark_safe(msg))
                    return redirect('login')
        print(self.key)
        context = {'form' : self.get_form(), 'key': self.key}
        return render(request, 'registration/activation-error.html', context)

    def post(self,reuqest, *args, **kwargs):
        # create form to recieve an email for activation
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    def form_valid(self,form):
        request = self.request
        msg="""Activation Link is sent , please check your email."""
        messages.success(request, msg)
        email = form.cleaned_data.get('email')
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super(AccountEmailActivationView, self).form_valid(form)

    def form_invalid(self, form):
        context = {'form' : form, 'key' :self.key}
        return render(self.request, 'registration/activation-error.html', context)



# def guest_register_view(request):
#     form_class = GuestForm(request.POST or None)
#     context = {
#         "form":form_class
#     }
#     next_ = request.GET.get('next')
#     print(next_)
#     next_post = request.POST.get('next')
#     print(next_post)
#     redirect_path = next_ or next_post or None
#     if form_class.is_valid():
#         print(form_class.cleaned_data)
#         email    = form_class.cleaned_data.get("email")
#         new_guest_email = GuestEmail.objects.create(email=email)
#         request.session["guest_email_id"]=new_guest_email.id
#         if is_safe_url(redirect_path, request.get_host()):
#             return redirect(redirect_path)
#         else:
#             # context['form'] = LoginForm
#             return redirect('/register/')
#     return redirect("/register/")

class GuestRegisterView(NextUrlMixin,RequestFormAttachMixin, CreateView):
    form_class = GuestForm
    default_next = '/register/'

    def get_success_url(self):
        return self.get_next_url()

    def form_invalid(self, form):
        return redirect(self.default_next)

    # def form_valid(self, form):
    #     request = self.request
    #     email    = form.cleaned_data.get("email")
    #     new_guest_email = GuestEmail.objects.create(email=email)
    #
    #     return redirect(self.get_next_url())


class LoginView(NextUrlMixin,RequestFormAttachMixin,FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'
    default_next = '/'

    def form_valid(self, form): #form_valid is built in method should be defined
        next_url = self.get_next_url()
        return redirect(next_url)



class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login/'


class UserDetailUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserDetailChangeForm
    template_name = 'accounts/detail-update-view.html'
    # success_url = 'account'  this is could do the same as get_success_url

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Change your account Details'
        return context

    def get_success_url(self):
        return reverse('account:home')

# User = get_user_model()
# def register_page(request):
#     form_class = RegisterForm(request.POST or None)
#     context={
#         "form":form_class
#     }
#     if form_class.is_valid():
#         form.save()
#     return render(request , "accounts/register.html", context)
        # we did up instead of the code down because the RegisterForm is ModelForm

        # print(form_class.cleaned_data)
        # username = form_class.cleaned_data.get('username')
        # email = form_class.cleaned_data.get('email')
        # password = form_class.cleaned_data.get('password')
        # new_user = User.objects.create_user(username,email,password)
        # print(new_user)
