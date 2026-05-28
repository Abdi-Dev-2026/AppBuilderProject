from django.shortcuts import render
# Nidaamka natiijada haddii aad dib ka dhisayso halkan ayuu views-kiisa u madax-bannaan yahay
def result_home(request):
    return render(request, 'result/result.html')