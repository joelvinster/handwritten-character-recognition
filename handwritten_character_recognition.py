# -*- coding: utf-8 -*-
"""Handwritten Character Recognition.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Jp4_H4oDHZBK-ESBjYu_iMqhug8XzVZx
"""

import tensorflow as tf
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt

# Ensure TensorFlow is using GPU (if available)
print("TensorFlow version:", tf.__version__)
print("Num GPUs Available:", len(tf.config.experimental.list_physical_devices('GPU')))

# Load dataset (example: MNIST, replace with your dataset)
(train_ds, test_ds), ds_info = tfds.load(
    "mnist",
    split=["train", "test"],
    as_supervised=True,  # Returns (image, label)
    with_info=True
)

# Print dataset information
print(ds_info)

def preprocess(image, label):
    image = tf.image.convert_image_dtype(image, tf.float32)  # Normalize [0,1]
    image = tf.image.resize(image, (28, 28))  # Resize
    image = tf.expand_dims(image, axis=-1)  # Ensure (28, 28, 1)
    return image, label

BATCH_SIZE = 64

# Apply preprocessing
train_ds = train_ds.map(preprocess).shuffle(10000).batch(BATCH_SIZE)
test_ds = test_ds.map(preprocess).batch(BATCH_SIZE)

# Check a sample batch
for image_batch, label_batch in train_ds.take(1):
    print("Image batch shape:", image_batch.shape)  # Should be (64, 28, 28, 1)
    print("Label batch shape:", label_batch.shape)

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')  # Adjust output for your dataset
])

# Compile model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Model Summary
model.summary()

EPOCHS = 5 # Adjust as needed

history = model.fit(train_ds, validation_data=test_ds, epochs=EPOCHS)

test_loss, test_acc = model.evaluate(test_ds)
print(f"Test Accuracy: {test_acc * 100:.2f}%")

import numpy as np

def show_sample_predictions(dataset, model):
    plt.figure(figsize=(10,5))
    for images, labels in dataset.take(1):  # Take one batch
        predictions = model.predict(images)

        for i in range(5):  # Show 5 samples
            plt.subplot(1, 5, i+1)
            plt.imshow(images[i].numpy().squeeze(), cmap='gray')
            plt.axis('off')
            plt.title(f"Pred: {np.argmax(predictions[i])}")

    plt.show()

show_sample_predictions(test_ds, model)

