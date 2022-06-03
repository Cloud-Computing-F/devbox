from devbox.models import Files, Folder
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .views import display_file_and_folder


# folder 공유 서비스
def display_file_and_folder_ui(request, uuid):
    folders = Folder.objects.filter(uuid=uuid)
    files = Files.objects.filter(uuid=uuid)
    return render(request, "home.html", context={
        "current_folder_id": 0,
        "files": files,
        "folders": folders,
    })


# 메일링 서비스
@csrf_exempt
def mailing(request):
    if request.method == 'POST':
        # 파일 혹은 폴더 선택
        selected_target = request.POST.get('selected_target')
        # 이메일 주소 입력 -> (2022.05.22 기준 이메일 하나만 작성가능)
        email_address = request.POST.get('email_address')
        recipient_list = [email_address]
        # 'devbox/mail.html' 에서 mailing 시 들어갈 email 화면을 꾸밀 수 있습니다.
        html_message = render_to_string('mail.html', context={
            # 주소는 공유 파일/폴더 주소에 맞게 수정하면 됩니다.
            # 우선은 가장 기본적인 것으로 설정해뒀습니다.
            'link': selected_target,
        })
        # send_mail (메일 제목, 메일 내용, email_from,recipient_list,html_message)
        send_mail("DevBox 공유 메일", "테스트 내용입니다.", settings.EMAIL_HOST_USER,
                  recipient_list, html_message=html_message)
        # 바로 홈 화면으로 넘어갑니다.
        return redirect("devbox:home")
