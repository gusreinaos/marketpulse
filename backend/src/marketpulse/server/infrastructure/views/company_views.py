# Author: Michael Larsson, Wojciech Pechmann

from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

from ...application.company.get_company_history_use_case import CompanyHistoryUseCase
from ...application.company.get_stock_trend_use_case import StockTrendUseCase
from ...application.company.get_inflation_trend_use_case import InflationTrendUseCase
from ...application.company.get_company_testimonials_use_case import CompanyTestimonialUseCase
from ...application.company.get_company_info_use_case import CompanyInfoUseCase
from ...application.company.get_all_predictions_use_case import GetAllPredictions

class CompanyView(viewsets.ViewSet):
    def get_stock_history(self, request, cmp=''):
        """
        Endpoint for getting the history for a specific company

        """

        if cmp != '':
            try:
                # Assuming ts is a parameter that should be passed to getCompanyHistory
                response = CompanyHistoryUseCase.getCompanyHistory(cmp)
                return Response(response, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "Invalid action, please specify a company"}, status=status.HTTP_400_BAD_REQUEST)
        
    def get_stock_trend(self, request, cmp=''):
        """
        Endpoint for getting the history for a specific company

        """

        if cmp != '':
            try:
                # Assuming ts is a parameter that should be passed to getCompanyHistory
                response = StockTrendUseCase.getStockTrend(cmp)
                return Response(response, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response({"error": "Invalid action, please specify a company"}, status=status.HTTP_400_BAD_REQUEST)
        
    def get_inflation_trend(self, request):
        """
        Endpoint for getting the history for a specific company

        """
        try:
            # Assuming ts is a parameter that should be passed to getCompanyHistory
            response = InflationTrendUseCase.getInflationTrend()
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get_testimonials(self, request, cmp):
        """
        Endpoint for retrieving the stocktwit popular messages about a specific company

        """
        try:
            response = CompanyTestimonialUseCase.getTestimonials(cmp)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get_company_info(self, request, cmp):
        """ 
        Endpoint for getting the short description of a specific company

        """
        try:
            response = CompanyInfoUseCase.getCompanyInfo(cmp)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get_all_companies(self, request):
        try:
            response = GetAllPredictions.get()
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

