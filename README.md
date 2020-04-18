myproject
==========

## 주식정보 가져오는 코드 짜기
* selenium을 사용하여 네이버 주식페이지에서 주식 정보를 가져온다.
* time을 사용해서 여러 종목을 가져올 때 시간차이를 준다.
* schedule을 통해 일정 시간마다 다시 불러올 수 있게 만들어준다.
* db와 연동시켜 code로 받아온 항목들의 데이터를 1분마다 업데이트 해 준다.

참고자료 : <https://bit.ly/scc-no-corona>

## 주식 이름과 가격 크롤링하는 코드 짜기
* requests를 이용해 웹 페이지의 정보를 가져와서 bs4로 가공한다.
* 가공한 정보를 pymongo를 통해 mongodb에 stocks로 저장해준다.
*  주식의 코드값을 db에 저장하여 위의 주식정보 업데이트에 사용될 수 있게 해준다.

## user의 db를 만들고 저장하고 기능 실행하는 코드 짜기
* email과 password를 받아서 db에서 회원이 있는지 확인하고 아니면 새로 db에 등록한다
* user의 기능으로 사는것과 로그아웃을 추가한다
+ 해야할일: 파는것과 살 때의 db 업데이트