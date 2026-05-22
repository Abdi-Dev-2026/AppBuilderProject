from import_export import resources
from .models import StudentResult

class StudentResultResource(resources.ModelResource):
    class Meta:
        model = StudentResult
        fields = (
            'id', 'school__school_name', 'full_name', 'roll_number', 
            'tarbiyo', 'carabi', 'af_soomaali', 'xisaab', 
            'cilmi_bulsho', 'saynis', 'ingiriisi', 'teknooloji', 
            'celceliska', 'goaan'
        )