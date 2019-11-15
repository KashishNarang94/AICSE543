import random
import matplotlib.pyplot as plt

N=8   #Number of queens
p=20  #population size
k=6 #Selecting k best states
itr_list=[]
avg_fitness_per_itr=[]

def population():
    pop=[]
    for popstrength in range(p):
        n=random.sample(range(0,N),N)   
        pop.append(n) 
    #print(pop)
    return pop

def fitnessOfState(state):
    clashes=0

    for r in range(len(state)):
        for c in range(r,len(state)):
            if r!=c:
                #Diagonal Clashes
                rr=abs(r-c)
                cc=abs(state[r]-state[c])
                if rr==cc:
                    clashes=clashes+1
                #Column clashes
                if state[r]==state[c]:
                    clashes=clashes+1
    return clashes

def popFitness(pop):
    popfitnesslist=[]
    for i in pop:
        fitval=fitnessOfState(i)
        popfitnesslist.append(fitval)
    #print("Fitness values")
    #print(popfitnesslist)
    return popfitnesslist



def avg_fitness(popfitnesslist):
    sum_fitness=0
    for i in range(len(popfitnesslist)):
        sum_fitness+=popfitnesslist[i]
    return sum_fitness/len(popfitnesslist)
    
def reproduce(p1,p2):
    #print("child reproduction")
    child=[]
    for i in range(len(p1)):
        if i%2==0:
            child.append(p1[i])
        else:
            child.append(p2[i])
    return child

def mutation(child):
    #print("Mutation")
    n=random.choice(range(0,N))
    k=random.choice(range(0,N))
    child[k]=n
    
    return child
    

def new_gen(pop):
    newpop=[]
    r=int(len(pop)/2)
    for i in range(r):
        p1=pop[2*i]
        #print(p1)
        p2=pop[2*i+1]
        #print(p2)
        
        #crossover
        child=reproduce(p1,p2)
     
        #mutation
        child=mutation(child)
        newpop.append(child) 
        
        #mutation2
        child=mutation(child)
        newpop.append(child) 
        
    pop.extend(newpop)
    
    return pop
    
def plotgraph(itr_list,avg_fitness_per_itr):
    plt.plot(itr_list,avg_fitness_per_itr)  
    plt.xlim(0.01,len(itr_list))
    plt.ylim(0,max(avg_fitness_per_itr))
    plt.xlabel('Iteration Number') 
    plt.ylabel('Average fitness') 
    plt.show()

    
    
def main():
    itr=0
    
    #insitialize population
    pop=population()
    
    #find fitness value
    popfitnesslist=popFitness(pop)
    
    
    while True:
        #sort combined list
        itr=itr+1
        itr_list.append(itr)
        #print("Iteration = ",itr)
        breakval=0
        popfitnesslist,pop=zip(*sorted(zip(popfitnesslist,pop)))
      
        #new generation creation
        newpop=new_gen(list(pop[:k]))
        pop=list(pop[k:p-k])
        pop.extend(newpop)
        
        #find fitness value
        popfitnesslist=popFitness(pop)
        
        #Avg fitness which show be low for a good solution
        avg_fitness_per_itr.append(avg_fitness(popfitnesslist))
    
        for i in range(len(popfitnesslist)):
            if popfitnesslist[i]==0:
                print("Found solution")
                print(pop[i])
                breakval=1
                break
        if breakval==1:
            break
    print("Total iterations =");print(itr)
    plotgraph(itr_list,avg_fitness_per_itr)
    

main()