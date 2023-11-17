import os

from docops.settings import MEDIA_ROOT

from django.shortcuts import render
from rest_framework import views , mixins,generics , viewsets
from rest_framework.response import Response 
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication


# Create your views here
from docops.authentication import CsrfExemptSessionAuthentication
from files.models.file_store import FileDoc
from files.models.file import File
from .serializers.serializer import FileSerializer , HeadingFileSerializer , CoverFileSerializer , FileRetriveSerializer , FileSpaceShowSerializer ,FileTextSerializer , FileSearchSerializer , FilePermissionSerializer
from rest_framework import parsers
from files.parser import MultiPartJsonParser

from .models.file import FileText

from spaces.models.space import Space
from .documents import FileHeadingDocument , FileTextDocument

from myauth.models import User


from files.serializers.request import RequestSerializer
from files.models.request import Request


from itertools import chain


from guardian.shortcuts import assign_perm


class RetrieveFileAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [CsrfExemptSessionAuthentication,]
    serializer_class = FileSerializer
    
    def get(self , request , *args , **kwargs):
        try:
            instance = File.objects.get(docId=self.kwargs['doc_id'])
            cover = instance.cover if(instance.cover) else None
            data = {
                "cover":cover,
                "heading":instance.heading
            }
            file  = FileDoc.objects.get(id=instance.docId)
            serializer = FileRetriveSerializer(data=data)
            if  serializer.is_valid(raise_exception=True):
                res = {
                    "meta":serializer.data,
                    "doc":file.doc
                }
                return Response(res)
            return Response(serializer.errors)
        except File.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class FileAPIView(generics.GenericAPIView , mixins.ListModelMixin):
    permission_classes = [IsAuthenticated ,]
    authentication_classes = [CsrfExemptSessionAuthentication,]
    parser_classes=[parsers.JSONParser]
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def post(self , request , *args , **kwargs):
        serializer_data = {
            "space":request.data['space'],
            "isPrivate":False
        }
        serializer  = FileSerializer(data=serializer_data , context={'request':request})
        serializer.is_valid(raise_exception=True)
        file = serializer.save()
        fileStore = FileDoc(sqlRef=file.id)
        file_text = FileText.objects.create(file=file , text='')
        fileStore.save()
        file.docId = str(fileStore.id)
        docId = file.docId
        file.save()
        return Response(docId)




class UpdateFileAPIView(views.APIView):
    permission_classes = [IsAuthenticated ,]
    authentication_classes = [CsrfExemptSessionAuthentication,]
    parser_classes=[ parsers.JSONParser]

    def put (self,request ,*args,**kwargs):
        docInstance = FileDoc.objects.get(id=self.kwargs['doc_id'])
        docInstance.doc = request.data['doc']
        docInstance.save()
        return Response("True")



class UpdataHeadingAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [CsrfExemptSessionAuthentication]
    lookup_url_kwarg = 'doc_id'
    serializer_class = HeadingFileSerializer
    queryset = File.objects.all()

    def put(self , request ,  *args , **kwargs ):
        try:
            instance = File.objects.get(docId=self.kwargs['doc_id'])
            print(request.data)
            serailizer = HeadingFileSerializer(instance , data=request.data)
            print(request.data)
            if serailizer.is_valid():
                serailizer.save()
                print(serailizer.data)
                return Response(serailizer.data)
            return Response(serailizer.errors)
        except File.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class UpdateCoverAPIView(generics.GenericAPIView , mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [CsrfExemptSessionAuthentication]
    lookup_url_kwarg = 'doc_id'
    serializer_class = CoverFileSerializer
    parser_classes = [parsers.MultiPartParser]
    queryset = File.objects.all()

    def put(self , request ,  *args , **kwargs ):
        try:
            instance = File.objects.get(docId=self.kwargs['doc_id'])
            serailizer = CoverFileSerializer(instance , data=request.data)
            if serailizer.is_valid():
                serailizer.save()
                print(serailizer.data)
                return Response(serailizer.data)
            return Response(serailizer.errors)
        except File.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self , request , *args , **kwargs):
        try:
            instance = File.objects.get(docId=self.kwargs['doc_id'])
            instance.cover.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except File.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)





class ListFilesSpaceAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]
    serializer_class = FileSpaceShowSerializer

    def get_queryset(self):
        space_id = self.kwargs['space_id']
        space = Space.objects.get(id=space_id)
        file_queryset = File.objects.filter(space=space)
        return file_queryset

class FileTextAPIView(generics.GenericAPIView):
    authentication_classes = [CsrfExemptSessionAuthentication ,]
    permission_classes = [IsAuthenticated]
    serializer_class = FileTextSerializer
    queryset = FileText.objects.all()
    lookup_url_kwarg='doc_id'

    def put(self , request , *args , **kwargs):
        doc_id = kwargs['doc_id']
        file = File.objects.get(docId=doc_id)
        instance = FileText.objects.get(file=file)
        serilizer = FileTextSerializer(data=request.data , instance=instance)
        serilizer.is_valid(raise_exception=True)
        serilizer.save()
        return Response(serilizer.data)


class FileSearchAPIView(generics.ListAPIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated , ]
    serializer_class = FileSearchSerializer

    def get_queryset(self):
        query = self.request.GET.get('query' , '')
        search_heading = FileHeadingDocument.search().query("match" , heading=query)
        search_text  = FileTextDocument.search().query('match' , text=query)
        heading_queryset = search_heading.to_queryset()
        file_text_queryset = search_text.to_queryset()
        file_queryset_from_text =File.objects.filter(id__in=file_text_queryset)
        file_queryset = list(chain(heading_queryset , file_queryset_from_text))
        return file_queryset



class UserPermissionForFileAPIView(generics.GenericAPIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    serializer_class = FilePermissionSerializer

    def get(self , request , *args , **kwargs):
        instance = File.objects.get(docId=self.kwargs['doc_id'])
        serializer = FilePermissionSerializer(instance=instance , context={'request':request})
        return Response(serializer.data)




class RequestFilesViewset(viewsets.ModelViewSet):
    serializer_class = RequestSerializer
    queryset = Request.objects.all()
    authentication_classes = [CsrfExemptSessionAuthentication ,]
