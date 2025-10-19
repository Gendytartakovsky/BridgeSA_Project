from rest_framework.routers import DefaultRouter
from .views import DocumentSubmissionViewSet, submission_pdf
from django.urls import path

# Router for the standard CRUD operations
router = DefaultRouter()
router.register(r'submissions', DocumentSubmissionViewSet, basename='submission')

# Combine router URLs with custom PDF endpoint
urlpatterns = router.urls + [
    path('submissions/<int:pk>/pdf/', submission_pdf, name='submission-pdf'),
]
