from django.conf.urls import url

from products.views import (
                        ProductListView,
                        #Product_list_view,
                        #ProductDetailView,
                        ProductDetailSlugView,
                        ProductDownloadView,
                        #Product_detail_view,
                        #ProductFeaturedDetailView,
                        #ProductFeaturedListView
                        )

urlpatterns = [
    url(r'^$',ProductListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$',ProductDetailSlugView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/(?P<pk>\d+)/$',ProductDownloadView.as_view(), name='download'),
]
