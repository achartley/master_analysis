# Imports
import os
import sys
sys.path.append("../../../master_scripts")
from master_scripts.classes import Experiment
from master_scripts.data_functions import (get_tf_device,
                                           get_git_root)
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten
import json
import tensorflow as tf
import numpy as np
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

# ================== Config =======================
with open(sys.argv[1], 'r') as fp:
    config = json.load(fp)

# ================== Callbacks ====================


# ================== Import Data ==================
DATA_PATH = get_git_root() + "data/simulated/"
images = np.load(DATA_PATH + config['data']['images'])
images = images.reshape(images.shape[0], 16, 16, 1)
labels = np.load(DATA_PATH + config['data']['labels'])

# log-scale the images if desireable
config['scaling'] = "minmax"
if "np.log" in config['scaling']:
    images = np.log1p(images)

# set tf random seed
tf.random.set_seed(config['random_seed'])
with tf.device(get_tf_device(20)):
    # Small CNN
    model = Sequential()
    model.add(
        Conv2D(8, kernel_size=3, activation='relu', input_shape=images.shape[1:], padding='same')
    )
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    # Run experiment
    experiment = Experiment(
        model=model,
        config=config,
        model_type="classification",
        experiment_name="full_training_cnn_small"
    )
    experiment.run(
        images,
        labels,
    )
    experiment.save(save_model=True, save_indices=False)
    print("Finished experiment:", experiment.id)
    lpath = experiment.config['path_args']['models'] + "models.log"
    log = open(lpath,"a")
    log.write(experiment.id + ":\n")
    log.write(os.path.basename(__file__)+"\n")
    log.write(repr(config) + "\n")
    log.close()

