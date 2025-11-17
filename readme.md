# ⚾ KBO 야구 경기 일정/성적 데이터 수집 & 웹 서비스 (SQLite + Flask)

KBO 공식 사이트  
▶ https://www.koreabaseball.com/schedule/schedule.aspx  
에서 **경기 일정**, **게임센터 상세 성적(타자/투수 박스 스코어)**를 크롤링하여  
SQLite 데이터베이스에 저장하고, Flask 웹앱으로 조회할 수 있는 프로젝트입니다.

---

# 프로젝트 개요

이 프로젝트는 다음 3가지를 목표로 합니다:

1. **KBO 경기 일정/결과 자동 수집**
2. **게임센터 상세 페이지의 선수 성적(타자/투수) 저장**
3. **Flask 기반 웹서비스에서 날짜/팀/구장으로 조회 후 세부 성적 확인**

---

# 아키텍처 개요

## 수집 대상

- **일정/결과(https://www.koreabaseball.com/schedule/schedule.aspx)**  
  - 날짜, 시간, 팀1, 팀2, 스코어, 구장, 게임센터 URL

- **게임센터 상세 (GameCenter/Main.aspx)**  
  - 타자 박스스코어 (타수·안타·홈런·타점 등)
  - 투수 박스스코어 (이닝·실점·삼진·볼넷 등)

---

## 데이터베이스 구조 (SQLite)

### 주요 테이블
- `game_schedule`
- `teams`
- `players`
- `box_batting`
- `box_pitching`

### 설계 개념
- 팀 / 선수 / 경기 / 기록 테이블로 정규화
- 하나의 경기(`game_id`) 아래 여러 선수 성적이 연결되는 구조

---

# SQLite 스키마 (DDL)

```sql
CREATE TABLE IF NOT EXISTS game_schedule (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  game_date TEXT NOT NULL,         -- 날짜 (예: 10.06)
  weekday TEXT,
  game_time TEXT,
  team1 TEXT,
  team2 TEXT,
  score TEXT,
  gamecenter_url TEXT,
  stadium TEXT
);
