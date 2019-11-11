import numpy as np
from master_data_functions.functions import import_data


# Generate a dataset of 1M samples

DATA_PATH = "../data/simulated/"
fname = "CeBr2Mil_Mix.txt"
data = import_data(DATA_PATH+fname, num_samples=1E6)
print("Data imported")
print("Saving energies")
np.save(DATA_PATH+"energies_1M.npy", data["energies"])
print("Saving positions")
np.save(DATA_PATH+"positions_1M.npy", data["positions"])
print("Saving images")
np.save(DATA_PATH+"images_1M.npy", data["images"])
print("Saving labels")
np.save(DATA_PATH+"labels_1M.npy", data["labels"])

