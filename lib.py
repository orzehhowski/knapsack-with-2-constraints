import copy
import random
import time


class Data:
    def __init__(self, size, minWeight, maxWeight, minCapacity, maxCapacity, minWorth, maxWorth):
        self.size = size
        self.vals = [[i] for i in range(self.size)]
        self.weight = []
        self.worth = []
        self.capacity = []
        for i in range(size):
            # generowanie losowych wartosci z danych przedzialow
            weight = random.randint(minWeight, maxWeight)
            worth = random.randint(minWorth, maxWorth)
            capacity = random.randint(minCapacity, maxCapacity)
            # weight[i] = waga przedmiotu o indeksie i
            self.weight.append(weight)
            self.worth.append(worth)
            self.capacity.append(capacity)
            # vals[i][0] = index   vals[i][1] = weight   vals[i][2] = capacity     vals[i][3] = worth
            # to do latwiejszego sortowania heurystyki
            self.vals[i].append(weight)
            self.vals[i].append(capacity)
            self.vals[i].append(worth)

    def bruteForce(self, weightConstrain, capacityConstrain):
        maxResult = 0
        ans = []

        # iterowanie po wszystkich podzbiorach przedmiotow
        for i in range(2 ** self.size):
            # generowanie binarnej reprezentacji podzbioru
            # binStr wyglada jak b0101
            binStr = str(bin(i))
            # tablica na rozwiazanie problemu
            answerArray = [0 for j in range(self.size)]
            # index przedmiotu
            currentIndex = self.size - 1
            # index cyfry binarnej reprezentacji podzbioru odpowiadajacy
            # aktualnemu przedmiotowi
            binIndex = len(binStr) - 1
            # binarna cyfra odpowiadajaca przedmiotowi
            current = binStr[binIndex]

            worth = 0
            weight = 0
            capacity = 0
            while current != 'b':
                # jesli current = '1' przedmiot nalezy do podzbioru
                if current == '1':
                    answerArray[currentIndex] = int(current)

                    worth += self.worth[currentIndex]
                    weight += self.weight[currentIndex]
                    capacity += self.capacity[currentIndex]
                currentIndex -= 1
                binIndex -= 1
                current = binStr[binIndex]

            # jesli podzbior spelnia ograniczenia jego wartosc
            # porownywana jest z maksymalna wczesniej uzyskana wartoscia
            if weight <= weightConstrain and capacity <= capacityConstrain:
                if maxResult < worth:
                    ans = answerArray
                    maxResult = worth
        return ans, maxResult

    def dynamicProgramming(self, weightConstrain, capacityConstrain):
        # inicjalizuje trojwymiarowa macierz wypelniona zerami:
        elementsCount = self.size
        matrix3d = [[[0 for _ in range(capacityConstrain + 1)] for _ in range(
            weightConstrain + 1)] for _ in range(elementsCount + 1)]
        '''
            i - rozmiar podproblemu
            l - ograniczenie wagi podproblemu
            m - ograniczenie objetosci podproblemu

            wypelniam macierz - szukam elementu 
            matrix3d[elementsCount - 1][weightConstrain][capacityConstrain]

            i = 0 oznacza, ze nie mam do dyspozycji zadnego przedmiotu
            i = 1 oznacza, ze mam do dyspozycji 1 przedmiot o indeksie 0
            troche pogmatwane
            dlatego musze uzywac i-1 przy pobieraniu danych z tablic obiektu self
        '''
        for i in range(1, elementsCount + 1):
            for l in range(1, weightConstrain + 1):
                for m in range(1, capacityConstrain + 1):
                    if (self.weight[i-1] > l or self.capacity[i-1] > m):
                        matrix3d[i][l][m] = matrix3d[i - 1][l][m]
                    else:
                        matrix3d[i][l][m] = max(
                            matrix3d[i - 1][l][m],
                            matrix3d[i - 1][l - self.weight[i-1]][m - self.capacity[i-1]] + self.worth[i-1])

        # odczytanie tablicy wynikowej
        answerArray = [0 for _ in range(elementsCount)]
        current = elementsCount
        currentL = weightConstrain
        currentM = capacityConstrain
        while (current > 0):
            if matrix3d[current][currentL][currentM] != matrix3d[current - 1][currentL][currentM]:
                answerArray[current - 1] = 1
                currentL -= self.weight[current - 1]
                currentM -= self.capacity[current - 1]
            current -= 1

        return answerArray, matrix3d[elementsCount][weightConstrain][capacityConstrain]

    def greedy(self, weightConstrain, capacityConstrain):
        vals = copy.deepcopy(self.vals)
        # posortowane po weight * capacity / worth
        vals.sort(key=lambda x: x[1]*x[2]/x[3])

        worth = 0
        weight = 0
        capacity = 0
        i = 0
        answerArray = [0 for _ in range(self.size)]
        while i < self.size:
            weight += vals[i][1]
            capacity += vals[i][2]
            if weight <= weightConstrain and capacity <= capacityConstrain:
                worth += vals[i][3]
                answerArray[vals[i][0]] = 1
                i += 1
            else:
                break
        return answerArray, worth


def timeOf(function, weightConstrain, capacityConstrain):
    y = time.time()
    function(weightConstrain, capacityConstrain)
    x = time.time()
    return x - y
