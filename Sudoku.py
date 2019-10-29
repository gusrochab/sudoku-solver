from collections import Counter


def cross(a, b):
    return [i+j for i in a for j in b]


def grid_values(str_version):
    values = {}
    for i in range(len(str_version)):
        if str_version[i] == '.':
            values.update({boxes[i]: '123456789'})
        else:
            values.update({boxes[i]: str_version[i]})
    return values


def str_versions(dic):
    str_version=''
    for i in dic:
        str_version +=dic.get(i)
    return str_version


def display(str_values):
    n = 0
    for i in range(3):
        for j in range(3):
            print('{} {} {} | {} {} {} | {} {} {}'.format(str_values[n], str_values[n + 1], str_values[n + 2],
                                                          str_values[n + 3], str_values[n + 4], str_values[n + 5],
                                                          str_values[n + 6], str_values[n + 7], str_values[n + 8]))
            n += 9
        if i < 2:
            print('------+-------+-------')


def eliminate(dic):
    for i in dic:
        box_list = []
        numbers = dic.get(i)
        if len(numbers) == 1:
            for j in range(9):
                if i in rows_units[j]:
                    box_list.append(rows_units[j])
                if i in colums_units[j]:
                    box_list.append(colums_units[j])
                if i in squares_units[j]:
                    box_list.append(squares_units[j])
            box_list = box_list[0] + box_list[1] + box_list[2]
            box_list = list(set(box_list))

            for k in dic:
                if k in box_list and k != i:
                    possible_numbers = dic.get(k)
                    possible_numbers = possible_numbers.replace(numbers, '')
                    dic.update({k: possible_numbers})
    return dic


def only_choice(dic, block):
    for unit in block:
        possible_nums = []
        single_nums = []
        for box in unit:
            possible_nums.append(dic.get(box))
        #print(possible_nums)
        possible_nums = ''.join(possible_nums)
        #print(possible_nums)
        counters = Counter(possible_nums)
        for counter in counters:
            if counters.get(counter) == 1:
                single_nums.append(counter)
        #print('single num: {}'.format(single_nums))
        for num in single_nums:
            for box in unit:
                if len(dic.get(box)) > 1:
                    if num in dic.get(box):
                        dic.update({box: num})
    return dic


def reduce_puzzle(dic):
    i=0
    possible_nums = []
    actual_possible_nums = []
    for box in dic:
        possible_nums.append(dic.get(box))
        actual_possible_nums.append(dic.get(box))
    possible_nums_str = ''.join(possible_nums)
    actual_possible_nums_str = possible_nums_str
    while len(possible_nums_str) > 81:
        possible_nums_str = actual_possible_nums_str
        dic = eliminate(dic)
        dic = only_choice(dic, rows_units)
        dic = only_choice(dic, colums_units)
        dic = only_choice(dic, squares_units)
        for box in dic:
            actual_possible_nums.append(dic.get(box))
        actual_possible_nums_str = ''.join(possible_nums)
        if len(actual_possible_nums_str) == len(possible_nums_str):
            return dic
            break
    return dic


def stop_condition(dic):
    for box in dic:
        if len(dic.get(box)) == 0:
            return True
    #str_v = str_versions(dic)
    #print(str_v)
    #print(len(str_v))
    #display(str_v)
    return False

def search(dic):
    dic = reduce_puzzle(dic)
    print(dic)
    nums = 0
    if stop_condition(dic):
        return False
    for box in dic:
        if len(dic.get(box)) == 1:
            nums +=1
            if nums == 81:
                print(dic)
                display(str_versions(dic))
    else:
        new_dics = []
        for box in dic:
            if len(dic.get(box)) == 2:
                for i in range(2):
                    new_dics.append(dic.copy())
                    new_dics[i].update({box: dic.get(box)[i]})
                return(search(new_dics[0]) + search(new_dics[1]))


rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
rows_units = [cross(row, cols) for row in rows]
colums_units = [cross(rows, col) for col in cols]
rowsby3 = [rows[i*3:i*3+3] for i in range(3)]
colsby3 = [cols[i*3:i*3+3] for i in range(3)]
squares_units = [cross(row, col) for row in rowsby3 for col in colsby3]
str_version = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
#display(str_version)
dictionary = grid_values(str_version)
print(dictionary)
dictionary = search(dictionary)
display(dictionary)

