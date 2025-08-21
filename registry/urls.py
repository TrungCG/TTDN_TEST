from django.urls import path

from . import views

urlpatterns = [
    path('provinces/', views.ProvinceList.as_view(), name='province-list'),
    path('commune-current/', views.CommuneCurrentSearch.as_view(), name='commune-current-search'),
    path('commune-old/', views.CommuneOldSearch.as_view(), name='commune-old-search'),
    path('mergers/', views.MergerList.as_view(), name='merger-list'),
    # path('districts/', views.DistrictList.as_view(), name='district-list'),
    path("", views.search_view, name="search"),
    # path("commune-search/", views.search_view, name="commune-search"),
]