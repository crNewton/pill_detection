import logging

from typing import Dict

from config.const import DATA_PATH, IMAGES_PATH


# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------- S U B N E T W O R K   C O N F I G S   T R A I N I N G -------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def sub_stream_network_configs_training(cfg) -> Dict:
    """
    Returns the dictionary containing the configuration details for the three different subnetworks
    (RGB, Texture, and Contour) used in the TripletLossModel.

    :return: A dictionary containing the configuration details for the three subnetworks.
    """

    network_config = {
        "Contour": {
            "channels":
                [1, 32, 48, 64, 128, 192, 256],
            "train_dataset_dir":
                IMAGES_PATH.get_data_path("ref_train_contour"),
            "valid_dataset_dir":
                IMAGES_PATH.get_data_path("ref_valid_contour"),
            "model_weights_dir": {
                "CNN":
                    DATA_PATH.get_data_path("weights_cnn_network_contour"),
                "EfficientNet":
                    DATA_PATH.get_data_path("weights_efficient_net_contour"),
                "EfficientNetV2":
                    DATA_PATH.get_data_path("weights_efficient_net_v2_contour")
            }.get(cfg.type_of_net, DATA_PATH.get_data_path("weights_cnn_network_contour")),
            "logs_dir": {
                "CNN":
                    DATA_PATH.get_data_path("logs_cnn_contour"),
                "EfficientNet":
                    DATA_PATH.get_data_path("logs_efficient_net_contour"),
                "EfficientNetV2":
                    DATA_PATH.get_data_path("logs_efficient_net_v2_contour"),
            }.get(cfg.type_of_net, DATA_PATH.get_data_path("logs_cnn_contour")),
            "hardest_negative_samples": {
                "CNN":
                    DATA_PATH.get_data_path("negative_cnn_network"),
                "EfficientNet":
                    DATA_PATH.get_data_path("negative_efficient_net"),
                "EfficientNetV2":
                    DATA_PATH.get_data_path("negative_efficient_net_v2")
            }.get(cfg.type_of_net, DATA_PATH.get_data_path("negative_cnn_network")),
            "hardest_positive_samples": {
                "CNN":
                    DATA_PATH.get_data_path("positive_cnn_network"),
                "EfficientNet":
                    DATA_PATH.get_data_path("positive_efficient_net"),
                "EfficientNetV2":
                    DATA_PATH.get_data_path("positive_efficient_net_v2")
            }.get(cfg.type_of_net, DATA_PATH.get_data_path("positive_cnn_network")),
            "learning_rate": {
                "CNN":
                    cfg.learning_rate_cnn_con,
                "EfficientNet":
                    cfg.learning_rate_en_con,
                "EfficientNetV2":
                    cfg.learning_rate_en_con
            }.get(cfg.type_of_net, cfg.learning_rate_cnn_con),
            "image_size": {
                "CNN":
                    cfg.img_size_cnn,
                "EfficientNet":
                    cfg.img_size_en,
                "EfficientNetV2":
                    cfg.img_size_en
            }.get(cfg.type_of_net, cfg.img_size_cnn),
            "grayscale": True
        },

        "LBP": {
            "channels":
                [1, 32, 48, 64, 128, 192, 256],
            "train_dataset_dir":
                IMAGES_PATH.get_data_path("ref_train_lbp"),
            "valid_dataset_dir":
                IMAGES_PATH.get_data_path("ref_valid_lbp"),
            "model_weights_dir": {
                "CNN":
                    DATA_PATH.get_data_path("weights_cnn_network_lbp"),
                "EfficientNet":
                    DATA_PATH.get_data_path("weights_efficient_net_lbp"),
                "EfficientNetV2":
                    DATA_PATH.get_data_path("weights_efficient_net_v2_lbp")
            }.get(cfg.type_of_net, DATA_PATH.get_data_path("weights_stream_network_lbp")),
            "logs_dir": {
                "CNN":
                    DATA_PATH.get_data_path("logs_cnn_lbp"),
                "EfficientNet":
                    DATA_PATH.get_data_path("logs_efficient_net_lbp"),
                "EfficientNetV2":
                    DATA_PATH.get_data_path("logs_efficient_net_v2_lbp")
            }.get(cfg.type_of_net, DATA_PATH.get_data_path("logs_cnn_lbp")),
            "hardest_negative_samples": {
                "CNN":
                    DATA_PATH.get_data_path("negative_cnn_network"),
                "EfficientNet":
                    DATA_PATH.get_data_path("negative_efficient_net"),
                "EfficientNetV2":
                    DATA_PATH.get_data_path("negative_efficient_net_v2")
            }.get(cfg.type_of_net, DATA_PATH.get_data_path("negative_cnn_network")),
            "hardest_positive_samples": {
                "CNN":
                    DATA_PATH.get_data_path("positive_cnn_network"),
                "EfficientNet":
                    DATA_PATH.get_data_path("positive_efficient_net"),
                "EfficientNetV2":
                    DATA_PATH.get_data_path("positive_efficient_net_v2")
            }.get(cfg.type_of_net, DATA_PATH.get_data_path("positive_cnn_network")),
            "learning_rate": {
                "CNN":
                    cfg.learning_rate_cnn_lbp,
                "EfficientNet":
                    cfg.learning_rate_en_lbp,
                "EfficientNetV2":
                    cfg.learning_rate_en_lbp
            }.get(cfg.type_of_net, cfg.learning_rate_cnn_lbp),
            "image_size": {
                "CNN":
                    cfg.img_size_cnn,
                "EfficientNet":
                    cfg.img_size_en,
                "EfficientNetV2":
                    cfg.img_size_en
            }.get(cfg.type_of_net, cfg.img_size_cnn),
            "grayscale": True
        },

        "RGB": {
            "channels":
                [3, 64, 96, 128, 256, 384, 512],
            "train_dataset_dir":
                IMAGES_PATH.get_data_path("ref_train_rgb"),
            "valid_dataset_dir":
                IMAGES_PATH.get_data_path("ref_valid_rgb"),
            "model_weights_dir": {
                "CNN":
                    DATA_PATH.get_data_path("weights_cnn_network_rgb"),
                "EfficientNet":
                    DATA_PATH.get_data_path("weights_efficient_net_rgb"),
                "EfficientNetV2":
                    DATA_PATH.get_data_path("weights_efficient_net_v2_rgb")
            }.get(cfg.type_of_net, DATA_PATH.get_data_path("weights_cnn_network_rgb")),
            "logs_dir": {
                "CNN":
                    DATA_PATH.get_data_path("logs_cnn_rgb"),
                "EfficientNet":
                    DATA_PATH.get_data_path("logs_efficient_net_rgb"),
                "EfficientNetV2":
                    DATA_PATH.get_data_path("logs_efficient_net_v2_rgb")
            }.get(cfg.type_of_net, DATA_PATH.get_data_path("logs_cnn_rgb")),
            "hardest_negative_samples": {
                "CNN":
                    DATA_PATH.get_data_path("negative_cnn_network"),
                "EfficientNet":
                    DATA_PATH.get_data_path("negative_efficient_net"),
                "EfficientNetV2":
                    DATA_PATH.get_data_path("negative_efficient_net_v2")
            }.get(cfg.type_of_net, DATA_PATH.get_data_path("negative_cnn_network")),
            "hardest_positive_samples": {
                "CNN":
                    DATA_PATH.get_data_path("positive_cnn_network"),
                "EfficientNet":
                    DATA_PATH.get_data_path("positive_efficient_net"),
                "EfficientNetV2":
                    DATA_PATH.get_data_path("positive_efficient_net_v2")
            }.get(cfg.type_of_net, DATA_PATH.get_data_path("positive_cnn_network")),
            "learning_rate": {
                "CNN":
                    cfg.learning_rate_cnn_rgb,
                "EfficientNet":
                    cfg.learning_rate_en_rgb,
                "EfficientNetV2":
                    cfg.learning_rate_en_rgb
            }.get(cfg.type_of_net, cfg.learning_rate_cnn_rgb),
            "image_size": {
                "CNN":
                    cfg.img_size_cnn,
                "EfficientNet":
                    cfg.img_size_en,
                "EfficientNetV2":
                    cfg.img_size_en
            }.get(cfg.type_of_net, cfg.img_size_cnn),
            "grayscale": False
        },

        "Texture": {
            "channels":
                [1, 32, 48, 64, 128, 192, 256],
            "train_dataset_dir":
                IMAGES_PATH.get_data_path("ref_train_texture"),
            "valid_dataset_dir":
                IMAGES_PATH.get_data_path("ref_valid_texture"),
            "model_weights_dir": {
                "CNN":
                    DATA_PATH.get_data_path("weights_cnn_network_texture"),
                "EfficientNet":
                    DATA_PATH.get_data_path("weights_efficient_net_texture"),
                "EfficientNetV2":
                    DATA_PATH.get_data_path("weights_efficient_net_v2_texture")
            }.get(cfg.type_of_net, DATA_PATH.get_data_path("weights_cnn_network_texture")),
            "logs_dir": {
                "CNN":
                    DATA_PATH.get_data_path("logs_cnn_texture"),
                "EfficientNet":
                    DATA_PATH.get_data_path("logs_efficient_net_texture"),
                "EfficientNetV2":
                    DATA_PATH.get_data_path("logs_efficient_net_v2_texture")
            }.get(cfg.type_of_net, DATA_PATH.get_data_path("logs_cnn_texture")),
            "hardest_negative_samples": {
                "CNN":
                    DATA_PATH.get_data_path("negative_cnn_network"),
                "EfficientNet":
                    DATA_PATH.get_data_path("negative_efficient_net"),
                "EfficientNetV2":
                    DATA_PATH.get_data_path("negative_efficient_net_v2")
            }.get(cfg.type_of_net, DATA_PATH.get_data_path("negative_cnn_network")),
            "hardest_positive_samples": {
                "CNN":
                    DATA_PATH.get_data_path("positive_cnn_network"),
                "EfficientNet":
                    DATA_PATH.get_data_path("positive_efficient_net"),
                "EfficientNetV2":
                    DATA_PATH.get_data_path("positive_efficient_net_v2")
            }.get(cfg.type_of_net, DATA_PATH.get_data_path("positive_cnn_network")),
            "learning_rate": {
                "CNN":
                    cfg.learning_rate_cnn_tex,
                "EfficientNet":
                    cfg.learning_rate_en_tex,
                "EfficientNetV2":
                    cfg.learning_rate_en_tex
            }.get(cfg.type_of_net, cfg.learning_rate_cnn_tex),
            "image_size": {
                "CNN":
                    cfg.img_size_cnn,
                "EfficientNet":
                    cfg.img_size_en,
                "EfficientNetV2":
                    cfg.img_size_en
            }.get(cfg.type_of_net, cfg.img_size_cnn),
            "grayscale": True
        }
    }

    return network_config


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------- S U B N E T W O R K   C O N F I G S   I N F E R E N C E ------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def sub_stream_network_config_inference(cfg) -> Dict:
    """
    Returns the configuration of subnetworks

    :return: dictionary containing subnetwork configuration
    """

    network_config = {
        "Contour": {
            "channels": [1, 32, 48, 64, 128, 192, 256],
            "model_weights_dir": {
                "CNN":
                    DATA_PATH.get_data_path("weights_cnn_network_contour"),
                "EfficientNet":
                    DATA_PATH.get_data_path("weights_efficient_net_contour"),
                "EfficientNetV2":
                    DATA_PATH.get_data_path("weights_efficient_net_v2_contour")
            }.get(cfg.type_of_net, DATA_PATH.get_data_path("weights_cnn_network_contour")),
            "image_size": {
                "CNN":
                    cfg.img_size_cnn,
                "EfficientNet":
                    cfg.img_size_en,
                "EfficientNetV2":
                    cfg.img_size_en
            }.get(cfg.type_of_net, cfg.img_size_cnn),
            "grayscale": True
        },

        "LBP": {
            "channels": [1, 32, 48, 64, 128, 192, 256],
            "model_weights_dir": {
                "CNN":
                    DATA_PATH.get_data_path("weights_cnn_network_lbp"),
                "EfficientNet":
                    DATA_PATH.get_data_path("weights_efficient_net_lbp"),
                "EfficientNetV2":
                    DATA_PATH.get_data_path("weights_efficient_net_v2_lbp")
            }.get(cfg.type_of_net, DATA_PATH.get_data_path("weights_cnn_network_lbp")),
            "image_size": {
                "CNN":
                    cfg.img_size_cnn,
                "EfficientNet":
                    cfg.img_size_en,
                "EfficientNetV2":
                    cfg.img_size_en
            }.get(cfg.type_of_net, cfg.img_size_cnn),
            "grayscale": True
        },

        "RGB": {
            "channels": [3, 64, 96, 128, 256, 384, 512],
            "model_weights_dir": {
                "CNN":
                    DATA_PATH.get_data_path("weights_cnn_network_rgb"),
                "EfficientNet":
                    DATA_PATH.get_data_path("weights_efficient_net_rgb"),
                "EfficientNetV2":
                    DATA_PATH.get_data_path("weights_efficient_net_v2_rgb")
            }.get(cfg.type_of_net, DATA_PATH.get_data_path("weights_cnn_network_rgb")),
            "image_size": {
                "CNN":
                    cfg.img_size_cnn,
                "EfficientNet":
                    cfg.img_size_en,
                "EfficientNetV2":
                    cfg.img_size_en
            }.get(cfg.type_of_net, cfg.img_size_cnn),
            "grayscale": False
        },

        "Texture": {
            "channels": [1, 32, 48, 64, 128, 192, 256],
            "model_weights_dir": {
                "CNN":
                    DATA_PATH.get_data_path("weights_cnn_network_texture"),
                "EfficientNet":
                    DATA_PATH.get_data_path("weights_efficient_net_texture"),
                "EfficientNetV2":
                    DATA_PATH.get_data_path("weights_efficient_net_v2_texture")
            }.get(cfg.type_of_net, DATA_PATH.get_data_path("weights_cnn_network_texture")),
            "image_size": {
                "CNN":
                    cfg.img_size_cnn,
                "EfficientNet":
                    cfg.img_size_en,
                "EfficientNetV2":
                    cfg.img_size_en
            }.get(cfg.type_of_net, cfg.img_size_cnn),
            "grayscale": True
        },
    }

    return network_config


# ------------------------------------------------------------------------------------------------------------------
# ---------------------------------- G E T   M A I N   N E T W O R K   C O N F I G ---------------------------------
# ------------------------------------------------------------------------------------------------------------------
def stream_network_config_inference(cfg) -> Dict:
    """
    Returns a dictionary containing the prediction and plotting folder paths for different types of networks
    based on the type_of_net parameter in cfg.
    :return: Dictionary containing the prediction and plotting folder paths.
    """

    network_type = cfg.type_of_net
    logging.info(network_type)
    network_configs = {
        'CNN': {
            'prediction_folder':
                DATA_PATH.get_data_path("predictions_cnn_network"),
            'plotting_folder':
                IMAGES_PATH.get_data_path("plotting_cnn_network"),
            'ref_vectors_folder':
                DATA_PATH.get_data_path("reference_vectors_cnn_network")
        },
        'EfficientNet': {
            'prediction_folder':
                DATA_PATH.get_data_path("predictions_efficient_net"),
            'plotting_folder':
                IMAGES_PATH.get_data_path("plotting_efficient_net"),
            'ref_vectors_folder':
                DATA_PATH.get_data_path("reference_vectors_efficient_net")
        },
        'EfficientNetV2': {
            'prediction_folder':
                DATA_PATH.get_data_path("predictions_efficient_net_v2"),
            'plotting_folder':
                IMAGES_PATH.get_data_path("plotting_efficient_net_v2"),
            'ref_vectors_folder':
                DATA_PATH.get_data_path("reference_vectors_efficient_net_v2")
        }
    }
    if network_type not in network_configs:
        raise ValueError(f'Invalid network type: {network_type}')

    return network_configs[network_type]


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------ M A I N   N E T W O R K   C O N F I G   F U S I O N   T R A I N I N G -----------------------
# ----------------------------------------------------------------------------------------------------------------------
def fusion_network_config(network_type) -> Dict:
    network_configs = {
        'CNNFusionNet': {
            'logs_folder':
                DATA_PATH.get_data_path("logs_fusion_network_cnn"),
            'weights_folder':
                DATA_PATH.get_data_path("weights_fusion_network_cnn"),
            'prediction_folder':
                DATA_PATH.get_data_path("predictions_fusion_network_cnn"),
            'plotting_folder':
                IMAGES_PATH.get_data_path("plotting_fusion_network_cnn"),
            'ref_vectors_folder':
                DATA_PATH.get_data_path("reference_vectors_fusion_network_cnn")
        },
        'EfficientNetSelfAttention': {
            'logs_folder':
                DATA_PATH.get_data_path("logs_fusion_network_efficient_net_self_attention"),
            'weights_folder':
                DATA_PATH.get_data_path("weights_fusion_network_efficient_net_self_attention"),
            'prediction_folder':
                DATA_PATH.get_data_path("predictions_fusion_network_efficient_net_self_attention_net"),
            'plotting_folder':
                IMAGES_PATH.get_data_path("plotting_fusion_network_efficient_net_self_attention"),
            'ref_vectors_folder':
                DATA_PATH.get_data_path("reference_vectors_fusion_net_efficient_net_self_attention")
        },
        'EfficientNetV2SelfAttention': {
            'logs_folder':
                DATA_PATH.get_data_path("logs_fusion_network_efficient_net_v2_self_attention"),
            'weights_folder':
                DATA_PATH.get_data_path("weights_fusion_network_efficient_net_v2_self_attention"),
            'prediction_folder':
                DATA_PATH.get_data_path("predictions_fusion_network_efficient_net_v2_self_attention_net"),
            'plotting_folder':
                IMAGES_PATH.get_data_path("plotting_fusion_network_efficient_net_v2_self_attention"),
            'ref_vectors_folder':
                DATA_PATH.get_data_path("reference_vectors_fusion_net_efficient_net_v2_self_attention")
        },
        "EfficientNetV2MultiHeadAttention": {
            'logs_folder':
                DATA_PATH.get_data_path("logs_fusion_network_efficient_net_v2_multi_head_attention"),
            'weights_folder':
                DATA_PATH.get_data_path("weights_fusion_network_efficient_net_v2_multi_head_attention"),
            'prediction_folder':
                DATA_PATH.get_data_path("predictions_fusion_network_efficient_net_v2_multi_head_attention"),
            'plotting_folder':
                IMAGES_PATH.get_data_path("plotting_fusion_network_efficient_net_v2_multi_head_attention"),
            'ref_vectors_folder':
                DATA_PATH.get_data_path("reference_vectors_fusion_net_efficient_net_v2_multi_head_attention")
        }
    }
    if network_type not in network_configs:
        raise ValueError(f'Invalid network type: {network_type}')

    return network_configs[network_type]
