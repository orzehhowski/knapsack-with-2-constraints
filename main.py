from lib import Data, timeOf

TEST_SIZES = [i for i in range(10, 22)]
NUM_PER_SIZE = 3
RESULTS = "results.txt"

with open(RESULTS, "w") as file:
    for testSize in TEST_SIZES:
        print(testSize)
        bf = dp = gd = 0
        for i in range(NUM_PER_SIZE):
            max = testSize
            min = 3
            data = Data(testSize, min, max,
                        min, max, min, max)
            weightConstrain = sum(data.weight) // 4
            capacityConstrain = sum(data.capacity) // 4
            bf += timeOf(data.bruteForce, weightConstrain, capacityConstrain)
            dp += timeOf(data.dynamicProgramming,
                         weightConstrain, capacityConstrain)
            gd += timeOf(data.greedy, weightConstrain, capacityConstrain)

        bf /= NUM_PER_SIZE
        dp /= NUM_PER_SIZE
        gd /= NUM_PER_SIZE
        file.write(
            f'{testSize}\nBF: {round(bf, 6)} DP: {round(dp, 6)} GD: {round(gd, 6)}\n')
