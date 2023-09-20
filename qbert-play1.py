import argparse
import sys
import pdb
import gymnasium as gym
from gymnasium import wrappers, logger


class Agent(object):
    """The world's simplesst agent!"""

    def __init__(self, action_space):
        self.action_space = action_space

    # You should modify this function
    def act(self, observation, reward, done):
        return self.action_space.sample()

# YOU MAY NOT MODIFY ANYTHING BELOW THIS LINE OR USE
# ANOTHER MAIN PROGRAM


def isqberthere(coordinate, frame):

    qbert_color = [181, 83, 40]
    coordinate[0] -= 7  # 4 is the height
    list_of_coordinates = [[coordinate], [coordinate[0], coordinate[1] + 1], [coordinate[0], coordinate[1] - 1]]
    for x, y in list_of_coordinates:
        if (frame[x][y] == qbert_color).all():
            print(f"found qbert at {coordinate[0], coordinate[1]}")
            return True
    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('--env_id', nargs='?', default='Qbert', help='Select the environment to run')
    args = parser.parse_args()

    # You can set the level to logger.DEBUG or logger.WARN if you
    # want to change the amount of output.
    logger.set_level(logger.INFO)

    env = gym.make(args.env_id, render_mode='human')

    # You provide the directory to write to (can be an existing
    # directory, including one with existing data -- all monitor files
    # will be namespaced). You can also dump to a tempdir if you'd
    # like: tempfile.mkdtemp().
    outdir = 'random-agent-results'

    env.unwrapped.seed(0)
    agent = Agent(env.action_space)

    episode_count = 100
    reward = 0
    terminated = False
    score = 0
    special_data = {}
    special_data['ale.lives'] = 3
    observation = env.reset()[0]

    while not terminated:
        env.render()
        action = agent.act(observation, reward, terminated)
        # pdb.set_trace()
        observation, reward, terminated, truncated, info = env.step(action)
        isqberthere([34, 77], observation)
        score += reward
        frame = env.render()

    # Close the env and write monitor result info to disk
    print("Your score: %d" % score)
    env.close()
