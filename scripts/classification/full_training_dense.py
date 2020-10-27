# Imports
from master_scripts.classes import Experiment
from master_scripts.data_functions import (get_tf_device,
                                           get_git_root)
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, InputLayer
import json
import tensorflow as tf
import numpy as np
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

# ================== Config =======================
with open("results_experiment_config.json", 'r') as fp:
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
    # Small Dense network
    model = Sequential()
    model.add(InputLayer(input_shape=(256,)))
    model.add(Dense(10, activation='relu'))
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
        experiment_name="full_training_dense_small"
    )
    experiment.run_kfold(
        images,
        labels,
    )
    experiment.save(save_model=True, save_indices=False)
    print("Finished experiment:", experiment.id)
