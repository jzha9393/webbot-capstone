"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from webbot import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductView, 'product')
router.register(r'reviews', views.ReviewView, 'review')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/products', views.searchProductByName.as_view()),
    path('api/products/<str:keyword>/<int:pageNumber>/<int:pageSize>', views.searchProductByName1),
    path('api/getProductById/<str:id>/', views.getProductById),
    path('api/getReviewsByProductId/<str:productId>/', views.getReviewsByProductId),
    path('api/getReviewsByKeyword/<str:productId>/<str:keyword>/', views.getReviewsByKeyword),
    path('api/getKeywordsByProductId/<str:productId>/', views.getKeywordsByProductId),
    path('api/getSummaryByProductId/<str:productId>/', views.getSummaryByProductId),
    path('api/getRatingStats/<str:productId>/', views.getRatingStats),
    path('api/getFeatureVisualByProductId/<str:productId>/', views.getFeatureVisualByProductId),
    path('api/getRatingBI/<str:productId>/', views.getRatingBI),
    path('api/getAspectBI/<str:productId>/', views.getAspectBI),
]
