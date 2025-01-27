from djangoProject import run_app
from polygonal_packit.alpha_zero_general.PackitAIPlayer import AIPlayer


def main():
    run_app({'triangular4': AIPlayer(4, 'triangular'),
             'hexagonal5': AIPlayer(5, 'hexagonal', local=True)}, False)


if __name__ == '__main__':
    main()
