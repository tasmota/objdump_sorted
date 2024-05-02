import argparse
import subprocess

try:
    import cpp_demangle
except ModuleNotFoundError:
    print(
        "cpp_demangle missing, install with\n\t> pip3 install cpp_demangle\n\tor\n\t> pip3 install -r requirements.txt")


def start(args):
    dump = subprocess.run(["objdump", "-t", args.filename], capture_output=True)
    dump = filter(lambda _: _, dump.stdout.decode().split("\n")[4:])
    unpacked = [row.split("\t") for row in dump]

    result = []

    for row in unpacked:
        try:
            flags, size_name = row
            if flags.endswith(".flash.text"):
                size, *hidden, name = size_name.split(" ")
                if not hidden:
                    size = f"0x{size}"
                    try:
                        name = cpp_demangle.demangle(name)
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
