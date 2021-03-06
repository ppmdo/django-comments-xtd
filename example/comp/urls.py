import django
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

if django.VERSION[:2] > (1, 9):
    from django.views.i18n import JavaScriptCatalog
else:
    from django.views.i18n import javascript_catalog
    
from django_comments_xtd import LatestCommentFeed
from django_comments_xtd.views import XtdCommentListView

from comp import views


admin.autodiscover()


urlpatterns = [
    url(r'^$', views.HomepageView.as_view(), name='homepage'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^articles/', include('comp.articles.urls')),
    url(r'^quotes/', include('comp.extra.quotes.urls')),
    url(r'^comments/', include('django_comments_xtd.urls')),
    url(r'^comments/$', XtdCommentListView.as_view(
        content_types=["articles.article", "quotes.quote"],
        paginate_by=10, page_range=5),
        name='comments-xtd-list'),
    url(r'^feeds/comments/$', LatestCommentFeed(), name='comments-feed'),    
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]

if django.VERSION[:2] > (1, 9):
    urlpatterns.extend([
        url(r'^jsi18n/$', JavaScriptCatalog.as_view(),
            name='javascript-catalog'),
        url(r'admin/', admin.site.urls),
    ])
else:
    js_info_dict = {
        'packages': ('django_comments_xtd',)
    }
    urlpatterns.extend([
        url(r'^jsi18n/$', javascript_catalog, js_info_dict,
            name='javascript-catalog'),
        url(r'^admin/', include(admin.site.urls)),
    ])

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [url(r'^rosetta/', include('rosetta.urls'))]
