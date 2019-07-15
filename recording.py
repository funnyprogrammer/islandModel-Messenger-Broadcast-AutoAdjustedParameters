import csv

def record_evolution(logID, log, parComb, par, round, parameters, islandNumber, highestValues, fitnessEvolution, alphabet, bestIndividual, globalStart, islandEnd, islandDuration, currentGeneration):

    parametersString = ''
    parametersValues = ''
    for i in range(len(parameters)):
        parametersString = parametersString + 'P' + str(i) + '	'
        parametersValues = parametersValues + str(parameters[i]) + '	'

    highestValuesValues = ''
    for i in range(len(highestValues)):
        highestValuesValues = highestValuesValues + str(highestValues[i]) + '	'

    #fields1 = ['PAR	ROUND	ISL	' + parametersString + 'GEN	START	END	DURANTION	TOT-FIT	COMP	TP	PREC	SIMP	ALPHABET	BEST INDIVIDUAL	LOG	FITNESS EVOLUTION']
    fields2a = [str(logID) + '	' + str(parComb) + '	' + str(par) + '	' + str(round) + '	' + str(islandNumber) + '	' + parametersValues + str(currentGeneration) + '	' + str(globalStart) + '	' + str(islandEnd) + '	' + str(islandDuration) + '	' + highestValuesValues + str(alphabet) + '	' + str(bestIndividual) + '	' + str(log) + '	' + str(fitnessEvolution)]
    fields2b = [str(logID) + '	' + str(parComb) + '	' + str(par) + '	' + str(round) + '	' + str(islandNumber) + '	' + parametersValues + str(currentGeneration) + '	' + str(globalStart) + '	' + str(islandEnd) + '	' + str(islandDuration) + '	' + highestValuesValues]
    with open('output-spreadsheet-complete' + '.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, dialect='excel', delimiter=',')
        #writer.writerow(fields1)
        writer.writerow(fields2a)
        csvfile.close()
    with open('output-spreadsheet-short' + '.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, dialect='excel', delimiter=',')
        #writer.writerow(fields1)
        writer.writerow(fields2b)
        csvfile.close()
    return