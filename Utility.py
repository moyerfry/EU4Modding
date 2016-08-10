test_num = 1


def safe_path_append(directory='', file_name=''):
    if directory and directory[-1] in ['/', '\\']:
        return directory + file_name
    elif directory:
        return directory + '/' + file_name
    else:
        return file_name


def print_x(x):
    print x


def pick_one(list_of_things):
    index = 0
    if len(list_of_things) == 1:
        return 0
    out = -1
    while 0 <= out < len(list_of_things):
        for item in list_of_things:
            print '{0}: {1}'.format(index, item)
            index += 1
        out = raw_input('Enter number to use: ')
    return out


def check_expect(actual, expected, desc=''):
    global test_num
    base_str = 'Test {0}{1}: '.format(test_num, ', ' + desc if desc else '')
    if actual == expected:
        print base_str + 'passed'
    else:
        print base_str + 'failed'
        print 'Actual ' + str(actual)
        print 'Expected ' + str(expected)
    test_num += 1


def concat_dicts(dict1, dict2):
    if not dict1:
        return dict2
    if not dict2:
        return dict1
    out_dict = {}
    for k in dict1.keys():
        if k in dict2.keys():
            if type(dict1[k]) == str and type(dict2[k]) == str:
                out_dict[k] = {k: [dict1[k], dict2[k]]}
            if type(dict1[k]) == str and type(dict2[k]) == list:
                dict2[k].append(dict1[k])
                out_dict[k] = dict2[k]
            if type(dict2[k]) == str and type(dict1[k]) == list:
                dict1[k].append(dict2[k])
                out_dict[k] = dict1[k]
            if type(dict1[k]) == list and type(dict2[k]) == list:
                dict1[k].extend(dict2[k])
                out_dict[k] = dict1[k]
        else:
            out_dict[k] = dict1[k]
    for k in dict2.keys():
        if k not in dict1.keys():
            out_dict[k] = dict2[k]
    return out_dict