# 01 ~ 13 = Spade
# 14 ~ 26 = Heart
# 27 ~ 39 = Diamond
# 40 ~ 52 = Clover

import random
card = [i for i in range(1, 53)] #카드 덱 생성
hand_Rankings = [] #카드 족보

print(card)

# 카드 뽑기
# 1. 리스트중 랜덤으로 하나를 뽑는 방법.
print("-------------1. 리스트중 랜덤으로 하나를 뽑는 방법. ---------------")
for i in range(52):
    drawCard = random.choice(card)
    print(drawCard)

# 2. 리스트를 셔플 한 뒤, 처음 리스트부터 뽑는 방법.
print("-------------2. 리스트를 셔플 한 뒤, 처음 리스트부터 뽑는 방법.---------------")
random.shuffle(card)
for i in range(52):
    drawCard = card[i]
    print(drawCard)





