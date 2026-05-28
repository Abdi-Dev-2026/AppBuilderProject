from django.shortcuts import render, redirect
from django.contrib import messages as django_messages
from .models import ContactMessage

def contact_page(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject') or "General"
        message = request.POST.get('message')

        if name and email and message:
            ContactMessage.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            django_messages.success(request, "Fariintaada waa la helay ✅")
            return redirect('contact')

        django_messages.error(request, "Fadlan buuxi dhammaan xogta.")

    return render(request, 'contact/contact.html')