import numpy as np
import scipy.special
import random
from dev import MUTATION_RATE, MUTATION_MIXING_RATE, MUTATION_RATE_OFFSPRING


class Nnet:
    def __init__(self, num_input, num_hidden1, num_hidden2, num_output):
        self.num_input = num_input
        self.num_hidden1 = num_hidden1
        self.num_hidden2 = num_hidden2
        self.num_output = num_output
        self.weight_input_hidden1 = np.random.sample(
            size=(self.num_hidden1, self.num_input)
        )
        self.weight_hidden1_hidden2 = np.random.uniform(
            size=(self.num_hidden2, self.num_hidden1)
        )
        self.weight_hidden2_output = np.random.uniform(
            size=(self.num_output, self.num_hidden2)
        )

        self.activation_function = lambda x: (np.exp(x)-np.exp(-x))/(np.exp(x)+np.exp(-x))

    def get_outputs(self, inputs_list):
        inputs = np.array(inputs_list, ndmin=2).T
        # print("inputs", inputs, sep="\n")
        hidden1_inputs = np.dot(self.weight_input_hidden1, inputs)
        # print("hidden1_inputs", hidden1_inputs, sep="\n")
        hidden1_outputs = self.activation_function(hidden1_inputs)
        # print("hidden1_outputs", hidden1_outputs, sep="\n")
        hidden2_inputs = np.dot(self.weight_hidden1_hidden2, hidden1_outputs)
        # print("hidden1_inputs", hidden1_inputs, sep="\n")
        hidden2_outputs = self.activation_function(hidden2_inputs)
        # print("hidden1_outputs", hidden1_outputs, sep="\n")
        final_inputs = np.dot(self.weight_hidden2_output, hidden2_outputs)
        # print("hidden1_inputs", hidden1_inputs, sep="\n")
        final_outputs = self.activation_function(final_inputs)
        # print("hidden1_outputs", hidden1_outputs, sep="\n")
        return final_outputs

    def modify_weights(self):
        Nnet.modify_array(self.weight_input_hidden1)
        Nnet.modify_array(self.weight_hidden1_hidden2)
        Nnet.modify_array(self.weight_hidden2_output)

    def modify_weights_offspring(self):
        Nnet.modify_array_offspring(self.weight_input_hidden1)
        Nnet.modify_array_offspring(self.weight_hidden1_hidden2)
        Nnet.modify_array_offspring(self.weight_hidden2_output)

    def create_mixed_weights(self, net1: "Nnet", net2: "Nnet"):
        self.weight_input_hidden1 = get_mix_from_arrays(
            net1.weight_input_hidden1, net2.weight_input_hidden1
        )
        self.weight_hidden1_hidden2 = get_mix_from_arrays(
            net1.weight_hidden1_hidden2, net2.weight_hidden1_hidden2
        )
        self.weight_hidden2_output = get_mix_from_arrays(
            net1.weight_hidden2_output, net2.weight_hidden2_output
        )

    def modify_array(a):
        for x in np.nditer(a, op_flags=["readwrite"]):
            if random.random() < MUTATION_RATE:
                x[...] = (np.random.random_sample() - 0.5) * 2

    def modify_array_offspring(a):
        for x in np.nditer(a, op_flags=["readwrite"]):
            if random.random() < MUTATION_RATE_OFFSPRING:
                x[...] = (np.random.random_sample() - 0.5) * 2

    def loaddata(self, a, b, c):
        self.weight_input_hidden1 = a
        self.weight_hidden1_hidden2 = b
        self.weight_hidden2_output = c


def get_mix_from_arrays(ar1, ar2):
    total_entries = ar1.size
    num_rows = ar1.shape[0]
    num_cols = ar1.shape[1]

    num_to_take = total_entries - int(total_entries * MUTATION_MIXING_RATE)
    idx = np.random.choice(np.arange(total_entries), num_to_take, replace=False)
    res = np.random.uniform(-1, 1, size=(num_rows, num_cols))
    for row in range(0, num_rows):
        for col in range(0, num_cols):
            index = row * num_cols + col
            if index in idx:
                res[row][col] = ar1[row][col]
            else:
                res[row][col] = ar2[row][col]
    return res


if __name__ == "__main__":
    pass
