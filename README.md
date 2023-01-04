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

-----------------
