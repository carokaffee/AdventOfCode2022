from src.tools.loader import load_data

TESTING = False


def execute_command(command):
    if command == "$ cd /":
        go_to_root()
    elif command == "$ cd ..":
        go_back()
    elif command.startswith("$ cd "):
        enter_dir(command[5:])
    elif command.startswith("dir "):
        create_dir(command[4:])
    elif command == "$ ls":
        pass
    else:
        add_file(*command.split())


def go_to_root():
    global current_dir
    current_dir = [""]


def go_back():
    current_dir.pop()


def enter_dir(dir):
    current_dir.append(dir)


def create_dir(name):
    pwd = "/".join(current_dir)
    new_dir = pwd + "/" + name
    existing_dirs.append(new_dir)
    files_in_dir[new_dir] = []
    files_in_dir[pwd].append((f"dir::{name}", 0))


def add_file(size, name):
    pwd = "/".join(current_dir)
    files_in_dir[pwd].append((f"file::{name}", int(size)))


def sort_by_depth(dirs):
    return list(reversed(sorted(dirs, key=lambda a: a.count("/"))))


def calculate_dir_size(dirs):
    sizes = {}
    for dir in dirs:
        sizes[dir] = 0
        for name, size in files_in_dir[dir]:
            sizes[dir] += size
            if name[:5] == "dir::":
                sizes[dir] += sizes[dir + "/" + name[5:]]
    return sizes


def sum_of_small_dirs(dirs):
    size = 0
    for val in dirs.values():
        if val <= 100000:
            size += val
    return size


def size_to_free_up_space(dirs):
    large_dirs = []

    for val in dirs.values():
        if val >= 30000000 - (70000000 - dirs[""]):
            large_dirs.append(val)
    return sorted(large_dirs)[0]


if __name__ == "__main__":
    data = load_data(TESTING, "\n")

    current_dir = [""]
    existing_dirs = [""]
    files_in_dir = {"": []}

    for command in data:
        execute_command(command)

    dirs_sorted_by_depth = sort_by_depth(existing_dirs)
    dir_size = calculate_dir_size(dirs_sorted_by_depth)

    # PART 1
    # test:     95437
    # answer: 1770595
    print(sum_of_small_dirs(dir_size))

    # PART 2
    # test:   24933642
    # answer:  2195372
    print(size_to_free_up_space(dir_size))
