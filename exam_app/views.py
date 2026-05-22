import csv
import io
import random
import openpyxl  # Hubi in aad 'pip install openpyxl' horta samaysay saaxiib
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import connection
from .models import SchoolProfile, StudentResult
from django.utils import timezone

# ========================================================
# SHAXDA DHIBCAHA IYO XISAABINTA (UTILITIES)
# ========================================================

GRADE_POINTS = {
    'A+': 4.0, 'A': 3.75, 'A-': 3.5,
    'B+': 3.25, 'B': 3.0,  'B-': 2.75,
    'C+': 2.5,  'C': 2.0,  'C-': 1.75,
    'D+': 1.5,  'D': 1.0,  'D-': 0.0
}

def calculate_gpa_and_status(grades_list):
    """Function xisaabinaya celceliska xarfaha iyo haddii uu ardaygu gudbay"""
    total_points = 0
    valid_subjects = 0
    
    for g in grades_list:
        if g and g in GRADE_POINTS:
            total_points += GRADE_POINTS[g]
            valid_subjects += 1
                
    if valid_subjects == 0:
        return 'D-', 'Haray'
        
    avg_point = total_points / valid_subjects
    
    closest_grade = 'D-'
    min_diff = float('inf')
    for grade, pt in GRADE_POINTS.items():
        diff = abs(pt - avg_point)
        if diff < min_diff:
            min_diff = diff
            closest_grade = grade
            
    status = "Gudbay" if avg_point >= 1.0 else "Haray"
    return closest_grade, status


# ========================================================
# BOGAGGA NIDAAMKA (VIEWS)
# ========================================================

def landing_page(request):
    """Bogga 1aad: Raadinta Natiijada, Diiwaan-gelinta Iskuulka iyo Login-ka"""
    schools = SchoolProfile.objects.filter(is_active=True)
    student_result = None
    search_performed = False

    if request.method == 'POST':
        # A. RAADINTA NATIIJADA ARDAYGA
        if 'search_student' in request.POST:
            school_id = request.POST.get('school_id')
            roll_number = request.POST.get('roll_number', '').strip()
            
            search_performed = True
            if school_id and roll_number:
                student_result = StudentResult.objects.filter(
                    school_id=school_id, 
                    roll_number__iexact=roll_number
                ).first()
                
                if not student_result:
                    messages.error(request, "Natiijo dambe laguma helin Roll Number-kaas saaxiib!")

        # B. DIIWAAN-GELIN CUSUB EE ISKUUL
        elif 'school_name' in request.POST:
            school_name = request.POST.get('school_name')
            school_logo = request.FILES.get('school_logo')
            secret_password = request.POST.get('secret_password')
            subscription_years = int(request.POST.get('subscription_years', 1))
            payment_method = request.POST.get('payment_method')
            
            amount_paid = subscription_years * 25
            
            if SchoolProfile.objects.filter(school_name=school_name).exists():
                messages.error(request, f"Iskuulka '{school_name}' horay ayuu u jirbaa saaxiib.")
                return redirect('landing_page')
                
            if not request.user.is_authenticated:
                messages.error(request, "Fadlan horta nidaamka weyn iska soo log-geli saaxiib.")
                return redirect('login')
                
            school = SchoolProfile.objects.create(
                admin_user=request.user,
                school_name=school_name,
                school_logo=school_logo,
                secret_password=secret_password,
                subscription_years=subscription_years,
                amount_paid=amount_paid,
                payment_method=payment_method,
                is_active=False
            )
            return redirect('payment_page', school_id=school.id)

        # C. LOGIN MAAMULE HORE U JIRAY
        elif 'login_admin' in request.POST or 'login_school_id' in request.POST:
            school_id = request.POST.get('login_school_id')
            password = request.POST.get('secret_password') or request.POST.get('login_password')
            
            try:
                school = SchoolProfile.objects.get(id=school_id)
                if school.secret_password == password:
                    if school.expires_at < timezone.now():
                        messages.warning(request, "Waqtiga rukunka waa kaa dhacay saaxiib. Fadlan dib u cuzboonaysii.")
                        return redirect('payment_page', school_id=school.id)
                        
                    if school.is_active:
                        request.session['managed_school_id'] = school.id
                        return redirect('school_dashboard')
                    else:
                        messages.error(request, "Iskuulkaaga rukunkiisa weli lama firfirconaysiin saaxiib!")
                else:
                    messages.error(request, "Fure sireedka (Password) waa ka khaldan yahay iskuulkan!")
            except SchoolProfile.DoesNotExist:
                messages.error(request, "Iskuulkan lama helo.")
                
            return redirect('landing_page')

    context = {
        'schools': schools,
        'student_result': student_result,
        'search_performed': search_performed,
    }
    return render(request, 'exam_app/landing_page.html', context)


def payment_page(request, school_id):
    """Bogga 2aad: Maamulidda Lacag Bixinta"""
    school = get_object_or_404(SchoolProfile, id=school_id)
    
    if request.method == 'POST':
        phone_number = request.POST.get('sender_phone')
        if not phone_number:
            messages.error(request, "Fadlan qor nambarka aad lacagta ka soo dirtay saaxiib!")
            return redirect('payment_page', school_id=school.id)
            
        school.sender_phone_number = phone_number
        school.save()
        
        messages.success(
            request, 
            f"Waad ku mahadsan tahay! Waxaan helnay ogeysiiska in aad lacagta ka soo dirtay nambarka {phone_number}. "
            f"Maamulka sare ayaa dhowaan kuu hawlgalin doona!"
        )
        return redirect('landing_page')
        
    return render(request, 'exam_app/payment_page.html', {'school': school})


def school_dashboard(request):
    """Bogga 3aad: Dashboard-ka rasmiga ah oo leh Shaandheyn, Raadin iyo Auto Roll Number"""
    school_id = request.session.get('managed_school_id')
    if not school_id:
        messages.error(request, "Fadlan horta fure sireedkaaga ku gasho saaxiib!")
        return redirect('landing_page')
        
    school = get_object_or_404(SchoolProfile, id=school_id)
    
    # Ka soo qaado ardayda iskuulkaan oo kaliya korna u soo qaad kuwii u dambeeyay
    students = StudentResult.objects.filter(school=school).order_by('-created_at')
    
    # ⚙️ 1. KAXAYNTA SHAANDHEYNTA DUFCADDA/HEERKA (Batch/Level Filter)
    batch_filter = request.GET.get('batch_filter')
    if batch_filter:
        students = students.filter(school_level=batch_filter)

    # ⚙️ 2. KAXAYNTA RAADINTA LUGTA LEH (Search Query)
    search_query = request.GET.get('search_query')
    if search_query:
        students = students.filter(
            full_name__icontains=search_query
        ) | students.filter(
            roll_number__icontains=search_query
        )
    
    # Auto-Generate Roll Number cusub ee foomka gacanta
    while True:
        random_digits = random.randint(100000, 999999)
        generated_roll = f"B25{random_digits}"
        if not StudentResult.objects.filter(roll_number=generated_roll).exists():
            break

    context = {
        'school': school,
        'students': students,
        'next_roll_number': generated_roll,
        'batch_filter': batch_filter,
        'search_query': search_query,
    }
    return render(request, 'exam_app/school_dashboard.html', context)


def add_student_manual(request):
    """Diiwaan-gelinta Gacanta ee labada Heer (Dhexe iyo Sare)"""
    school_id = request.session.get('managed_school_id')
    if not school_id:
        return redirect('landing_page')
        
    school = get_object_or_404(SchoolProfile, id=school_id)
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        roll_number = request.POST.get('roll_number')
        level = request.POST.get('school_level', 'dhexe')
        
        if StudentResult.objects.filter(roll_number=roll_number).exists():
            messages.error(request, f"Roll Number-ka '{roll_number}' horay ayuu u jirbaa saaxiib!")
            return redirect('school_dashboard')
            
        # Wadaagga maadooyinka
        tarbiyo     = request.POST.get('tarbiyo', 'D-').strip().upper()
        carabi      = request.POST.get('carabi', 'D-').strip().upper()
        af_soomaali = request.POST.get('af_soomaali', 'D-').strip().upper()
        xisaab      = request.POST.get('xisaab', 'D-').strip().upper()
        ingiriisi   = request.POST.get('ingiriisi', 'D-').strip().upper()
        teknooloji  = request.POST.get('teknooloji', 'D-').strip().upper()
        
        if level == 'dhexe':
            cilmi_bulsho = request.POST.get('cilmi_bulsho', 'D-').strip().upper()
            saynis       = request.POST.get('saynis', 'D-').strip().upper()
            biology = chemistry = physics = juqraafi = taariikh = business = None
            all_grades = [tarbiyo, carabi, af_soomaali, xisaab, ingiriisi, teknooloji, cilmi_bulsho, saynis]
        else:
            cilmi_bulsho = saynis = None
            biology   = request.POST.get('biology', 'D-').strip().upper()
            chemistry = request.POST.get('chemistry', 'D-').strip().upper()
            physics   = request.POST.get('physics', 'D-').strip().upper()
            juqraafi  = request.POST.get('juqraafi', 'D-').strip().upper()
            taariikh  = request.POST.get('taariikh', 'D-').strip().upper()
            business  = request.POST.get('business', 'D-').strip().upper()
            all_grades = [tarbiyo, carabi, af_soomaali, xisaab, ingiriisi, teknooloji, 
                          biology, chemistry, physics, juqraafi, taariikh, business]
            
        celcelis_grade, goaan_student = calculate_gpa_and_status(all_grades)
            
        StudentResult.objects.create(
            school=school, full_name=full_name, roll_number=roll_number, school_level=level,
            tarbiyo=tarbiyo, carabi=carabi, af_soomaali=af_soomaali, xisaab=xisaab, ingiriisi=ingiriisi, teknooloji=teknooloji,
            cilmi_bulsho=cilmi_bulsho, saynis=saynis, biology=biology, chemistry=chemistry, physics=physics,
            juqraafi=juqraafi, taariikh=taariikh, business=business, celceliska=celcelis_grade, goaan=goaan_student
        )
        
        messages.success(request, f"Natiijada ardayga {full_name} si guul ah ayaa loo kaydiyay!")
        return redirect('school_dashboard')


def edit_student_result(request, student_id):
    """Bogga wax ka beddelka darajooyinka ardayga (Edit)"""
    school_id = request.session.get('managed_school_id')
    if not school_id:
        return redirect('landing_page')
        
    student = get_object_or_404(StudentResult, id=student_id, school_id=school_id)
    
    if request.method == 'POST':
        student.full_name = request.POST.get('full_name')
        
        # Soo qaado darajooyinka cusub
        student.tarbiyo     = request.POST.get('tarbiyo', 'D-').strip().upper()
        student.carabi      = request.POST.get('carabi', 'D-').strip().upper()
        student.af_soomaali = request.POST.get('af_soomaali', 'D-').strip().upper()
        student.xisaab      = request.POST.get('xisaab', 'D-').strip().upper()
        student.ingiriisi   = request.POST.get('ingiriisi', 'D-').strip().upper()
        student.teknooloji  = request.POST.get('teknooloji', 'D-').strip().upper()
        
        if student.school_level == 'dhexe':
            student.cilmi_bulsho = request.POST.get('cilmi_bulsho', 'D-').strip().upper()
            student.saynis       = request.POST.get('saynis', 'D-').strip().upper()
            all_grades = [student.tarbiyo, student.carabi, student.af_soomaali, student.xisaab, student.ingiriisi, student.teknooloji, student.cilmi_bulsho, student.saynis]
        else:
            student.biology   = request.POST.get('biology', 'D-').strip().upper()
            student.chemistry = request.POST.get('chemistry', 'D-').strip().upper()
            student.physics   = request.POST.get('physics', 'D-').strip().upper()
            student.juqraafi  = request.POST.get('juqraafi', 'D-').strip().upper()
            student.taariikh  = request.POST.get('taariikh', 'D-').strip().upper()
            student.business  = request.POST.get('business', 'D-').strip().upper()
            all_grades = [student.tarbiyo, student.carabi, student.af_soomaali, student.xisaab, student.ingiriisi, student.teknooloji, 
                          student.biology, student.chemistry, student.physics, student.juqraafi, student.taariikh, student.business]
            
        student.celceliska, student.goaan = calculate_gpa_and_status(all_grades)
        student.save()
        
        messages.success(request, f"Xogta ardayga {student.full_name} si guul ah ayaa loo hagaajiyay saaxiib!")
        return redirect('school_dashboard')
        
    return render(request, 'exam_app/edit_student.html', {'student': student})


def import_excel_results(request):
    """Nidaamka Bulk Import-ka ee Excel"""
    school_id = request.session.get('managed_school_id')
    if not school_id:
        messages.error(request, "Fadlan horta system-ka soo gal saaxiib!")
        return redirect('landing_page')
        
    school = get_object_or_404(SchoolProfile, id=school_id)
    
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        level = request.POST.get('school_level', 'dhexe')
        
        try:
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active
            success_count = 0
            
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if not row[0]:
                    continue
                    
                full_name = str(row[0]).strip()
                
                tarbiyo      = str(row[1]).strip().upper() if row[1] else 'D-'
                carabi       = str(row[2]).strip().upper() if row[2] else 'D-'
                af_soomaali  = str(row[3]).strip().upper() if row[3] else 'D-'
                xisaab       = str(row[4]).strip().upper() if row[4] else 'D-'
                ingiriisi    = str(row[5]).strip().upper() if row[5] else 'D-'
                teknooloji   = str(row[6]).strip().upper() if row[6] else 'D-'
                
                if level == 'dhexe':
                    cilmi_bulsho = str(row[7]).strip().upper() if row[7] else 'D-'
                    saynis       = str(row[8]).strip().upper() if row[8] else 'D-'
                    biology = chemistry = physics = juqraafi = taariikh = business = None
                    all_grades = [tarbiyo, carabi, af_soomaali, xisaab, ingiriisi, teknooloji, cilmi_bulsho, saynis]
                else:
                    biology      = str(row[7]).strip().upper() if row[7] else 'D-'
                    chemistry    = str(row[8]).strip().upper() if row[8] else 'D-'
                    physics      = str(row[9]).strip().upper() if row[9] else 'D-'
                    juqraafi     = str(row[10]).strip().upper() if row[10] else 'D-'
                    taariikh     = str(row[11]).strip().upper() if row[11] else 'D-'
                    business     = str(row[12]).strip().upper() if row[12] else 'D-'
                    cilmi_bulsho = saynis = None
                    all_grades = [tarbiyo, carabi, af_soomaali, xisaab, ingiriisi, teknooloji, 
                                  biology, chemistry, physics, juqraafi, taariikh, business]
                
                celcelis_grade, goaan_student = calculate_gpa_and_status(all_grades)
                
                while True:
                    random_digits = random.randint(100000, 999999)
                    generated_roll = f"B25{random_digits}"
                    if not StudentResult.objects.filter(roll_number=generated_roll).exists():
                        break
                
                StudentResult.objects.create(
                    school=school, full_name=full_name, roll_number=generated_roll, school_level=level,
                    tarbiyo=tarbiyo, carabi=carabi, af_soomaali=af_soomaali, xisaab=xisaab, ingiriisi=ingiriisi, teknooloji=teknooloji,
                    cilmi_bulsho=cilmi_bulsho, saynis=saynis, biology=biology, chemistry=chemistry, physics=physics,
                    juqraafi=juqraafi, taariikh=taariikh, business=business, celceliska=celcelis_grade, goaan=goaan_student
                )
                success_count += 1
                
            messages.success(request, f"Guul saaxiib! {success_count} arday si toos ah ayaa loo xisaabiyay loona shubay!")
        except Exception as e:
            messages.error(request, f"Cillad baa dhacday: {str(e)}")
            
    return redirect('school_dashboard')


def import_students_csv(request):
    """Shaqada akhrinta faylka CSV"""
    school_id = request.session.get('managed_school_id')
    if not school_id:
        messages.error(request, "Fadlan marka hore iskuul soo dooro saaxiib!")
        return redirect('landing_page')

    school = get_object_or_404(SchoolProfile, id=school_id)
    level = request.POST.get('school_level', 'sare')

    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Fadlan soo geli fayl leh qaabka .csv oo kaliya!")
            return redirect('school_dashboard')

        try:
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string) # Ka bood Headers-ka

            saas_loo_galiyay = 0
            for row in csv.reader(io_string, delimiter=','):
                if not row or len(row) < 2:
                    continue
                
                full_name = row[0].strip()
                
                tarbiyo      = row[1].strip().upper() if len(row) > 1 and row[1] else 'D-'
                carabi       = row[2].strip().upper() if len(row) > 2 and row[2] else 'D-'
                af_soomaali  = row[3].strip().upper() if len(row) > 3 and row[3] else 'D-'
                xisaab       = row[4].strip().upper() if len(row) > 4 and row[4] else 'D-'
                ingiriisi    = row[5].strip().upper() if len(row) > 5 and row[5] else 'D-'
                teknooloji   = row[6].strip().upper() if len(row) > 6 and row[6] else 'D-'
                
                if level == 'dhexe':
                    cilmi_bulsho = row[7].strip().upper() if len(row) > 7 and row[7] else 'D-'
                    saynis       = row[8].strip().upper() if len(row) > 8 and row[8] else 'D-'
                    biology = chemistry = physics = juqraafi = taariikh = business = None
                    all_grades = [tarbiyo, carabi, af_soomaali, xisaab, ingiriisi, teknooloji, cilmi_bulsho, saynis]
                else:
                    biology      = row[7].strip().upper() if len(row) > 7 and row[7] else 'D-'
                    chemistry    = row[8].strip().upper() if len(row) > 8 and row[8] else 'D-'
                    physics      = row[9].strip().upper() if len(row) > 9 and row[9] else 'D-'
                    juqraafi     = row[10].strip().upper() if len(row) > 10 and row[10] else 'D-'
                    taariikh     = row[11].strip().upper() if len(row) > 11 and row[11] else 'D-'
                    business     = row[12].strip().upper() if len(row) > 12 and row[12] else 'D-'
                    cilmi_bulsho = saynis = None
                    all_grades = [tarbiyo, carabi, af_soomaali, xisaab, ingiriisi, teknooloji, 
                                  biology, chemistry, physics, juqraafi, taariikh, business]

                celcelis_grade, goaan_student = calculate_gpa_and_status(all_grades)

                while True:
                    random_digits = random.randint(100000, 999999)
                    generated_roll = f"B25{random_digits}"
                    if not StudentResult.objects.filter(roll_number=generated_roll).exists():
                        break

                StudentResult.objects.create(
                    school=school, full_name=full_name, roll_number=generated_roll, school_level=level,
                    tarbiyo=tarbiyo, carabi=carabi, af_soomaali=af_soomaali, xisaab=xisaab, ingiriisi=ingiriisi, teknooloji=teknooloji,
                    cilmi_bulsho=cilmi_bulsho, saynis=saynis, biology=biology, chemistry=chemistry, physics=physics,
                    juqraafi=juqraafi, taariikh=taariikh, business=business, celceliska=celcelis_grade, goaan=goaan_student
                )
                saas_loo_galiyay += 1

            messages.success(request, f"Hambalyo saaxiib! Waxaa si guul ah loo soo geliyay {saas_loo_galiyay} arday oo cusub!")
        except Exception as e:
            messages.error(request, f"Cillad ayaa ka dhalatay akhrinta faylka CSV: {str(e)}")
            
    return redirect('school_dashboard')


def print_selected_students(request):
    """Soo saarista hal bog oo ay ku wada jiraan ardayda la doortay (Bulk Slip)"""
    school_id = request.session.get('managed_school_id')
    if not school_id:
        messages.error(request, "Fadlan marka hore fure sireedkaaga ku gasho saaxiib!")
        return redirect('landing_page')
        
    school = get_object_or_404(SchoolProfile, id=school_id)
    
    if request.method == 'POST':
        student_ids = request.POST.getlist('selected_students')
        
        if not student_ids:
            messages.warning(request, "Fadlan horta dooro ugu yaraan hal arday saaxiib!")
            return redirect('school_dashboard')
            
        students = StudentResult.objects.filter(id__in=student_ids, school=school)
        
        if not students.exists():
            messages.error(request, "Ardayda aad dooratay laguma helin nidaamka!")
            return redirect('school_dashboard')
            
        context = {
            'students': students,
            'school': school,
            'current_date': timezone.now(),
        }
        return render(request, 'exam_app/print_selected.html', context)
        
    return redirect('school_dashboard')


# ========================================================================
# HAWLAHA RE-SETTING ID-GA & TIRTIRISTA BADAN (BULK DELETE + RESET AUTO_INC)
# ========================================================================

def delete_student(request, student_id):
    """Khadkaan wuxuu tirtirayaa hal arday wuxuuna dib u hagaajinayaa xisaabiyaha ID-ga"""
    school_id = request.session.get('managed_school_id')
    if not school_id:
        messages.error(request, "Fadlan marka hore fure sireedkaaga ku gasho saaxiib!")
        return redirect('landing_page')
        
    student = get_object_or_404(StudentResult, id=student_id, school_id=school_id)
    student_name = student.full_name
    student.delete()
    
    # 🔥 TRICK-KA DIB-U-ISTICMAALKA ID-GA EE DATABASE-KA:
    with connection.cursor() as cursor:
        if connection.vendor == 'sqlite':
            cursor.execute("UPDATE sqlite_sequence SET seq = (SELECT COALESCE(MAX(id), 0) FROM exam_app_studentresult) WHERE name='exam_app_studentresult';")
        elif connection.vendor == 'postgresql':
            cursor.execute("SELECT setval(pg_get_serial_sequence('exam_app_studentresult', 'id'), COALESCE(MAX(id), 1), false) FROM exam_app_studentresult;")
    
    messages.success(request, f"Waxaa guul ku tirtiray xogta ardayga: {student_name}. ID-gii dib ayaa loo xisaabiyay!")
    return redirect(request.META.get('HTTP_REFERER', 'school_dashboard'))


def delete_batch_students(request):
    """Khadkaan wuxuu hal mar wada tirtirayaa dufcad dhan (Dhexe ama Sare) wuxuuna dib u habaynayaa ID-yada"""
    school_id = request.session.get('managed_school_id')
    if not school_id:
        messages.error(request, "Fadlan marka hore nidaamka soo gal saaxiib!")
        return redirect('landing_page')
        
    if request.method == 'POST':
        school_level = request.POST.get('school_level') 
        
        if school_level in ['dhexe', 'sare']:
            deleted_count, _ = StudentResult.objects.filter(
                school_id=school_id, 
                school_level=school_level
            ).delete()
            
            # 🔥 TRICK-KA DIB-U-ISTICMAALKA ID-GA MARKAY DUFCADU BADAN TAHAY:
            with connection.cursor() as cursor:
                if connection.vendor == 'sqlite':
                    cursor.execute("UPDATE sqlite_sequence SET seq = (SELECT COALESCE(MAX(id), 0) FROM exam_app_studentresult) WHERE name='exam_app_studentresult';")
                elif connection.vendor == 'postgresql':
                    cursor.execute("SELECT setval(pg_get_serial_sequence('exam_app_studentresult', 'id'), COALESCE(MAX(id), 1), false) FROM exam_app_studentresult;")
            
            messages.success(
                request, 
                f"Waxaa guul ku tirtiray {deleted_count} arday oo ka tirsanaa Dugsi {school_level.capitalize()}. ID-yadii weynaa dib ayaa loo habeeyay saaxiib!"
            )
        else:
            messages.error(request, "Fadlan dooro heerka dugsiga aad rabto in aad tirtirto (dhexe ama sare)!")
            
    return redirect(request.META.get('HTTP_REFERER', 'school_dashboard'))