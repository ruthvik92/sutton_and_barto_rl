"""
This code shows a greedy actor in gridworld.
At each iteration, it solves for the state-value function of the current greedy policy
"""
from copy import deepcopy
from time import sleep

import gym
import numpy as np
from gym.envs.classic_control import GridWorld

from grid_world_model import evaluate_policy, S, A, Env, R


def pi_to_string(pi):
    for r in range(pi.shape[0]):
        rs = ""
        for c in range(pi.shape[1]):
            if pi[r][c][0]:
                rs += 'N '
            elif pi[r][c][1]:
                rs += 'S '
            elif pi[r][c][2]:
                rs += 'E '
            elif pi[r][c][3]:
                rs += 'W '
        print(rs)


if __name__ == "__main__":
    env = gym.make("GridWorld-v0")

    obs = env.reset()
    env.render()
    j = 0
    sleep(0.1)
    pi = np.ones((5, 5, 4)) * 0.25

    def Pi(state, action):
        if action == 'N':
            return pi[state][0]
        elif action == 'S':
            return pi[state][1]
        elif action == 'E':
            return pi[state][2]
        elif action == 'W':
            return pi[state][3]


    done = False
    while not done:
        # Policy Evaluation
        V = evaluate_policy(gamma=0.9, pi=Pi)

        def best_move(s):
            best_V = -1e12
            best_a = env.action_space.sample()
            for a in A(s):
                s1 = Env(s, a)
                r = R(s, a, s1)
                if r + V[s1] > best_V:
                    best_V = r + V[s1]
                    best_a = a

            move = GridWorld.string_to_action(best_a)
            return move


        # Policy Improvement
        old_pi = deepcopy(pi)
        for s_ in S():
            m = best_move(s_)
            pi[s_] = np.array([0, 0, 0, 0])
            pi[s_][m] = 1

        if np.all(old_pi == pi):
            print("solved at iter {}".format(j))
            print("Final V:")
            print(V)
            print("Final Pi:")
            print(pi_to_string(pi))
            done = True

        obs, reward, _, info = env.step(best_move(obs))
        env.render()
        sleep(0.1)
        j += 1
