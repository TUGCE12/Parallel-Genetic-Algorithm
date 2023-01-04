# Parallel-Genetic-Algorithm
It was made within the scope of GSU INF443 Distributed Systems and Applications Course.


The codes in the [Evolutionary-Algorithm-for-Assignment-Problem-with-Python](https://github.com/TUGCE12/Evolutionary-Algorithm-for-Assignment-Problem-with-Python/blob/main/tugceCelikGenetikAlgo.py) repository have been made objective-oriented. As a result, the genAlg.py file was created.
[For details of the problem, please refer to the description pdf in that relevant repo.](https://github.com/TUGCE12/Evolutionary-Algorithm-for-Assignment-Problem-with-Python/blob/main/assignment_2.pdf)

## Structures:
### 1. Agent:

Correspond to individuals in the population.

         productA = [] # 30
         productB = [] # 40
         productC = [] # 20
         productD = [] # 40
         productE = [] # 20
         
individual = [productA,....,productE] ## is the individual's gene sequence.

The number of indexes for productX is equivalent to the number of products we have.

The numbers 0, 1, 2, 3, 4 are kept in the productX array.

These figures represent the cities where the products are sold.

For example, let A be apples. That means we have 30 apples. Each index corresponds to 1 apple. Let productA[0] = 4, which means apple in index 0 sold in the 4th city.

The reason to set up the problem this way is that we want to sell all the products we have, and the product to be sold will never be more than what we have in our warehouse.

The importance of cities is since the price of each product differs from city to city. We keep this price list in the allPrice array.

We calculate how much profit the agent brings with the def fitness(self): function.
See fitness account details.

### 2. Evolution:
Selection cross-over and mutation operations are performed in this class.

# To run the standard GA:

in the [Master.py()](https://github.com/TUGCE12/Parallel-Genetic-Algorithm/blob/main/Master.py) file

    if __name__ == '__main__':

All code in the block is in the comment line.

You just have to uncomment the code below and run Master.py.

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




# To run the parallel GA:

in the [Master.py()](https://github.com/TUGCE12/Parallel-Genetic-Algorithm/blob/main/Master.py) file

    if __name__ == '__main__':

All code in the block is in the comment line.

You just have to uncomment the code below and run Master.py from terminal.

     generation = GA.evolution(population_size)
     TCP_IP = 'localhost'
     TCP_PORT = 6001
     BUFFER_SIZE = 100000
     tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     tcpServer.bind((TCP_IP, TCP_PORT))
     threads = []
     tcpServer.listen(2)
     for i in range(2):
         (conn, (ip, port)) = tcpServer.accept()
         print('A slave connected!')
         threadLock.acquire()
         connectedConns.append(conn)
         masterThread = Master(ip, port, conn, i)
         threadLock.release()
         masterThread.start()
         threads.append(masterThread)
    
     for t in threads:
         t.join()
         
After master.py is running, Slow.py and Fast.py need to be run from different terminals. 
