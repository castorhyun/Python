# coding: utf-8

print("hello world")

aa = 124
ab = -154
ac = 0

print(aa)
print(ab)
print(ac)

bb = 23.222
print(bb)


bb = 32.4E-2
print(bb)



print("테스트중  : I`m OK!!! ")


# /n 개행
# /r 캐리지 리턴
# /" 큰 따움표 출력
# /' 작은 따옴표 출력
# /000 : null 문자
# /t


a= "hello, It`s Python Class"
b= "Nice to meet you"

print(a+b)

c= "multiply str"


print("*" *30)
print(c)
print("*" *30)


## 인덱싱 / 슬라이싱

str = "you`ve got friend"

print(str[4])


for x in xrange( 0,len(str) ):
	print(str[x])
	pass

print(str[-6:-0])


str = "20160303121300"

date = str[:8]
time = str[8:]

print(date)
print(time)
