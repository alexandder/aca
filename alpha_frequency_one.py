__author__ = 'aleksander'

import os
import random

def write_dict_to_file_for_rule(rule, N, alpha, path):
    k = 1500
    print ("Rule " + str(rule) + ". k = " + str(k))
    abf_dict = show_frequencies_for_different_initial_vector(N, k, rule, alpha)
    create_dir(path, rule)
    fl = open(path + str(rule) + '/' + str(alpha), 'a')
    fl.write(str(abf_dict))
    fl.close()

def show_frequencies_for_different_initial_vector(N, k, rule, alpha):
    result = {"111": [], "110": [], "101": [], "100": [], "011": [], "001": [], "010": [], "000": []}
    for i in range(200):
        I = create_random_initial_vector(N)
        sim = simulate(I, N*k, rule, alpha)
        freq = getFrequenciesOfSimulation(sim)
        blockFreqs = getAggregateFrequenciesForEachBlock(freq)
        for block in blockFreqs:
            lastFreq = blockFreqs[block][len(blockFreqs[block]) - 1]
            result[block].append(lastFreq)
        print("For i = " + str(i))
    print("Ended for rule = " + str(rule) + ", alpha = " + str(alpha))
    return result

def create_random_initial_vector(n):
    return [random.randint(0,1) for i in range(n)]

def getAggregateFrequenciesForEachBlock(frequencies):
    result = {"111": [], "110": [], "101": [], "100": [], "011": [], "001": [], "010": [], "000": []}
    f0 = frequencies[0]
    sum = 0
    for b in f0:
        sum = 1.0 * sum + f0[b]
    for i in range(len(frequencies)):
        f = frequencies[i]
        for block in f:
            if i == 0:
                result[block].append(f[block] / sum)
            else:
                prev = sum * i * result[block][i - 1]
                result[block].append((prev + f[block]) / (sum * (i + 1)))
    return result

def getFrequenciesOfSimulation(simulation):
    result = []
    for step in simulation:
        result.append(getFrequencies(step))
    return result

def getFrequencies(vector):
    res = {"111": 0, "110": 0, "101": 0, "100": 0, "011": 0, "001": 0, "010": 0, "000": 0}
    for i in range(len(vector)):
        if i == len(vector) - 2:
            index = str(vector[i]) + str(vector[i + 1]) + str(vector[0])
            res[index] = res[index] + 1
        elif i == len(vector) - 1:
            index = str(vector[i]) + str(vector[0]) + str(vector[1])
            res[index] = res[index] + 1
        else:
            index = str(vector[i]) + str(vector[i + 1]) + str(vector[i + 2])
            res[index] = res[index] + 1
    return res

def apply_rule(rule, l, c, r, alpha):
    if alpha < 0 or alpha > 1:
        raise Exception('Wrong alpha: ' + str(alpha))
    random_number = random.random()
    if random_number < alpha:
        return applyRule(rule, l, c, r)
    return applyRule(204, l, c, r)

def applyRule(number, l, c, r):
    binary_rule_number = format(number, "#010b")[2:]
    neighborhood = int(str(l) + str(c) + str(r), 2)
    position = -neighborhood + 7
    return int(binary_rule_number[position])

def apply_rule_to_vector(a, rule_number, alpha):
    result = []
    for i in range(len(a)):
        if i == len(a) - 1:
            result.append(apply_rule(rule_number, a[i - 1], a[i], a[0], alpha))
        elif i == 0:
            result.append(apply_rule(rule_number, a[len(a) - 1], a[i], a[i + 1], alpha))
        else:
            result.append(apply_rule(rule_number, a[i - 1], a[i], a[i + 1], alpha))
    return result

def simulate(initial, T, ruleNumber, alpha):
    res = []
    res.append(initial)
    for k in range(T):
        res.append(apply_rule_to_vector(res[len(res) - 1], ruleNumber, alpha))
    return res

def create_dir(path, rule):
    if not os.path.exists(path + str(rule)):
        os.makedirs(path + str(rule))

def write_freqs_to_file_for_alphas(rule, N, alphas, path):
    for alpha in alphas:
        write_dict_to_file_for_rule(rule, N, alpha, path)

path = '/users/kdm/wbolt/aleksander/aca/chartsAca/'
alphas = [0.01, 0.02, 0.03, 0.04, 0.05, 0.7, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45,
          0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.92, 0.95, 0.97, 1.0]
rules = []
for rule in range(25):
    write_freqs_to_file_for_alphas(rule, 77, alphas, path)