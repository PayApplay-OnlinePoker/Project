# 페어플레이 프로젝트
## 프로젝트 정보
### 프로젝트 명
온라인 포커
### 프로젝트 참가 멤버
* 윤성우
* 이지형
* 이지관
## 포커 규칙
### 베팅
* 체크
* 콜
* 폴드
* 하프
* 쿼터
* 올인
* 방 생성 화면에서 기본 판돈, 초기 지급 돈 결정
### 족보
* 스하다클
* High Card(Top)
* One pair
* Two pair
* Three of kind(Triple)
* Straight
* Back Straight
* Mountain
* Flush
* Full House
* Four cards
* Straight Flush
* Back Straight Flush
* Royal Straight Flush
## 게임 진행
### 카드
#### 초기 세팅
* 각 플레이어는 4장의 카드를 받음.
* 받은 카드중 1장을 버림(비공개)
* 남은 카드중 1장을 공개함
* 이후 공개패를 받고 베팅 3회 반복.
* 히든카드를 받고(자신은 봄) 마지막 베팅
### 베팅
* 선은 체크, 레이즈, 폴드를 할 수 있음.
    * 레이즈는 하프, 쿼터, 올인
* 이후 사람은 콜, 레이즈, 폴드를 할 수 있음.
* 모든 사람이 콜 혹은 폴드를 할 때까지 반복.
* 각 베팅별 인당 레이즈 가능 횟수는 2회.
### 프로그램 초기 화면
* 닉네임을 적는다.
* 서버에 닉네임을 전송하면 서버가 ID를 알려준다.
* 이후 방 생성 혹은 방 참가를 한다.
### 방 생성
* 호스트는 방을 생성할 때 방의 이름, 비밀번호, 기본 판돈, 초기 자금을 설정한다.
    * 초기 자금 : 50, 75, 100중 택1
    * 기본 판돈 : 1~10 범위 내에서
* 호스트가 방을 나가면 방이 제거된다.
### 방 참가
* 참여자는 리스트 되어있는 방중 원하는 방을 선택한다.
* 선택한 방의 패스워드를 입력하면 참가한다.
* 참여한 방에서 나가면 소지금은 초기화된다.
## 내부 구현
### 코드 스타일
#### 인덴트
* 4 space
#### 변수명
* camelCase
#### 함수명
* snake\_case
#### 타입명
* PascalCase
### 카드
* 01 ~ 13 : 스페이드(S)
* 14 ~ 26 : 하트(H)
* 27 ~ 39 : 다이아몬드(D)
* 40 ~ 52 : 클로버(C)
### API
* callerID destinationID Command Arguments
* serverID : 0
#### Commands
* join
    * roomID
        * roomPW
* create
    * roomName
        * roomPW
            * baseBetting
                * baseMoney
* leave
* bet
    * check
    * call
    * (many many raises)
        * money
    * fold
* drawCard
    * card
        * isHidden
* discard
    * card
* openCard
    * card
* startGame
* checkUserMoney
    * money
* checkTableMoney
    * money
* winner
    * ID
        * nickname
* response
    * forwarded
        * destinationID
    * registered
        * ID
    * joined
        * hostID
    * leaved
        * roomID
    * betted
    * created
        * roomID
    * cardReceived
        * ID
            * cardNumber
            * -1
    * badRequest
        * noSuchID
            * destinationID
        * callerIDNotMatched
            * expectedID
        * wrongCommand
    * joinRoomError
        * noSuchRoomID
            * roomID
        * roomIsFull
            * roomID
        * passwordNotMatched
            * roomID
        * alreadyJoined
            * requestedRoomID
                * currentJoinedRoomID
    * badResponse
        * unexpectedCommand
            * command
        * unexpectedAck
            * ack
    * fetch
        * rooms
            * start
            * end
            * room
                * roomID
                    * roomName
                        * baseBetting
                            * baseMoney
                                * hostNickname
        * users
            * end
            *user
                * userID
                    * userNickname
                        * userMoney
* register
    * nickname
* othersCard
    * ID
        * cardNumber
        * -1(hidden)
* fetch
    * rooms
### 서버 구현
* 포트 : 31597
