from EuropaClass import *
from Utility import *
import os
import re


class EuropaMod:

    def __init__(self, dir_name='', mod_name=''):
        if dir_name and mod_name:
            self.mod_file = EUFile(dir_name, mod_name + '.mod')
            self.mod_base_path = safe_path_append(dir_name, mod_name)
            replace_files = map(lambda x: x[1:-1], self.mod_file.get_attribute('replace_path'))
            self.file_dict = {}
            for item in replace_files:
                path_here = safe_path_append(self.mod_base_path, item)
                self.file_dict[path_here] = map(lambda x: EUFile(path_here, x), os.listdir(path_here))
        self.env_vars = {}

    def get_file(self, find_val):
        relevant_files = []
        for k in self.file_dict.keys():
            relevant_files.extend(filter(lambda x: x.tag == find_val or x.name == find_val, self.file_dict[k]))
        if relevant_files:
            return relevant_files[pick_one(relevant_files)]
        else:
            return None

    @staticmethod
    def remove_spaces_command(command):
        for char in ['\[', '\]', '\{', '\}', ',', ':', '=']:
            command = re.sub(r'\s*' + char + '\s*', char[-1], command)
        return command.replace("'", '')

    @staticmethod
    def create_var(piece):
        if ',' in piece and ':' not in piece:
            return piece.split(',')
        elif ':' in piece:
            out_dict = {}
            for mapping in piece.replace('{', '').replace('}', '').split(','):
                if ':' not in mapping:
                    print 'Invalid mapping {0}'.format(mapping)
                else:
                    split_var = mapping.split(':')
                    out_dict[split_var[0]] = EuropaMod.create_var(split_var[1])
            return out_dict
        else:
            return piece

    # Takes in a string and returns a list of strings, list, and dict
    def parse(self, command):
        com_split = filter(lambda x: x, re.split(r'[\[\]{} ]', self.remove_spaces_command(command)))
        out_list = []
        for piece in com_split:
            if '$' in piece:
                var_name = re.findall(r'\$[a-zA-Z0-9]*', piece)[0][1:]
                if var_name in self.env_vars.keys():
                    piece = piece.replace('$' + var_name, self.remove_spaces_command(str(self.env_vars[var_name])))
            if '=' in piece:
                split_piece = piece.split('=')
                var_name = split_piece[0]
                self.env_vars[var_name] = self.create_var(split_piece[1])
            out_list.append(self.create_var(piece))
        return out_list




