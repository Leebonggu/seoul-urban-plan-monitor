# 고시문 인사이트 생성 프롬프트

> insight_generator.py에서 LLM API 호출 시 사용하는 프롬프트입니다.

## 구조

```
시스템 프롬프트 = expert_persona.md + 출력 형식(OUTPUT_FORMAT)
유저 프롬프트   = 고시문 정보 + 고시 내용 + policy_reference.md
```

## 페르소나

`expert_persona.md` 참조. 전문가 프로필과 글쓰기 스타일을 정의합니다.
페르소나를 바꾸면 글의 톤과 관점이 바뀝니다.

## 출력 형식 (JSON)

| 필드 | 설명 | 분량 |
|------|------|------|
| hook | 도입부 (질문형/흥미로운 사실) | 1~2문장 |
| summary | 쉬운 설명 | 3~5문장 |
| background | 고시 배경, 지역 맥락 | 3~5문장 |
| key_changes | 핵심 변경 내용 (수치 포함) | 3~5문장 |
| impact_residents | 주민 생활 영향 | 2~4문장 |
| impact_realestate | 부동산 시장 영향 | 2~4문장 |
| policy_context | 관련 정책 연결 (없으면 null) | 3~4문장 |
| timeline | 향후 예상 일정 | 2~3문장 |
| expert_opinion | 전문가 종합 코멘트 | 2~4문장 |
| keywords | 핵심 키워드 | 3~7개 |

## 유저 프롬프트

```
## 고시문 정보
- 고시번호: {notice_no}
- 고시일자: {notice_date}
- 고시기관: {organ_name}
- 고시유형: {notice_type}
- 위치: {location}
- 중심지 등급: {center_grade}
- 중심지: {center_name}
- 제목: {title}

## 고시 내용
{content}

## 정책 레퍼런스
{policy_reference_content}
```
