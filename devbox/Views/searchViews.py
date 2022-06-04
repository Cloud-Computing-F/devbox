from .utilsViews import search, sort, download
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# 파일 및 폴더 검색
def searchFileAndFolder(request):
    template = 'search_result.html'
    if request.method == "GET":
        query = request.GET.get('search_input')
        if query is not None:  # 파일 및 폴더 이름 검색
            context = search(query)

            return render(request, template, context)
        else:  # 검색 단어 입력하지 않았을 경우 예외 처리
            return render(request, template)
    else:
        return render(request, template)


# 파일 검색 후 파일 및 폴더 정렬
def sortFromSearch(request, query):
    template = 'search_result.html'
    if request.method == "GET":
        sortMode = request.GET.get('sortFileAndFolder')
        search_context = search(query)

        sort_context = sort(sortMode, search_context["files"], search_context["folders"])
        sort_context["query"] = search_context["query"]
        sort_context["resSum"] = search_context["resSum"]
        return render(request, template, context=sort_context)

    else:
        return render(request, template)


# 파일 다운로드
@csrf_exempt
def downloadFromSearch(request, query):
    print(query)
    if request.method == "POST":
        selected = request.POST.getlist("selected_file")

        # 파일 다운로드
        if len(selected) >= 1:
            return download(selected)

        # 파일 선택 안함 예외 처리 (수정)
        elif len(selected) < 1:
            return download(selected)


# 파일 삭제
@csrf_exempt
def deleteFromSearch(request, query):
    pass
