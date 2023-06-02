from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .serializers import *
from rest_framework import generics
from django.db.models import Avg, Count, Min, Sum


class Scans_Response(APIView):

    def get(self, request):
        model = Scans.objects.all()
        serializer = Scans_Serializer(model, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = Scans_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UpcDetail_Old_Response(generics.ListAPIView):
    serializer_class = UpcDetail_Serializer

    def get_queryset(self):
        queryset = UpcDetail.objects.all()
        upc_param = self.request.query_params.get('UPC', '')
        if upc_param:
            return queryset.filter(id=upc_param)
        return queryset


class UpcDetail_Response(APIView):

    def get(self, request):
        model = UpcDetail.objects.annotate(onhand=Sum('scans__delta'))
        upc_param = self.request.query_params.get('UPC', '')
        if upc_param:
            model = model.filter(id=upc_param)
        serializer = OnHand_Serializer(model, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UpcDetail_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UpcDetail_Image_Upload(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        print(request.data)
        serializer = UpcDetail_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class OnHand_Response(generics.ListAPIView):
    serializer_class = OnHand_Serializer

    def get_queryset(self):
        upc_param = self.request.query_params.get('UPC', '')
        queryset = Scans.objects.raw(f"""
            select a.BASID
                  ,a.UPC
                  ,a.DESCRIPTION
                  ,a.DETAILS
                  ,SUM(b.DELTA) as DELTA
            from inventory_upcdetail a
            join inventory_scans b on a.BASID = b.UPC_BASID_id
            where a.UPC = '{upc_param}'
            group by a.BASID, a.UPC, a.DETAILS, a.DESCRIPTION""")
        return queryset

