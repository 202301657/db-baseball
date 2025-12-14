# ⚾ KBO 야구 경기 일정/성적 데이터 수집 & 웹 서비스 (SQLite + Flask)

KBO 공식 사이트  
▶ https://www.koreabaseball.com/schedule/schedule.aspx  
에서 경기 일정, 게임센터 상세 성적(타자 박스 스코어)를 참고하여 SQLite 데이터베이스에 저장하고, Flask 웹앱으로 조회할 수 있는 프로젝트입니다.

---

## 프로젝트 개요

이 프로젝트는 다음 3가지를 목표로 합니다:

1. **KBO 경기 일정/결과 수집**
2. **게임센터 상세 페이지의 선수 성적(타자) 저장**
3. **Flask 기반 웹서비스에서 날짜/팀/구장으로 조회 후 세부 성적 확인**

---
## 시연 영상 
아래 사진을 클릭하시면 영상을 다운로드 받으실 수 있습니다. 
[![시연 영상](database_img.png)](데이터베이스_과제_시연영상_염보은.mp4)

## 참고 자료
https://www.notion.so/2b14a4fafdfe80188aece49729f8c6bc?source=copy_link

---

## 아키텍처 개요

### 1. 수집 대상

#### (1) 일정/결과  
- URL: `https://www.koreabaseball.com/schedule/schedule.aspx`  
- 수집 필드
  - 날짜
  - 시간
  - 팀1
  - 팀1 점수
  - 팀2 점수
  - 팀2
  - 승리팀
  - 리뷰
  - 구장

#### (2) 게임센터 상세
- **경기 리뷰 (_ vs _)**
  - 팀 기록 
  - 팀1 타자 기록
  - 팀2 타자 기록

- **타자 박스스코어**
  - 선수명
  - 타수
  - 안타
  - 타점
  - 득점
  - 타율

---

## 데이터베이스 구조 (SQLite)

### 주요 테이블

- `batting`
- `games`
- `sqlite_sequence`
- `team_stats`

### 설계 개념

- 팀 / 선수 / 경기 / 기록 테이블로 **정규화**
- 하나의 경기(`game_id`) 아래 선수 성적(`batting`)이 연결되는 구조

---

## SQLite 스키마 (DDL)

(1) games 테이블
```sql
CREATE TABLE games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    time TEXT,
    team1 TEXT,
    team2 TEXT,
    stadium TEXT,
    score_team1 INTEGER,
    score_team2 INTEGER,
    winner TEXT,
    gamecenter_url TEXT
);
```
(2) team_stats 테이블
```sql
CREATE TABLE team_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER,
    team TEXT,
    hits INTEGER,
    home_runs INTEGER,
    avg REAL,
    strikeouts INTEGER,
    stolen_bases INTEGER,
    errors INTEGER,
    double_plays INTEGER,
    left_on_base INTEGER,
    walks INTEGER,
    FOREIGN KEY (game_id) REFERENCES games(id)
);
```
(3) batting 테이블
```sql 
CREATE TABLE batting (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER,
    player_name TEXT,
    at_bats INTEGER,
    hits INTEGER,
    rbi INTEGER,
    run INTEGER,
    avg REAL,
    team TEXT,
    FOREIGN KEY (game_id) REFERENCES games(id)
);
```