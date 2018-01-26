import numpy as np
import pandas as pd


# the function will return an array which contains 1, 0 or -1
def sentiment_extraction(csv_name):
    df = pd.read_csv(csv_name)
    sentiment_vector = []
    increase_vector = np.loadtxt("increase.txt", dtype=np.str)
    decrease_vector = np.loadtxt("decrease.txt", dtype=np.str)
    for interaction in df["interaction"]:
        increase_weight = 0  # the weight represents for "increase sentiment"
        decrease_weight = 0

        # each "increase sentiment" word contained in interaction string will increase the weight by 1
        for i_word in increase_vector:
            if str(interaction).find(i_word) > -1:
                increase_weight += 1
        for d_word in decrease_vector:
            if str(interaction).find(d_word) > -1:
                decrease_weight += 1

        # compare two weights and add the result into the sentiment vector
        if increase_weight > decrease_weight:
            sentiment_vector.append(1)
        elif decrease_weight > increase_weight:
            sentiment_vector.append(-1)
        else:
            sentiment_vector.append(0)
    print(sentiment_vector)

sentiment_extraction("drug_info_part1.csv")
