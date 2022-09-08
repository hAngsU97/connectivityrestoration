# 最小字符序问题
# t = int(input())
# for i in range(t):
#     tmp = input().split(' ')
#     n,k = int(tmp[0]),int(tmp[1])
#     s = input()
#     for j in range(k):
#         if s == str('a' * n):
#             break
#         else:
#             sign = 0
#             s_tmp = s[sign:]
#             for index in range(len(s_tmp)):
#                 if s_tmp[index] != 'a':
#                     s_tmp[index] = chr(ord(s_tmp[index])-1)
#                 elif s[sign] == 'a':
#                     sign += 1
#                     k -= 1
#                 if sign == n:
#                     break
#                 s = s[sign:]+s_tmp
#     print(''.join(s))

# #多多排名期望问题
# import math
# shuru = input().split() # 人数、容量、排名
# n,c,r = int(shuru[0]), int(shuru[1]),int(shuru[2])
# room_num = math.ceil(n/c) # 教室数
# rest = n%room_num # 最后一层人数
# roll = math.floor(n/room_num)
# grades = []
# for _ in range(n):
#     shuru1 = input().split()
#     grades.append(int(shuru1[1]))
#
# sorted(grades)
# A = 0
# for i in range(roll):
#     for j in range(room_num):
#         if i*room_num + j < n-rest:
#             if i*room_num <= r-1 and (i+1)*room_num > r-1 :
#                 continue
#             else:
#                 A += grades[i*room_num+j]
# A /= room_num
# B = 0
# if rest != 0:
#     B = sum(grades[n-rest:])/rest
#
# print("A:",A,"B:",B,"剩余人数:",rest,"层数:",roll,"教室数:",room_num)
# res = (A+B+grades[r-1])*(rest/room_num)/(roll+1) + (A+grades[r-1])*(1-rest/room_num)/roll if rest != 0 else (A+grades[r-1])/roll
#
# print(res)


# 寻找美丽数问题
# def findmeilishu(t,Ls,Rs,ts):
#     counts = []
#     for i in range(t):
#         count = 0
#         for num in range(Ls[i],Rs[i]+1):
#             s = [int(n) for n in str(num).split()]
#             l = s[0]
#             if len(s)>1:
#                 for p in s[1:]:
#                     l ^= p
#         if l == ts[i]:
#             counts.append(count)
#
#     res = ''
#     for i in range(t-1):
#         res += str(counts[i])+' '
#     res += str(counts[-1])
#
#     print(res)
#     return res
#
#
# t = int(input())
# Ls = [int(n) for n in input.split()]
# Rs = [int(n) for n in input.split()]
# ts = [int(n) for n in input().split()]
#
# for i in range(t):
#     count = 0
#     l = 0
#     for num in range(Ls[i],Rs[i]+1):
#         s = [int(n) for n in list(str(num))]
#         l = s[0]
#         if len(s)>1:
#             for p in s[1:]:
#                 l ^= p
#         if l == ts[i]:
#             count += 1
#     print(count,end="")

# # 打印美丽数
#
# for i in range(1,70001):
#     s = [int(n) for n in list(str(i))]
#     l = s[0]
#     if len(s) > 1:
#         for p in s[1:]:
#             l ^= p
#     print(str(l)+(',' if i != 70000 else ""),end='')
#     if i % 50 == 0:
#         print()


# MVC框架： 控制、界面、数据库
# SSH：struts、spring、hibernate
# SSM：springMVC、spring、Mybatis