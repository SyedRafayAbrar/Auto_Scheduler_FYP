from django.shortcuts import render, redirect
from django.contrib import messages
from Auto_Scheduler.api import serializers
from Auto_Scheduler.com.Classes import Room,Professor
from Auto_Scheduler.models import Rooms,Professors,Semester,Day_Time,Semester_Courses,Day_Time_Professor
import random
from random import randint,randrange

POPULATION_SIZE = 10
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

        newgene = Gene

        if len(newgene["Available_TimeSlots"]) == 0:
            for time in arrayofTime:
                if time in newgene["Professor"].availability:
                    newgene["Available_TimeSlots"].append(time)

        newtime = random.choice(newgene["Available_TimeSlots"])

        if newgene["isLab"] == True:
            newgene["roomAlotted"] = random.choice(LABS)
        elif newgene["isPhysics_Lab"]:
            newgene["roomAlotted"] = random.choice(PhysicsLAB)
        else:
            newgene["roomAlotted"] = random.choice(ROOMS)

        newgene["Assigned-timeSlot"] = newtime
        newgene["Professor"].courses.append(newtime)


        return newgene

    def calcFitness(self):
        clashMsg = ""
        alreadyCounted = []
        countedIndex = []
        fitness = 0
        ifFound = False
            
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

        if num % 2 != 0:
            num = len(p2.chromosome) - 1 // 2
            isOdd = True

        randomNum = randint(0, num)
        sub = len(p2.chromosome) - randomNum

        for i in range(0, num - 1, +1):

            child.append(p2.chromosome[i])
        for j in range(num - 1, len(p2.chromosome), +1):

            child.append(self.chromosome[j])
        newchild = self.mutation(child)

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

        global POPULATION_SIZE
        global arrayofTime
        global GENES
        global LABS
        global ROOMS
        selected_id = request.POST.get('r1')

        meetingsperweek = 1
        prevFitness = 10
        COURSES = []
        fitness_Same_Count = 0
        ifFound = False
        population = []
        generation = 1
        isLabsAvailable = False
        isPhysics_LabsAvailable = False

        currentSemester = Semester.objects.filter(id=selected_id).last()
        roomCollection = []
        rooms = Rooms.objects.all()
        day_time = Day_Time.objects.all()

        for room in rooms:
            p_lab = False
            lab = False
            if room.is_physics_lab:
                p_lab = True
                isPhysics_LabsAvailable = True

            if room.islab:
                lab = True
                isLabsAvailable = True
                
            roomCollection.append(Room.Room(room.room_name,room.room_capacity,lab,p_lab))



        if isPhysics_LabsAvailable == False:
            messages.error(request,"No PHYSICS LABS Available")
            return redirect("scheduler-createtable")
        
        if isLabsAvailable == False:
            messages.error(request,"No LABS Available")
            return redirect("scheduler-createtable")

        for r in roomCollection:

            if r.isLab == True:
                LABS.append(r)
            elif r.isPhysicsLab == True:
                PhysicsLAB.append(r)
            else:
                ROOMS.append(r)



        for d_t in day_time:
            arrayofTime.append(d_t.day_time)

        meetingsperweek = currentSemester.meetings_per_week
        Courses = Semester_Courses.objects.filter(semester=currentSemester.id)


        if len(LABS)<=0:
            messages.error(request, "No LABS Available")
            return redirect("scheduler-createtable")
        if len(PhysicsLAB) <= 0:
            messages.error(request, "No PHYSICS LABS Available")
            return redirect("scheduler-createtable")
        if len(ROOMS)<=0:
            messages.error(request, "No Room Available")
            return redirect("scheduler-createtable")

        for _ in range(0,meetingsperweek,+1):  # FOR SUMMER SEMESTER
            for course in Courses:
                avail = []
                availability = Day_Time_Professor.objects.filter(prof=course.selected_Professor.id)
                for a in availability:
                    avail.append(a.day_time.day_time)
                
                _id = course.selected_Professor.id
                name = course.selected_Professor.professor_name

                profe = Professor.Professor(_id,name,avail,"",0,[])
                # messages.error(request, avail)
                # return redirect("scheduler-createtable")
                temp = {"Name": course.Course.course_name,"Professor":profe,"Capacity":course.Course.course_capacity,"Assigned-timeSlot": "", "Available_TimeSlots": [],"roomAlotted": None, "isLab": course.Course.course_isLab,"isPhysics_Lab":course.Course.course_isPhysics_Lab}
                COURSES.append(temp)

        GENES = COURSES
        for _ in range(POPULATION_SIZE):
            gnome = Individual.create_gnome()      
            population.append(Individual(gnome))

        while not ifFound:

            population = sorted(population, key=lambda x: x.fitness)

            if population[0].fitness <= 0:
                ifFound = True
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

            for _ in range(ns):
                rand = randint(s, ns - 1)
                parent1 = population[rand]
                rand = randint(s, ns - 1)
                parent2 = population[rand]

                child = parent1.crossover(parent2)
                new_generation.append(child)

            population = new_generation


            generation += 1

        print('SELECTED GENERATION ')
        data = []
        acheivedFitness = population[0].fitness
        achivedPopulation = []
        count=0
        for pop in population:
            count+=1
            if pop.fitness == acheivedFitness:
                achivedPopulation.append(pop)
            else:
                break
            if count>=5:
                break
        for i in range(0,len(achivedPopulation),+1):
            options = []
            for ch in achivedPopulation[i].chromosome:
                n_data = {"Name": ch["Name"], "Professor":ch["Professor"].name, "TimeSlot":ch["Assigned-timeSlot"],"Room":ch["roomAlotted"].room}
                options.append(n_data)
            data.append(options)
    
        return render(request, 'showtimetable.html',{'data': data})