from lib import Data

x = 7

data = Data(x, 1, x, 1, x, 1, x)
print("constrains")
print(data.weight)
print(data.capacity)
print("worths")
print(data.worth, end="\n\n")

y = 2*x

bfAns = data.bruteForce(y, y)
pdAns = data.dynamicProgramming(y, y)
gdAns = data.greedy(y, y)

print("brute force")
print(bfAns)
print("dynamic programming")
print(pdAns)
print("greedy")
print(gdAns)
