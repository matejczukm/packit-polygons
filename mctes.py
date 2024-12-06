from our_packit.mcts_games import HexagonalPackit, TriangularPackit
from mcts_simple import UCT, MCTS
import concurrent.futures

def main():
    games = [TriangularPackit(4), TriangularPackit(5), TriangularPackit(6), HexagonalPackit(3), HexagonalPackit(4)][0:4:3]
    trees = [UCT(game, False, True) for game in games]
    names = ['tri4', 'tri5', 'tri6', 'hex3', 'hex4'][0:4:3]

    def train_tree(tree, n, name, c):
        name += str(c)
        name += 'v2' 
        name += '.mcts'
        tree.self_play(n)
        tree.save(name)
    n = 3000
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     futures = [executor.submit(train_tree, tree, n, name) for tree,name in zip(trees, names)]
    #     results = [future.result() for future in concurrent.futures.as_completed(futures)]
    # c_vals = [0.5, 1, 1.5, 2]
    c_vals = [2, 2.5, 3, 10]
    for game, tree, name in zip(games, trees, names):
        for c in c_vals:
            tree.c = c
            train_tree(tree, n, name, c)
    
    game = TriangularPackit(4)
    tree = UCT(game, False, True, 2)
    tree.self_play(10000)
    tree.save('megamocnyTri4.mcts')

    game = HexagonalPackit(3)
    tree = UCT(game, False, True, 2)
    tree.self_play(10000)
    tree.save('megamocnyHex3.mcts')



if __name__ == '__main__':
    main()

# results = pd.concat(results, ignore_index=True)
# # print('Steps')
# # print(results)
# results.to_csv('results_steps.csv')