from django.shortcuts import render , get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
# Create your views here.
from analytics.mixins import ObjectViewedMixin
from carts.models import Cart
from .models import Product, ProductFile

class ProductFeaturedListView(ListView):
    template_name = "products/list.html"

    def get_queryset(self , *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()

class ProductDetailSlugView(ObjectViewedMixin,DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args,**kwargs)
        cart_obj, new_obj=Cart.objects.new_or_get(self.request)
        context['cart']=cart_obj
        print(cart_obj)
        return context

    def get_object(self ,*args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        # instance = get_object_or_404(Product,slug=slug, active=True)
        try:
            instance = Product.objects.get(slug=slug, active = True)
        except Product.DoesNotExist:
            raise Http404("not found..")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Huhh")
        # object_viewed_signal.send(instance.__class__, instance=instance , request=request)
        return instance

class ProductFeaturedDetailView(ObjectViewedMixin,DetailView):
    # queryset = Product.objects.all()
    template_name = "products/featured-detail.html"

    def get_queryset(self, *args , **kwargs):
        request = self.request
        return Product.objects.all().featured()


class UserProductHistoryView(LoginRequiredMixin, ListView):
    # queryset = Product.objects.all()
    template_name = "products/user-history.html" #another way
    # template_name = "products/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView,self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context
    def get_context_data(self, *args, **kwargs):
        context = super(UserProductHistoryView, self).get_context_data(*args,**kwargs)
        cart_obj, new_obj=Cart.objects.new_or_get(self.request)
        context['cart']=cart_obj
        print(cart_obj)
        return context

    def get_queryset(self , *args, **kwargs):
        request = self.request
        # views = request.user.objectviewed_set.by_model(Product, model_queryset=False) #all().filter(content_type='product')
        views = request.user.objectviewed_set.by_model(Product, model_queryset=False)[:3] #only three
        # viewed_ids = [x.object_id for x in views]
        # Products.objects.filter(pk__in=viewed_ids)
        return views
        # print(viewed_ids)


class ProductListView(ListView):
    # queryset = Product.objects.all()
    template_name = "products/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView,self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context
    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args,**kwargs)
        cart_obj, new_obj=Cart.objects.new_or_get(self.request)
        context['cart']=cart_obj
        print(cart_obj)
        return context

    def get_queryset(self , *args, **kwargs):
        request = self.request
        return Product.objects.all()

        # this is should be written in every class based view in order to know the context of the class based view


def Product_list_view(request):
    queryset= Product.objects.all()
    context = {
        'object_list' : queryset
    }
    return render(request,"products/list.html",context)

import os
from wsgiref.util import FileWrapper # this used in django not python
from django.conf import settings
from mimetypes import guess_type
from orders.models import ProductPurchase

class ProductDownloadView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        pk = kwargs.get('pk')
        downloads_qs = ProductFile.objects.filter(pk=pk, product__slug=slug)
        if downloads_qs.count() != 1:
            raise Http404("Download not found")
        download_obj = downloads_qs.first()
        # permission checks

        can_download = False
        user_ready  = True
        if download_obj.user_required:
            if not request.user.is_authenticated():
                user_ready = False

        purchased_products = Product.objects.none()
        if download_obj.free:
            can_download = True
            user_ready = True
        else:
            # not free
            purchased_products = ProductPurchase.objects.products_by_request(request)
            if download_obj.product in purchased_products:
                can_download = True
        if not can_download or not user_ready:
            messages.error(request, "You do not have access to download this item")
            return redirect(download_obj.get_default_url())

        aws_filepath = download_obj.generate_download_url()
        print(aws_filepath)
        return HttpResponseRedirect(aws_filepath)
        # file_root = settings.PROTECTED_ROOT
        # filepath = download_obj.file.path # .url has /media/ in it
        # final_filepath = os.path.join(file_root, filepath) # where the file is stored
        # with open(final_filepath, 'rb') as f:
        #     wrapper = FileWrapper(f)
        #     mimetype = 'application/dorce-download'
        #     guessed_mimetype = guess_type(filepath)[0] # filename.mp4
        #     if guessed_mimetype:
        #         mimetype = guessed_mimetype
        #     response = HttpResponse(wrapper, content_type='text/plain')
        #     response['Content-Disposition'] = "attachment;filename=%s" %(download_obj.name)
        #     response['X-SendFile'] = str(download_obj.name)
        #     return response
        # return redirect(download_obj.get_default_url()) # we have to create get_default_url

class ProductDetailView(ObjectViewedMixin,DetailView):
    # queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView,self).get_context_data(*args, **kwargs)
        print(context)
        # context['abc']=123
        # the line above is tell us that we can add a context value like the normal view function as the function below
        return context

    def get_object(self ,*args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product is not exist")
        return instance

        # this is should be written in every class based view in order to know the context of the class based view


def Product_detail_view(request, pk, *args , **kwargs):
    # instance = Product.objects.get(pk=pk)
    # instance = get_object_or_404(Product,pk=pk)
    # try:
    #     instance= Product.objects.get(id=pk)
    # except Product.DoesNotExist:
    #     print('no products here')
    #     raise Http404('Products does not exist')
    # except:
    #     print('huh')
    #
    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Product is not exist")
    # print(instance)
    # qs = Product.objects.filter(id=pk)
    # # print(qs)
    # if qs.exists() and qs.count()==1:
    #     instance = qs.first()
    # else:
    #     raise Http404("products doen't exist")
    context = {
        'object' : instance
        # 'abc':123
    }
    return render(request,"products/detail.html",context)
