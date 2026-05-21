from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import QuizQuestion, ExamYear, ReadingMaterial

# Widget gaar ah oo ka hortagaya cilada 'MultipleObjectsReturned'
class SafeExamYearWidget(ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return None
        # Haddii ay dhacdo in labo shay ay isku sanad yihiin (English 2020 iyo Tarbiya 2020)
        # Waxaynu ka soo qabanaynaa kan ugu horreeya si uusan nidaamku u jabin, ama waxaad ku shaandheyn kartaa row['subject']
        queryset = self.get_queryset(value, row, *args, **kwargs)
        obj = queryset.filter(**{self.field: value}).first()
        return obj

class QuizQuestionResource(resources.ModelResource):
    exam_year = fields.Field(
        column_name='exam_year',
        attribute='exam_year',
        widget=SafeExamYearWidget(ExamYear, 'year') # Isticmaal widget-ka rasmiga ah ee ammaan ka ah loops-ka
    )

    class Meta:
        model = QuizQuestion
        fields = ('id', 'exam_year', 'question_text', 'option1', 'option2', 'option3', 'option4', 'correct_option_index')
        import_id_fields = ('id',)

class ReadingMaterialResource(resources.ModelResource):
    exam_year = fields.Field(
        column_name='exam_year',
        attribute='exam_year',
        widget=SafeExamYearWidget(ExamYear, 'year')
    )

    class Meta:
        model = ReadingMaterial
        fields = ('id', 'exam_year', 'title', 'content')
        import_id_fields = ('id',)