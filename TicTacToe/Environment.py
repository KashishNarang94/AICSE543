import random


class Environment:
    def __init__(self, player1, player2, episodes):
        # e stands for empty cell
        self.board = ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e']
        self.player = ['X', 'O']
        self.actions = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.player1 = player1
        self.player2 = player2
        self.winner = ' '
        self.episodes = episodes
        self.done = False

    def printBoard(self):
        print("Board is ")
        print(self.board[0], "||", self.board[1], "||", self.board[2])
        print(self.board[3], "||", self.board[4], "||", self.board[5])
        print(self.board[6], "||", self.board[7], "||", self.board[8])

    def printWinner(self):
        print("Winner of this game is", self.winner)

    def resetEnv(self):
        self.board = ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e']
        self.player = ['X', 'O']
        self.actions = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.winner = ' '
        return self.board

    def possible_actions(self):
        return self.actions

    def checkBoard(self, playersymbol):
        print("Checking board after action")
        # Row check for win
        for i in range(3):
            if playersymbol == self.board[i * 3] and self.board[i * 3] == self.board[i * 3 + 1] and self.board[
                i * 3 + 1] == self.board[i * 3 + 2]:
                return 1, True

        # Column check for win
        for i in range(3):
            if playersymbol == self.board[i] and self.board[i] == self.board[i + 3] and self.board[i + 3] == self.board[
                i + 6]:
                return 1, True

        # Digonal check for win
        if playersymbol == self.board[0] and self.board[0] == self.board[4] and self.board[4] == self.board[8]:
            return 1, True
        if playersymbol == self.board[2] and self.board[2] == self.board[4] and self.board[4] == self.board[6]:
            return 1, True

        # Draw check
        if len(self.actions) == 0:
            return 0.5, True

        return 0, False

    def step(self, player, action_pos):
        print("Taking action")
        if player == self.player1:
            playersymbol = self.player[0]
        elif player == self.player2:
            playersymbol = self.player[1]

        # If not already marked position
        if self.board[action_pos] == 'e':
            print("symbol morked", playersymbol, "at position", action_pos)
            self.board[
                action_pos] = playersymbol  # Mark player symbol at that location#Make it a list first as string is immmutable
            self.actions.remove(action_pos)  # delete this postion from posible actions for next player turn
            reward, done = self.checkBoard(playersymbol)

            if reward == 1:
                self.winner = playersymbol
        else:
            print("Not a valid step")
            return 0,False
        # return new state with reward and whether its completed or n
        return reward, done

    def trainAgent(self):
        wonRL = 0
        wonR = 0
        drawcount = 0
        for i in range(self.episodes):
            curr_board = self.resetEnv()
            done = False
            player = None
            turn_no = 0

            isP = random.choice([True, False])

            while not done:

                # Chose action
                if isP:  # Player 1 will play first
                    action = self.player1.chooseAction(curr_board, self.possible_actions())
                    player = self.player1
                else:
                    action = self.player2.chooseAction(self.possible_actions())
                    player = self.player2

                # Take step and add new state to q table
                reward, done = self.step(player, action)
                turn_no += 1
                print("Turn ", turn_no, "of this match", i)

                # add new state to the q table also
                self.player1.addNewBoardtoQtable(self.board)

                self.printBoard()

                if done:
                    # Game won or draw
                    if reward == 1:
                        self.player1.updateQtable(curr_board, self.board, action, reward)
                        self.printWinner()
                        if self.winner == self.player[0]:
                            wonRL += 1
                        else:
                            wonR += 1
                        print("--------------Match completed----------------")
                    elif reward == 0.5:  # draw
                        drawcount+=1
                        self.player1.updateQtable(curr_board, self.board, action, reward)
                        print("**************Match Draw*********************")
                    break

                elif reward == 0:  # continue game
                    self.player1.updateQtable(curr_board, self.board, action, reward)

                isP = not isP
                print("Next player turn")

        print("Match won by RL agent(X):", wonRL)
        print("Match won by Random agent(O):", wonR)
        print("Match draw:", drawcount)
        return wonRL

    def saveIntoFile(self,i):
        file="RLagentQtable"+str(i)
        self.player1.storeQvalue(file)


    def loadFromFile(self,i):
        file = "RLagentQtable" + str(i)
        self.player1.loadQvalue(file)


    def playGameAgainstHuman(self):
        print("Now Time to Showdown", self.player2.getName(), "you are ", self.player[1])
        done=False

        isP = random.choice([True, False])
        if isP: print("RL agent will start first as ",self.player[0])
        else:print("You are starting first")

        self.resetEnv()
        self.printBoard()

        while not done:
            print("Play begin")

            if isP:  # Computer will play first
                action = self.player1.chooseAction(self.board, self.possible_actions())
                player = self.player1
            else:
                action = self.player2.chooseAction(self.possible_actions())
                player = self.player2

            reward, done = self.step(player, action)

            self.printBoard()

            if reward==1:
                self.printWinner()
                print("--------------Match completed----------------")
                break
            elif reward==0.5:
                print("**************Match Draw*********************")
                break
            elif reward==0:
                print("Next player turn")
            isP = not isP

    def playGameAgainstRandomAgent(self):
        epidoes=100
        print("Now Time to Showdown")

        wonRL=0
        wonR=0
        drawcount=0
        for i in range(epidoes):
            done = False

            isP = random.choice([True, False])
            if isP:
                print("RL agent will start first as", self.player[0])
            else:
                print("Random Agent will start first", self.player[1])

            self.resetEnv()
            self.printBoard()

            while not done:

                if isP:  # Computer will play first
                    action = self.player1.chooseAction(self.board, self.possible_actions())
                    player = self.player1
                else:
                    action = self.player2.chooseAction(self.possible_actions())
                    player = self.player2

                reward, done = self.step(player, action)

                self.printBoard()

                if reward == 1:
                    self.printWinner()
                    if self.winner==self.player[0]:
                        wonRL+=1
                    else: wonR+=1
                    print("--------------Match completed----------------")
                    break
                elif reward == 0.5:
                    drawcount+=1
                    print("**************Match Draw*********************")
                    break
                elif reward == 0:
                    print("Next player turn")
                isP = not isP

        print("Match won by RL agent(X):",wonRL)
        print("Match won by Random agent(O):",wonR)
        print("Match draw:", drawcount)


