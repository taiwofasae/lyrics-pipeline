
import sys


def generate(template_file, key_value_pairs):
    
    with open(template_file, "r", encoding='utf-8') as file:
        text = file.read()
    
    template = text
    for p in key_value_pairs:
        template = template.replace(p[0], p[1])
    
    return template

if __name__ == '__main__':
    
    if len(sys.argv) < 3:
        print("usage: script template_file key1 val1 key2 val2 ...")
        sys.exit()
    
    template_file = sys.argv[1]
        
    pairs = list(zip(sys.argv[2::2], sys.argv[3::2]))
    
    print(generate(template_file=template_file, key_value_pairs=pairs))
    
    