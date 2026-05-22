from django.urls import path
from . import views

urlpatterns = [
    path('portal/', views.landing_page, name='landing_page'),
    path('portal/payment/<int:school_id>/', views.payment_page, name='payment_page'),
    path('portal/dashboard/', views.school_dashboard, name='school_dashboard'),
    path('portal/dashboard/add-student/', views.add_student_manual, name='add_student_manual'),
    path('import-excel/', views.import_excel_results, name='import_excel_results'),
    path('edit-student/<int:student_id>/', views.edit_student_result, name='edit_student_result'),
    path('print-selected/', views.print_selected_students, name='print_selected_students'),
    path('import-students-csv/', views.import_students_csv, name='import_students_csv'),
    
    # ⚙️ LABADAN KHAD EE TIRTIRISTA AH AYAA SI SAX AH LOOGU DARAY SAAXIIB:
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('delete-batch-students/', views.delete_batch_students, name='delete_batch_students'),
]