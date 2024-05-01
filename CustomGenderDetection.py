import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB7
from tensorflow.keras.applications.efficientnet_v2 import EfficientNetV2M
from tensorflow.keras.applications.convnext import ConvNeXtBase
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.optimizers.experimental import Adamax, Adadelta, Adagrad, Ftrl, Nadam, RMSprop, SGD
import cv2
import warnings
warnings.filterwarnings('ignore')

# Function to detect faces in the right side of an image using OpenCV's pre-trained Haar Cascade classifier
def detect_right_driver_face(image_path):
    # Load the image
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    # Define ROI for the right side of the image
    roi_x = int(width / 2)  # Start X from half of the image width
    roi_y = 0  # Start Y from the top
    roi_width = int(width / 2)  # Set the width to be half of the image width
    roi_height = height  # Full height of the image

    # Crop the right side ROI from the image
    roi = image[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]

    # Convert ROI to grayscale
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Load the pre-trained face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Detect faces in the ROI
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Extract faces and their coordinates
    face_images = []
    face_coordinates = []

    for (x, y, w, h) in faces:
        # Convert face coordinates to global image coordinates
        global_x = x + roi_x
        global_y = y + roi_y
        face_coordinates.append((global_x, global_y, w, h))
        face_images.append(image[global_y:global_y+h, global_x:global_x+w])

    return face_images, face_coordinates

# Define parameters
image_size = (224, 224)
batch_size = 32
num_classes = 2  # Assuming 2 classes: Male and Female

# Data Augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

# Load and Split Data
train_generator = train_datagen.flow_from_directory(
    './gender_split/image_data/',
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    './gender_split/image_data/',
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation'
)

# Load EfficientNetB0 base model
# base_model = EfficientNetB7(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
# base_model = ConvNeXtBase(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model = EfficientNetV2M(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False

# Add custom classification head
x = GlobalAveragePooling2D()(base_model.output)
x = Dense(256, activation='relu')(x)
predictions = Dense(num_classes, activation='softmax')(x)

# Combine base model with custom head
model = Model(inputs=base_model.input, outputs=predictions)

# Freeze base layers
for layer in base_model.layers:
    layer.trainable = False

# Compile the model
model.compile(optimizer=Adadelta(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy',])

# Train the model
history = model.fit(
    train_generator,
    epochs=25,
    validation_data=validation_generator
)

# Save the trained model
model.save('./gender_split/efficientnet_v2m.h5')
