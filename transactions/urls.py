from django.urls import path

from . import views

urlpatterns = [

    path('trnsaction', views.TransactionView.as_view()),
    path('cachedTrnsaction', views.CachedTransactionView.as_view()),

]