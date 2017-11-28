import sys

def print_test(lines=1000):
    if isinstance(lines, str) or isinstance(lines, unicode):
        lines = int(lines)
    for i in range(lines):
        print("output"*100)
    for i in range(lines):
        print("error"*100, file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print_test(*sys.argv[1:])
    else:
        print("Need times!")