import matplotlib.pyplot as plt
import statistics
import copy
import database
import numpy as np

password = "privet"
amplitude = 1

def proceed(lines):
    for i in range(len(lines)):
        lines[i]=lines[i].split("\n")
        for j in range(len(lines[i])):
            lines[i][j]=lines[i][j].split()
            if (j==0):
                offset = int(lines[i][j][2])
            lines[i][j][2] = int(lines[i][j][2]) - offset
    #print(lines)
    return lines

def delay_calc(lines):
    new_data = copy.deepcopy(lines)
    for i in range(len(new_data)):
        for j in reversed(range(len(new_data[i]))):
            if (j != 0):
                new_data[i][j][2] = new_data[i][j][2] - new_data[i][j - 1][2]
    return new_data

def mean_data(inputs, exp):
    data = copy.deepcopy(inputs)[0]
    for i in range(len(data) - 1):
        data[i + 1][2] = exp[i]
    return data

def hold_calc(data):
    hold_data = []
    #print(data)
    for i in range(len(data)):
        if (data[i][0]=='up'):
            continue
        for j in range(i+1,len(data)):
            if (data[i][1]==data[j][1]):
                hold_data.append(data[j][2]-data[i][2])
                break
    return hold_data

def key_rel_data(data):
    key_data = []
    for i in range(len(data)):
        if (data[i][0]=='up'):
            continue
        for j in range(i+1,len(data)):
            if (data[i][1]==data[j][1]):
                key_data.append([data[i][1],data[i][2],data[j][2]])
                break
    return key_data

def remove_release(lines):
    new_data = []
    for i in range(len(lines)):
        new_data.append([x for x in lines[i] if x[0] == 'down'])
    return new_data

def identify_keys(input):
    xAxis = [0] * len(input)
    count = 0
    for i in range(len(input)):
        if (input[i][0] == 'down'):
            xAxis[i] = count
            for j in range(count + 1, len(input)):
                if (input[j][1] == input[i][1] and input[j][0] == 'up'):
                    xAxis[j] = count
                    break
            count += 1
    return xAxis

def plot_input(input):
    xAxis = identify_keys(input)
    xAxis=[password[i] for i in xAxis]
    print(xAxis)
    keys = [x[2] for x in input]
    plt.scatter(xAxis,keys)
    plt.show()

def exp_learn(new_data):
    exp = []
    #print(new_data)
    for i in range(len(new_data[0])):
        exp.append(0)
        for j in range(len(new_data)):
            exp[i]+=new_data[j][i][2]
        exp[i]=exp[i]/len(new_data)
    exp = exp[1:]
    return exp

def dispersion(data):
    disp = []
    for i in range(1,len(data[0])):
        temp = []
        for j in range(len(data)):
            temp.append(data[j][i][2])
        print("For ",password[i]," key:",temp)
        disp.append(
            round(np.sqrt(statistics.variance(temp))))
    return disp

def normalizeData(mean_attempts):
    max_time = mean_attempts[len(mean_attempts)-1][2]
    for i in range(len(mean_attempts)):
        mean_attempts[i][2] = mean_attempts[i][2]/max_time
    return mean_attempts

def calcAmpl(key_data, t, num):
    global amplitude

    for i in range(len(key_data)):
        if (i==num):
            continue
        if (key_data[i][1]<=t and t<=key_data[i][2]):
            return 2*amplitude
    return amplitude

def calcHaar(r,m,t):
    if (r==0 and m==0):
        return 1

    if ((m-1)/pow(2,r)<=t and t<(m-0.5)/pow(2,r)):
        return pow(2,r/2)
    elif ((m-0.5)/pow(2,r)<=t and t<m/pow(2,r)):
        return -pow(2,r/2)
    else:
        return 0

def calcAmplVector(key_data):
    a_vector = []
    for i in range(len(key_data)):
        a_vector.append(calcAmpl(key_data,key_data[i][1],i))
    return a_vector

def calcHaarVector(key_data):
    n = len(key_data)
    r_norm = n / np.log2(n)

    haar = []
    a_vector = calcAmplVector(key_data)
    sum = 0
    for r in range(n):
        sum=0
        m_norm = n / pow(2,r)
        for m in range(n):
            haar_val = calcHaar(r/r_norm,m/m_norm,key_data[r][1])
            #haar_val = calcHaar(r, m, key_data[r][1])
            sum+=haar_val*a_vector[m]
        haar.append(abs(sum)/n)
    return haar


def graph(data):
    xAxis = [password[i] for i in range(1,len(password))]
    plt.bar(range(len(data)),data)
    plt.xticks(range(len(data)),xAxis)
    plt.show()

def print_exp_value(data):
    test = "Expected values: "
    for el in data:
        test = test + str(el)
        test = test + " ms, "
    test = test[:-2]
    #print(test)

def print_dispersion(data):
    test = "Dispersion: "
    for el in data:
        test = test + str(el)
        test = test + " ms, "
    test = test[:-2]
    print(test)

def overlap_analysis(data):
    part_overlap = []
    full_overlap = []
    overlap = []
    ids = identify_keys(data)
    for i in range(len(data)):
        debug_i = data[i][1]
        if (data[i][0]=='up'):
            continue
        consumed = []
        for j in range(i+1,len(data)):
            debug_j = data[j][1]
            if (data[j][1]==data[i][1]):
                break
            else:
                consumed.append([data[j][1],ids[j]])
        overlap.append([data[i][1],consumed])
    for el in overlap:
        consumed_part = []
        consumed_full = []
        checked = []
        found = False
        for i in range(len(el[1])):
            curr = el[1][i][1]
            if (curr not in checked):
                for j in range(i+1,len(el[1])):
                    if (el[1][i][1]==el[1][j][1]):
                        consumed_full.append(el[1][i][0])
                        checked.append(el[1][i][1])
                        found = True
                        break
                if (not found):
                    consumed_part.append(el[1][i][0])
                    checked.append(el[1][i][1])
        if (len(consumed_full)!=0):
            full_overlap.append([el[0],consumed_full])
        if (len(consumed_part) != 0):
            part_overlap.append([el[0], consumed_part])
    return [full_overlap,part_overlap]

def print_overlap(overlap):
    str = ''
    for j in range(len(overlap)):
        str+=overlap[j][0]+':'
        for k in range(len(overlap[j][1])):
            str+=' '+overlap[j][1][k]+','
        str = str[:-1] + '\n'
    str = str[:-1]
    print(str)


def run(login):
    file = open("Y:\\Keyboard\\"+login, "r")
    lines = file.read().split('\n\n')
    file.close()
    lines = lines[:-1]
    data = proceed(lines)
    one = data[0]
    overlaps = overlap_analysis(one)
    plot_input(one)
    exp_res = exp_learn(remove_release(delay_calc(data)))
    graph(exp_res)
    print_exp_value(exp_res)
    disp = dispersion(remove_release(delay_calc(data)))
    graph(disp)
    print_dispersion(disp)
    print("Full Overlap: ")
    print_overlap(overlaps[0])
    print("Part Overlap: ")
    print_overlap(overlaps[1])

def make_sign(login):
    file = open("Y:\\Keyboard\\"+login, "r")
    lines = file.read().split('\n\n')
    file.close()
    lines = lines[:-1]
    data = proceed(lines)
    exp = exp_learn(data)
    mean = mean_data(data,exp)
    norm_data = normalizeData(mean)
    key_rel = key_rel_data(norm_data)
    vec = calcHaarVector(key_rel)
    #print(vec)
    return vec

def save_sign(login, vector):
    database.save(database.User(login, vector, password))