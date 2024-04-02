import json
import logging
import numpy as np
import os

from config.config import ConfigAugmentation
from config.config_selector import dataset_images_path_selector
from utils.utils import find_latest_file_in_directory, NumpyEncoder, create_timestamp, plot_euclidean_distances


def normalize_values(values, operation, dataset_name=None):
    normalized_values = {}

    for key, value in values.items():

        data1 = np.array(value[0])
        normalized_data1 = (data1 - np.min(data1)) / (np.max(data1) - np.min(data1))

        if operation == 'lab':
            if dataset_name != "cure_one_sided":
                data2 = np.array(value[1])
                normalized_data2 = (data2 - np.min(data2)) / (np.max(data2) - np.min(data2))
                concat_data = np.concatenate((normalized_data1, normalized_data2), axis=1)
            else:
                concat_data = normalized_data1
        elif operation == "fourier":
            concat_data = normalized_data1
        else:
            raise ValueError("Unknown operation {}".format(operation))

        concat_data_flattened = np.reshape(concat_data, (1, -1))
        normalized_values[key] = concat_data_flattened

    return normalized_values


def load_json_files(dataset_name, feature_type: str):
    path = (
        dataset_images_path_selector(dataset_name).get("dynamic_margin").get(feature_type)
    )
    json_file = find_latest_file_in_directory(path, "json")
    json_file_name = os.path.join(path, json_file)

    with open(json_file_name, "r") as file:
        values = json.load(file)

    logging.info(f"Loaded json file: {json_file_name}")

    return values


def save_json_file(dataset_name, timestamp, combined_vectors):
    combined_vectors_path = (
        dataset_images_path_selector(dataset_name).get("dynamic_margin").get("concatenated_vectors")
    )
    combined_vectors_name = os.path.join(combined_vectors_path, f"{timestamp}_concatenated_vectors.json")
    with open(combined_vectors_name, "w") as file:
        json.dump(combined_vectors, file, cls=NumpyEncoder)

    logging.info(f"Saved json file: {combined_vectors_name}")


def reshape_one_hot_encoded_vectors(dataset_name, vector_type):
    encoded_vectors = load_json_files(dataset_name, vector_type)

    normalized_values = {}

    for key, value in encoded_vectors.items():
        concat_data_flattened = np.reshape(value, (1, -1))
        normalized_values[key] = concat_data_flattened

    return normalized_values


def process_vectors(lab_values, fourier_desc_values, imprint_values, score_values):
    """
    
    Args:
        lab_values:
        fourier_desc_values:
        imprint_values:
        score_values:

    Returns:

    """
    combined_vectors = {}

    for class_id in lab_values.keys():
        combined_vectors[class_id] = []

        combined_vector = np.hstack((
                lab_values[class_id],
                fourier_desc_values[class_id],
                imprint_values[class_id],
                score_values[class_id]
        ))

        combined_vectors[class_id].append(combined_vector)

    combined_vectors = {class_id: values[0] for class_id, values in combined_vectors.items()}
    return combined_vectors


def main():
    cfg = ConfigAugmentation().parse()
    timestamp = create_timestamp()
    dataset_name = cfg.dataset_name

    # L*a*b* values
    lab_values = load_json_files(dataset_name, "colour_vectors")
    norm_lab_values = normalize_values(lab_values, "lab", cfg.dataset_name)

    # Fourier descriptors
    fourier_desc_values = load_json_files(dataset_name, "Fourier_saved_mean_vectors")
    norm_fourier_desc_values = normalize_values(fourier_desc_values, "fourier")

    # imprint vectors
    imprint_values = reshape_one_hot_encoded_vectors(dataset_name, "imprint_vectors")

    # score vectors
    score_values = reshape_one_hot_encoded_vectors(dataset_name, "score_vectors")

    # Combine vectors
    combined_vectors = process_vectors(norm_lab_values, norm_fourier_desc_values, imprint_values, score_values)

    # Save it to a json file
    save_json_file(dataset_name, timestamp, combined_vectors)

    # Plot Euclidean matrix
    plot_euc_dir = dataset_images_path_selector(dataset_name).get("dynamic_margin").get("combined_vectors_euc_dst")
    filename = os.path.join(plot_euc_dir, f"euclidean_distances_{timestamp}.png")
    plot_euclidean_distances(vectors=combined_vectors,
                             dataset_name=cfg.dataset_name,
                             filename=filename,
                             normalize=False,
                             operation="combined_vectors",
                             plot_size=80)


if __name__ == "__main__":
    main()
