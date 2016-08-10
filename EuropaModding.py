from EuropaMod import *

mod_dir = 'C:/Users/moyer/Documents/Paradox Interactive/Europa Universalis IV/mod'
mod_name = 'StrongItaly'
history_dir = mod_dir + '/' + mod_name + '/history'
country_info_dir = history_dir + '/countries'
province_info_dir = history_dir + '/provinces'


def run_command(mod_instance, command):
    command_arr = mod_instance.parse(command)
    try:
        # commands are in the form <set/get> <type> <file_name/id> <values>
        if type(command_arr[2]) is str:
            command_arr[2] = [command_arr[2]]
        relevant_files = map(lambda x: mod_instance.get_file(x), command_arr[2])
        if not relevant_files:
            print 'No file matching {0}'.format(command_arr[2])
            return
        if command_arr[0] == 'get':
            if command_arr[1] == 'attr':
                attr = map(lambda x: [x, x.get_attribute(command_arr[3])], relevant_files)
                for file_and_val in attr:
                    if file_and_val[1]:
                        print '{0}: {1}'.format(file_and_val[0], file_and_val[1])
                    else:
                        print '{0}: Has no attribute {1}'.format(file_and_val[0], command_arr[3])
            elif command_arr[1] in ['name', 'tag']:
                map(print_x, relevant_files)
        elif command_arr[0] == 'set':
            if command_arr[1] == 'attr':
                if len(command_arr) > 5 and command_arr[5] == 'a':
                    prepend_dict = map(lambda x: [x, x.get_attribute(command_arr[3].keys())], relevant_files)
                else:
                    prepend_dict = map(lambda x: [x, {}], relevant_files)
                for val in prepend_dict:
                    val[0].set_attribute(concat_dicts(val[1], command_arr[3]))
    except IndexError:
        print 'Command: {0} Invalid, please give more arguments'.format(command)


def run_interface(mod_instance):
    print '\nEntering GUI\nPlease enter "exit" if you wish to quit'
    command = raw_input('EU4: ')
    while command not in ['exit', 'quit']:
        run_command(mod_instance, command)
        command = raw_input('EU4: ')
    print 'Leaving interface'


def run_tests():
    test_mod = EuropaMod()
    test_against = ['set', 'attr', ['1', '2', '3', '4'], {'owner' : 'ITA', 'add_core' : 'ITA'}]
    check_expect(test_mod.parse('set attr [1, 2, 3, 4] { owner : ITA, add_core : ITA }'),
                                test_against,
                 'Testing base parser stuff')
    test_mod.parse('var=test')
    check_expect('var' in test_mod.env_vars.keys(), True, 'Can get environment variable name')
    check_expect(test_mod.env_vars['var'], 'test', 'Test if value gotten correctly')
    check_expect(test_mod.parse('$var'), ['test'], 'Test if variables replaced well')
    check_expect(test_mod.parse('set attr [$var, other_val] { add_core : SWE }'),
                 ['set', 'attr', ['test', 'other_val'], {'add_core': 'SWE'}],
                 'Test if env var replacement works in a full command')


def main():
    global mod_dir, mod_name
    my_mod = EuropaMod(mod_dir, mod_name)
    run_interface(my_mod)


if __name__ == '__main__':
    test = False
    if test:
        run_tests()
    else:
        main()
