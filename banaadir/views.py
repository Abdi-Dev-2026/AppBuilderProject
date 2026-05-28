import json
from django.shortcuts import render
from .models import Subject, GlobalNotice

def banaadir_view(request):
    subjects = Subject.objects.all()
    data_dict = {}
    
    for sub in subjects:
        data_dict[sub.name] = {}
        for yr in sub.years.all():
            data_dict[sub.name][str(yr.year)] = {
                "read": [
                    {
                        "title": r.title,
                        "content": r.content,
                        "image_file": r.image_file.url if hasattr(r, 'image_file') and r.image_file else "",
                        "image_url": getattr(r, 'image_url', ""),
                        "video_file": r.video_file.url if hasattr(r, 'video_file') and r.video_file else "",
                        "video_url": getattr(r, 'video_url', ""),
                        "is_portrait": getattr(r, 'is_portrait', False)
                    } for r in yr.readings.all()
                ],
                "quiz": [
                    {
                        "q": q.question_text,
                        "choices": [q.option1, q.option2, q.option3, q.option4],
                        "answer": q.correct_option_index,
                        "image_file": q.image_file.url if hasattr(q, 'image_file') and q.image_file else "",
                        "image_url": getattr(q, 'image_url', ""),
                        "video_file": q.video_file.url if hasattr(q, 'video_file') and q.video_file else "",
                        "video_url": getattr(q, 'video_url', ""),
                        "is_portrait": getattr(q, 'is_portrait', False)
                    } for q in yr.quizzes.all()
                ]
            }

    notices_from_admin = GlobalNotice.objects.filter(is_active=True).order_by('-created_at')
    global_ads_list = []
    for notice in notices_from_admin:
        global_ads_list.append({
            'title': notice.title,
            'description': notice.description or '',
            'image_file': notice.image_file.url if notice.image_file else '',
            'image_url': notice.image_url or '',
            'video_file': notice.video_file.url if notice.video_file else '',
            'video_url': notice.video_url or '',
            'is_portrait': notice.is_portrait,
        })
    
    data_dict['global_ads'] = global_ads_list

    subjects_data = []
    for s in subjects:
        subjects_data.append({
            'name': s.name,
            'icon_emoji': getattr(s, 'icon_emoji', ''),
            'icon_image_file': s.icon_image_file.url if hasattr(s, 'icon_image_file') and s.icon_image_file else '',
            'icon_image_url': getattr(s, 'icon_image_url', ''),
            'icon_video_file': s.icon_video_file.url if hasattr(s, 'icon_video_file') and s.icon_video_file else '',
            'icon_video_url': getattr(s, 'icon_video_url', ''),
        })

    context = {
        'subjects_json': json.dumps(subjects_data),
        'data_json': json.dumps(data_dict)
    }
    return render(request, 'banaadir/banaadir.html', context)