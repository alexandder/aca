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
alphas = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
rules = [76, 77, 78, 79, 80, 81, 82, 83, 84, 85,
          87, 88, 91, 92, 93, 94, 95, 97, 98, 99, 100, 103, 104, 107, 108, 109, 111, 112,
          113, 114, 115, 116, 117, 118, 119, 121, 123, 125, 127, 130, 131, 132,
          133, 134, 138, 139, 140, 141, 142, 143, 144, 145, 148, 152, 154, 155, 156, 157,
          158, 159, 162, 163, 164, 166, 167, 170, 171, 172, 173, 174, 175, 176, 177,
          178, 179, 180, 181, 184, 185, 186, 187, 188, 189, 190, 191, 194, 196, 197,
          198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212,
          213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 226, 227, 228, 229,
          230, 231, 232, 233, 236, 237, 240, 241, 242, 243, 244, 245, 246, 247]
for rule in rules:
    write_freqs_to_file_for_alphas(rule, 77, alphas, path)