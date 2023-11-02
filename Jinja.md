# 개념
### 파이썬으로 작성된 템플릿팅 엔진으로, API 응답을 쉽게 렌더링할 수 있도록 한다.
### 사용하기 위해서는 <font color=red>jinja 패키지를 설치</font>하고 <font color=red>기존 작업 directory에 template이라는 신규 폴더</font>를 생성해야 한다.
template 폴더에 모든 jinja 관련 파일(jinja 구문이 섞여 있는 html 파일)이 저장된다.

---
# 자주 사용되는 구문
```jinja
{% ... %}
```
구조(처리)를 제어하기 위한 명령을 지정할 때 사용
```jinja
{{todo.item}}
```
식의 값을 전달할 때 사용한다.
```jinja
{# ... #}
```
주석을 기입할 때 사용되며 웹 페이지상에는 표시되지 않는다.

---
# 주로 사용되는 기본 기능
### 필터
파이썬과 jinja는 유사한 구문을 사용하지만 문자열 병합이나 첫 문자를 대문자로 변환하기 등의 파이썬 문자열 수정 구문은 jinja에선 사용할 수 없다. 따라서 이런 수정 작업은 jinja의 필터 기능을 사용한다.
#### 기본 형태
기본적으로 파이프 기호(|)를 사용해서 변수와 구분하며 괄호를 사용해 선택적 인수를 지정한다.
```jinja
{{ variable | filter_name(*args) }}
```
인수가 없다면 다음처럼 정의해도 된다.
```jinja
{{ variable | filter_name }}
```
#### 기본 필터 예시
전달된 값이 None일 때(= 값이 없을 때) 사용할 값을 지정한다.
```jinja
{{ todo.item | default('이것은 기본 todo 아이템이다.') }}
```
#### 이스케이프 필터 예시
HTML을 변환하지 않고 그대로 렌더링한다.
```jinja
{{ "<title>Example</title>" | escape }}
```
#### 변환 필터 예시
데이터 유형을 변환한다.
```jinja
{{ 3.142 | int }}
3

{{ 31 | float }}
31.0
```
#### 병합 필터 예시
리스트 내의 요소들을 병합해서 하나의 문자열로 만든다.
```jinja
{{ ['나는', '밥을', '먹었습니다.'] | join(' ') }}
나는 밥을 먹었습니다.
```
#### 길이 필터 예시
전달된 객체의 길이를 반환한다. 파이썬의 len()과 같은 역할
```jinja
{{ Entity | length }}
```
### if문
파이썬과 사용법이 유사하며 {% %} 제어 블록 내에서 사용 가능하다.
```jinja
{% if todo | length<5 %}
    if문 예제
{% else %}
    if문 예제2
{% else if %}
```
### 반복문
역시 {% %} 제어 블록 내에서 사용 가능하다.</br>
jinja에서는 변수를 사용해 반복 처리가 가능하다. 리스트 또는 일반적인 함수를 사용할 수도 있다.
```
{% for todo in todos %}
    <b> {{ todo.item }} </b>
{% endfor %}
```
반복문 내에서는 특수한 변수를 사용할 수 있다.
|변수|설명|
|---|---|
loop.index|반복의 현재 인덱스를 보여준다.(시작 인덱스=1)|
loop.index0|반복의 현재 인덱스를 보여준다.(시작 인덱스=0)|
loop.revindex|뒤에서부터의 반복 인덱스를 보여준다(시작 인덱스=1)|
loop.revindex0|뒤에서부터의 반복 인덱스를 보여준다(시작 인덱스=0)|
loop.first|첫 번째 반복이면 True 반환|
loop.last|마지막 반복이면 True 반환|
loop.length|리스트 등의 아이템 수를 반환|
loop.cycle|리스트 내의 값을 차례대로 사용|
loop.depth|재귀적 반복에서의 현재 렌더링 단계를 보여준다.(1단계부터 시작)|
loop.depth0|재귀적 반복에서의 현재 렌더링 단계를 보여준다.(0단계부터 시작)|
loop.previtem|이전 반복에 사용한 아이템을 반환한다.(첫 반복에서는 정의되지 않음)|
loop.nextitem|다음 반복에 사용할 아이템을 반환한다.(마지막 반복에서는 정의되지 않음)|
loop.changed(*val)|이전에 호출한 값과 다르면 True를 반환(전혀 호출되지 않은 경우도 포함)|
### 매크로
jinja의 매크로는 하나의 함수로, HTML 문자열을 반환한다.<br/>
#### 매크로 예시 - 입력(input) 매크로 정의
```jinja
{% macro input(name, value='', type='text', size=20) %}
    <div class="form">
        <input type="{{ type }}" name="{{ name }}"
            value="{{ value|escape }}" size="{{ size }}">
    </div>
{% endmacro %}
```
해당 매크로를 호출해서 폼에 사용할 입력 요소를 간단하게 만들 수 있다.
```jinja
{{ input('item') }}
```
해당 코드는 다음곽 같은 HTML을 반환한다.
```html
<div class="form">
    <input type="text" name="item" value"" size="20">
</div>
```
### 템플릿 상속(template inheritance)
jinja의 가장 강력한 기능으로 중복 배제(DRY, Don't Repeat Yourself) 원칙에 근거하여 큰 규모의 웹 애플리케이션을 개발할 때 많은 도움이 된다.<br/>
템플릿 상속은 기본 템플릿을 정의한 다음 이 템플릿을 자식 템플릿이 상속하거나 교체해서 사용할 수 있게 한다.
