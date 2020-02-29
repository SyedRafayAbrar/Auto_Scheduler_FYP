from Auto_Scheduler.com.Classes import Room,Professor
from Auto_Scheduler.models import Rooms,Professors,Semester,Day_Time
import random
from random import randint

POPULATION_SIZE = 100
GENES = []
ROOMS = []
LABS = []
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
        global arrayofTime
        global ROOMS
        global LABS
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
        else:
            newgene["roomAlotted"] = random.choice(ROOMS)

        newgene["Assigned-timeSlot"] = newtime
        # newGENE = Gene
        # print('Gene->>>>>>', newgene)

        return newgene

    def calcFitness(self):
        clashMsg = ""
        fitness = 0
        ifFound = False
        for i in range(0, len(self.chromosome), +1):
            if self.chromosome[i]["Assigned-timeSlot"] in self.chromosome[i]["Professor"].availability:
                for ch in range(0, len(self.chromosome), +1):
                    if ch != i:
                        if self.chromosome[i]["Assigned-timeSlot"] == self.chromosome[ch]["Assigned-timeSlot"] and \
                            self.chromosome[ch]["roomAlotted"].room == self.chromosome[i]["roomAlotted"].room:
                            # print('CLASH WITH OTHER TEACHER')
                            clashMsg = "CLASH WITH OTHER TEACHER"
                            ifFound = True
                            fitness += 1
                        # if self.chromosome[i]["Professor"].name == self.chromosome[ch]["Professor"].name:
                        #     if self.chromosome[i]["Assigned-timeSlot"][0:3] == self.chromosome[ch]["Assigned-timeSlot"][0:3]:
                        #         fitness+=1
                        #         clashMsg = "SameTime"


            else:
                # self.chromosome[i]["isClash"] = True
                # print('NOT IN AVAILABLE TIMESLOT')
                fitness += 1
            if self.chromosome[i]["roomAlotted"].capacity < self.chromosome[i]["Capacity"]:
                clashMsg = "CAPACITY ISSUE"
                ifFound = True
                fitness += 1

            if self.chromosome[i]["isLab"] == False:
                if self.chromosome[i]["roomAlotted"].isLab == True:
                    clashMsg = "LAB Issue"
                    ifFound = True
                    fitness += 1

        if ifFound == False:
            self.chromosome[i]["isClash"] = ""
        self.chromosome[i]["isClash"] = clashMsg
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
        global ROOMS
        for gene in range(0, len(mutatedChromosome), +1):
            for nextGene in range(0, len(mutatedChromosome), +1):

                if nextGene != gene:
                    # print(mutatedChromosome[gene]["Assigned-timeSlot"])
                    # print(mutatedChromosome[nextGene]["Assigned-timeSlot"])
                    # if self.chromosome[gene]["Professor"].name == self.chromosome[nextGene]["Professor"].name:
                    #         if self.chromosome[gene]["Assigned-timeSlot"][0:3] == self.chromosome[nextGene]["Assigned-timeSlot"][0:3]:

                    if mutatedChromosome[gene]["Assigned-timeSlot"] == mutatedChromosome[nextGene]["Assigned-timeSlot"]:

                        if mutatedChromosome[gene]["roomAlotted"].room == mutatedChromosome[nextGene][
                            "roomAlotted"].room:
                            if len(mutatedChromosome[gene]["Available_TimeSlots"]) > 1:
                                for i in mutatedChromosome[gene]["Available_TimeSlots"]:
                                    if i != mutatedChromosome[gene]["Assigned-timeSlot"]:
                                        mutatedChromosome[gene]["Assigned-timeSlot"] = i
                                        break
                                # mutatedChromosome[gene]["Assigned-timeSlot"] = random.choice(
                                #     mutatedChromosome[gene]["Available_TimeSlots"])
                            elif len(mutatedChromosome[nextGene]["Available_TimeSlots"]) > 1:
                                for i in mutatedChromosome[nextGene]["Available_TimeSlots"]:
                                    if i != mutatedChromosome[nextGene]["Assigned-timeSlot"]:
                                        mutatedChromosome[nextGene]["Assigned-timeSlot"] = i
                                        break
                                # mutatedChromosome[nextGene]["Assigned-timeSlot"] = random.choice(
                                #     mutatedChromosome[nextGene]["Available_TimeSlots"])

                        # if self.chromosome[i]["isLab"] == False:
                        #     if self.chromosome[i]["roomAlotted"].isLab == True:
                        #         fitness += 1
            if mutatedChromosome[gene]["isLab"] == False:
                if mutatedChromosome[gene]["roomAlotted"].isLab == True:
                    mutatedChromosome[gene]["roomAlotted"] = random.choice(ROOMS)

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
        selected_id = request.POST.get('semester_id')
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

        # {"Name": "MAD", "Professor": Professor("Shoaib",
        #                                        [arrayofTime[0], arrayofTime[1], arrayofTime[2], arrayofTime[3],
        #                                         arrayofTime[4],
        #                                         arrayofTime[5], arrayofTime[6]], "", 0),
        #  "Capacity": 55, "Assigned-timeSlot": "", "Available_TimeSlots": [], "isClash": "",
        #  "roomAlotted": None, "isLab": True}