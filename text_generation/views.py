
from rest_framework import views, status
from rest_framework.response import Response

from .fact_check import qna_response


class FactChecker(views.APIView):

    def get(self, request):
        upload_response = qna_response(request.GET.get('text'))
        return Response(data=upload_response, status=status.HTTP_200_OK)