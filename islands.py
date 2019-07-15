from random import randint
import cycle as cycle
from multiprocessing import Pool

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line

def creator_plotting_files(var):
    plot = open('results/plotting_{0}.txt'.format(var), 'w')
    plot.close()

def create_plotting_files(num_islands, num_threads):
    p = Pool(num_threads)
    p.map(creator_plotting_files, num_islands)
    p.close()

def set_broadcast(population, sortedEvaluatedPopulation, islandNumber, percentageOfBestIndividualsForMigrationPerIsland, broadcast):
    allBests = []
    for i in range(int((len(population)) * percentageOfBestIndividualsForMigrationPerIsland)):
        allBests.append([population[sortedEvaluatedPopulation[i][5]], [sortedEvaluatedPopulation[i][0]]])
    broadcast[islandNumber] = allBests

def pick_island(island_number, island_size, num_islands, percentageOfBestIndividualsForMigrationPerIsland, migration_index, broadcast, islandSizes, percentageOfBestIndividualsForMigrationAllIslands):
    pickedIsland = randint(0, num_islands - 1)
    count = 0
    while (pickedIsland == island_number) or (migration_index[pickedIsland] >= int(percentageOfBestIndividualsForMigrationAllIslands[pickedIsland]*islandSizes[pickedIsland])) or (len(broadcast[pickedIsland]) == 0):
        if count == 10:
            return -1
        else:
            count = count + 1
            pickedIsland = randint(0, num_islands - 1)
    return pickedIsland

def send_individuals(population, sortedEvaluatedPopulation, island_number, num_islands, messenger):
    topBests = []
    for i in range(int((len(population)) * 0.15)):
        topBests.append([population[sortedEvaluatedPopulation[i][5]], [sortedEvaluatedPopulation[i][0]]])
    pickedIsland = randint(0, num_islands-1)
    count = 0 
    while (pickedIsland == island_number):
        if count == 10:
            pickedIsland = -1 
        else:
            count = count + 1
            pickedIsland = randint(0, num_islands - 1)
    
    #send message
    if pickedIsland != -1:
        messenger[island_number] = [topBests, pickedIsland]
        print('Message sent from', island_number, 'to', pickedIsland)
        
def receive_individuals(population, island_number, island_fitness, messenger):
    for island in range(len(messenger)):
        message = messenger[island]
        if message and message[1] == island_number:
            worst_gen_list = []
            count = 0
            for individuo in range(len(island_fitness)):
                worst_gen_list.append([island_fitness[individuo], count])
                count += 1
            sorted_worst_gen_list = sorted(worst_gen_list, reverse=False, key=cycle.takeFirst)
            iter = 0
            while iter < len(message[0]):
                worst_fit = sorted_worst_gen_list[iter][0]
                list_ind = message[0]
                best_fit = list_ind[iter][1][0]
                if worst_fit < best_fit:
                    population[sorted_worst_gen_list[iter][1]] = message[0][iter][0]
                iter = iter + 1
            print('Message recieved from', island, 'to me', island_number)
            message = [] 
            

def do_migration(island_population, island_number, num_islands, island_fitness, percentageOfIndividualsForMigrationPerIsland, percentageOfBestIndividualsForMigrationPerIsland, broadcast, islandSizes, percentageOfBestIndividualsForMigrationAllIslands):
    #if (int(percentageOfIndividualsForMigrationPerIsland * (len(island_population)))) > ((num_islands - 1) * (int(percentageOfBestIndividualsForMigrationPerIsland * (len(island_population))))):
    #    percentageOfIndividualsForMigrationPerIsland = (((num_islands - 1) * (int(percentageOfBestIndividualsForMigrationPerIsland * (len(island_population)))))) / (len(island_population))
    migration_index = []
    for i in range(num_islands):
        migration_index.append(0)
    worst_gen_list = []
    count = 0
    for individuo in range(len(island_fitness)):
        worst_gen_list.append([island_fitness[individuo], count])
        count += 1
    sorted_worst_gen_list = sorted(worst_gen_list, reverse=False, key=cycle.takeFirst)
    iter = 0
    while iter < percentageOfIndividualsForMigrationPerIsland * (len(island_population)):
        picked_island = pick_island(island_number, len(island_population), num_islands, percentageOfBestIndividualsForMigrationPerIsland, migration_index, broadcast, islandSizes, percentageOfBestIndividualsForMigrationAllIslands)
        if picked_island != -1:
            worst_fit = sorted_worst_gen_list[iter][0]
            island_selected = broadcast[picked_island]
            best_ind = island_selected[migration_index[picked_island]]
            best_fit = best_ind[1][0]
            migration_index[picked_island] += 1
            if worst_fit < best_fit:
                island_population[sorted_worst_gen_list[iter][1]] = best_ind[0]
            iter = iter + 1
        else:
            break
    return
