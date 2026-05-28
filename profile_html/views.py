from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import UserProfile
# Midkaan kaliya ayaa ku filan maadaama utils uu ku dhex jiro isla app-ka profile_html
from .utils import generate_qr_code, generate_id_card_pdf

@login_required
def profile(request):
    profile_obj, created = UserProfile.objects.get_or_create(user=request.user)
    qr_image = ""
    if profile_obj.user_id_code:
        qr_image = generate_qr_code(profile_obj.user_id_code)

    return render(request, 'profile_html/profile.html', {
        'profile': profile_obj,
        'qr_image': qr_image
    })

@login_required
def download_id_card(request):
    profile_obj = get_object_or_404(UserProfile, user=request.user)
    # Maadaama uu yahay badhanka Download-ka, hubi inuu yahay POST ama GET
    user_password = request.POST.get('manual_password', "Lama hayo") if request.method == 'POST' else "Lama hayo"

    pdf_buffer = generate_id_card_pdf(profile_obj, password=user_password)

    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{profile_obj.user_id_code}_ID.pdf"'

    return response