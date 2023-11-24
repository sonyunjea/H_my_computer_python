

s: str = "aaccbbbd"
compare: str = ""
count: int = 1

for i in range(len(s)-1):
    if s[i] == s[i+1]:
        count +=1
    else:
        compare += s[i] +str(count)
        count =1

compare += s[-1] +str(count)

print("입력된 문자열은",compare)

