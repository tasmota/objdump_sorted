import argparse
import subprocess

def demangle(name):
    args = ['c++filt', name]
    demangled = subprocess.run(args, capture_output=True)
    return demangled.stdout.decode()[:-1]


def start(args):
    dump = subprocess.run(["objdump", "-t", args.filename], capture_output=True)
    dump = filter(lambda _: _, dump.stdout.decode().split("\n")[4:])
    unpacked = [row.split("\t") for row in dump]

    result = []
    print(f"Parsing {args.filename} ...")

    for row in unpacked:
        try:
            flags, size_name = row
            if flags.endswith(".flash.text"):
                size, *hidden, name = size_name.split(" ")
                if not hidden:
                    size = f"0x{size}"
                    try:
                        name = demangle(name)
                    except ValueError:
                        pass
                    result.append((size, name))
        except Exception as e:
            print(e, row)

    for row in sorted(result):
        size, name = row
        print(size, name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="ObjDump_sorted")
    parser.add_argument("filename")

    args = parser.parse_args()

    start(args)
