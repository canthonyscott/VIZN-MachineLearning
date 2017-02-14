# This script will be used for preprocessing VIZN zebrabox data outputs
# into arrays useable for machine learning


# This function below reads all files in a directory and pulls out wells passed to
# it in the fish_to_pull list. It returns a dict containing an array of values
# and a list of wells skipped during its processing.

# todo add new non-norm method

def one_file_extract_and_no_norm(file):
    import pandas as pd
    import numpy as np
    from . import constants

    flashes = [1800, 1830, 1860, 1890, 1920]
    collection = []
    wells_skipped = []

    print("Extracting Stimuli time points...")

    data = pd.read_table(file, low_memory=False)

    if data.iloc[95,0] == 'w048':
        plate_size = 48
        fish_to_pull = constants.wells48
        print("48 well plate detected, using 48 well layout.")

    elif data.iloc[95,0] == 'w096':
        fish_to_pull = constants.wells96
        plate_size = 96
        print("96 well plate detected, using 96 well layout.")

    else:
        raise ValueError('Could not determine plate size, file likely has errors')

    # pull out individual fish
    for item in fish_to_pull:
        fish = data.loc[data.animal == item].actinteg.values

        if len(fish) < 1950:
            wells_skipped.append(item)
            continue

        # calculate background activity level for normalization
        baseline = fish[10:1979].mean()

        # check for empty well/dead fish
        if baseline == 0:
            wells_skipped.append(item)
            continue

        # subset for desired times
        timepoints = []
        for flash in flashes:
            timepoints.append(fish[flash])

        # convert to nparray and normalize
        # timepoints = np.array(timepoints)/baseline

        collection.append(timepoints)

    arr = np.array(collection)
    print("Array generated from tab delim files")
    print("n_samples, n_features: " + str(arr.shape))
    # create dict of data to return
    output = {'array': arr, 'skipped': wells_skipped, 'plate': plate_size}

    return output


def match_to_plate_new(result_array, skipped_wells, plate_size):
    # import pandas as pd
    # import numpy as np
    from . import constants
    from collections import OrderedDict

    if plate_size == 48:
        all_wells = constants.wells48
    elif plate_size == 96:
        all_wells = constants.wells96

    # matched_dict = OrderedDict()
    ordered = []
    counter = 0

    for well in all_wells:
        if well not in skipped_wells:
            ordered.append(result_array[counter])
            counter += 1
        else:
            ordered.append('skipped')

    return ordered

def match_to_plate_json(result_array, skipped_wells, plate_size, probability=False):
    """Takes Result array (Class labels or probabilities), skipped wells,
    plate size and outputs a JSON object with the plate size along with an array containing
    well IDs and the result output. If using probabilities the probability flag must be
    set to True."""

    from . import constants
    import json

    if plate_size == 48:
        all_wells = constants.wells48
    elif plate_size == 96:
        all_wells = constants.wells96

    # matched_dict = OrderedDict()
    ordered = []
    final = []
    final.append({'plate_size:': plate_size})
    counter = 0

    for well in all_wells:
        if well not in skipped_wells:
            if probability:
                result = result_array[:,1][counter]
                ordered.append({'well': well, 'result': result})
            else:
                ordered.append({'well': well, 'result': result_array[counter]})
            counter += 1
        else:
            ordered.append({'well': well, 'result': 'skipped'})

    final.append({'data': ordered})
    return json.dumps(final)



def process_for_prediction(input):
    """Takes a raw input array, scales it, takes the log1p of it,
    and returns a numpy array of the result ready to be put tested against
    the model"""

    from sklearn.externals import joblib
    import numpy as np
    from vizn_ml_django.settings import BASE_DIR
    import os

    scaler = joblib.load(os.path.join(BASE_DIR, 'analysis/scripts/model/new_scaler_Jan_31_2016.scaler'))
    test_data = scaler.transform(input)
    test_data = np.log1p(test_data)

    return test_data



