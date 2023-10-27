from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
import os
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, filters
from IPython.display import Image

from .serializers import ProductSerializer, ReviewSerializer
from .models import Product, Review
from .services import rake_extract, get_kw, col_to_string, sample_extractive_summarization, authenticate_client, \
    getRatingStatsService, word_frequency

from .bi import aspectBI, ratingBI

'''
    Product model views
'''


class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class searchProductByName(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


@api_view(['GET'])
def searchProductByName1(request, keyword, pageNumber, pageSize):
    if keyword == '*':
        queryset = Product.objects.all()
    else:
        queryset = Product.objects.filter(name__icontains=keyword)
    result = queryset[pageSize * (pageNumber - 1):pageNumber * pageSize]
    serializer = ProductSerializer(result, many=True)
    new = list(serializer.data)
    new.append({'total': len(queryset)})
    return Response(new)

# BI
@api_view(['GET'])
def getRatingBI(request, productId):
    reviews = Review.objects.filter(product=productId)
    ratings = [e.rating for e in reviews]
    dic = ratingBI(ratings)
    return Response(dic)


@api_view(['GET'])
def getAspectBI(request, productId):
    reviews = Review.objects.filter(product=productId)
    texts = [e.text for e in reviews]
    dic = aspectBI(texts)
    return Response(dic)


@api_view(['GET'])
def getProductById(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


'''
    Review model views
'''


class ReviewView(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


@api_view(['GET'])
def getReviewsByProductId(request, productId):
    reviews = Review.objects.filter(product=productId)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getReviewsByKeyword(request, productId, keyword):
    reviews = Review.objects.filter(product=productId)
    keyword_reviews = reviews.filter(text__icontains=keyword)
    serializer = ReviewSerializer(keyword_reviews, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def getKeywordsByProductId(request, productId):
    reviews = Review.objects.filter(product=productId)
    review_string = ' '.join([str(i.text) for i in reviews])
    kw = get_kw(review_string)

    return Response(kw)


client = authenticate_client()


@api_view(['GET'])
def getSummaryByProductId(request, productId):
    reviews = Review.objects.filter(product=productId)
    review_string = ' '.join([str(i.text) for i in reviews])
    summary = sample_extractive_summarization(client, review_string)

    return Response(summary)


## Response visualization image
@api_view(['GET'])
def getRatingStats(request, productId):
    return Response(getRatingStatsService(productId))


def getFeatureVisualByProductId(request, productId):
    res = word_frequency(productId)
    return JsonResponse(res)
