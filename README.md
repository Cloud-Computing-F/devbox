## Model
- :heavy_check_mark: 파일 데이터베이스 Files(_id(pk)_, fileName, fileSize, uploadedFile, dateTimeOfUpload, parent_id(Folder _id_))
- :heavy_check_mark: 폴더 데이터 베이스 Folder(_id(pk)_, folderName, dateTimeOfUpload, parent_id(Folder _id_))


## Implementation
- :heavy_check_mark: 홈 디렉토리 보기 Display Home Directory 
- :heavy_check_mark: 다중 파일 업로드 Upload file, Upload mltiple files
- :heavy_check_mark: 다중 파일 다운로드 Download file, Download mltiple files 
- :heavy_check_mark: 폴더 생성 Create folder 
- :heavy_check_mark: 디렉토리 이동 Change Directory 
- :heavy_check_mark: 파일 및 폴더 삭제 Delete files and folders 
- :heavy_check_mark: 파일 및 폴더 이름 수정 Rename files and folders 


## Future Plan
- :x: 파일 및 폴더 이동

- :x: 휴지통 데이터베이스 RecycleBins() 
  - :x: 삭제한 파일 및 폴더를 한 번에 볼 수 있는 template 필요
  - :x: 삭제 30일 지나면 영구 삭제 (시간에 대한 column 필요)
  - :x: 선택한 파일 다시 복구 (원래 폴더로 이동할 수 있도록 Folder id를 참조키로 가지고 있어야함)
  - :x: 하위항목에 대한 데이터도 같이 보관되어야함
  - 다소 복잡할 것으로 예상

- :x: 북마크 데이터베이스 BookMarks()
  - :x: 선택한 파일 북마크
  - :x: 북마크에 추가된 파일을 한 번에 볼 수 있는 template 필요
  
- :x: 최대 용량 및 현재까지 사용한 용량 표시
- :x: tree 모양으로 현재 디렉토리 구조 표시
