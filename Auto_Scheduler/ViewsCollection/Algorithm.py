from django.shortcuts import render, redirect
from django.contrib import messages
from Auto_Scheduler.api import serializers
from Auto_Scheduler.com.Classes import Room,Professor
from Auto_Scheduler.models import Rooms,Professors,Semester,Day_Time,Semester_Courses,Day_Time_Professor
import random
from random import randint,randrange

POPULATION_SIZE = 100
GENES = []
ROOMS = []
LABS = []
SAMEPROFESSORS = []
PhysicsLAB = []
arrayofTime = []


class Individual(object):

    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.calcFitness()

    @classmethod
    def create_gnome(self):
        '''
        create chromosome or string of genes
        '''
        global GENES

        gnome_len = len(GENES)
        # print("LENGth", gnome_len)
        gene = GENES
        return [self.mutated_genes(gene[i]) for i in range(gnome_len)]

    @classmethod
    def mutated_genes(self, Gene):
        '''
        create random genes for mutation
        '''
        global ROOMS, PhysicsLAB,SAMEPROFESSORS,LABS,arrayofTime
        # gene = random.choice(arrayofTime) ,"Available_TimeSlots":[]

        newgene = Gene
        # newgene["Available_TimeSlots"] =

        if len(newgene["Available_TimeSlots"]) == 0:
            for time in arrayofTime:
                # print('time', time)
                if time in newgene["Professor"].availability:
                    # Gene["Assigned-timeSlot"] = time
                    newgene["Available_TimeSlots"].append(time)

        newtime = random.choice(newgene["Available_TimeSlots"])

        # print('newtime', newtime)
        if newgene["isLab"] == True:
            newgene["roomAlotted"] = random.choice(LABS)
        elif newgene["isPhysics_Lab"]:
            newgene["roomAlotted"] = random.choice(PhysicsLAB)
        else:
            newgene["roomAlotted"] = random.choice(ROOMS)

        newgene["Assigned-timeSlot"] = newtime
        newgene["Professor"].courses.append(newtime)
        # txt = newgene["Professor"].name+"-"+newtime[0:3]
        # if txt in SAMEPROFESSORS:
        #     newgene["Professor"].sameDayCount = 1
        # else:
        #     SAMEPROFESSORS.append(txt)
        # newGENE = Gene
        # print('Gene->>>>>>', newgene)

        return newgene

    def calcFitness(self):
        clashMsg = ""
        alreadyCounted = []
        countedIndex = []
        fitness = 0
        ifFound = False
        # for c in self.chromosome:
            # currentC = 
            # for co in range(0,len(c["Professor"].courses),+1):

            #     for d_c in range(0,len(c["Professor"].courses),+1):
            #         if d_c != co:
            #             if d_c not in alreadyCounted:
            #                 if c["Professor"].courses[d_c][0:3] == c["Professor"].courses[co][0:3]:
            #                     fitness += 1
            #                     alreadyCounted.append(d_c)
            #                     alreadyCounted.append(co)

            
        for i in range(0, len(self.chromosome), +1):
            for ch in range(0, len(self.chromosome), +1):
                if ch != i:
                    if self.chromosome[i]["Assigned-timeSlot"] == self.chromosome[ch]["Assigned-timeSlot"] and self.chromosome[ch]["roomAlotted"].room == self.chromosome[i]["roomAlotted"].room:        
                        ifFound = True
                        fitness += 1
                        countedIndex.append(ch)
                
                    if self.chromosome[i]["Professor"].name == self.chromosome[ch]["Professor"].name:
                        if self.chromosome[i]["Assigned-timeSlot"] == self.chromosome[ch]["Assigned-timeSlot"]:        
                            fitness += 1
                            countedIndex.append(ch)
            
            if self.chromosome[i]["roomAlotted"].capacity < self.chromosome[i]["Capacity"]:
                clashMsg = "CAPACITY ISSUE"
                ifFound = True
                fitness += 1

            if self.chromosome[i]["isLab"] == False:
                if self.chromosome[i]["roomAlotted"].isLab == True:
                    
                    fitness += 1

            if self.chromosome[i]["isPhysics_Lab"] == False:
                if self.chromosome[i]["roomAlotted"].isPhysicsLab == True:
                    
                    fitness += 1
        

        for gene in range(0, len(self.chromosome), +1):
            localCount = 1
            for nextGene in range(0, len(self.chromosome), +1):
                if gene != nextGene and nextGene not in alreadyCounted:
                    if self.chromosome[gene]["Professor"].name == self.chromosome[nextGene]["Professor"].name:
                        if self.chromosome[gene]["Assigned-timeSlot"] == self.chromosome[nextGene]["Assigned-timeSlot"]:
                            self.chromosome[nextGene]["Assigned-timeSlot"] = random.choice(self.chromosome[nextGene]["Available_TimeSlots"])
                        if self.chromosome[gene]["Assigned-timeSlot"][0:3] == self.chromosome[nextGene]["Assigned-timeSlot"][0:3]:
                            localCount += 1
                            if localCount > 2:
                                fitness += 1
                            alreadyCounted.append(gene)
                            alreadyCounted.append(nextGene)

        return fitness

    def crossover(self, p2):
        child = []
        isOdd = False
        num = len(p2.chromosome) // 2
        # print('Before CrossOver', p2.chromosome)
        # print('Total', num)
        if num % 2 != 0:
            num = len(p2.chromosome) - 1 // 2
            isOdd = True
        # num = num//2
        # print(num)
        randomNum = randint(0, num)
        sub = len(p2.chromosome) - randomNum
        # child.extend(self.chromosome[:randomNum])
        for i in range(0, num - 1, +1):
            # print(p2.chromosome[i]['Assigned-timeSlot'])
            child.append(p2.chromosome[i])
        for j in range(num - 1, len(p2.chromosome), +1):
            # print(self.chromosome[j]['Assigned-timeSlot'])
            child.append(self.chromosome[j])
        newchild = self.mutation(child)
        # print('After CrossOver', child)

        # print('Child Len', len(child))
        return Individual(newchild)

    def mutation(self, chromosome):
        mutatedChromosome = chromosome

        global ROOMS,LABS,physicsLab
        rand = randrange(0,len(mutatedChromosome)+1,1)
        for gene in range(0, len(mutatedChromosome), +1):
            if gene == rand:
                mutatedChromosome[gene]["Assigned-timeSlot"] = random.choice(mutatedChromosome[gene]["Available_TimeSlots"])
                isFound = False
                while isFound:
                    rand = randrange(0,len(mutatedChromosome)+1,1)
                    if rand != gene:
                        isFound = True

            
            if mutatedChromosome[gene]["isLab"] == False:
                if mutatedChromosome[gene]["roomAlotted"].isLab == True:
                    mutatedChromosome[gene]["roomAlotted"] = random.choice(ROOMS)

            if mutatedChromosome[gene]["isPhysics_Lab"] == True:
                if mutatedChromosome[gene]["roomAlotted"].isPhysicsLab == False:
                    mutatedChromosome[gene]["roomAlotted"] = random.choice(PhysicsLAB)
            if mutatedChromosome[gene]["isLab"] == True:
                if mutatedChromosome[gene]["roomAlotted"].isLab == False:
                    mutatedChromosome[gene]["roomAlotted"] = random.choice(LABS)        
            if mutatedChromosome[gene]["roomAlotted"].capacity < mutatedChromosome[gene]["Capacity"]:
                if mutatedChromosome[gene]["isLab"] == True:
                    mutatedChromosome[gene]["roomAlotted"] = random.choice(LABS)
                else:
                    mutatedChromosome[gene]["roomAlotted"] = random.choice(ROOMS)
        
        
       
                        
        return mutatedChromosome



def create_Time_Table(request):
    if request.method == "POST":
        # ch = request.POST.get('r1')

        global POPULATION_SIZE
        global arrayofTime
        global GENES
        global LABS
        global ROOMS
        selected_id = request.POST.get('r1')

        meetingsPerweek = 1
        prevFitness = 10
        COURSES = []
        fitness_Same_Count = 0
        ifFound = False
        population = []
        generation = 1
        currentSemester = Semester.objects.filter(id=selected_id).last()
        
        rooms = Rooms.objects.all()
        day_time = Day_Time.objects.all()
        for room in rooms:
            ROOMS.append(Room(room.room_name,room.room_capacity,room.islab))

        for d_t in day_time:
            arrayofTime.append(d_t.day_time)

        meetingsPerweek = currentSemester.meetings_per_week
        Courses = Semester_Courses.objects.filter(semester=currentSemester.id)


        for mpw in range(0,meetingsPerweek,+1):  # FOR SUMMER SEMESTER
            for course in Courses:
                avail = []
                availability = Day_Time_Professor.objects.filter(prof=course.selected_Professor.id)
                for a in availability:
                    avail.append(a.day_time)
                
                _id = course.selected_Professor.id
                name = course.selected_Professor.professor_name
                profe = Professor.Professor(_id,name,avail,"",0,[])
                temp = {"Name": course.Course.course_name,"Professor":profe,"Capacity":course.Course.course_capacity,"Assigned-timeSlot": "", "Available_TimeSlots": [],"roomAlotted": None, "isLab": course.Course.course_isLab,"isPhysics_Lab":course.Course.course_isPhysics_Lab}
                COURSES.append(temp)

        GENES = COURSES
        for _ in range(POPULATION_SIZE):
            gnome = Individual.create_gnome()
        # print('GNOME',gnome)
            population.append(Individual(gnome))

            print('Fitness-----', Individual(gnome).fitness)
        
    # Population Created
        while not ifFound:
        # sort the population in increasing order of fitness score
            population = sorted(population, key=lambda x: x.fitness)
            # print('Fitness After-----', population[0].fitness)

            if population[0].fitness <= 0:
                ifFound = True
            # print('SELECTED GENERATION')
            # for i in population[0].chromosome:
            #     print('', i['Name'], i['Assigned-timeSlot'] )
                break
            elif population[0].fitness == prevFitness:
                fitness_Same_Count += 1
                if fitness_Same_Count > 40:
                    ifFound = True
                    break
            elif generation >= 100:
                ifFound = True
                break
            else:
                prevFitness = population[0].fitness
                fitness_Same_Count = 0

            new_generation = []
            s = int((10 * POPULATION_SIZE) // 100)
            for ch in range(0, s, +1):
                ind = Individual(population[ch].mutation(population[ch].chromosome))
                new_generation.append(ind)

            ns = int((90 * POPULATION_SIZE) // 100)
        # print(ns)
        # sub = ns - s
            for _ in range(ns):
                rand = randint(s, ns - 1)
                parent1 = population[rand]
                rand = randint(s, ns - 1)
                parent2 = population[rand]

                child = parent1.crossover(parent2)
                new_generation.append(child)

            population = new_generation
        # print('new', population[0].chromosome)
        # print('Generation: ', generation)
        # print('Population: ', population[0].chromosome)
        # print('Fitness: ', population[0].fitness)

        # print("Generation: {}\tDict: {}\tFitness: {}".format(generation, "".join(population[0].chromosome),population[0].fitness))

            generation += 1

        print('SELECTED GENERATION ')
        data = []
        for ch in population[0].chromosome:
        #     print('Name : ', ch["Name"])
        #     print('Professor : ', ch["Professor"].name)
        #     print('TimeSlot : ', ch["Assigned-timeSlot"])
        # # print('Available : ', ch["Available_TimeSlots"])
        # print('Room : ', ch["roomAlotted"].room)
        # print('\n')
            n_data = {"Name": ch["Name"], "Professor":ch["Professor"].name, "TimeSlot":ch["Assigned-timeSlot"],"Room":ch["roomAlotted"].room}
            data.append(n_data)
    
        render(request, 'Alert.html',{'data': data})