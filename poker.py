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
beforeAllinCredit = 0
#High Card(Top)->One pair->Two pair->Three of kind(Triple)->Straight->Back Straight->Mountain->Flush->Full House->Four cards->Straight Flush->Back Straight Flush->Royal Straight Flush

def print_player_hand(playerHand, Name):
    print(Name," 님께서 지금 가지고 계신 패는",  ','.join(playerHand) ,'입니다.')

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
    global playerList
    highestRankIdx = 0
    if len(rankList) == 1:
        return rankList[0]
    else:
        for i in range(len(playerList)):
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
            return 1
        elif RANK.index(user.playerHandRanking[0]) >= 5 and RANK.index(user.playerHandRanking[0]) < 10:
            return random.randint(3, 5)

        elif RANK.index(user.playerHandRanking[0]) >= 10:
            return random.randint(3, 6)

    else: #후 일때
        if RANK.index(user.playerHandRanking[0]) < 2:
            temp = random.randint(0, 16)
            if temp >= 15:
                return 6
            else:
                return 2

        elif RANK.index(user.playerHandRanking[0]) >= 5 and RANK.index(user.playerHandRanking[0]) < 10:
            return random.randint(3, 5)

        elif RANK.index(user.playerHandRanking[0]) >= 10:
            return random.randint(3, 6)

def betting(selectMenu, user, tableMoney, call):
    global beforeBetting
    global beforeAllinCredit
    global playerList
    global playerName
    global foldedList
    bettingMoney = 0

    if user.money == 0:
        print("소지금이 0원입니다.")
        return bettingMoney

    if selectMenu == 1: #Check

        if call == False:
            print("체크입니다!")
        beforeBetting = 1
        return bettingMoney

    elif selectMenu == 2: #Call
        print("콜입니다!")
        if beforeBetting != 5:
            return betting(beforeBetting, user, tableMoney, True)
        else:
             return betting(5, user, tableMoney, True)

    elif selectMenu == 3: #Half
        beforeBetting = 3
        print("레이즈! 하프입니다!")
        if user.money > tableMoney //2 :
            user.money -= tableMoney // 2
            bettingMoney = tableMoney // 2
            print(bettingMoney, "$ 베팅했습니다")
            return bettingMoney
        else:
            return betting(5, user, tableMoney, False)

    elif selectMenu == 4: #quarter
        beforeBetting = 4
        if call == False:
            print("레이즈! 쿼터입니다!")
        if user.money > tableMoney //2 :
            user.money -= tableMoney // 4
            bettingMoney = tableMoney // 4
            print(bettingMoney, "$ 베팅했습니다")
            return bettingMoney
        else:
            return betting(5, user, tableMoney, False)
        
    elif selectMenu == 5: #Allin
        beforeBetting = 5
        beforeAllinCredit = user.money
        user.money -= beforeAllinCredit
        bettingMoney = beforeAllinCredit
        print(beforeAllinCredit, "$ 베팅했습니다")
        print("올인입니다!")
        return bettingMoney
    elif selectMenu == -1: #Allin on by betting
        if beforeAllinCredit >= user.money:
            beforeAllinCredit = user.money
            user.money -= beforeAllinCredit
            bettingMoney = beforeAllinCredit
            print(beforeAllinCredit, "$ 베팅했습니다")
            print("올인입니다!")
        else:
            user.money -= beforeAllinCredit
            bettingMoney = beforeAllinCredit
            print(beforeAllinCredit, "$ 베팅했습니다")
        return bettingMoney


    else: #Fold
        print("폴드입니다!")
        del playerName[playerList.index(user)]
        playerList.remove(user)
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
        player.money = (BASEMONEY[choiceBaseMoney - 1] - baseBetting)
        tableMoney += baseBetting
        for count in range(4):
            player.playerHand.append(number_to_card(cardInstance.card_draw(),player.playerHandNum, player.playerHandPattern))
        print_player_hand(player.playerHand,playerName[playerList.index(player)])
        
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
        print(playerName[playerList.index(player)], "님의 패는", cardInstance.calculate_ranking(player.handCardList, player.playerHandNum, player.playerHandPattern), "입니다.")
        



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
    inputWating = input   

    for player in playerList:
            print_open_card(player.openCardList,playerName[playerList.index(player)])
            

    #오픈 카드 3장 주기.
    for playTurn in range(4, 7):
        for player in playerList:
            if len(playerName) <= 1:
                highestRankUser = playerName[0]
            else:
                player.playerHand.append(number_to_card(cardInstance.card_draw(),player.playerHandNum, player.playerHandPattern))
                print(playerName[playerList.index(player)],"님의", playTurn, "번째 카드는", player.playerHand[-1], "입니다.")
                player.openCardList.append(player.playerHand[-1])
                player.playerHand[-1] = player.playerHand[-1] + "(open)"
                print_player_hand(player.playerHand, playerName[playerList.index(player)])

            #현재 패 족보 계산.
            player.handCardList_Clear()
            makeHandCard(player.handCardList, player.playerHandNum, player.playerHandPattern)
            rankList.append([playerName[playerList.index(player)],cardInstance.calculate_ranking(player.handCardList, player.playerHandNum, player.playerHandPattern)])
            player.playerHandRanking = cardInstance.calculate_ranking(player.handCardList, player.playerHandNum, player.playerHandPattern)
            print(playerName[playerList.index(player)], "님의 패는",cardInstance.calculate_ranking(player.handCardList, player.playerHandNum, player.playerHandPattern), "입니다.")

            for player in playerList:
                print_open_card(player.openCardList,playerName[playerList.index(player)])
            


    #---------------------베팅----------------------------------------
        print(rankList)
        if len(playerName) <= 1:
            highestRankUser = playerName[0]
        else:
            highestRankUser = rankList[compareRank(rankList)][0]
            print(highestRankUser)
            firstBettingUser = playerList[playerName.index(highestRankUser)]

            print("tablemoney = ", tableMoney)
            if highestRankUser == nickname:
                print("베팅을 선택해주세요.", end = '')
                print("               현재 플레이어의 소유 머니 :", playerList[playerName.index(highestRankUser)].money)
                playerBetting = int(input("1.check, 3.half, 4.quarter, 5.allIn, 6(or Other).fold :"))
                if playerBetting == 2:
                    tableMoney += betting(6, playerList[playerName.index(highestRankUser)], tableMoney, False)
                    
                else:
                    tableMoney += betting(playerBetting, playerList[playerName.index(highestRankUser)], tableMoney, False)
                    
            #컴퓨터가 선일때
            else:
                print(highestRankUser, "의 베팅 턴입니다.")
                playerBetting = computer_betting(firstBettingUser,True)#컴퓨터 베팅 알고리즘.
                tableMoney += betting(playerBetting, playerList[playerName.index(highestRankUser)], tableMoney, False)
                


            #후 베팅
        if len(playerName) <= 1:
            highestRankUser = playerName[0]
        else:
            for BettingUser in playerName:
                if BettingUser != highestRankUser:
                    print("tablemoney = ", tableMoney)
                    if BettingUser == nickname:
                        print("베팅을 선택해주세요.", end = '')
                        print("               현재 플레이어의 소유 머니 :", playerList[playerName.index(BettingUser)].money)
                        playerBetting = int(input("2.call, 3.half, 4.quarter, 5.allIn, 6(or Other).fold :"))
                        if playerBetting == 1:
                            tableMoney += betting(6, playerList[playerName.index(BettingUser)], tableMoney, False)
                            
                        else:
                            tableMoney += betting(playerBetting, playerList[playerName.index(BettingUser)], tableMoney, False)
                            
                    else:
                        print(BettingUser, "의 베팅 턴입니다.")
                        playerBetting = computer_betting(playerList[playerName.index(BettingUser)], False)#컴퓨터 베팅 알고리즘.
                        tableMoney += betting(playerBetting, playerList[playerName.index(BettingUser)], tableMoney, False)
                        

        rankList = []
        #-----------------------------------------------------------


        #히든 카드 1장 주기.
    print("7번째 히든 카드 입니다.")
    for player in playerList:
        player.playerHand.append(number_to_card(cardInstance.card_draw(),player.playerHandNum, player.playerHandPattern))
        print_player_hand(player.playerHand, playerName[playerList.index(player)])
        
        rankList.append([playerName[playerList.index(player)],cardInstance.calculate_ranking(player.handCardList, player.playerHandNum, player.playerHandPattern)])
        player.playerHandRanking = cardInstance.calculate_ranking(player.handCardList, player.playerHandNum, player.playerHandPattern)
        print(playerName[playerList.index(player)], "님의 패는",cardInstance.calculate_ranking(player.handCardList, player.playerHandNum, player.playerHandPattern), "입니다.")
        
        for player in playerList:
            print_open_card(player.openCardList,playerName[playerList.index(player)])
            

        player.handCardList_Clear()
        makeHandCard(player.handCardList, player.playerHandNum, player.playerHandPattern)
        print(playerName[playerList.index(player)], "님의 패는", cardInstance.calculate_ranking(player.handCardList, player.playerHandNum, player.playerHandPattern), "입니다.")
    if len(playerName) <= 1:
        highestRankUser = playerName[0]
    else:
        print(compareRank(rankList))
        print(rankList)
        print(rankList[compareRank(rankList)][0])
        highestRankUser = rankList[compareRank(rankList)][0]
    print("승자는", highestRankUser, "입니다.")
    #이후 우승자에게 테이블 머니만큼 돈 추가.
    #userList 원상복구(Gamelist 이용)
    cardInstance.generate_deck()
    playerList[playerName.index(highestRankUser)].playerMoney += tableMoney
    for i in playerList:
        print(playerName[playerList.index(i)],"님의 현재 소지 금액은", playerList.playerMoney, "$ 입니다.")
    #반복.
