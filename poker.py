# 01 ~ 13 = Spade
# 14 ~ 26 = Heart
# 27 ~ 39 = Diamond
# 40 ~ 52 = Clover
#S-H-D-C

#imports
import random
import time
import library


#constants
CLIENT_CARD = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
CARD_NUM = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
CLIENT_PATTEN = ["Spade", "Heart", "Diamond", "Clover"]
CARD_PATTEN = ["S", "H" , "D" ,"C"]
handCardList = [int(0) for i in range(17) ]
BASEMONEY = [50, 75, 100]
RANK = ["High Card","One Pair","Two Pair","Three of kind","Straight","Back Straight","Mountain","Flush","Full House","Four cards","Straight Flush","Back Straight Flush","Royal Straight Flush"]
rankList = []
foldedList = []
beforeBetting = 0
beforeCredit = 0
#High Card(Top)->One pair->Two pair->Three of kind(Triple)->Straight->Back Straight->Mountain->Flush->Full House->Four cards->Straight Flush->Back Straight Flush->Royal Straight Flush

def print_player_hand(playerHand, Name):
    print(Name,"님께서 지금 가지고 계신 패는",  ','.join(playerHand) ,'입니다.')

def print_open_card(openCardList, Name):
    print(Name,"님의 오픈된 카드는", ",".join(openCardList), "입니다.")

def number_to_card(number, playerHandNum, playerHandPattern):
    if number in range(1, 14): #Spade
        this_card = CLIENT_PATTEN[0] + CLIENT_CARD[number - 1]
        cardPatten = CARD_PATTEN[0]
        cardNum = CARD_NUM[number - 1]
        playerHandNum.append(cardNum)
        playerHandPattern.append(cardPatten)
        return this_card
    elif number in range(14, 27): #Heart
        this_card = CLIENT_PATTEN[1] + CLIENT_CARD[number - 14]
        cardPatten = CARD_PATTEN[1]
        cardNum = CARD_NUM[number - 14]
        playerHandNum.append(cardNum)
        playerHandPattern.append(cardPatten)
        return this_card
    elif number in range(27, 40): #Diamond
        this_card = CLIENT_PATTEN[2] + CLIENT_CARD[number - 27]
        cardPatten = CARD_PATTEN[2]
        cardNum = CARD_NUM[number - 27]
        playerHandNum.append(cardNum)
        playerHandPattern.append(cardPatten)
        return this_card
    elif number in range(40, 53): #Clover
        this_card = CLIENT_PATTEN[3] + CLIENT_CARD[number - 40]
        cardPatten = CARD_PATTEN[3]
        cardNum = CARD_NUM[number - 40]
        playerHandNum.append(cardNum)
        playerHandPattern.append(cardPatten)
        return this_card

def makeHandCard(handCardList, playerHandNum, playerHandPattern):
    for number in playerHandNum:
        handCardList[number - 1] += 1
    for pattern in playerHandPattern:
        if pattern == "S":
            handCardList[13] += 1
        elif pattern == "H":
            handCardList[14] += 1
        elif pattern == "D":
            handCardList[15] += 1
        else:
            handCardList[16] += 1

#선(랭크 높은 사람)판정
def compareRank(rankList):
    global RANK
    global CARD_PATTEN
    global betters

    highestRankIdx = 0
    if len(rankList) == 1:
        return rankList[0]
    else:
        for i in range(len(betters)):
            if RANK.index(rankList[highestRankIdx][1][0]) < RANK.index(rankList[i][1][0]):
                highestRankIdx = i
            elif RANK.index(rankList[highestRankIdx][1][0]) == RANK.index(rankList[i][1][0]):
                if rankList[highestRankIdx][1][1] < rankList[i][1][1]:
                    if rankList[highestRankIdx][1][1] != 1:
                        highestRankIdx = i
                elif rankList[highestRankIdx][1][1] == rankList[i][1][1]:
                    if CARD_PATTEN.index(rankList[highestRankIdx][1][2]) > CARD_PATTEN.index(rankList[i][1][2]):
                        highestRankIdx = i
        return highestRankIdx

def computer_betting(user, First):
    if First == True: #선 일때
        if RANK.index(user.playerHandRanking[0]) < 2:
            temp = random.choice([1,3,3,3,4,4])
            return temp
        elif RANK.index(user.playerHandRanking[0]) >= 5 and RANK.index(user.playerHandRanking[0]) < 10:
            return random.randint(3, 5)

        elif RANK.index(user.playerHandRanking[0]) >= 10:
            return random.randint(3, 5)

    else: #후 일때
        if RANK.index(user.playerHandRanking[0]) < 2:
            temp = random.randint(2, 4)
            return temp


        elif RANK.index(user.playerHandRanking[0]) >= 5 and RANK.index(user.playerHandRanking[0]) < 10:
            return random.randint(3, 5)

        elif RANK.index(user.playerHandRanking[0]) >= 10:
            return random.randint(3, 5)

def betting(selectMenu, user, tableMoney):
    global beforeBetting
    global beforeCredit
    global betters
    global bettersName
    global foldedList
    bettingMoney = 0

    if user.playerMoney == 0:
        print("소지금이 0원입니다.")
        return bettingMoney

    if selectMenu == 1: #Check
        print("체크입니다!")
        beforeBetting = 1
        return bettingMoney

    elif selectMenu == 2: #Call
        print("콜입니다!")
        bettingMoney = beforeCredit
        if user.playerMoney > bettingMoney :
            user.playerMoney -= bettingMoney
            print(bettingMoney, "$ 베팅했습니다")
            return bettingMoney
        else:
            return betting(-1, user, tableMoney)

    elif selectMenu == 3: #Half
        beforeBetting = 3
        print("레이즈! 하프입니다!")
        if user.playerMoney > tableMoney //2 :
            user.playerMoney -= tableMoney // 2
            bettingMoney = tableMoney // 2
            beforeCredit = bettingMoney
            print(bettingMoney, "$ 베팅했습니다")
            return bettingMoney
        else:
            return betting(-1, user, tableMoney)

    elif selectMenu == 4: #quarter
        beforeBetting = 4
        print("레이즈! 쿼터입니다!")
        if user.playerMoney > tableMoney //2 :
            user.playerMoney -= tableMoney // 4
            bettingMoney = tableMoney // 4
            beforeCredit = bettingMoney
            print(bettingMoney, "$ 베팅했습니다")
            return bettingMoney
        else:
            return betting(-1, user, tableMoney)

    elif selectMenu == 5: #Allin
        beforeBetting = 5
        beforeCredit = user.playerMoney
        user.playerMoney -= beforeCredit
        bettingMoney = beforeCredit
        print(beforeCredit, "$ 베팅했습니다")
        print("올인입니다!")
        return bettingMoney
    elif selectMenu == -1: #Allin on by betting
        if beforeCredit >= user.playerMoney:
            beforeCredit = user.playerMoney
            user.playerMoney -= beforeCredit
            bettingMoney = beforeCredit
            print(beforeCredit, "$ 베팅했습니다")
            print("올인입니다!")
        else:
            user.playerMoney -= beforeCredit
            bettingMoney = beforeCredit
            print(beforeCredit, "$ 베팅했습니다")
        return bettingMoney


    else: #Fold
        print("폴드입니다!")
        del bettersName[betters.index(user)]
        betters.remove(user)
        return bettingMoney




cardInstance = library.Gameplay()
tableMoney = 0
nickname = "NEVERNEVERSETHISNICKNAME"
playerName = ["Com1", "Com2", "com3"]
GameName = ["Com1", "Com2", "com3" ]
#초기화면

#초기 설정
while (len(playerName) != 1) or nickname in playerName:
    playerList = [library.Player() for i in range(4)]
    playerName = ["Com1", "Com2", "com3"]

    if nickname == "NEVERNEVERSETHISNICKNAME":
        print('---------------')
        nickname = input("닉네임을 입력하세요. : ")
        playerName.insert(0, nickname)
        GameName.insert(0, nickname)
        print("게임 시작과 게임 종료 중 하나를 선택해주세요. ")
        joinOrCreate = int(input("1.게임 시작, 2.게임 종료 : "))
        if joinOrCreate == 1:#create
            print("시작하기에 앞서, 기본적인 설정을 진행합니다.")
            print("초기 소지 금액을 선택해주세요.")
            choiceBaseMoney = int(input("1. 50$, 2. 75$, 3. 100$ : "))
            while choiceBaseMoney not in range(1, 4):
                print("1번, 2번, 3번 중 하나를 선택해주세요.")
                choiceBaseMoney = int(input("1. 50$, 2. 75$, 3. 100$ : "))
            baseMoney = int(BASEMONEY[choiceBaseMoney -1])
            print("기본 베팅 금액을 설정해주세요. ")
            baseBetting = int(input("(1~10사이 숫자를 입력하세요.): "))
            while baseBetting not in range(1, 11):
                print("1~10사이 숫자를 입력해주세요.")
                baseBetting = int(input("(1~10사이 숫자를 입력하세요.): "))
        elif joinOrCreate == 2:
            print("게임을 종료합니다.")
            exit()
        else:
            print("잘못된 입력입니다.")

    else:
        playerName.insert(0, nickname)
        print("게임을 시작합니다.")

    for player in playerList:
        player.playerMoney = (BASEMONEY[choiceBaseMoney - 1] - baseBetting)
        tableMoney += baseBetting
        for count in range(4):
            player.playerHand.append(number_to_card(cardInstance.card_draw(),player.playerHandNum, player.playerHandPattern))
    print_player_hand(playerList[0].playerHand,playerName[0])

    #카드 한장 버리기
    print("1:" + playerList[playerName.index(nickname)].playerHand[0], "2:" + playerList[playerName.index(nickname)].playerHand[1], "3:" + playerList[playerName.index(nickname)].playerHand[2], "4:" + playerList[playerName.index(nickname)].playerHand[3])
    removeCard = int(input("버릴 카드를 선택해주세요. : "))
    del playerList[playerName.index(nickname)].playerHand[removeCard - 1]
    del playerList[playerName.index(nickname)].playerHandNum[removeCard - 1]
    del playerList[playerName.index(nickname)].playerHandPattern[removeCard - 1]

    for computer in playerList[1:]:
        removeCard = random.randint(1, 4)
        del computer.playerHand[removeCard - 1]
        del computer.playerHandNum[removeCard - 1]
        del computer.playerHandPattern[removeCard - 1]

    #현재 패 족보 계산.
    for player in playerList:
        player.handCardList_Clear()
        makeHandCard(player.handCardList, player.playerHandNum, player.playerHandPattern)
        player.playerHandRanking = cardInstance.calculate_ranking(player.handCardList, player.playerHandNum, player.playerHandPattern)
    print(playerName[0], "님의 패는", cardInstance.calculate_ranking(playerList[0].handCardList, playerList[0].playerHandNum, playerList[0].playerHandPattern), "입니다.")

    #카드 한장 오픈하기
    print("1:" + playerList[playerName.index(nickname)].playerHand[0], "2:" + playerList[playerName.index(nickname)].playerHand[1], "3:" + playerList[playerName.index(nickname)].playerHand[2])

    openCard = int(input("오픈할 카드를 선택해주세요. : "))
    playerList[playerName.index(nickname)].openCardList.append(playerList[playerName.index(nickname)].playerHand[openCard -1])
    playerList[playerName.index(nickname)].playerHand[openCard -1] = playerList[playerName.index(nickname)].playerHand[openCard - 1] + "(open)"

    #PlayerHandSWAP
    swap = playerList[playerName.index(nickname)].playerHand[0]
    playerList[playerName.index(nickname)].playerHand[0] = playerList[playerName.index(nickname)].playerHand[openCard-1]
    playerList[playerName.index(nickname)].playerHand[openCard -1 ] = swap

    #PlayerHandNumSWAP
    swap = playerList[playerName.index(nickname)].playerHandNum[0]
    playerList[playerName.index(nickname)].playerHandNum[0] = playerList[playerName.index(nickname)].playerHandNum[openCard-1]
    playerList[playerName.index(nickname)].playerHandNum[openCard -1 ] = swap

    #PlayerHandPatternSWAP
    swap = playerList[playerName.index(nickname)].playerHandPattern[0]
    playerList[playerName.index(nickname)].playerHandPattern[0] = playerList[playerName.index(nickname)].playerHandPattern[openCard-1]
    playerList[playerName.index(nickname)].playerHandPattern[openCard -1 ] = swap

    for computer in playerList[1:]:
        openCard = random.randint(1, 3)
        computer.openCardList.append(computer.playerHand[openCard -1])
        computer.playerHand[openCard -1] = computer.playerHand[openCard - 1] + "(open)"

    print_player_hand(playerList[playerName.index(nickname)].playerHand,playerName[0])

    for player in playerList:
            print_open_card(player.openCardList,playerName[playerList.index(player)])

    inputWating = input("계속하시려면 (enter)를 눌러주세요...") system('clear')


    #오픈 카드 3장 주기.
    betters = playerList[:]
    bettersName = playerName[:]
    for playTurn in range(4, 7):
        for player in betters:
            if len(bettersName) <= 1:
                highestRankUser = bettersName[0]

            else:
                player.playerHand.append(number_to_card(cardInstance.card_draw(),player.playerHandNum, player.playerHandPattern))
                player.openCardList.append(player.playerHand[-1])
                player.playerHand[-1] = player.playerHand[-1] + "(open)"

            #현재 패 족보 계산.
            player.handCardList_Clear()
            makeHandCard(player.handCardList, player.playerHandNum, player.playerHandPattern)
            rankList.append([bettersName[betters.index(player)],cardInstance.calculate_ranking(player.handCardList, player.playerHandNum, player.playerHandPattern)])
            player.playerHandRanking = cardInstance.calculate_ranking(player.handCardList, player.playerHandNum, player.playerHandPattern)
        if betters[0] == playerList[0]:
            print(bettersName[0],"님의", playTurn, "번째 카드는", betters[0].playerHand[-1], "입니다.")
            print_player_hand(betters[bettersName.index(nickname)].playerHand,bettersName[0])
            print(bettersName[0], "님의 패는", cardInstance.calculate_ranking(betters[0].handCardList, betters[0].playerHandNum, betters[0].playerHandPattern), "입니다.")
            for player in betters:
                print_open_card(player.openCardList,bettersName[betters.index(player)])

        inputWating = input("계속하시려면 (enter)를 눌러주세요...") system('clear')


    #---------------------베팅----------------------------------------
        if len(bettersName) <= 1:
            highestRankUser = bettersName[0]
        else:
            highestRankUser = rankList[compareRank(rankList)][0]
            firstBettingUser = betters[bettersName.index(highestRankUser)]

            print("tablemoney = ", tableMoney)
            if highestRankUser == nickname:
                print("베팅을 선택해주세요.", end = '')
                print("               현재 플레이어의 소유 머니 :", playerList[bettersName.index(highestRankUser)].playerMoney)
                playerBetting = int(input("1.check, 3.half, 4.quarter, 5.allIn, 6(or Other).fold :"))
                if playerBetting == 2:
                    tableMoney += betting(6, betters[bettersName.index(highestRankUser)], tableMoney)

                else:
                    tableMoney += betting(playerBetting, betters[bettersName.index(highestRankUser)], tableMoney)

            #컴퓨터가 선일때
            else:
                print(highestRankUser, "의 베팅 턴입니다.")
                playerBetting = computer_betting(firstBettingUser,True)#컴퓨터 베팅 알고리즘.
                tableMoney += betting(playerBetting, betters[bettersName.index(highestRankUser)], tableMoney)

            inputWating = input("계속하시려면 (enter)를 눌러주세요...") system('clear')


            #후 베팅
        if len(bettersName) <= 1:
            highestRankUser = bettersName[0]
        else:
            for BettingUser in bettersName:
                if BettingUser != highestRankUser:
                    print("tablemoney = ", tableMoney)
                    if BettingUser == nickname:
                        print("베팅을 선택해주세요.", end = '')
                        print("               현재 플레이어의 소유 머니 :", betters[bettersName.index(BettingUser)].playerMoney)
                        playerBetting = int(input("2.call, 3.half, 4.quarter, 5.allIn, 6(or Other).fold :"))
                        if playerBetting == 1:
                            tableMoney += betting(6, betters[bettersName.index(BettingUser)], table)

                        else:
                            tableMoney += betting(playerBetting, betters[bettersName.index(BettingUser)], tableMoney)

                    else:
                        print(BettingUser, "의 베팅 턴입니다.")
                        playerBetting = computer_betting(betters[bettersName.index(BettingUser)], False)#컴퓨터 베팅 알고리즘.
                        tableMoney += betting(playerBetting, betters[bettersName.index(BettingUser)], tableMoney)

        inputWating = input("계속하시려면 (enter)를 눌러주세요...") system('clear')

        rankList = []
        beforeCredit = 0
        #-----------------------------------------------------------


        #히든 카드 1장 주기.
    print("7번째 히든 카드 입니다.")
    for player in betters:
        player.playerHand.append(number_to_card(cardInstance.card_draw(),player.playerHandNum, player.playerHandPattern))
        print_player_hand(player.playerHand, bettersName[betters.index(player)])

        rankList.append([bettersName[betters.index(player)],cardInstance.calculate_ranking(player.handCardList, player.playerHandNum, player.playerHandPattern)])
        player.playerHandRanking = cardInstance.calculate_ranking(player.handCardList, player.playerHandNum, player.playerHandPattern)
        player.handCardList_Clear()
        makeHandCard(player.handCardList, player.playerHandNum, player.playerHandPattern)
        print(bettersName[betters.index(player)], "님의 패는", cardInstance.calculate_ranking(player.handCardList, player.playerHandNum, player.playerHandPattern), "입니다.")

    if len(bettersName) <= 1:
        highestRankUser = bettersName[0]
    else:
        highestRankUser = rankList[compareRank(rankList)][0]
    print("승자는", highestRankUser, "입니다.")
    #이후 우승자에게 테이블 머니만큼 돈 추가.
    #userList 원상복구(Gamelist 이용)
    cardInstance.generate_deck()
    betters[bettersName.index(highestRankUser)].playerMoney += tableMoney
    for i in playerList:
        print(playerName[playerList.index(i)],"님의 현재 소지 금액은", i.playerMoney, "$ 입니다.")
        player.clear()
    QuestionGame = input("종료하시려면 1번을, 계속하시려면 그 외 아무키나 눌러주세요. ")
    if QuestionGame == "1":
        exit()
    else:
        pass

    #반복.
