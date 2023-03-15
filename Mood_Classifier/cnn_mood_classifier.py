import h5py
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt

from Camera import get_camera_photo

def load_happy_dataset():
    train_dataset = h5py.File('datasets/train_happy.h5', "r")
    train_set_x_orig = np.array(train_dataset["train_set_x"][:])  # your train set features
    train_set_y_orig = np.array(train_dataset["train_set_y"][:])  # your train set labels

    test_dataset = h5py.File('datasets/test_happy.h5', "r")
    test_set_x_orig = np.array(test_dataset["test_set_x"][:])  # your test set features
    test_set_y_orig = np.array(test_dataset["test_set_y"][:])  # your test set labels

    classes = np.array(test_dataset["list_classes"][:])  # the list of classes

    train_set_y_orig = train_set_y_orig.reshape((1, train_set_y_orig.shape[0]))
    test_set_y_orig = test_set_y_orig.reshape((1, test_set_y_orig.shape[0]))

    return train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig, classes


X_train_orig, Y_train_orig, X_test_orig, Y_test_orig, classes = load_happy_dataset()

# Normalize image vectors
X_train = X_train_orig / 255.
X_test = X_test_orig / 255.

# Reshape
Y_train = Y_train_orig.T
Y_test = Y_test_orig.T

print(X_test.shape)
print(X_train.shape)
print(np.array([X_train[0]]).shape)


def happyModel():
    """
    Implements the forward propagation for the binary classification model:
    ZEROPAD2D -> CONV2D -> BATCHNORM -> RELU -> MAXPOOL -> FLATTEN -> DENSE

    Note that for simplicity and grading purposes, you'll hard-code all the values
    such as the stride and kernel (filter) sizes.
    Normally, functions should take these values as function parameters.

    Arguments:
    None

    Returns:
    model -- TF Keras model (object containing the information for the entire training process)
    """
    model = tf.keras.Sequential([
        tf.keras.layers.ZeroPadding2D(padding=3, input_shape=(64, 64, 3)),
        tf.keras.layers.Conv2D(filters=32, kernel_size=7),
        tf.keras.layers.BatchNormalization(axis=3),
        tf.keras.layers.ReLU(),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(1, activation="sigmoid")
    ])

    return model


# happy_model = happyModel()
#
# happy_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
#
# happy_model.summary()
#
# happy_model.fit(X_train, Y_train, epochs=10, batch_size=16)
#
# happy_model.save("model_output/happy_model")

# It can be used to reconstruct the model identically.
happy_model = tf.keras.models.load_model("model_output/happy_model")

# happy_model.evaluate(X_test, Y_test)

# Image from the given dataset
# index = 130
# plt.imshow(X_train_orig[index])
# plt.show()
# input_image = np.array([X_train[index]])
# print(happy_model.predict(input_image))
#
camera_outputs = get_camera_photo('camera_output/')
print(camera_outputs)
#
from tensorflow.keras.preprocessing import image

for output in camera_outputs:
    img_path = "camera_output/" + output
    img = image.load_img(img_path, target_size=(64, 64))
    img = image.img_to_array(img)
    print(img.shape)
    img = img / 255.
    print(happy_model.predict(np.array([img])))
