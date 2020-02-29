import random
from .Room import Room

POPULATION_SIZE = 50
GENES = []
ROOMS = []
arrayofTime = ["Mon-08:30-11:30","Mon-11:45-02:45","Mon-3:00-06:00",
                "Tue-08:30-11:30","Tue-11:45-02:45","Tue-3:00-06:00",
                "Wed-08:30-11:30","Wed-11:45-02:45","Wed-3:00-06:00",
                "Thurs-08:30-11:30","Thurs-11:45-02:45","Thurs-3:00-06:00",
                "Sat-08:30-11:30","Sat-11:45-02:45","Sat-3:00-06:00",
                "Sun-08:30-11:30","Sun-11:45-02:45","Sun-3:00-06:00"
                ]

class Individual(object):
    
    def __init__(self,chromosome):
        self.chromosome = chromosome
        self.fitness = self.calcFitness()

    @classmethod
    def create_gnome(self): 
        '''
        create chromosome or string of genes 
        '''
        global GENES 
        gnome_len = len(GENES)
        return [self.mutated_genes(GENES[i]) for i in range(gnome_len)]
    
    
    
    @classmethod
    def mutated_genes(self,Gene):
        ''' 
        create random genes for mutation 
        '''
        global arrayofTime
        # gene = random.choice(arrayofTime) ,"Available_TimeSlots":[]
        Gene["Available_TimeSlots"] = []
        for time in arrayofTime:
            
            if time in Gene["Availability"]:
                # Gene["Assigned-timeSlot"] = time
                Gene["Available_TimeSlots"].append(time)
        newtime = random.choice(Gene["Available_TimeSlots"])
        Gene["Assigned-timeSlot"] = newtime
        newGENE = Gene
        # print('Gene->>>>>>', gene)
        return newGENE
  

    
    
    def calcFitness(self):
        fitness = 0
        for i in range(0,len(self.chromosome),1):
            if self.chromosome[i]["Assigned-timeSlot"] in self.chromosome[i]["Availability"]:
                for ch in range(0,len(self.chromosome),1):
                    if ch != i:
                        if self.chromosome[i]["Assigned-timeSlot"] == self.chromosome[ch]["Assigned-timeSlot"]:
                            # print('CLASH WITH OTHER TEACHER')
                            self.chromosome[i]["isClash"] = True

                            fitness+=1
                        else:
                            self.chromosome[i]["isClash"] = False
            else:
                self.chromosome[i]["isClash"] = True
                # print('NOT IN AVAILABLE TIMESLOT')
                fitness+=1
            # for j in i["Availability"]:
            #     print('j ======',j)    
            # print('i ======',i)
        # for gs, gt in zip(self.chromosome, TARGET): 
        #     if gs != gt: fitness+= 1
        return fitness 
    
    def crossover(self,p2):
        child = []
        num = random.randrange(0,len(p2.chromosome)-1,1)
        randomNum = (len(p2.chromosome)-num)
        child.extend(self.chromosome[:randomNum])
        child.extend(p2.chromosome[num:])
        child = self.mutation(child)
        return Individual(child)

    def mutation(self,chromosome):
        mutatedChromosome = chromosome
        for gene in range(0,len(mutatedChromosome),+1):
            for nextGene in range(0,len(mutatedChromosome),+1):
                if nextGene != gene:
                    if mutatedChromosome[gene]["Assigned-timeSlot"] == mutatedChromosome[nextGene]["Assigned-timeSlot"]:
                        mutatedChromosome[gene]["Assigned-timeSlot"] = random.choice(mutatedChromosome[gene]["Available_TimeSlots"])

        return mutatedChromosome
    
def main():
    global POPULATION_SIZE
    global arrayofTime
    global GENES
    global ROOMS
    prevFitness = 10
    fitness_Same_Count = 0
    ifFound = False
    population = []
    #current generation 
    generation = 1
    room = [
    Room("CS-101",60),
    Room("CS-102",40),
    Room("CS-103",50),
    Room("Lab-1",50),
    Room("CS-104",40),
    Room("CS-105",60),
    Room("Lab-2",30),
    Room("CS-106",50)
    ]
    ROOMS = room

    course1 = {"Name": "MAD", "Professor": "Shoaib", "Availability":[arrayofTime[0],arrayofTime[1],arrayofTime[2],arrayofTime[6],arrayofTime[7]],"Capacity": 55, "Assigned-timeSlot":"","Available_TimeSlots":[],"isClash":False,"roomAlotted":None}
    course2 = {"Name": "Probability", "Professor": "Shoaib", "Availability":[arrayofTime[0],arrayofTime[1],arrayofTime[12],arrayofTime[13]],"Capacity": 50,"Assigned-timeSlot":"","Available_TimeSlots":[],"isClash":False,"roomAlotted":None}
    course3 = {"Name": "AI LAB", "Professor": "Shoaib", "Availability":[arrayofTime[2]],"Capacity": 30,"Assigned-timeSlot":"","Available_TimeSlots":[],"isClash":False,"roomAlotted":None}
    course4 = {"Name": "Multi", "Professor": "Shoaib", "Availability":[arrayofTime[1],arrayofTime[2]],"Capacity": 50,"Assigned-timeSlot":"","Available_TimeSlots":[],"isClash":False,"roomAlotted":None}
    course5 = {"Name": "POM", "Professor": "Shoaib", "Availability":[arrayofTime[10],arrayofTime[11]],"Capacity": 50,"Assigned-timeSlot":"","Available_TimeSlots":[],"isClash":False,"roomAlotted":None}
    course6 = {"Name": "AI", "Professor": "Shoaib", "Availability":[arrayofTime[0],arrayofTime[1],arrayofTime[2]],"Capacity": 30,"Assigned-timeSlot":"","Available_TimeSlots":[],"isClash":False,"roomAlotted":None}
    course7 = {"Name": "CAO", "Professor": "Shoaib", "Availability":arrayofTime,"Capacity": 60,"Assigned-timeSlot":"","Available_TimeSlots":[],"isClash":False,"roomAlotted":None}
    course8 = {"Name": "DCL", "Professor": "Shoaib", "Availability":[arrayofTime[1]],"Capacity": 50,"Assigned-timeSlot":"","Available_TimeSlots":[],"isClash":False,"roomAlotted":None}
    course9 = {"Name": "FYP", "Professor": "Shoaib", "Availability":arrayofTime,"Capacity": 60,"Assigned-timeSlot":"","Available_TimeSlots":[],"isClash":False,"roomAlotted":None}
    course10 = {"Name": "Calculus", "Professor": "Shoaib", "Availability":arrayofTime,"Capacity": 60,"Assigned-timeSlot":"","Available_TimeSlots":[],"isClash":False,"roomAlotted":None}
    courses = [course1,course2,course3,course4,course5,course6,course7,course8,course9,course10]
    GENES = courses
        
    for _ in range(POPULATION_SIZE):
        gnome = Individual.create_gnome()
        population.append(Individual(gnome)) 
                
        print('Fitness-----',Individual(gnome).fitness)

    #Population Created
    while not ifFound:
        # sort the population in increasing order of fitness score 
        population = sorted(population, key=lambda x:x.fitness, reverse=False) 
        print('Fitness After-----',population[0].fitness)

            # if the individual having lowest fitness score ie.  
            # 0 then we know that we have reached to the target 
            # and break the loop 
        prevFitness=population[0].fitness
        if population[0].fitness <= 0: 
            ifFound = True
            break
        elif population[0].fitness == prevFitness:
            fitness_Same_Count+=1
            if fitness_Same_Count > 4:
                ifFound = True
                break
                

            
        new_generation = []
        s = int((10*POPULATION_SIZE)/100)
        new_generation.extend(population[:s])

        ns = int((90*POPULATION_SIZE)/100)
        sub = ns-s
        for _ in range(ns):
            parent1 = random.choice(population[:sub])
            # print('parent--->', parent1.chromosome)
            parent2 = random.choice(population[sub:])
            child = parent1.crossover(parent2)
            new_generation.append(child)
            
        population = new_generation 
        # print('Generation: ', generation)
        # print('Population: ', population[0].chromosome)
        # print('Fitness: ', population[0].fitness)
        
        # print("Generation: {}\tDict: {}\tFitness: {}".format(generation, "".join(population[0].chromosome),population[0].fitness)) 
  
        generation += 1
        
    print('SELECTED GENERATION \n ', population[0].chromosome)
    
if __name__ == "__main__":
    main()



