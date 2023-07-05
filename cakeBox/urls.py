"""cakeBox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from myapp import views as api_views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("api/cakes",api_views.CakesView,basename="cakes")

router.register("api/v1/cakes",api_views.CakeViewsetView,basename="ccakes")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("cakes/add/",views.CakeCreateView.as_view(),name="cake-add"),
    path("cakes/all/",views.CakeListView.as_view(),name="cake-list"),
    path("cakes/<int:pk>",views.CakeDetailView.as_view(),name="cake-detail"),
    path("cakes/<int:pk>/change/",views.CakeEditView.as_view(),name="cake-edit"),
    path("cakes/<int:pk>/remove/",views.CakeDeleteView.as_view(),name="cake-delete"),
    path("register/",views.SignUpView.as_view(),name="register"),
    path("login/",views.SignInView.as_view(),name="signin"),
    path("logout/",views.signout_view,name="signout"),
    


]+router.urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
