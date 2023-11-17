from rest_framework.parsers import MultiPartParser ,  DataAndFiles
import json
from django.http import QueryDict


class MultiPartJsonParser(MultiPartParser):
    def parse(self,stream ,media_type = None,parser_context=None):
        result = super().parse(
            stream=stream,
            media_type=media_type,
            parser_context=parser_context
        )
        doc = {}
        doc = json.loads(result.data["doc"])
        return DataAndFiles(doc , result.files)