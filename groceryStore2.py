import simpy
import math
import random
import numpy
import matplotlib.pyplot as plot
def genShoppingList():
     shoppingList=[]
     for x in range(7):
          shoppingList.append(random.randint(0,5))
     return shoppingList


def calculateMos(shoppingList, itemsBought, qTime, didPant):
     MOS=0
     shoppingListCount = sum(shoppingList)
     if didPant:
          itemVariable = (shoppingListCount-shoppingList[0]+1)/shoppingListCount
     else:
          itemVariable = itemsBought/shoppingListCount
     print("itemVariable", itemVariable)
     print(shoppingList, itemsBought, qTime)
     if itemVariable == 1  and qTime == 0:
          MOS = 5
     elif itemVariable > 0.9 and qTime <0.3:
          MOS = 4
     elif itemVariable > 0.8 and qTime <0.6:
          MOS = 3
     elif itemVariable > 0.7  and qTime <1:
          MOS = 2
     else:
          MOS = 1

     print("calcmos", MOS)
     return MOS


#calculateMos(genShoppingList(), 15,0.5)





def inter_arrival_time(lambda_):
     print("calcuklating timeout")
     print(numpy.random.exponential(1/lambda_))
     return numpy.random.exponential(1/lambda_) # beta = 1/lambda


def customerGenerator(env):
     id=0
     while True:
          new_customer = customer(env, id)
          env.process(new_customer)
          yield env.timeout(numpy.random.exponential(1/lambda_c))
          print("new customer added")
          id+=1



def customer(env, id):
     print("starting shopping customer with id")
     didPant = False
     i = 0
     items = 0
     queueTime = 0
     global tally, n
     shoppingList = genShoppingList()
     print("liste", shoppingList, containers)
     entry_time = env.now
     if shoppingList[i]>0 and shoppingList[i]<containers[i].level:
          containers[i].get(shoppingList[i])
          print("fetched pantelapp")
          items+=1
          didPant = True
          print(items)
     yield env.timeout(inter_arrival_time(lambda_t))
          #yield env.timeout(2)
     i+=1
     print("i", i)
     for i in range(1, 7):
     #while i<7 and i>=1:
          print(i)
          print(shoppingList[i], containers[i].level)
          if shoppingList[i]>0 and shoppingList[i]<containers[i].level:
               containers[i].get(shoppingList[i])
               print("added items to cart", )
               items = items+shoppingList[i]
               print(items)
               yield env.timeout(shoppingList[i]*timeToTakeItem[i])
               #yield env.timeout(2)
               print("item taken")

               print("waited")
          yield env.timeout(inter_arrival_time(lambda_t))
          i+=1
          print("i incremented", i)


     #print(items > 0)
     #print(items>0)
     if items>=1:
          print("entering checkout")

          start_queue = env.now
          req = containers[i].request()
          print(start_queue)
          yield req
          start_checkout = env.now
          yield env.timeout(items*time_scan+time_pay)
          containers[i].release(req)
          stop_checkout = env.now
          queueTime = start_checkout - start_queue
          print("queueTime", queueTime)
     print("fetching mos", id, shoppingList, items, queueTime)
     MOS_scores.append(calculateMos(shoppingList, items, queueTime, didPant))

def employee(env, id):
     i=0
     print("new emp")
     yield env.timeout(inter_arrival_time(lambda_t))
     while True:
          print(p_i,containers[i].level/containers[i].capacity<p_i, stationResources[i].users, stationResources[i].count==0, "ratio and employee")
          if containers[i].level/containers[i].capacity<p_i and stationResources[i].count == 0:
               print("refill required no employee at station")
               #add check if employee is on station

               req = stationResources[i].request()
               yield req
               yield env.timeout(timeToFillSection[i])
               containers[i].put((containers[i].capacity-containers[i].level))
               stationResources[i].release(req)
               print("refill complete", containers[i].level, containers[i].capacity)




          if i==6:
               i=0
          else:
               i+=1

          yield env.timeout(inter_arrival_time(lambda_t))
     #while i<7:
     #     #print("empcheck", i, containers[i].level, containers[i].capacity, containers[i].level/containers[i].capacity, p_i)
     #     if containers[i].level/containers[i].capacity<p_i:
     #          print("refill required")
     #          containers[i].put(containers[1].capacity-containers[i].level)
     #          req = stationResources[i].request()
     #          yield req
     #          yield env.timeout(timeToFillSection[i])
     #     if i==6:
     #          i=0
     #     else:
     #          i+=1








#defining stations
##SIMULATION
lambda_c = 1/3
lambda_t = 2
time_scan = 0.1
time_pay = 0.2
MOS_scores = []
timeToTakeItem = [0.1, 0.15, 0.1,0.1,0.15,0.1,0.2]
timeToFillSection = [60,36,42,42,30,60,90]
tally = 0
n = 0
#employees = 4
p_i = 0
containers = []
stationResources = []

def runSim(employees, simCount):
     MOS_averages = []
     global containers
     global stationResources
     for i in range(simCount):
          containers = []
          stationResources= []
          global p_i
          env = simpy.Environment()
          p_i = 0.05 * employees
          print("pppp", p_i)
          for x in range(employees):
               print("new emp")
               new_employee = employee(env, x)
               env.process(new_employee)
          for x in range(7):
               stationResources.append(simpy.Resource(env, capacity=1))
          print(stationResources)
          stationBottles = containers.append(simpy.Container(env, capacity=100, init=100))
          stationProduce = containers.append(simpy.Container(env, capacity=150, init=150))
          stationBread = containers.append(simpy.Container(env, capacity=50, init=50))
          stationDairy = containers.append(simpy.Container(env, capacity=150, init=150))
          stationMeat = containers.append(simpy.Container(env, capacity=80, init=80))
          stationFrozen = containers.append(simpy.Container(env, capacity=40, init=40))
          stationGeneral = containers.append(simpy.Container(env, capacity=250, init=250))
          stationCheckout = containers.append(simpy.Resource(env, capacity=4))
          print(containers)
          print(containers[1].capacity)

          env.process(customerGenerator(env))
          env.run(until=960)
          print("mos scores", MOS_scores)
          MOS_averages.append(sum(MOS_scores) / len(MOS_scores))
          print(MOS_averages)
     return MOS_averages



#for x in range(employees):
#     new_employee = customerGenerator2(env)
#     env.process(new_employee)
average_mos = []
for x in range(10):
     average_mos.append(runSim(x, 10))
     #print(average_mos)
print("get cancer", average_mos)
#plot.use('TkAgg')
plot.title("cancer mate")
plot.xlabel("get cancer")
plot.ylabel("bbbbrt")
plot.grid(color = "green", axis = "y")
plot.boxplot(average_mos)
plot.show()




