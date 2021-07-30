# Naver finance
### 구조

네이버 증권 웹사이트에 get요청을 통해 얻은 html 정보를 pandas를 통해 페이지의 표정보를 받아서 저장한다.  
개발방식은 함수들로 구성된 프로그래밍방식으로, 기능을 담당하는 함수를 작성하고, `example.py`에서 필요한 함수를 호출하는 방식으로 원하는 결과를 저장한다.  
https 요청으로 requests 패키지를 사용하고, pandas 패키지로 기본적인 파싱을하고, 추가로 필요한 경우 BeautifulSoup 패키지를 사용한다.  

### 요소

|함수명|파일|목적|
|:-|:-|:-|
|`naver_sise_time_url`|`naver_finance.py`|네이버 당일 시간별 시세 조회의 url을 생성한다|
|`naver_sise_day_url`|`naver_finance.py`|네이버 일별 시세 조회의 url을 생성한다|
|`naver_board_url`|`naver_finance.py`|네이버 종목토론실 조회의 url을 생성한다|
|`get_naver_sise_time`|`naver_finance.py`|주식의 지정한 날짜의 시간별 시세 정보를 조회한다|
|`get_naver_sise_day`|`naver_finance.py`|주식의 지정한 날짜까지의 모든 시세 정보를 조회한다|
|`get_naver_board`|`naver_finance.py`|지정한 날짜까지의 종목토론실 정보를 조회한다|
|`get_naver_sise_high_down`|`naver_finance.py`|네이버에서 제공하는 당일 급락 정보를 조회한다|

### 결과 분석

주식입문으로 주식의 정보를 조회하고 저장했고, 향후 자연어 처리를 통해 공포지수와 같은 수치를 계산하는 알고리즘을 구현하고자 한다.
