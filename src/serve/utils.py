import numpy as np

def is_complete(json_keys, properties):
    array1 = np.array(json_keys)
    array2 = np.array(properties)

    array1_sorted = np.sort(array1)
    array2_sorted = np.sort(array2)

    return np.array_equal(array1_sorted, array2_sorted)