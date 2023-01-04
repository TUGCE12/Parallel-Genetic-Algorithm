import numpy as np
import matplotlib.pyplot as plt

import random
from operator import itemgetter
from math import *

priceA = [1, 4, 6, 4, 4]
priceB = [3, 8, 2, 5, 15]
priceC = [3, 12, 3, 5, 5]
priceD = [2, 6, 10, 2, 4]
priceE = [10, 5, 12, 6, 3]

allPrice = []

allPrice.append(priceA)
allPrice.append(priceB)
allPrice.append(priceC)
allPrice.append(priceD)
allPrice.append(priceE)

p = 1

class agent():
    def __init__(self, idx, m=15):
        self.id = idx
        self.m = m
        self.genome = self.create_gene()

    def create_gene(self):
        productA = []  # 30     uzunlugu 30 olmak zorunda fazla ya da az olamaz
        productB = []  # 40
        productC = []  # 20
        productD = []  # 40
        productE = []  # 20
        for i in range(40):
            if i < 30:
                productA.append(random.randint(0, 4))
                if i < 20:
                    productC.append(random.randint(0, 4))
                    productE.append(random.randint(0, 4))
            productB.append(random.randint(0, 4))
            productD.append(random.randint(0, 4))
        individual = []
        individual.append(productA)
        individual.append(productB)
        individual.append(productC)
        individual.append(productD)
        individual.append(productE)
        return individual

    def set_gene(self, new_gene):
        self.genome = new_gene

    def findf2or3Rate(self, xn):
        difference = max(xn) - min(xn)
        f2rate = 0
        if difference == 0:
            f2rate = 0.2
        elif difference < 20 and difference > 0:
            f2rate = difference / 100
        return f2rate

    def fitness(self):
        global allPrice
        fbase = 0  # Durum 0: fbase hesabi

        f2 = 0  # Durum 2  degiskenleri
        x1 = []
        x2 = []
        x3 = []
        x4 = []
        x5 = []
        fx1base = 0
        fx2base = 0
        fx3base = 0
        fx4base = 0
        fx5base = 0  # Durum 2 degiskenleri

        # Durum 1: t�m �ehirlerin ziyaret edilmesi
        flag = [0, 0, 0, 0, 0]
        f1 = 0
        for i in range(len(self.genome)):
            x1.append(self.genome[i].count(0))  # durum 2 icin gereken parametrelerin hesabi
            x2.append(self.genome[i].count(1))
            x3.append(self.genome[i].count(2))
            x4.append(self.genome[i].count(3))
            x5.append(self.genome[i].count(4))
            fx1base = fx1base + x1[i] * allPrice[i][0]
            fx2base = fx2base + x2[i] * allPrice[i][1]
            fx3base = fx3base + x3[i] * allPrice[i][2]
            fx4base = fx4base + x4[i] * allPrice[i][3]
            fx5base = fx5base + x5[i] * allPrice[i][4]  # durum 2 sonu
            for j in range(5):
                p = allPrice[i][j]  # durum 0 fbase hesabi
                itemNum = self.genome[i].count(j)
                fbase = fbase + (p * itemNum)  # durum 0 fbase hesabi
                if (self.genome[i].count(j) > 0):  # durum 1 kontrolu
                    flag[j] = 1

        if (flag.count(0) == 0):  # durum 1 kontrolu
            f1 = 100

        # Durum 2: Her bir sehir icin, Her urunden ayni miktarda satilmasi

        f2 = f2 + fx1base * self.findf2or3Rate(x1)
        f2 = f2 + fx2base * self.findf2or3Rate(x2)
        f2 = f2 + fx3base * self.findf2or3Rate(x3)
        f2 = f2 + fx4base * self.findf2or3Rate(x4)
        f2 = f2 + fx5base * self.findf2or3Rate(x5)
        # Durum 3: Tum sehirlerde dengeli miktarda urun satilmasi durumu (en iyi durum hepsinde 30 urun satilmasi)
        # bunun icin tum sehirlerde satilan toplam urun miktarlarini tuttugumuz bir dizi olusturalim
        f3 = 0
        Cities = [sum(x1), sum(x2), sum(x3), sum(x4), sum(x5)]
        f3 = f3 + fbase * self.findf2or3Rate(Cities)
        """print("fbase:", fbase)
        print("f1:", f1)
        print("f2:", f2)
        print("f3:", f3)"""
        score = fbase + f1 + f2 + f3
        return score


class evolution():
    def __init__(self, N):
        self.N = N
        self.population = {i: agent(i) for i in range(N)}
        self.update_probabilities()

    def update_probabilities(self):
        self.success = {i: self.population[i].fitness() for i in range(self.N)}
        total_success = sum(self.success.values())

        self.reproduction_probability = {i: self.success[i] / total_success for i in range(self.N)}

        sorted_by_success = sorted(self.success.items(), key=lambda kv: kv[1])
        self.best_agent = self.population[sorted_by_success[-1][0]]

    def selection(self):
        pr = [self.reproduction_probability[i] for i in range(self.N)]
        select = np.random.choice(self.N, 2, replace=False, p=pr)
        return select

    def crossover(self, selectedParents):
        parent0 = self.population[selectedParents[0]].genome
        parent1 = self.population[selectedParents[1]].genome
        child_gene = []
        cut = np.random.randint(len(parent1))
        for i in range(0, cut):
            child_gene.append(parent0[i])
        for i in range(cut, len(parent1)):
            child_gene.append(parent1[i])

        #child_gene = np.hstack((parent0[:cut], parent1[cut:]))
        return child_gene

    def mutation(self, child_gene):
        global p
        mutation_point = np.random.randint(len(child_gene))
        if np.random.rand() < p:
            for i in range(15):
                mutation_point2 = np.random.randint(len(child_gene[mutation_point]))
                child_gene[mutation_point][mutation_point2] = np.random.randint(5)
        return child_gene

    def create_offspring(self):
        parents = self.selection()
        child_gene = self.crossover(parents)

        child_gene = self.mutation(child_gene)
        return child_gene

    def create_new_population(self):
        sorted_by_success = sorted(self.success.items(), key=lambda kv: kv[1])
        self.best_agent = self.population[sorted_by_success[-1][0]]

        for i in range(self.N // 2):
            child_gene = self.create_offspring()
            agent_id = sorted_by_success[i][0]
            self.population[agent_id].set_gene(child_gene)

        self.update_probabilities()

    def evolve(self, G=10):
        for i in range(G):
            self.create_new_population()
        return self.population


