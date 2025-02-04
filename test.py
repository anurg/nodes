from datetime import datetime
num = 10
for i in range(num):
    if i > num:
        print("Hello World" + " " + str(i+1))

christmas = datetime(year=2025, month=2, day=1)
birthday = datetime(year=2025, month=10, day=8)
delta =  birthday - christmas 

print(" There are ", delta.days, " between christmas and my birthdsay")