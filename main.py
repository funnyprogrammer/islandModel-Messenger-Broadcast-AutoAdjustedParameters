import plotting as plot
import recording as record
import cycle as cycle
import initialPopulation as iniPop
import operators as op
import fitness as fit
import islands as isl
import logs as logs
import multiprocessing
import copy
import newsimulatedAnnealing as sa
from ast import literal_eval
from datetime import datetime
from functools import partial

import pandas as pd

log_list = [0, 8, 31, 23, 35, 2, 17, 26, 32, 36, 4, 27, 33, 6, 34, 37]

numberOfParametersCombinations = 10
numberOfThreads = 4
numberOfRounds = 5

def runRound(par, parComb, parCount, logIndex, numberOfThreads, round, broadcast, messenger, progressions, definitions, islandSizes, percentageOfBestIndividualsForMigrationAllIslands, islandNumber):
    islandStart = datetime.now()
    population_size = int(par[islandNumber + parCount][1])
    numberOfGenerations = int(par[islandNumber + parCount][2])
    crossoverType = int(par[islandNumber + parCount][3])
    crossoverTasksNumPerc = float(par[islandNumber + parCount][4])
    crossoverProbability = float(par[islandNumber + parCount][5])
    mutationType = int(par[islandNumber + parCount][6])
    mutationTasksNumPerc = float(par[islandNumber + parCount][7])
    tasksMutationStartProbability = float(par[islandNumber + parCount][8])
    tasksMutationEndProbability = float(par[islandNumber + parCount][9])
    operatorsMutationStartProbability = float(par[islandNumber + parCount][10])
    operatorsMutationEndProbability = float(par[islandNumber + parCount][11])
    changeMutationRateType = int(par[islandNumber + parCount][12])
    changeMutationRateExpBase = float(par[islandNumber + parCount][13])
    drivenMutation = int(par[islandNumber + parCount][14])
    drivenMutationPart = float(par[islandNumber + parCount][15])
    limitBestFitnessRepetionCount = int(par[islandNumber + parCount][16])
    numberOfcyclesAfterDrivenMutation = int(par[islandNumber + parCount][17])
    completenessWeight = float(par[islandNumber + parCount][18])
    TPweight = float(par[islandNumber + parCount][19])
    precisenessStart = float(par[islandNumber + parCount][22])
    simplicityStart = int(par[islandNumber + parCount][23])
    evolutionEnd = int(par[islandNumber + parCount][24])
    completenessAttemptFactor1 = int(par[islandNumber + parCount][25])
    completenessAttemptFactor2 = float(par[islandNumber + parCount][26])
    elitismPerc = float(par[islandNumber + parCount][27])
    selectionOp = int(par[islandNumber + parCount][28])
    selectionTp = int(par[islandNumber + parCount][29])
    lambdaValue = int(par[islandNumber + parCount][30])
    HammingThreshold = int(par[islandNumber + parCount][31])
    migrationtime = int(par[islandNumber + parCount][32])
    percentageOfBestIndividualsForMigrationPerIsland = float(par[islandNumber + parCount][34])
    percentageOfIndividualsForMigrationPerIsland = float(par[islandNumber + parCount][35])
    fitnessStrategy = int(par[islandNumber + parCount][37])
    #Depois deve existir no Excel
    maxTempGen = 100
    satime = 1
    expectedProgression = 0.5

    names = ['[8] tasksMutationStartProbability', '[10] operatorsMutationStartProbability',
             '[32] migrationtime','[34] percentageOfBestIndividualsForMigrationPerIsland',
             '[35] percentageOfIndividualsForMigrationPerIsland']

    if fitnessStrategy == 0:
        precisenessWeight = float(par[islandNumber + parCount][20])
        simplicityWeight = float(par[islandNumber + parCount][21])
    else:
        precisenessWeight = 0
        simplicityWeight = 0
    islandSizes[islandNumber] = population_size
    percentageOfBestIndividualsForMigrationAllIslands[islandNumber] = percentageOfBestIndividualsForMigrationPerIsland
    alphabet = []
    log = copy.deepcopy(logs.logList[logIndex])
    logSizeAndMaxTraceSize = [0, float('inf'), 0]
    iniPop.createAlphabet(log, alphabet)
    iniPop.processLog(log, logSizeAndMaxTraceSize)
    highestValueAndPosition = [[0, 0, 0], -1]
    if highestValueAndPosition[0][1] >= precisenessStart:
        precisenessWeight = float(par[islandNumber + parCount][20])
    (population, evaluatedPopulation, referenceCromossome, averageEnabledTasks) = iniPop.initializePopulation(islandNumber, population_size, TPweight, precisenessWeight, simplicityWeight, completenessWeight, completenessAttemptFactor1, completenessAttemptFactor2, selectionOp, alphabet, log)
    fitnessEvolution = []
    (highestValueAndPosition, sortedEvaluatedPopulation) = cycle.chooseHighest(evaluatedPopulation)
    lowestValue = cycle.chooseLowest(sortedEvaluatedPopulation)
    averageValue = cycle.calculateAverage(evaluatedPopulation)
    fitnessEvolution.append([lowestValue, highestValueAndPosition[0][0], averageValue, 0, highestValueAndPosition[0][1], highestValueAndPosition[0][2], highestValueAndPosition[0][3], highestValueAndPosition[0][4], 0, 0, 0, 0])
    if (fitnessEvolution[0][10] >= simplicityStart) and (precisenessWeight > 0):
        simplicityWeight = float(par[islandNumber + parCount][21])
    print('LOG:', logIndex, '| COMB:', parComb, '| RND:', round, '| GEN:', 0, '| TF:', '%.6f' % highestValueAndPosition[0][0], '| C:', '%.6f' % highestValueAndPosition[0][1], '| TP:', '%.6f' % highestValueAndPosition[0][2], '| P:', '%.6f' % highestValueAndPosition[0][3], '| S:', '%.6f' % highestValueAndPosition[0][4], '| REP:', fitnessEvolution[0][3], fitnessEvolution[0][8], fitnessEvolution[0][9], fitnessEvolution[0][10], fitnessEvolution[0][11], '| ISL:', islandNumber, '| PAR:', islandNumber)
    drivenMutatedIndividuals = [0 for _ in range(len(population))]
    drivenMutatedGenerations = 0
    for currentGeneration in range(1, numberOfGenerations):
        if highestValueAndPosition[0][1] >= precisenessStart:
            precisenessWeight = float(par[islandNumber + parCount][20])
        (tasksMutationProbability, operatorsMutationProbability) = op.defineMutationProbability(tasksMutationStartProbability, tasksMutationEndProbability, operatorsMutationStartProbability, operatorsMutationEndProbability, numberOfGenerations, currentGeneration, changeMutationRateType, changeMutationRateExpBase)
        (population, evaluatedPopulation, drivenMutatedIndividuals, drivenMutatedGenerations) = cycle.generation(population, referenceCromossome, evaluatedPopulation, crossoverType, crossoverProbability, crossoverTasksNumPerc, mutationType, mutationTasksNumPerc, tasksMutationProbability, operatorsMutationProbability, drivenMutation, drivenMutationPart, limitBestFitnessRepetionCount, fitnessEvolution[currentGeneration - 1][3], drivenMutatedIndividuals, drivenMutatedGenerations, TPweight, precisenessWeight, simplicityWeight, completenessWeight, elitismPerc, sortedEvaluatedPopulation, selectionOp, selectionTp, lambdaValue, HammingThreshold, currentGeneration, completenessAttemptFactor1, completenessAttemptFactor2, numberOfcyclesAfterDrivenMutation, alphabet, log)
        (highestValueAndPosition, sortedEvaluatedPopulation) = cycle.chooseHighest(evaluatedPopulation)
        isl.set_broadcast(population, sortedEvaluatedPopulation, islandNumber, percentageOfBestIndividualsForMigrationPerIsland, broadcast)
        lowestValue = cycle.chooseLowest(sortedEvaluatedPopulation)
        averageValue = cycle.calculateAverage(evaluatedPopulation)
        fitnessEvolution.append([lowestValue, highestValueAndPosition[0][0], averageValue, 0, highestValueAndPosition[0][1], highestValueAndPosition[0][2], highestValueAndPosition[0][3], highestValueAndPosition[0][4], 0, 0, 0, 0])
        if fitnessEvolution[currentGeneration][1] == fitnessEvolution[currentGeneration - 1][1]:
            fitnessEvolution[currentGeneration][8] = fitnessEvolution[currentGeneration - 1][8] + 1
        if fitnessEvolution[currentGeneration][4] == fitnessEvolution[currentGeneration - 1][4]:
            fitnessEvolution[currentGeneration][3] = fitnessEvolution[currentGeneration - 1][3] + 1
        if fitnessEvolution[currentGeneration][5] == fitnessEvolution[currentGeneration - 1][5]:
            fitnessEvolution[currentGeneration][9] = fitnessEvolution[currentGeneration - 1][9] + 1
        if fitnessEvolution[currentGeneration][6] == fitnessEvolution[currentGeneration - 1][6]:
            fitnessEvolution[currentGeneration][10] = fitnessEvolution[currentGeneration - 1][10] + 1
        if fitnessEvolution[currentGeneration][7] == fitnessEvolution[currentGeneration - 1][7]:
            fitnessEvolution[currentGeneration][11] = fitnessEvolution[currentGeneration - 1][11] + 1
        if (fitnessEvolution[currentGeneration][10] >= simplicityStart) and (precisenessWeight > 0):
            simplicityWeight = float(par[islandNumber + parCount][21])
        print('LOG:', logIndex,
              '|COMB:', parComb,
              '|RND:', round,
              '|GEN:', currentGeneration,
              '|TF:', '%.6f' % highestValueAndPosition[0][0],
              '|C:', '%.6f' % highestValueAndPosition[0][1],
              '|TP:', '%.6f' % highestValueAndPosition[0][2],
              '|P:', '%.6f' % highestValueAndPosition[0][3],
              '|S:', '%.6f' % highestValueAndPosition[0][4],
              '|REP:', fitnessEvolution[currentGeneration][8], fitnessEvolution[currentGeneration][3], fitnessEvolution[currentGeneration][9], fitnessEvolution[currentGeneration][10], fitnessEvolution[currentGeneration][11],
              '|ISL:', islandNumber,
              '|PAR:', islandNumber)
        if ((fitnessStrategy == 0) and ((highestValueAndPosition[0][1] >= 1.0) and (fitnessEvolution[currentGeneration][8] >= evolutionEnd))) or ((fitnessStrategy == 1) and ((highestValueAndPosition[0][1] == 1.0) and (highestValueAndPosition[0][3] > 0) and (highestValueAndPosition[0][4] > 0) and (fitnessEvolution[currentGeneration][10] >= evolutionEnd) and (fitnessEvolution[currentGeneration][11] >= evolutionEnd))):
        #if (highestValueAndPosition[0][1] == 1.0) and (highestValueAndPosition[0][2] == 1.0):
            broadcast[-1] = 0
        if broadcast[-1] == 0:
            break
        isl.send_individuals(population, sortedEvaluatedPopulation, islandNumber, numberOfThreads, messenger)
        if (currentGeneration > 0) and (currentGeneration % migrationtime == 0):
            island_fitness = []
            for i in range(len(evaluatedPopulation[1])):
                island_fitness.append(evaluatedPopulation[1][i][0])
            isl.receive_individuals(population, islandNumber, island_fitness, messenger)
            isl.do_migration(population, islandNumber, numberOfThreads, island_fitness, percentageOfIndividualsForMigrationPerIsland, percentageOfBestIndividualsForMigrationPerIsland, broadcast, islandSizes, percentageOfBestIndividualsForMigrationAllIslands)
            evaluatedPopulation = fit.evaluationPopulation(population, referenceCromossome, TPweight, precisenessWeight, simplicityWeight, completenessWeight, completenessAttemptFactor1, completenessAttemptFactor2, selectionOp, alphabet, log)
            (highestValueAndPosition, sortedEvaluatedPopulation) = cycle.chooseHighest(evaluatedPopulation)

        if (currentGeneration > 0 and (numberOfGenerations-currentGeneration > 10) and currentGeneration%satime == 0):
            print("ISLAND: ", islandNumber, "currently at Simulated Annealing")
            #Simulated Annealing
            island_fitness = []
            for i in range(len(evaluatedPopulation[1])):
                island_fitness.append(evaluatedPopulation[1][i][0])
            currentFitness = max(island_fitness)
            parametersTP = [tasksMutationStartProbability,operatorsMutationStartProbability,
                             migrationtime,percentageOfBestIndividualsForMigrationPerIsland,
                             percentageOfIndividualsForMigrationPerIsland]
            sa.SA(islandNumber, expectedProgression, currentGeneration, maxTempGen,
                  definitions, progressions, parametersTP, currentFitness)
            tasksMutationStartProbability = parametersTP[0]

    #Update altered parameters (somente para [10] operatorsMutationStartProbability)
    df = pd.read_csv("input-parameters.csv", sep=";")
    parI = 0 
    for name in names:
        df.at[islandNumber + parCount - 1, name] = parametersTP[parI]
        #print("changed", name, 'of island', islandNumber, 'to', parametersTP[parI])
        parI += 1
    df.to_csv("input-parameters.csv", sep=";", index= False)
    print("ISLAND: ", islandNumber, "finished with Simulated Annealing")
        
    cycle.postProcessing(population, alphabet)
    #plot.plot_evolution_per_island(fitnessEvolution, str(islandNumber), str(round), islandNumber)
    prevPlot = []
    with open('results/plotting_{0}.txt'.format(islandNumber), 'r') as plott:
        for line in isl.nonblank_lines(plott):
            prevPlot.append(literal_eval(line))
    plott.close()
    prevPlot.extend(fitnessEvolution)
    with open('results/plotting_{0}.txt'.format(islandNumber), 'w') as plott:
        for ini in range(len(prevPlot)):
            plott.write(str(prevPlot[ini]) + '\n')
    plott.close()
    islandEnd = datetime.now()
    islandDuration = islandEnd - islandStart
    record.record_evolution(logIndex, log, str(parComb), str(islandNumber), str(round), par[islandNumber + parCount], islandNumber, highestValueAndPosition[0], fitnessEvolution, alphabet, population[highestValueAndPosition[1]], islandStart, islandEnd, islandDuration, currentGeneration)
    print(islandNumber, islandDuration, '%.5f' % highestValueAndPosition[0][0], '%.5f' % highestValueAndPosition[0][1], '%.5f' % highestValueAndPosition[0][2], '%.5f' % highestValueAndPosition[0][3], alphabet, population[highestValueAndPosition[1]])
    return

if __name__ == '__main__':
    par = []
    with open('input-parameters.csv', 'r') as parameters:
        for line in isl.nonblank_lines(parameters):
            par.append(line.split(';'))
    parameters.close()

    definitions = [['[8] tasksMutationStartProbability',0.001, 0, 0.1, "float"],
                   ["[10] operatorsMutationStartProbability", 0.01, 0, 1, "float"],
                   ['[32] migrationtime', 1, 1, 50, "int"],
                   ['[34] percentageOfBestIndividualsForMigrationPerIsland', 0.1, 0, 1, "float"],
                   ['[35] percentageOfIndividualsForMigrationPerIsland', 0.1, 0, 1, "float"]]
    
    globalStart = datetime.now()
    for logID in range(len(log_list)):
        parCount = 1
        for parComb in range(numberOfParametersCombinations):
            num_islands = []
            for thread in range(numberOfThreads):
                num_islands.append(thread)
            isl.create_plotting_files(num_islands, numberOfThreads)
            p = multiprocessing.Pool(numberOfThreads)
            m = multiprocessing.Manager()
            broadcast = m.list()
            messenger = m.list()
            progressions = m.list()
            for i in range(numberOfThreads):
                #progressions.append([["[10] operatorsMutationStartProbability", 0, 0]])
                progressions.append([['[8] tasksMutationStartProbability',0,0],
                                     ['[10] operatorsMutationStartProbability',0,0],
                                     ['[32] migrationtime',0,0],
                                     ['[34] percentageOfBestIndividualsForMigrationPerIsland',0,0],
                                     ['[35] percentageOfIndividualsForMigrationPerIsland',0,0]])
            islandSizes = m.list()
            percentageOfBestIndividualsForMigrationAllIslands = m.list()
            func = partial(runRound, par, parComb, parCount, log_list[logID], numberOfThreads)
            for round in range(numberOfRounds):
                for thread in range(numberOfThreads):
                    broadcast.append([])
                    messenger.append([])
                    islandSizes.append(0)
                    percentageOfBestIndividualsForMigrationAllIslands.append(0)
                broadcast.append(1)
                func2 = partial(func, round, broadcast, messenger, progressions, definitions, islandSizes, percentageOfBestIndividualsForMigrationAllIslands)
                p.map(func2, num_islands)
                #plot.plot_evolution_integrated(str(round), numberOfThreads)
                globalEnd = datetime.now()
                globalDuration = globalEnd - globalStart
                print('Global Start:    ', globalStart)
                print('Global End:      ', globalEnd)
                print('Global Duration: ', globalDuration)
            p.close()
            parCount = parCount + numberOfThreads
