from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import QuizQuestion, ExamYear, ReadingMaterial

class QuizQuestionResource(resources.ModelResource):
    # Halkan waxaan ka dhignay 'year' halkii ay ka ahayd 'id'
    # Si aad Excel-ka ugu qorto "2019" ama "Fasalka 5" halkii aad ka qori lahayd ID-ga (1, 2, 3)
    exam_year = fields.Field(
        column_name='exam_year',
        attribute='exam_year',
        widget=ForeignKeyWidget(ExamYear, 'year') # 'year' waa field-ka model-kaaga ExamYear ku jira
    )

    class Meta:
        model = QuizQuestion
        fields = ('id', 'exam_year', 'question_text', 'option1', 'option2', 'option3', 'option4', 'correct_option_index')
        import_id_fields = ('id',)

class ReadingMaterialResource(resources.ModelResource):
    # Kan isna sidoo kale 'year' ayaan ku raadinaynaa
    exam_year = fields.Field(
        column_name='exam_year',
        attribute='exam_year',
        widget=ForeignKeyWidget(ExamYear, 'year')
    )

    class Meta:
        model = ReadingMaterial
        fields = ('id', 'exam_year', 'title', 'content')
        import_id_fields = ('id',)