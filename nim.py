from typing import List


class NimGame:
    def __init__(self, n):
        # initialize the game - only the number 'n' is required -> stack initial size
        self.n = [n]

    def startState(self):
        return self.n

    def isEnd(self, state):
        # the game has reached the end state if there are no possible actions
        return True if len(self.possible_actions(state)) == 0 else False

    def utility(self, state, player):
        # The utility is +1 for the player having won and -1 for the losing player
        if self.isEnd(state):
            if player == 1:  # player max
                return -1
            else:  # player min
                return 1

    @staticmethod
    def possible_actions(state: List[int]) -> List[List[int]]:
        result = []

        for index, element in enumerate(state):
            new_state = state[:]
            del new_state[index]
            j = 1
            subtraction_result = element - j
            while (subtraction_result > 0) and (subtraction_result > j):
                result.append([subtraction_result, j, *new_state])
                j += 1
                subtraction_result = element - j
        return list(map(lambda l: sorted(l, reverse=True), result))

    # equal to the possible action taken
    def successor(self, state, action):
        if action in self.possible_actions(state):
            return action


# cache values globally to speed up the minimax recursion (dynamic programming memoization)
cached_results = {}


def minimaxSolver(game: NimGame, state: List[int], player: int) -> List[int]:

    def recurse(state: List[int], player: int):

        # recursion base cases
        if game.isEnd(state):
            # return the utility of the state, no more actions that can be taken
            return game.utility(state, player), state
        if (tuple(state), player) in cached_results:
            return cached_results[(tuple(state), player)]

        # all possible choices, the player is toggled each time it is called (since Nim is a 2-player game)
        choices = [(recurse(game.successor(state, action), -1 * player)[0], action) for action in
                   game.possible_actions(state)]

        if player == 1:
            tuple_value = max(choices)  # maximize over the expected utility
        else:
            tuple_value = min(choices)  # minimize over the expected utility
        cached_results[(tuple(state), player)] = tuple_value
        return tuple_value

    _, optimal_action = recurse(state, player)
    return optimal_action


if __name__ == "__main__":
    n = int(input("-> stack size : "))
    game = NimGame(n)
    state = game.startState()
    # player 1 <- player / player -1 <- computer
    taken_actions = []
    print('= You are max player =')

    while not game.isEnd(state):
        print(f"--- Current game state is: {state} ---")
        action = [n]
        valid_action = False
        while not valid_action:
            action = sorted(list(map(int, input('Make your choice : ').split('-'))), reverse=True)
            valid_action = (sum(action) == n) and (action in game.possible_actions(state))
            if not valid_action:
                print('INVALID action, please respect the game rules and try again!')

        state = action
        taken_actions.append(('Player', state))
        if game.isEnd(state):
            print("You Lost!")
            print("Taken actions :")
            print(' -> '.join(map(str, taken_actions)))
            break
        ai_action = minimaxSolver(game, state, 1)
        state = ai_action
        taken_actions.append(('Ai', state))
        print(f"Computer action is: {state}")
        if game.isEnd(state):
            print("You Won!")
            print("Taken actions :")
            print(' -> '.join(map(str, taken_actions)))
