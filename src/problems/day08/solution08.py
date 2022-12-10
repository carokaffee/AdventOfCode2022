from src.tools.loader import load_data

TESTING = True


def get_slices(row, col):
    return [
        [(x, col) for x in reversed(range(row))],
        [(x, col) for x in range(row+1, num_rows)],
        [(row, y) for y in reversed(range(col))],
        [(row, y) for y in range(col+1, num_cols)]
    ]


def tree_visible(row, col):
    slices = get_slices(row, col)

    visible = False
    for slice in slices:
        highest_tree = max((trees[x][y] for x,y in slice), default=-1)
        slice_visible = highest_tree  < trees[row][col]
        visible = visible or slice_visible

    return visible


def count_visible_trees():
    counter = 0
    for x in range(num_rows):
        for y in range(num_cols):
            if tree_visible(x,y):
                counter += 1
            
    return counter


def get_scenic_score(row,col):
    slices = get_slices(row, col)
    tree_score = 1

    for slice in slices:
        current_height = 0
        distance = 0
        for x, y in slice:
            if current_height < trees[row][col]:
                current_height = trees[x][y]
                distance += 1
        tree_score *= distance
    
    return tree_score


def get_largest_scenic_score():
    max_scenic_score = 0

    for x in range(num_rows):
        for y in range(num_cols):
            max_scenic_score = max(max_scenic_score, get_scenic_score(x,y))

    return max_scenic_score



if __name__ == '__main__':
    data = load_data(TESTING, '\n')

    trees = []
    for line in data:
        trees.append(list(map(int, line)))

    num_rows = len(trees)
    num_cols = len(trees[0])

    # solution 1
    print(count_visible_trees())

    # solution 2
    print(get_largest_scenic_score())