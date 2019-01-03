import random
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from PythonEcommerceProject.aws.utils import ProtectedS3Storage
#above FileSystemStorage will override the default file storage for any given field
from django.db import models
from django.db.models import Q
from PythonEcommerceProject.aws.download.utils import AWSDownload
from django.db.models.signals import pre_save, post_save
from PythonEcommerceProject.utils import unique_slug_generator, get_filename
from django.urls import reverse

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name , ext = os.path.splitext(base_name)
    return name,ext
# Create your models here.

def upload_image_path(instance, filename):
    # print(instance)
    # print(filename)
    new_filename = random.randint(1, 12312432)
    name, ext = get_filename_ext(filename)
    final_filename='{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "products/{new_filename}/{final_filename}".format(new_filename=new_filename,final_filename=final_filename)

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)
    def featured(self):
        return self.filter(featured=True, active=True)
    def search(self,query):
        lookups = Q(title__icontains=query)| Q(description__icontains=query) |Q(price__icontains=query)|Q(tag__title__icontains=query)
        #Q(tag__name__icontains=query)
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self): # if you want to call Product.objects.featured
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count()==1:
            return qs.first()
        return None

    def search(self,query):
        return self.get_queryset().active().search(query)


class Product(models.Model):
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price       = models.DecimalField(decimal_places=2, max_digits=20 , default=39.99)
    image       = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured    = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    is_digital  = models.BooleanField(default=False) # user library

    objects = ProductManager()
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return "/products/{slug}/".format(slug=self.slug)
        return reverse("products:detail", kwargs={"slug":self.slug})

    @property
    def name(self):
        return self.title

    def get_downloads(self):
        qs = self.productfile_set.all()
        return qs



def product_pre_save_receiver(sender , instance , *args , **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)


def upload_product_file_loc(instance, filename):
    slug = instance.product.slug
    id_ = instance.id
    print(instance.id)
    print(id_)
    if id_ is None:
        klass = instance.__class__
        qs = klass.objects.all().order_by('-pk')
        if qs.exists():
            id_ = qs.first().id +1
        else:
            id_=0
    if not slug:
        slug = unique_slug_generator(instance.product)
    location = 'product/{slug}/{id}/'.format(slug=slug, id=id_)
    return location + filename



class ProductFile(models.Model):
    product         = models.ForeignKey(Product)
    file            = models.FileField(upload_to= upload_product_file_loc, storage=ProtectedS3Storage()) #FileSystemStorage(location=settings.PROTECTED_ROOT))
    name            = models.CharField(max_length=120, null=True, blank=True)
    free            = models.BooleanField(default=False)
    user_required   = models.BooleanField(default=False)


    def __str__(self):
        return str(self.file.name)

    def get_default_url(self):
        return self.product.get_absolute_url()

    @property
    def display_name(self):
        og_name = get_filename(self.file.name)
        if self.name:
            return self.name
        return og_name

    def generate_download_url(self):
        bucket = getattr(settings, 'AWS_STORAGE_BUCKET_NAME')
        region = getattr(settings, 'S3DIRECT_REGION')
        access_key = getattr(settings, 'AWS_ACCESS_KEY_ID')
        secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY')
        if not secret_key or not access_key or not bucket or not region:
            return "/product-not-found/"
        PROTECTED_DIR_NAME = getattr(settings, 'PROTECTED_DIR_NAME', 'protected')
        path = "{base}/{file_path}".format(base=PROTECTED_DIR_NAME, file_path=str(self.file))
        aws_dl_object =  AWSDownload(access_key, secret_key, bucket, region)
        file_url = aws_dl_object.generate_url(path, new_filename=self.display_name)
        return file_url

    def get_download_url(self):
        return reverse("products:download", kwargs={"slug":self.product.slug, "pk":self.pk})

    # @property
    # def name(self):
    #     return self.display_name
    # because we have already a display name field and a property which is display_name
    # property is another field which is customized to bring different value when you call the original field name
    # so whenever you did a change in the property it means you're doing a change in the field it self so you have to do the migrations again
