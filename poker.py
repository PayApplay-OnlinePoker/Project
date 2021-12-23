# 01 ~ 13 = Spade
# 14 ~ 26 = Heart
# 27 ~ 39 = Diamond
# 40 ~ 52 = Clover
#S-H-D-C

import random
HAND_RANKING = ["HC", "OP", "TP", "TK", "S", "BS", "MT", "F", "FH", "FC", "SF", "BSF", "RSF"]
CLIENT_CARD = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
CARD_PATTEN = ["S", "H", "D", "C"]
CLIENT_PATTEN = ["Spade", "Heart", "Diamond", "Clover"]
#High Card(Top)->One pair->Two pair->Three of kind(Triple)->Straight->Back Straight->Mountain->Flush->Full House->Four cards->Straight Flush->Back Straight Flush->Royal Straight Flush

class Apicall:
    def join(self, roomID, roomPW):
        pass

    def create(self, roomName, roomPW, baseBetting, baseMoney):
        pass

    def leave(self):
        pass

    def bet(self, check, call, allin, half, quarter, fold, money):
        pass

    def drawCard(self, card, isHidden):
        pass

    def removeCard(self, card):
        pass

    def openCard(self, card):
        pass

    def startGame(self):
        pass

    def checkUserMoney(self, money):
        pass

    def checkTableMoney(self, money):
        pass

    def winner(ID, nickname):
        pass


class Gameplay:
    def __init__(self):
        self.generate_deck()

    def generate_deck(self): #generate card deck
        deck = [i for i in range(1, 53)]
        self.deck = deck


    def card_draw(self): #draw a card
        # 1. draw a card randomly from a list
        drawCard = random.choice(self.deck)
        self.deck.remove(drawCard)
        return drawCard

    def calculate_ranking(self): #hand-ranking
        global HAND_RANKING
        pass

def number_to_card(number):
    if number in range(1, 14): #Spade
        this_card = CLIENT_PATTEN[0] + CLIENT_CARD[number - 1]
        return this_card
    elif number in range(14, 27): #Heart
        this_card = CLIENT_PATTEN[1] + CLIENT_CARD[number - 14]
        return this_card
    elif number in range(27, 40): #Diamond 
        this_card = CLIENT_PATTEN[2] + CLIENT_CARD[number - 27]
        return this_card
    elif number in range(40, 53): #Clover
        this_card = CLIENT_PATTEN[3] + CLIENT_CARD[number - 40]
        return this_card

def print_player_hand():
    global clientHand
    print("지금 가지고 계신 패는",  ','.join(clientHand) ,'입니다.')


#4장을 준다
test = Gameplay()
clientHand = [] #사용자가 보는 것.
playerHand = [] #족보 계산용
#CUI Part
'''
일단 서버와의 통신 없이.  CUI만 구현, 이후 통신이 구현 되면 필요한 부분 수정.
'''
userList = []
roomList = {"Hello" : 1234}
nickname = input("닉네임을 입력하세요. : ")
while nickname in userList: #리스트에 있는 유저 닉네임과 비교, 만약 같은 닉네임이 있으면 생성 제한.
    print("이미 존재하는 닉네임입니다.")
    nickname = input("닉네임을 다시 입력하세요. : ")

while True:
    print("방 생성과 방 참가 중 하나를 선택해주세요. ")
    joinOrCreate = int(input("1.방 생성, 2.방 참가, 3.종료: "))

    if joinOrCreate == 1:#create

        print("방을 생성합니다. ")d
        createRoomName = input("방 제목을 입력해주세요: ")

        createRoomPW = input("방 비밀번호를 입력해주세요: ")

        BASEMONEY = [50, 75, 100]
        print("초기 소지 금액을 선택해주세요.")
        choiceBaseMoney = int(input("1. 50$, 2. 75$, 3. 100$ : "))
        while choiceBaseMoney not in range(1, 4):
            print("1번, 2번, 3번 중 하나를 선택해주세요.")
        createBaseMoney = int(BASEMONEY[choiceBaseMoney -1])

        print("기본 베팅 금액을 설정해주세요. ")
        createBaseBetting = int(input("(1~10사이 숫자를 입력하세요.): "))
        while createBaseBetting not in range(1, 11):
            print("1~10사이 숫자를 입력해주세요.")
        print("호스트:", nickname, ", 방 제목:", createRoomName , ", 비밀번호:",createRoomPW, ", 초기 소지 금액:", str(createBaseMoney) +"$",", 기본 베팅 금액:", str(createBaseBetting) +"$")
        print("방이 생성되었습니다.")    
        break



    elif joinOrCreate == 2:#join
        joinRoomName = input("방 제목을 입력해주세요: ")
        if joinRoomName in roomList:
            joinRoomPW = int(input("비밀번호를 입력해주세요: "))
            if joinRoomPW == roomList[joinRoomName]:
                print("룸에 입장하셨습니다.")
                break
            else:
                print("비밀번호가 일치하지 않습니다.")
                continue
        else:
            print("방이 존재하지 않습니다.")
            continue

    elif joinOrCreate == 3:
        print("게임을 종료합니다.")
        quit()

    else:
        print("잘못된 입력입니다.")


#초기 패 설정
for count in range(4): 
    clientHand.append(number_to_card(test.card_draw()))
print_player_hand()

#카드 한장 버리기
print("1:" + clientHand[0], "2:" + clientHand[1], "3:" + clientHand[2], "4:" + clientHand[3])
removeCard = int(input("버릴 카드를 선택해주세요. : "))
del clientHand[removeCard - 1]

#카드 한장 오픈하기
print("1:" + clientHand[0], "2:" + clientHand[1], "3:" + clientHand[2])

openCard = int(input("오픈할 카드를 선택해주세요. : "))
clientHand[openCard -1] = clientHand[openCard - 1] + "(open)"

#SWAP
swap = clientHand[0] 
clientHand[0] = clientHand[openCard-1]
clientHand[openCard -1 ] = swap
print_player_hand()

#오픈 카드 3장 주기.
for playTurn in range(4, 7):
    print(playTurn, "번째 카드입니다.")
    clientHand.append(number_to_card(test.card_draw()))
    clientHand[-1] = clientHand[-1] + "(open)"
    print_player_hand()

#히든 카드 1장 주기.
print("7번째 카드 입니다.")
clientHand.append(number_to_card(test.card_draw()))
print_player_hand()
