## feature/current

환경변수파일 생성 및 settings.py에 aws s3 연동 


#### 변동사항
✅ Devbox/view.py -> html 링크 변경 <br>
✅ Config/url.py -> url 변경 <br>

#### 진행사항
✅몇 개의 기능들이 겹쳐지면서 작동을 안하는 것처럼 보이나, 실제로는 작동함 <br>
✅테스트한 기능 : 폴더 만들기, 파일 업로드, 메일링, 다운로드, 삭제, 검색 <br>
✅url 충돌 해결하였습니다 : home_2.html라는 중간 페이지를 걸쳐서 넘어갈 수 있도록 했습니다. <br>
✅follow 기능 수정 했습니다. <br>
✅django secret key, aws s3관련 key, mail관련 아이디와 비밀번호를 환경변수로 설정하였습니다. <br>




