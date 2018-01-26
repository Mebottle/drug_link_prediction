import numpy as np
import pandas as pd
import tensorflow as tf


def weight_variable(shape):
    """weight_variable generates a weight variable of a given shape."""
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    """bias_variable generates a bias variable of a given shape."""
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


# Model Inputs
x = tf.placeholder(tf.float32, [None, 44])
y_ = tf.placeholder(tf.float32, [None, 5])

# Define the graph
# First fully connected layer
W_fc1 = weight_variable([44, 500])
b_fc1 = bias_variable([500])
# h_fc1 = tf.nn.sigmoid(tf.matmul(x, W_fc1) + b_fc1)
h_fc1 = tf.nn.relu(tf.matmul(x, W_fc1) + b_fc1)

# Second fully connected layer
W_fc2 = weight_variable([500, 5])
b_fc2 = bias_variable([5])
y_mlp = tf.matmul(h_fc1, W_fc2) + b_fc2

# Loss
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_mlp))

# Evaluation
correct_prediction = tf.equal(tf.argmax(y_mlp, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


# Optimizers: Try out a few different parameters for SGD and SGD momentum
train_step_SGD = tf.train.GradientDescentOptimizer(learning_rate=0.13).minimize(cross_entropy)
train_step_momentum = tf.train.MomentumOptimizer(learning_rate=0.05, momentum=.9).minimize(cross_entropy)
train_step_ADAM = tf.train.AdamOptimizer().minimize(cross_entropy)

# Op for initializing all variables
initialize_all = tf.global_variables_initializer()


def tag2vec(l):
    n_list = []
    for tag in l:
        list_i = [0, 0, 0, 0, 0]
        list_i[int(tag) - 1] = 1
        n_list.append(list_i)
    return n_list


def feature2vec(l):
    n_list = []
    for s in l:
        n_list.append([float(f) for f in s.split(" ")])
    return n_list


class Batch:
    def __init__(self, data):
        self.data = data
        self.times = 0
        self.length = len(data[0])

    # get a part of data every time call the func
    def next_batch(self, batch_size):
        ind_list = np.random.choice(self.length, batch_size)
        feature = []
        tag = []
        for ind in ind_list:
            feature.append(self.data[0][ind])
            tag.append(self.data[1][ind])
        return [feature, tag]


# train, test: pandas.DataFrame
def train_mlp(train, test, train_step_optimizer, iterations=3000):
    test = test.sample(frac=1)
    test_x = feature2vec(test['feature'].tolist())
    test_y_ = tag2vec(test['tag'].tolist())

    train = train.sample(frac=1)
    train_x = feature2vec(train['feature'].tolist())
    train_y_ = tag2vec(train['tag'].tolist())
    train_batch = Batch([train_x, train_y_])

    with tf.Session() as sess:
        # Initialize (or reset) all variables
        sess.run(initialize_all)

        # Initialize arrays to track losses and validation accuracies
        valid_accs = []
        losses = []

        for i in range(iterations):
            # Validate every 250th batch
            if i % 250 == 0:
                validation_accuracy = 0
                for v in range(10):
                    batch = train_batch.next_batch(50)
                    validation_accuracy += (1/10) * accuracy.eval(feed_dict={x: batch[0], y_: batch[1]})
                print('step %d, validation accuracy %g' % (i, validation_accuracy))
                valid_accs.append(validation_accuracy)

            # Train
            batch = train_batch.next_batch(50)
            loss, _ = sess.run([cross_entropy, train_step_optimizer], feed_dict={x: batch[0], y_: batch[1]})
            losses.append(loss)

        print('test accuracy %g' % accuracy.eval(feed_dict={x: test_x, y_: test_y_}))
    return valid_accs, losses

if __name__ == '__main__':
    for n in range(10):
        test_path = ("../data/train_test/test_%d.csv" % n)
        train_path = ("../data/train_test/train_%d.csv" % n)
        df_test = pd.read_csv()
