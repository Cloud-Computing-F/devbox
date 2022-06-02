from pipes import Template
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf import settings

from contents.views import HomeView, RelationView

admin.site.site_header = "Fastgram Admin"
admin.site.site_title = "Fastgram Admin Site"
admin.site.index_title = "Hello everyone:)"


class NonUserTemplateView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            return redirect('contents_home')
        return super(NonUserTemplateView, self).dispatch(request, *args, **kwargs)
    

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeView.as_view(), name='contents_home'),
    path('login/', NonUserTemplateView.as_view(template_name='login.html'), name='login'),
    path('register/', NonUserTemplateView.as_view(template_name='register.html'), name='register'),
    path('relation/', RelationView.as_view(), name='contents_relation'),
    path('apis/', include('apis.urls')),

    path("home/", include('devbox.urls')),
]


urlpatterns += [
    path('accounts/', include('allauth.urls'))
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


