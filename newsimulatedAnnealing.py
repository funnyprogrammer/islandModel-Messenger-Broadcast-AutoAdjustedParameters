import math
import random as random

def mapT(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

def acceptance_probability(old,new, temperature):
    return math.exp((new-old)/temperature)

def make_move(enum):
    nhb = random.choice(range(0, len(enum))) # choose from all points
    return enum[nhb][1]

def SA(islandNumber, expectedProgression, currentGen, maxTempGen, definitions, progressions, parametersToProgress, current_fitness):    
    temperature = mapT(currentGen, 0, maxTempGen, 1e4, 0) #simulação de temperatura diminuindo (0-N para 0-1e4) desnec? 
    for i, parameter in zip(range(len(parametersToProgress)),parametersToProgress):
        lower_limit = float(definitions[i][2]) #provavelmente 0
        upper_limit = float(definitions[i][3]) #máximo que o parâmetro deveria alcançar (geralmente 1)
        type = str(definitions[i][4])
        #faço essa verifição a cada nova execução de SA, ao invés de testar na hora
        deltaE = current_fitness - float(progressions[islandNumber][i][1]) #fitness novo - antigo    
        if(deltaE <= 0 or (deltaE < expectedProgression)): #progresso piorou ou não mudou
            if(temperature == 0):
                maxTempGen = maxTempGen*10
                temperature = mapT(currentGen, 0, maxTempGen, 1e4, 0) #recalcular
            ap = float(acceptance_probability(float(progressions[islandNumber][i][1]), current_fitness, temperature))
            if(random.random() >= ap):
                A = []
                for j in range(100):
                    if(type == 'float'): A.append(random.uniform(lower_limit, upper_limit)) #gerar uma lista de valores que o parâmetro pode ter
                    else: A.append(random.randint(lower_limit, upper_limit))
                A = list(A)
                enum = list(enumerate(A)) #enumerar a lista
                newParameter = make_move(enum) #escolher uma posição nova
                progressions[islandNumber][i][1] = current_fitness #atualizar coluna do fitness antigo
                progressions[islandNumber][i][2] = parametersToProgress[i] #atualizar coluna do antigo valor
                parametersToProgress[i] = newParameter #dar um salto no valor (fugir de máximas locais)
        elif(deltaE >= expectedProgression): #progresso melhorou
            progressions[islandNumber][i][1] = current_fitness #atualizar coluna do fitness antigo
            progressions[islandNumber][i][2] = parametersToProgress[i] #atualizar coluna do antigo valor
            scl = random.random()
            if(scl >= 0.66):
                if(parametersToProgress[i] + float(definitions[i][1]) <= 1):
                    parametersToProgress[i] += float(definitions[i][1]) #subir um pouco
            elif(scl <= 0.33 and (parametersToProgress[i] - float(definitions[i][1]) >= 0)):
                parametersToProgress[i] -= float(definitions[i][1]) #descer um pouco
            expectedProgression = expectedProgression/2
            
                
