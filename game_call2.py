import os
import numpy as np
from game import PongZone

class QLearningAgent:
    def __init__(self, num_actions, alpha, gamma):
        self.Q_table = {}
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma

    def get_action_prob(self, state):
        if state not in self.Q_table:
            self.Q_table[state] = np.zeros(self.num_actions)
        action_values = self.Q_table[state]
        exp_action_values = np.exp(action_values - np.max(action_values))
        action_probabilities = exp_action_values / np.sum(exp_action_values)
        action_probabilities = np.nan_to_num(action_probabilities, nan=1/self.num_actions)
        return action_probabilities


    def update_Q_table(self, state, action, reward, next_state):
        if state not in self.Q_table:
            self.Q_table[state] = np.zeros(self.num_actions)
        if next_state not in self.Q_table:
            self.Q_table[next_state] = np.zeros(self.num_actions)
        current_value = self.Q_table[state][action]
        max_next_value = np.max(self.Q_table[next_state])
        updated_value = current_value + self.alpha * (reward + self.gamma * max_next_value - current_value)
        self.Q_table[state][action] = updated_value
        
    def load_Q_table(self, file_path):
        if os.path.exists(file_path):
            self.Q_table = np.load(file_path, allow_pickle=True).item()
        else:
            print(f"No file found at {file_path}")


class PongQLearning:
    def __init__(self, runs, alpha_a, gamma_a, alpha_b, gamma_b):
        self.runs = runs
        self.alpha_a = alpha_a
        self.gamma_a = gamma_a
        self.alpha_b = alpha_b
        self.gamma_b = gamma_b
        self.pong_game = PongZone()
        self.agent_a = QLearningAgent(3, alpha_a, gamma_a)
        self.agent_b = QLearningAgent(3, alpha_b, gamma_b)

    def load_models(self, round_num):
        self.agent_a.load_Q_table(f'modelAb/QA_table_{round_num}.npy')
        self.agent_b.load_Q_table(f'modelBb/QB_table_{round_num}.npy')
                
    def save_models(self, round_num):
        np.save(f'modelAb/QA_table_{round_num}', self.agent_a.Q_table)
        np.save(f'modelBb/QB_table_{round_num}', self.agent_b.Q_table)

    def train_agents(self):
        #self.load_models() #load trained module here
        for round in range(1, 300):
            print(f'### Round: {round} ###')
            total_score_a = 0
            total_score_b = 0
            for episode in range(self.runs):
                state = self.pong_game.reset()
                done = False
                while not done:
                    action_a = np.random.choice(range(3), p=self.agent_a.get_action_prob(state))
                    action_b = np.random.choice(range(3), p=self.agent_b.get_action_prob(state))
                    next_state, reward_a, reward_b, done = self.pong_game.render(action_a, action_b)
                    self.agent_a.update_Q_table(state, action_a, reward_a, next_state)
                    self.agent_b.update_Q_table(state, action_b, reward_b, next_state)
                    total_score_a += reward_a
                    total_score_b += reward_b
                    state = next_state
            mean_score_a = total_score_a / self.runs
            mean_score_b = total_score_b / self.runs
            print('##### Mean Reward for bot A: ', mean_score_a)
            print('##### Mean Reward for bot B: ', mean_score_b)
            self.save_models(round * self.runs)#save trained module here

if __name__ == '__main__':
    try:
        os.mkdir('modelAb')
        os.mkdir('modelBb')
    except:
        pass
    pong_q_learning = PongQLearning(1000, 0.9, 0.9, 0.5, 0.5)
    pong_q_learning.train_agents()
