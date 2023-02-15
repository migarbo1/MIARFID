import click
import os

def parse_string(str):
    return str.replace('\n', '').replace('\t', '')

def create_ref_dict(ref):
    path = os.getcwd()
    filename = os.path.join(path, ref)
    ref_dict = {}
    with open(filename, 'r') as file:
        for line in file.readlines():
            line = parse_string(line)
            state, name = line.split(' ')
            ref_dict[state] = name
    return ref_dict

def parse_line(line):
    parsed_line = {}
    line = parse_string(line)
    for pair in str(line).split(' '):
        if pair.__contains__('@'):  
            content, state = pair.split('@')
            parsed_line[state] = parsed_line.get(state, '') + '{} '.format(content)
    return parsed_line

def create_ref(line_dict, ref_dict):
    res = '@inproceedings{\n'
    for key in sorted(line_dict.keys()):
        name = ref_dict[key]
        content = line_dict[key]
        res += '\t{} = \t{{ {} }}\n'.format(name, content)
    res += '}'
    return res

def read_input_file(file):
    path = os.getcwd()
    filename = os.path.join(path, file)
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines

@click.command()
@click.option('--file', help="file to parse")
@click.option('--ref', help="state reference file")
def main(file, ref):
    ref_dict = create_ref_dict(ref)
    for line in read_input_file(file):
        parsed_line = parse_line(line)
        print(create_ref(parsed_line, ref_dict))

if __name__== '__main__':
    main()
