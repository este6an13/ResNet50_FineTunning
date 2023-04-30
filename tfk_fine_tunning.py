# pip install tensorflow
# pip install pillow
# pip install matplotlib
# pip install numpy

from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
import matplotlib as plt
import numpy as np

# Set up the paths to the train, validation, and test directories
train_dir = 'D:/dequi/Documents/mmimdb_train'
valid_dir = 'D:/dequi/Documents/mmimdb_valid'
test_dir = 'D:/dequi/Documents/mmimdb_test'

# Set up the image dimensions and batch size
img_width, img_height = 224, 224
batch_size = 32

# Create the data generators for the train, validation, and test sets
train_datagen = ImageDataGenerator(rescale=1./255, horizontal_flip=True)
valid_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary',
    shuffle=True
)

valid_generator = valid_datagen.flow_from_directory(
    valid_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary',
    shuffle=True
)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary',
    shuffle=True
)

# Load the ResNet50 model with imagenet weights
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(img_width, img_height, 3))

# Add a global average pooling layer and a dense layer to the ResNet50 base
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
x = Dropout(0.2)(x)
predictions = Dense(1, activation='sigmoid')(x)

# Set up the model to train the new layers we added, while keeping the pretrained layers frozen
model = Model(inputs=base_model.input, outputs=predictions)
for layer in base_model.layers:
    layer.trainable = False

# Compile the model with a binary cross-entropy loss and Adam optimizer
model.compile(optimizer=Adam(learning_rate=1e-3), loss='binary_crossentropy', metrics=['accuracy'])

# Train the model on the train data and validate on the validation data
model.fit(
    train_generator,
    steps_per_epoch=train_generator.n // batch_size,
    epochs=3,
    validation_data=valid_generator,
    validation_steps=valid_generator.n // batch_size
)

# Evaluate the model on the test data
test_loss, test_acc = model.evaluate(test_generator, steps=test_generator.n // batch_size)
print('Freezed Test Loss:', test_loss)
print('Freezed Test Accuracy:', test_acc)


for layer in model.layers:
    layer.trainable = True

# Compile the model with a binary cross-entropy loss and Adam optimizer
model.compile(optimizer=Adam(learning_rate=1e-5), loss='binary_crossentropy', metrics=['accuracy'])

# Train the model on the train data and validate on the validation data
model.fit(
    train_generator,
    steps_per_epoch=train_generator.n // batch_size,
    epochs=10,
    validation_data=valid_generator,
    validation_steps=valid_generator.n // batch_size
)

# Evaluate the model on the test data
test_loss, test_acc = model.evaluate(test_generator, steps=test_generator.n // batch_size)
print('Unfreezed Test loss:', test_loss)
print('Unfreezed Test accuracy:', test_acc)