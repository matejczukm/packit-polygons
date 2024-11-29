import numpy as np


def validate_polygon(polygon_vector):
    # takes np.array

    vector_length = len(polygon_vector)
    if vector_length == 1:
        return True

    tmp_polygon_vector = np.array(polygon_vector)
    tmp_polygon_vector = np.append(tmp_polygon_vector, -1)

    i = 1
    last_element = polygon_vector[0]
    current_element = tmp_polygon_vector[i]

    while i < vector_length and last_element == current_element - 1:
        last_element = current_element
        i += 1
        current_element = tmp_polygon_vector[i]

    while i < vector_length and last_element == current_element:
        last_element = current_element
        i += 1
        current_element = tmp_polygon_vector[i]

    while i < vector_length and last_element == current_element + 1:
        last_element = current_element
        i += 1
        current_element = tmp_polygon_vector[i]

    return True if current_element == -1 else False


def cut_zeroes_from_polygon_vector(polygon_vector):
    # takes validated vector
    # probably not needed
    dezeroed_vector = []
    for i in polygon_vector:
        if i != 0:
            dezeroed_vector.append(i)
    return dezeroed_vector


def convert_polygon_vector_to_matrices(polygon_vector):
    # HAS TO BE REDONE - offset increases when last value bigger, for left it always increases
    # rretruns list of arrays

    height = len(polygon_vector)
    width = np.max(polygon_vector)

    right_leaning_matrix = np.zeros([height, width])
    # matrix for symmetrical and left-leaning polygon (always exists for validated vector)
    max_val_counter = 0
    offset = 0
    for row in range(height):

        if polygon_vector[row] == width:
            max_val_counter += 1  # only max value can duplicate

        if row != 0 and polygon_vector[row] < polygon_vector[row - 1]:
            offset += 1

        for column in range(offset, offset + polygon_vector[row]):
            right_leaning_matrix[row][column] = 1

    if max_val_counter > 1:
        first_max_row = np.argmax(polygon_vector)
        left_leaning_matrix = np.hstack((np.array(right_leaning_matrix), np.zeros([height, max_val_counter - 1])))
        left_offset = 0
        for row in range(first_max_row + 1, height):
            if polygon_vector[row] == width:
                left_offset += 1
            left_leaning_matrix[row] = np.roll(left_leaning_matrix[row], left_offset)

        return [right_leaning_matrix, left_leaning_matrix]

    return [right_leaning_matrix]


def get_polygon_vectors(polygon_size, board_size):
    def helper(remaining, current):
        if len(current) > board_size:
            return
        if remaining == 0 and validate_polygon(current) and check_if_vector_fits_on_board(current, board_size):
            polygon_vectors.append(np.array(current))
            return
        for i in range(1, remaining + 1):
            helper(remaining - i, current + [i])

    polygon_vectors = []
    helper(polygon_size, [])

    return polygon_vectors


def check_if_vector_fits_on_board(vector, board_size):
    # takes validated vector

    max_row_length = np.max(vector)
    max_row_count = np.count_nonzero(vector == max_row_length)
    # check if polygon fits horizontally
    if max_row_length + max_row_count - 1 > board_size:
        return False
    # check if polygon fits vertically
    min_row_length = np.min(vector)
    row_length_diff = max_row_length - min_row_length

    return max_row_count + row_length_diff - (board_size - max_row_length) <= (board_size + 1) / 2


def expand_to_hex_board(polygon, board_size, left, top):
    # takes np.array matrix repr of polygon, np.array matrix repr of board, and 2 ints
    polygon_height = len(polygon)
    polygon_width = len(polygon[0])

    assert polygon_height + top <= board_size, 'Invalid vertical offset'
    assert polygon_width + left <= board_size, 'Invalid horizontal offset'

    left_offset = np.zeros([polygon_height, left])
    right_offset = np.zeros([polygon_height, board_size - left - polygon_width])
    top_offset = np.zeros([top, board_size])
    bottom_offset = np.zeros([board_size - top - polygon_height, board_size])

    expanded_polygon = np.hstack((left_offset, polygon, right_offset))
    expanded_polygon = np.vstack((top_offset, expanded_polygon, bottom_offset))

    return expanded_polygon


def generate_board(board_side):
    board_size = board_side * 2 - 1
    board = np.zeros([board_size, board_size])
    for row in range(board_side):
        for column in range(board_side + row, board_size):
            board[row, column] = 1
    for row in range(board_side):
        for column in range(row):
            board[row + board_side - 1, column] = 1
    return board


def get_possible_placements(polygon_matrix, board):
    board_size = len(board)
    horizontal_offset = board_size - len(polygon_matrix[0]) + 1
    vertical_offset = board_size - len(polygon_matrix) + 1
    possible_placements = [None] * (horizontal_offset * vertical_offset)
    count = 0
    for top in range(vertical_offset):
        for left in range(horizontal_offset):

            expanded_polygon = expand_to_hex_board(polygon_matrix, board_size, left, top)
            if not np.any(board + expanded_polygon == 2):
                possible_placements[count] = expanded_polygon
                count += 1
    return possible_placements[:count]


def get_possible_placements_for_k(board, k):
    board_size = len(board)
    valid_vectors = get_polygon_vectors(k, board_size)
    polygon_matrices = []
    for vector in valid_vectors:
        polygon_matrices.extend(convert_polygon_vector_to_matrices(vector))
    possible_placements = []
    for polygon_matrix in polygon_matrices:
        possible_placements.extend(get_possible_placements(polygon_matrix, board))
    return possible_placements


def get_possible_placements_for_turn(board, turn):
    res = get_possible_placements_for_k(board, turn)
    res.extend(
        get_possible_placements_for_k(board, turn + 1)
    )
    return res


def place_polygon(board, polygon):
    return board + polygon


def print_board(board):
    for row in board:
        print(row)


def numpy_board_to_list(board_np):
    board = []
    board_np = board_np.astype(int)
    n = board_np.shape[0]
    offset = int(
        np.floor(n / 2)
    )
    for i in range(offset + 1):
        board.append(board_np[i].tolist()[:n - offset + i])
    for i in range(offset):
        board.append(board_np[offset + 1 + i].tolist()[1 + i:])
    return board


def list_board_to_numpy(board, value=0):
    n = len(board)
    offset = int(
        np.floor(n / 2)
    )
    for i in range(offset):
        board[i].extend([value] * (offset - i))
    for i in range(offset):
        board[offset + 1 + i] = [value] * (i + 1) + board[offset + 1 + i]

    return np.array(board)


def play(board_size):
    board = generate_board(board_size)
    turn = 1
    moves = get_possible_placements_for_turn(board, turn)
    while moves:
        moves_dict = {i: move for i, move in enumerate(moves)}
        for i, move in moves_dict.items():
            print(f'Move {i}:')
            print_board(numpy_board_to_list(move))
        print('Board: ')
        print_board(numpy_board_to_list(board))
        chosen_move = int(input('Choose move number: '))
        board = place_polygon(board, moves_dict[chosen_move])
        turn += 1
        moves = get_possible_placements_for_turn(board, turn)
        # print('Board: ')
        # print(board)
    print(f'Player {1 + turn % 2} wins after {turn - 1} turns')
    print('Board: ')
    print_board(numpy_board_to_list(board))
    return


if __name__ == '__main__':
    # print(
    #     place_polygon(
    #         generate_board(5),
    #         get_possible_placements_for_k(
    #             generate_board(5), 2
    #         )[0]
    #     )
    # )
    # print(
    #     get_possible_placements_for_turn(generate_board(5), 1)
    # )
    # play(5)
    board = [
        [1, 1, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [0, 0, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0]
    ]

    board_np = list_board_to_numpy(board, 1)
    # board_np = generate_board(4)
    x = get_possible_placements_for_turn(board_np, 7)
    for i in x:
        print_board(numpy_board_to_list(i))

    # print(numpy_board_to_list(generate_board(4)))
    # print(generate_board(5))
