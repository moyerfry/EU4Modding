from Utility import *
import re


class EUFile:
    def __init__(self, path, file_name):
        split_name = file_name.split('.')[0].split('-')
        self.tag = split_name[0].replace(' ', '')
        self.name = split_name[-1].replace(' ', '')
        print 'Loading {0}'.format(self.name)
        self.abs_file_name = safe_path_append(path, file_name)
        with open(self.abs_file_name, 'r') as f:
            self.information = f.readlines()
        self.edited = False

    def __del__(self):
        if self.edited:
            with open(self.abs_file_name, 'w') as f:
                f.writelines(self.information)

    def __str__(self):
        return 'Tag: {0}, Name: {1}'.format(self.tag, self.name)

    def get_attribute(self, name):
        if type(name) is str:
            relevant_lines = filter(lambda x: name in x, self.information)
            return map(lambda x: re.sub('\s', '', re.sub(r'' + name + ' *=', '', x)), relevant_lines)
        if type(name) is list:
            return map(lambda x: self.get_attribute(x), name)

    def set_attribute(self, in_dict):
        for k in in_dict.keys():
            relevant_lines = filter(lambda x: k in x, self.information)
            if len(relevant_lines) > 0:
                index = self.information.index(relevant_lines[0])
                self.information = filter(lambda x: x not in relevant_lines, self.information)
                if type(in_dict[k]) is str:
                    self.information.insert(index, k + ' = ' + in_dict[k] + '\n')
                if type(in_dict[k]) is list:
                    for item in reversed(in_dict[k]):
                        self.information.insert(index, k + ' = ' + item + '\n')
        self.edited = True
