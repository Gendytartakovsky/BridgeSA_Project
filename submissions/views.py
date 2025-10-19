from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import DocumentSubmission
from .serializers import DocumentSubmissionSerializer
import random, string

# ---------------------------
# ViewSet for CRUD operations
# ---------------------------
class DocumentSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Enable search and ordering
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['submitted_at', 'title']
    ordering = ['-submitted_at']

    def get_queryset(self):
        # Each user only sees their own submissions
        return DocumentSubmission.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Generate a random reference code automatically
        ref_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        serializer.save(user=self.request.user, reference_code=ref_code)

    # ---------------------------
    # Custom action to toggle status
    # ---------------------------
    @action(
        detail=True,
        methods=['post'],
        url_path='toggle-status',
        url_name='toggle_status',
        permission_classes=[permissions.IsAuthenticated],
        description="Toggle submission status (complete/incomplete)"
    )
    def toggle_status(self, request, pk=None):
        submission = self.get_object()
        submission.status = not submission.status
        submission.save()
        return Response(
            {
                "id": submission.id,
                "title": submission.title,
                "status": submission.status
            },
            status=status.HTTP_200_OK
        )


# ---------------------------
# Endpoint to generate PDF
# ---------------------------
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def submission_pdf(request, pk):
    try:
        submission = DocumentSubmission.objects.get(pk=pk, user=request.user)
    except DocumentSubmission.DoesNotExist:
        return HttpResponse("Submission not found.", status=404)

    # Create PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="submission_{submission.reference_code}.pdf"'

    # Create the PDF
    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, "Submission Confirmation")
    p.setFont("Helvetica", 12)
    p.drawString(100, 770, f"Reference Code: {submission.reference_code}")
    p.drawString(100, 750, f"Title: {submission.title}")
    p.drawString(100, 730, f"Description: {submission.description}")
    p.drawString(100, 710, f"Status: {'Complete' if submission.status else 'Incomplete'}")
    p.drawString(100, 690, f"Uploaded by: {submission.user.username}")
    p.drawString(100, 670, f"Submitted at: {submission.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}")
    p.showPage()
    p.save()

    return response
