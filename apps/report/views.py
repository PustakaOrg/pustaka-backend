from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse

from apps.report.generator import LibraryReportGenerator
from core.permissions import IsAdminOrLibrarianOnly

# Create your views here.

class ReportQueryParamsSerializer(serializers.Serializer):
    month = serializers.IntegerField(min_value=1, max_value=12, required=True)
    year = serializers.IntegerField(min_value=2000, required=True)



class GenerateReportPDFView(APIView): # Renamed view for clarity
    """
    API endpoint to generate and download the Library Loan Report PDF directly.
    Accepts GET requests with month and year as query parameters.
    """
    # permission_classes = [IsAdminOrLibrarianOnly] # Add permissions as needed

    def get(self, request, *args, **kwargs):
        serializer = ReportQueryParamsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        month = serializer.validated_data['month']
        year = serializer.validated_data['year']

        try:
            generator = LibraryReportGenerator()
            pdf_bytes = generator.generate_report(month, year) 
            
            response = HttpResponse(pdf_bytes, content_type='application/pdf')
            
            suggested_filename = generator.filename 
            response['Content-Disposition'] = f'attachment; filename="{suggested_filename}"'
            
            return response

        except ValueError as ve:
            return Response(
                {"detail": f"Report generation error: {str(ve)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.exception(f"Unhandled error generating loan report for {month}/{year}")
            return Response(
                {"detail": f"An internal server error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
