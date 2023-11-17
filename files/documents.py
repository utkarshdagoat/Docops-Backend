from django_elasticsearch_dsl import Document , fields
from django_elasticsearch_dsl.registries import registry
from .models.file import File , FileText

from elasticsearch_dsl import analyzer , tokenizer

autocomplete_analyser  = analyzer('autocomplete_analyser' , tokenizer=tokenizer('trigram' , 'ngram' , min_gram=3, max_gram=20) , filter=['lowercase'])



@registry.register_document
class FileHeadingDocument(Document):
    heading = fields.TextField(required=True , analyzer=autocomplete_analyser)


    class Index:
        name = 'headings'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0,
                    'max_ngram_diff':20
                    }
    class Django:
        model = File
        fields = []



@registry.register_document
class FileTextDocument(Document):

    text = fields.TextField(required=True ,analyzer=autocomplete_analyser )

    class Index:
        name = 'text'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0,
                    'max_ngram_diff':20
                    }
    class Django:
        model = FileText
        fields = []
