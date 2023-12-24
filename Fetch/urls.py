from .views import ArchiveList, ArchiveListLT, ArchiveCreate
from django.urls import path

urlpatterns = [
    path('', ArchiveList.as_view()),
    path('last-ten/', ArchiveListLT.as_view()),
    path('create/', ArchiveCreate.as_view()),
]
