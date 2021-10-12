import matplotlib.pyplot as plt
import statistics
import copy
import numpy as np

password = "privet"

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

def graph(data):
    xAxis = [password[i] for i in range(1,len(password))]
    plt.bar(range(len(data)),data)
    plt.xticks(range(len(data)),xAxis)
    plt.show()


# def analyse(input):
#     file = open("D:\\Progs\\HappyMeal\\KeySig\\inputs_old","r")
#     lines = file.read().split('\n\n')
#     file.close()
#     lines = lines[:-1]
#     ref = exp_learn(proceed(lines))
#     data = [x for x in proceed([input])][0][1:]
#     #print("res")
#     res = [a - b for a,b in zip(ref,data)]

def print_exp_value(data):
    test = "Expected values: "
    for el in data:
        test = test + str(el)
        test = test + " ms, "
    test = test[:-2]
    print(test)

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


def run():
    file = open("D:\\Progs\\HappyMeal\\KeySig\\inputs", "r")
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

run()

