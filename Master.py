import genAlg as GA
import pickle
import socket
from threading import Thread, Lock

reiteration = 20

connectedConns = []
threadLock = Lock()
receivedPopulation = []
generation = None
evCount = 0
totalEvCount = 0
currentBestScore = 0
foundCount = 0
population_size = 10
runTimes = 100
fitness_value = 1200.0
class Master(Thread):
    def __init__(self, ip, port, conn, index):
        Thread.__init__(self)
        self.ip, self.port = ip, port
        self.connection = conn
        self.connectionIndex = index

    def SendData(self, data):
        global connectedConns
        convertedData = pickle.dumps(data)
        connectedConns[0].send(convertedData)
        connectedConns[1].send(convertedData)

    def Process(self):
        global generation
        global evCount
        global currentBestScore
        global foundCount
        global totalEvCount
        global reiteration
        global population_size
        global runTimes
        global fitness_value

        evCount += 1
        generation = self.Merge2Population()
        generation.update_probabilities()
        if generation.best_agent.fitness() >= fitness_value:
            print(f'{round(generation.best_agent.fitness(), 3)} is found in {evCount} iteration with 2 different mutation chance')
            if foundCount < reiteration:
                foundCount += 1
                totalEvCount += evCount
                # reset part
                evCount = 0
                generation = GA.evolution(population_size)
                self.SendData(generation.population)
                # util.DrawFace(generation.best_agent.genome)
            else:
                print(f'The algorithm ran {reiteration} times. The Average Evolution Count is: {totalEvCount / reiteration}. iteration with 2 different mutation chance')
                exit()
        elif runTimes > evCount:
            self.SendData(generation.population)
        else:
            print(
                f'{round(generation.best_agent.fitness(), 3)} is found in {evCount} iteration with 2 different mutation chance')
            if foundCount < reiteration:
                foundCount += 1
                totalEvCount += evCount
                # reset part
                evCount = 0
                generation = GA.evolution(population_size)
                self.SendData(generation.population)
                # util.DrawFace(generation.best_agent.genome)
            else:
                print(
                    f'The algorithm ran {reiteration} times. The Average Evolution Count is: {totalEvCount / reiteration}. iteration with 2 different mutation chance')
                exit()
    def Merge2Population(self):
        global receivedPopulation #Merged population of size 2N (Fast +Slow)
        temp = GA.evolution(len(receivedPopulation))
        for i in range(len(receivedPopulation)):
            temp.population[i].set_gene(receivedPopulation[i].genome)  # 2N arrayini yeni populasyonumuza aktaralım
        temp.update_probabilities()
        # print("update ok")
        # Now let's reduce this combined population to N people, for this we will choose the genomes with the best fitness.
        N = len(receivedPopulation) // 2
        pr = [temp.reproduction_probability[agent_id] for agent_id in range(N * 2)]
        pr.sort()
        ti = len(pr) // 2
        newpr = []  #The fitness values of N individuals with high fitness are kept here
        for i in range(ti, len(pr)):
            newpr.append(pr[i])
        merged = GA.evolution(N)
        for i in range(N):
            for j in range(len(temp.reproduction_probability)):
                if (temp.reproduction_probability[j] == newpr[i]):  # individuals are checked to see if their fitness is high
                    merged.population[i].set_gene(temp.population[j].genome)  # high fitness individuals are added to the new population.
        # return evolution object
        receivedPopulation.clear()
        return merged

    def Listen(self):
        global connectedConns
        global receivedPopulation #Holds agent objects in the population from low and fast
        global threadLock
        while True:
            data = self.connection.recv(100000)
            if not data: continue
            convertedData = pickle.loads(data)
            threadLock.acquire()
            for i in range(len(convertedData)):
                receivedPopulation.append(convertedData[i])
            threadLock.release()
            if len(receivedPopulation) >= population_size*2: # to merge and resend when we receive populations from both slow and fast
                self.Process()

    def run(self):
        global connectedConns
        global generation
        if len(connectedConns) > 1:
            self.SendData(generation.population)
        self.Listen()


if __name__ == '__main__':
    # generation = GA.evolution(population_size)
    # TCP_IP = 'localhost'
    # TCP_PORT = 6001
    # BUFFER_SIZE = 100000
    # tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # tcpServer.bind((TCP_IP, TCP_PORT))
    # threads = []
    # tcpServer.listen(2)
    # for i in range(2):
    #     (conn, (ip, port)) = tcpServer.accept()
    #     print('A slave connected!')
    #     threadLock.acquire()
    #     connectedConns.append(conn)
    #     masterThread = Master(ip, port, conn, i)
    #     threadLock.release()
    #     masterThread.start()
    #     threads.append(masterThread)
    #
    # for t in threads:
    #     t.join()
    #Standart GA için burayı çalıştırın
    tryArr = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.90, 0.95, 1]

    for prob in range(len(tryArr)):
        totalEv = 0
        GA.p = tryArr[prob]
        for j in range(20):
            world = GA.evolution(10)
            for i in range(1000):
                best = world.evolve(G=1)
                totalEv = totalEv + 1
                if world.best_agent.fitness() >= fitness_value:
                    break
            #print(j, i, world.best_agent.fitness())
        print(f'For probabilty : {GA.p}\nThe algorithm ran {j + 1} times.The Average Evolution Count is: {totalEv / 20}')
        print(f'Final fitness Score: {world.best_agent.fitness()}\n')
