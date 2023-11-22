from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views.book import BookViewSet, BookInstancePhotoViewSet
from .views.borrow import BorrowedBookViewSet
from .bot import webhook


router = DefaultRouter()

router.register('books', BookViewSet)
router.register('photos', BookInstancePhotoViewSet)
router.register('borrow', BorrowedBookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('request/', webhook),
    
]
