"""
File: config_selector.py
Author: Richárd Rádli
E-mail: radli.richard@mik.uni-pannon.hu
Date: Jul 10, 2023

Description:
The program holds the different configurations for the substream network, stream network and fusion network.
"""

import logging

from typing import Dict

from config.const import DATA_PATH, DATASET_PATH, IMAGES_PATH, NLP_DATA_PATH


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------- C A M E R A   C O N F I G --------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def nlp_configs() -> Dict:
    nlp_config = {
        "pill_names":
            NLP_DATA_PATH.get_data_path("pill_names"),
        "full_sentence_csv":
            NLP_DATA_PATH.get_data_path("full_sentence_csv"),
        "vector_distances":
            NLP_DATA_PATH.get_data_path("vector_distances"),
        "nlp_vector":
            NLP_DATA_PATH.get_data_path("nlp_vector"),
        "word_vector_vis":
            NLP_DATA_PATH.get_data_path("word_vector_vis"),
        "elbow":
            NLP_DATA_PATH.get_data_path("elbow"),
        "silhouette":
            NLP_DATA_PATH.get_data_path("silhouette"),
        "patient_information_leaflet_doc":
            NLP_DATA_PATH.get_data_path("patient_information_leaflet_doc"),
        "patient_information_leaflet_docx":
            NLP_DATA_PATH.get_data_path("patient_information_leaflet_docx"),
        "extracted_features_files":
            NLP_DATA_PATH.get_data_path("extracted_features_files")
    }

    return nlp_config


def Fourier_configs():
    Fourier_paths = {
        "Fourier_collected_images_by_shape_nih":
            IMAGES_PATH.get_data_path("Fourier_collected_images_by_shape_nih"),
        "Fourier_euclidean_distance":
            IMAGES_PATH.get_data_path("Fourier_euclidean_distance"),
        "Fourier_plot_shape":
            IMAGES_PATH.get_data_path("Fourier_plot_shape"),
        "Fourier_saved_mean_vectors":
            DATA_PATH.get_data_path("Fourier_saved_mean_vectors")
    }

    return Fourier_paths


# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------- S U B N E T W O R K   C O N F I G S   T R A I N I N G -------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def sub_stream_network_configs(cfg) -> Dict:
    """
    Returns the dictionary containing the configuration details for the four different subnetworks
    (Contour, LBP, RGB, Texture) used in the StreamNetwork phase.

    :return: A dictionary containing the configuration details for the four subnetworks.
    """

    network_config = {
        # ----------------------------------------------- C O N T O U R ------------------------------------------------
        "Contour": {
            "channels":
                [1, 32, 48, 64, 128, 192, 256],
            "embedded_dim":
                1024,
            "train":
                {
                    "nih":
                        IMAGES_PATH.get_data_path("train_contour_stream_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("train_contour_stream_ogyei"),
                },
            "valid":
                {
                    "nih":
                        IMAGES_PATH.get_data_path("valid_contour_stream_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("valid_contour_stream_ogyei"),
                },
            "test":
                {
                    "nih":
                        IMAGES_PATH.get_data_path("test_contour_stream_ref_nih"),

                    "ogyei":
                        IMAGES_PATH.get_data_path("test_contour_stream_ref_ogyei"),
                },
            "query":
                {
                    "nih":
                        IMAGES_PATH.get_data_path("test_contour_stream_query_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("test_contour_stream_query_ogyei")
                },
            "model_weights_dir": {
                "EfficientNet":
                    {
                        "nih":
                            DATA_PATH.get_data_path("weights_efficient_net_contour_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("weights_efficient_net_contour_ogyei"),
                    },
                "EfficientNetV2":
                    {
                        "nih":
                            DATA_PATH.get_data_path("weights_efficient_net_v2_contour_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("weights_efficient_net_v2_contour_ogyei"),
                    },
            },
            "logs_dir": {
                "EfficientNet":
                        {
                            "nih":
                                DATA_PATH.get_data_path("logs_efficient_net_contour_nih"),
                            "ogyei":
                                DATA_PATH.get_data_path("logs_efficient_net_contour_ogyei"),
                        },
                "EfficientNetV2":
                        {
                            "nih":
                                DATA_PATH.get_data_path("logs_efficient_net_v2_contour_nih"),
                            "ogyei":
                                DATA_PATH.get_data_path("logs_efficient_net_v2_contour_ogyei"),
                        },
            },
            "hardest_negative_samples": {
                "EfficientNet":
                    {
                        "nih":
                            DATA_PATH.get_data_path("negative_efficient_net_contour_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("negative_efficient_net_contour_ogyei"),
                    },
                "EfficientNetV2":
                    {
                        "nih":
                            DATA_PATH.get_data_path("negative_efficient_net_v2_contour_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("negative_efficient_net_v2_contour_ogyei"),
                    },
            },
            "hardest_positive_samples": {
                "EfficientNet":
                    {
                        "nih":
                            DATA_PATH.get_data_path("positive_efficient_net_contour_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("positive_efficient_net_contour_ogyei"),
                    },
                "EfficientNetV2":
                    {
                        "nih":
                            DATA_PATH.get_data_path("positive_efficient_net_v2_contour_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("positive_efficient_net_v2_contour_ogyei"),
                    },
            },
            "learning_rate": {
                "EfficientNet":
                    cfg.learning_rate_en_con,
                "EfficientNetV2":
                    cfg.learning_rate_env2_con
            }.get(cfg.type_of_net, cfg.learning_rate_en_con),
            "image_size": {
                "EfficientNet":
                    cfg.img_size_en,
                "EfficientNetV2":
                    cfg.img_size_en
            }.get(cfg.type_of_net, cfg.img_size_en),
            "grayscale": True
        },

        # --------------------------------------------------- L B P ----------------------------------------------------
        "LBP": {
            "channels":
                [1, 32, 48, 64, 128, 192, 256],
            "embedded_dim":
                1024,
            "train":
                {
                    "nih":
                        IMAGES_PATH.get_data_path("train_lbp_stream_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("train_lbp_stream_ogyei"),
                },
            "valid":
                {
                    "nih":
                        IMAGES_PATH.get_data_path("valid_lbp_stream_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("valid_lbp_stream_ogyei"),
                },
            "test":
                {
                    "nih":
                        IMAGES_PATH.get_data_path("test_lbp_stream_ref_nih"),

                    "ogyei":
                        IMAGES_PATH.get_data_path("test_lbp_stream_ref_ogyei"),
                },
            "query":
                {
                    "nih":
                        IMAGES_PATH.get_data_path("test_lbp_stream_query_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("test_lbp_stream_query_ogyei")
                },
            "model_weights_dir": {
                "EfficientNet":
                    {
                        "nih":
                            DATA_PATH.get_data_path("weights_efficient_net_lbp_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("weights_efficient_net_lbp_ogyei"),
                    },
                "EfficientNetV2":
                    {
                        "nih":
                            DATA_PATH.get_data_path("weights_efficient_net_v2_lbp_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("weights_efficient_net_v2_lbp_ogyei"),
                    },
            },
            "logs_dir": {
                "EfficientNet":
                        {
                            "nih":
                                DATA_PATH.get_data_path("logs_efficient_net_lbp_nih"),
                            "ogyei":
                                DATA_PATH.get_data_path("logs_efficient_net_lbp_ogyei"),
                        },
                "EfficientNetV2":
                    {
                            "nih":
                                DATA_PATH.get_data_path("logs_efficient_net_v2_lbp_nih"),
                            "ogyei":
                                DATA_PATH.get_data_path("logs_efficient_net_v2_lbp_ogyei"),
                    },
            },
            "hardest_negative_samples": {
                "EfficientNet":
                    {
                        "nih":
                            DATA_PATH.get_data_path("negative_efficient_net_lbp_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("negative_efficient_net_lbp_ogyei"),
                    },
                "EfficientNetV2":
                    {
                        "nih":
                            DATA_PATH.get_data_path("negative_efficient_net_v2_lbp_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("negative_efficient_net_v2_lbp_ogyei"),
                    },
            },
            "hardest_positive_samples": {
                "EfficientNet":
                    {
                        "nih":
                            DATA_PATH.get_data_path("positive_efficient_net_lbp_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("positive_efficient_net_lbp_ogyei"),
                    },
                "EfficientNetV2":
                    {
                        "nih":
                            DATA_PATH.get_data_path("positive_efficient_net_v2_lbp_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("positive_efficient_net_v2_lbp_ogyei"),
                    },
            },
            "learning_rate": {
                "EfficientNet":
                    cfg.learning_rate_en_lbp,
                "EfficientNetV2":
                    cfg.learning_rate_env2_lbp
            }.get(cfg.type_of_net, cfg.learning_rate_en_lbp),
            "image_size": {
                "EfficientNet":
                    cfg.img_size_en,
                "EfficientNetV2":
                    cfg.img_size_en
            }.get(cfg.type_of_net, cfg.img_size_en),
            "grayscale": True
        },
        # --------------------------------------------------- R G B ----------------------------------------------------
        "RGB": {
            "channels":
                [3, 64, 96, 128, 256, 384, 512],
            "embedded_dim":
                1024,
            "train":
                {
                    "nih":
                        IMAGES_PATH.get_data_path("train_rgb_stream_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("train_rgb_stream_ogyei"),
                },
            "valid":
                {
                    "nih":
                        IMAGES_PATH.get_data_path("valid_rgb_stream_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("valid_rgb_stream_ogyei"),
                },
            "test":
                {
                    "nih":
                        IMAGES_PATH.get_data_path("test_rgb_stream_ref_nih"),

                    "ogyei":
                        IMAGES_PATH.get_data_path("test_rgb_stream_ref_ogyei"),
                },
            "query":
                {
                    "nih":
                        IMAGES_PATH.get_data_path("test_rgb_stream_query_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("test_rgb_stream_query_ogyei")
                },
            "model_weights_dir": {
                "EfficientNet":
                    {
                        "nih":
                            DATA_PATH.get_data_path("weights_efficient_net_rgb_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("weights_efficient_net_rgb_ogyei"),
                    },
                "EfficientNetV2":
                    {
                        "nih":
                            DATA_PATH.get_data_path("weights_efficient_net_v2_rgb_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("weights_efficient_net_v2_rgb_ogyei"),
                    },
            },
            "logs_dir": {
                "EfficientNet":
                        {
                            "nih":
                                DATA_PATH.get_data_path("logs_efficient_net_rgb_nih"),
                            "ogyei":
                                DATA_PATH.get_data_path("logs_efficient_net_rgb_ogyei"),
                        },
                "EfficientNetV2":
                        {
                            "nih":
                                DATA_PATH.get_data_path("logs_efficient_net_v2_rgb_nih"),
                            "ogyei":
                                DATA_PATH.get_data_path("logs_efficient_net_v2_rgb_ogyei"),
                        },
            },
            "hardest_negative_samples": {
                "EfficientNet":
                    {
                        "nih":
                            DATA_PATH.get_data_path("negative_efficient_net_rgb_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("negative_efficient_net_rgb_ogyei"),
                    },
                "EfficientNetV2":
                    {
                        "nih":
                            DATA_PATH.get_data_path("negative_efficient_net_v2_rgb_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("negative_efficient_net_v2_rgb_ogyei"),
                    },
            },
            "hardest_positive_samples": {
                "EfficientNet":
                    {
                        "nih":
                            DATA_PATH.get_data_path("positive_efficient_net_rgb_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("positive_efficient_net_rgb_ogyei"),
                    },
                "EfficientNetV2":
                    {
                        "nih":
                            DATA_PATH.get_data_path("positive_efficient_net_v2_rgb_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("positive_efficient_net_v2_rgb_ogyei"),
                    },
            },
            "learning_rate": {
                "EfficientNet":
                    cfg.learning_rate_en_rgb,
                "EfficientNetV2":
                    cfg.learning_rate_env2_rgb
            }.get(cfg.type_of_net, cfg.learning_rate_en_rgb),
            "image_size": {
                "EfficientNet":
                    cfg.img_size_en,
                "EfficientNetV2":
                    cfg.img_size_en
            }.get(cfg.type_of_net, cfg.img_size_en),
            "grayscale": False
        },
        # ----------------------------------------------- T E X T U R E ------------------------------------------------
        "Texture": {
            "channels":
                [1, 32, 48, 64, 128, 192, 256],
            "embedded_dim":
                1024,
            "train":
                {
                    "nih":
                        IMAGES_PATH.get_data_path("train_texture_stream_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("train_texture_stream_ogyei"),
                },
            "valid":
                {
                    "nih":
                        IMAGES_PATH.get_data_path("valid_texture_stream_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("valid_texture_stream_ogyei"),
                },
            "test":
                {
                    "nih":
                        IMAGES_PATH.get_data_path("test_texture_stream_ref_nih"),

                    "ogyei":
                        IMAGES_PATH.get_data_path("test_texture_stream_ref_ogyei"),
                },
            "query":
                {
                    "nih":
                        IMAGES_PATH.get_data_path("test_texture_stream_query_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("test_texture_stream_query_ogyei")
                },
            "model_weights_dir": {
                "EfficientNet":
                    {
                        "nih":
                            DATA_PATH.get_data_path("weights_efficient_net_texture_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("weights_efficient_net_texture_ogyei"),
                    },
                "EfficientNetV2":
                    {
                        "nih":
                            DATA_PATH.get_data_path("weights_efficient_net_v2_texture_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("weights_efficient_net_v2_texture_ogyei"),
                    },
            },
            "logs_dir": {
                "EfficientNet":
                        {
                            "nih":
                                DATA_PATH.get_data_path("logs_efficient_net_texture_nih"),
                            "ogyei":
                                DATA_PATH.get_data_path("logs_efficient_net_texture_ogyei"),
                        },
                "EfficientNetV2":
                    {
                            "nih":
                                DATA_PATH.get_data_path("logs_efficient_net_v2_texture_nih"),
                            "ogyei":
                                DATA_PATH.get_data_path("logs_efficient_net_v2_texture_ogyei"),
                    },
            },
            "hardest_negative_samples": {
                "EfficientNet":
                    {
                        "nih":
                            DATA_PATH.get_data_path("negative_efficient_net_texture_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("negative_efficient_net_texture_ogyei"),
                    },
                "EfficientNetV2":
                    {
                        "nih":
                            DATA_PATH.get_data_path("negative_efficient_net_v2_texture_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("negative_efficient_net_v2_texture_ogyei"),
                    },
            },
            "hardest_positive_samples": {
                "EfficientNet": {
                    "nih":
                        DATA_PATH.get_data_path("positive_efficient_net_texture_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("positive_efficient_net_texture_ogyei"),
                },
                "EfficientNetV2": {
                    "nih":
                        DATA_PATH.get_data_path("positive_efficient_net_v2_texture_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("positive_efficient_net_v2_texture_ogyei"),
                },
            },
            "learning_rate": {
                "EfficientNet":
                    cfg.learning_rate_en_tex,
                "EfficientNetV2":
                    cfg.learning_rate_env2_tex
            }.get(cfg.type_of_net, cfg.learning_rate_en_tex),
            "image_size": {
                "EfficientNet":
                    cfg.img_size_en,
                "EfficientNetV2":
                    cfg.img_size_en
            }.get(cfg.type_of_net, cfg.img_size_en),
            "grayscale": True
        }
    }

    return network_config


# ------------------------------------------------------------------------------------------------------------------
# ---------------------------------- G E T   M A I N   N E T W O R K   C O N F I G ---------------------------------
# ------------------------------------------------------------------------------------------------------------------
def stream_network_config(cfg) -> Dict:
    """
    Returns a dictionary containing the prediction, plotting, and reference vectors folder paths for different types of
    networks based on the type_of_net parameter in cfg.
    :return: Dictionary containing the prediction and plotting folder paths.
    """

    network_type = cfg.type_of_net
    logging.info(network_type)
    network_configs = {
        'EfficientNet': {
            'prediction_folder': {
                "nih":
                    DATA_PATH.get_data_path("predictions_efficient_net_nih"),
                "ogyei":
                    DATA_PATH.get_data_path("predictions_efficient_net_ogyei")
            },
            'plotting_folder': {
                "nih":
                    IMAGES_PATH.get_data_path("plotting_efficient_net_nih"),
                "ogyei":
                    IMAGES_PATH.get_data_path("plotting_efficient_net_ogyei")
            },
            'confusion_matrix': {
                "nih":
                    IMAGES_PATH.get_data_path("conf_mtx_efficient_net_nih"),
                "ogyei":
                    IMAGES_PATH.get_data_path("conf_mtx_efficient_net_ogyei")
            },
            'ref_vectors_folder': {
                "nih":
                    DATA_PATH.get_data_path("reference_vectors_efficient_net_nih"),
                "ogyei":
                    DATA_PATH.get_data_path("reference_vectors_efficient_net_ogyei"),
            },
            'hardest_contour_directory': {
                "nih":
                    IMAGES_PATH.get_data_path("contour_hardest_efficient_net_nih"),
                "ogyei":
                    IMAGES_PATH.get_data_path("contour_hardest_efficient_net_ogyei"),
            },
            'hardest_lbp_directory': {
                "nih":
                    IMAGES_PATH.get_data_path("lbp_hardest_efficient_net_nih"),
                "ogyei":
                    IMAGES_PATH.get_data_path("lbp_hardest_efficient_net_ogyei"),
            },
            'hardest_rgb_directory': {
                "nih":
                    IMAGES_PATH.get_data_path("rgb_hardest_efficient_net_nih"),
                "ogyei":
                    IMAGES_PATH.get_data_path("rgb_hardest_efficient_net_ogyei"),
            },
            'hardest_texture_directory': {
                "nih":
                    IMAGES_PATH.get_data_path("texture_hardest_efficient_net_nih"),
                "ogyei":
                    IMAGES_PATH.get_data_path("texture_hardest_efficient_net_ogyei"),
            },
            'hard_negative': {
                "contour": {
                    "nih":
                        DATA_PATH.get_data_path("negative_efficient_net_contour_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("negative_efficient_net_contour_ogyei"),
                },
                "lbp": {
                    "nih":
                        DATA_PATH.get_data_path("negative_efficient_net_lbp_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("negative_efficient_net_lbp_ogyei"),
                },
                "rgb": {
                    "nih":
                        DATA_PATH.get_data_path("negative_efficient_net_rgb_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("negative_efficient_net_rgb_ogyei"),
                },
                "texture": {
                    "nih":
                        DATA_PATH.get_data_path("negative_efficient_net_texture_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("negative_efficient_net_texture_ogyei"),
                },
            },
            'hard_positive': {
                "contour": {
                    "nih":
                        DATA_PATH.get_data_path("positive_efficient_net_contour_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("positive_efficient_net_contour_ogyei"),
                },
                "lbp": {
                    "nih":
                        DATA_PATH.get_data_path("positive_efficient_net_lbp_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("positive_efficient_net_lbp_ogyei"),
                },
                "rgb": {
                    "nih":
                        DATA_PATH.get_data_path("positive_efficient_net_rgb_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("positive_efficient_net_rgb_ogyei"),
                },
                "texture": {
                    "nih":
                        DATA_PATH.get_data_path("positive_efficient_net_texture_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("positive_efficient_net_texture_ogyei"),
                },
            },
        },
        'EfficientNetV2': {
            'prediction_folder': {
                "nih":
                    DATA_PATH.get_data_path("predictions_efficient_net_v2_nih"),
                "ogyei":
                    DATA_PATH.get_data_path("predictions_efficient_net_v2_ogyei")
            },
            'plotting_folder': {
                "nih":
                    IMAGES_PATH.get_data_path("plotting_efficient_net_v2_nih"),
                "ogyei":
                    IMAGES_PATH.get_data_path("plotting_efficient_net_v2_ogyei")
            },
            'confusion_matrix': {
                "nih":
                    IMAGES_PATH.get_data_path("conf_mtx_efficient_net_v2_nih"),
                "ogyei":
                    IMAGES_PATH.get_data_path("conf_mtx_efficient_net_v2_ogyei")
            },
            'ref_vectors_folder': {
                "nih":
                    DATA_PATH.get_data_path("reference_vectors_efficient_net_v2_nih"),
                "ogyei":
                    DATA_PATH.get_data_path("reference_vectors_efficient_net_v2_ogyei"),
            },
            'hardest_contour_directory': {
                "nih":
                    IMAGES_PATH.get_data_path("contour_hardest_efficient_net_v2_nih"),
                "ogyei":
                    IMAGES_PATH.get_data_path("contour_hardest_efficient_net_v2_ogyei"),
            },
            'hardest_lbp_directory': {
                "nih":
                    IMAGES_PATH.get_data_path("lbp_hardest_efficient_net_v2_nih"),
                "ogyei":
                    IMAGES_PATH.get_data_path("lbp_hardest_efficient_net_v2_ogyei"),
            },
            'hardest_rgb_directory': {
                "nih":
                    IMAGES_PATH.get_data_path("rgb_hardest_efficient_net_v2_nih"),
                "ogyei":
                    IMAGES_PATH.get_data_path("rgb_hardest_efficient_net_v2_ogyei"),
            },
            'hardest_texture_directory': {
                "nih":
                    IMAGES_PATH.get_data_path("texture_hardest_efficient_net_v2_nih"),
                "ogyei":
                    IMAGES_PATH.get_data_path("texture_hardest_efficient_net_v2_ogyei"),
            },
            'hard_negative': {
                "contour": {
                    "nih":
                        DATA_PATH.get_data_path("negative_efficient_net_v2_contour_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("negative_efficient_net_v2_contour_ogyei"),
                },
                "lbp": {
                    "nih":
                        DATA_PATH.get_data_path("negative_efficient_net_v2_lbp_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("negative_efficient_net_v2_lbp_ogyei"),
                },
                "rgb": {
                    "nih":
                        DATA_PATH.get_data_path("negative_efficient_net_v2_rgb_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("negative_efficient_net_v2_rgb_ogyei"),
                },
                "texture": {
                    "nih":
                        DATA_PATH.get_data_path("negative_efficient_net_v2_texture_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("negative_efficient_net_v2_texture_ogyei"),
                },
            },
            'hard_positive': {
                "contour": {
                    "nih":
                        DATA_PATH.get_data_path("positive_efficient_net_v2_contour_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("positive_efficient_net_v2_contour_ogyei"),
                },
                "lbp": {
                    "nih":
                        DATA_PATH.get_data_path("positive_efficient_net_v2_lbp_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("positive_efficient_net_v2_lbp_ogyei"),
                },
                "rgb": {
                    "nih":
                        DATA_PATH.get_data_path("positive_efficient_net_v2_rgb_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("positive_efficient_net_v2_rgb_ogyei"),
                },
                "texture": {
                    "nih":
                        DATA_PATH.get_data_path("positive_efficient_net_v2_texture_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("positive_efficient_net_v2_texture_ogyei"),
                },
            },
        },
    }
    if network_type not in network_configs:
        raise ValueError(f'Invalid network type: {network_type}')

    return network_configs[network_type]


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------ M A I N   N E T W O R K   C O N F I G   F U S I O N   T R A I N I N G -----------------------
# ----------------------------------------------------------------------------------------------------------------------
def fusion_network_config(network_type) -> Dict:
    """
    Returns a dictionary containing the prediction, plotting, and reference vectors folder paths for different types of
    networks based on the type_of_net parameter in cfg.
    :return: Dictionary containing the prediction and plotting folder paths.
    """

    network_configs = {
        'EfficientNetSelfAttention': {
            'logs_folder':
                {
                    "nih":
                        DATA_PATH.get_data_path("logs_fusion_network_efficient_net_self_attention_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("logs_fusion_network_efficient_net_self_attention_ogyei"),
                },
            'weights_folder':
                {
                    "nih":
                        DATA_PATH.get_data_path("weights_fusion_network_efficient_net_self_attention_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("weights_fusion_network_efficient_net_self_attention_ogyei"),
                },
            'prediction_folder':
                {
                    "nih":
                        DATA_PATH.get_data_path("predictions_fusion_network_efficient_net_self_attention_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("predictions_fusion_network_efficient_net_self_attention_ogyei"),
                },
            'plotting_folder':
                {
                    "nih":
                        IMAGES_PATH.get_data_path("plotting_fusion_network_efficient_net_self_attention_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("plotting_fusion_network_efficient_net_self_attention_ogyei"),
                },
            'confusion_matrix':
                {
                    "nih":
                        IMAGES_PATH.get_data_path("conf_mtx_fusion_network_efficient_net_self_attention_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("conf_mtx_fusion_network_efficient_net_self_attention_ogyei"),
                },
            'ref_vectors_folder':
                {
                    "nih":
                        DATA_PATH.get_data_path("reference_vectors_fusion_network_efficient_net_self_attention_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("reference_vectors_fusion_network_efficient_net_self_attention_ogyei"),
                },
        },
        'EfficientNetV2SelfAttention': {
            'logs_folder':
                {
                    "nih":
                        DATA_PATH.get_data_path("logs_fusion_network_efficient_net_v2_self_attention_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("logs_fusion_network_efficient_net_v2_self_attention_ogyei"),
                },
            'weights_folder':
                {
                    "nih":
                        DATA_PATH.get_data_path("weights_fusion_network_efficient_net_v2_self_attention_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("weights_fusion_network_efficient_net_v2_self_attention_ogyei"),
                },
            'prediction_folder':
                {
                    "nih":
                        DATA_PATH.get_data_path("predictions_fusion_network_efficient_net_v2_self_attention_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("predictions_fusion_network_efficient_net_v2_self_attention_ogyei"),
                },
            'plotting_folder':
                {
                    "nih":
                        IMAGES_PATH.get_data_path("plotting_fusion_network_efficient_net_v2_self_attention_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("plotting_fusion_network_efficient_net_v2_self_attention_ogyei"),
                },
            'confusion_matrix':
                {
                    "nih":
                        IMAGES_PATH.get_data_path("conf_mtx_fusion_network_efficient_net_v2_self_attention_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("conf_mtx_fusion_network_efficient_net_v2_self_attention_ogyei"),
                },
            'ref_vectors_folder':
                {
                    "nih":
                        DATA_PATH.get_data_path(
                            "reference_vectors_fusion_network_efficient_net_v2_self_attention_nih"
                        ),
                    "ogyei":
                        DATA_PATH.get_data_path(
                            "reference_vectors_fusion_network_efficient_net_v2_self_attention_ogyei"
                        ),
                },
        },
        "EfficientNetV2MultiHeadAttention": {
            'logs_folder':
                {
                    "nih":
                        DATA_PATH.get_data_path("logs_fusion_network_efficient_net_v2_multi_head_attention_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("logs_fusion_network_efficient_net_v2_multi_head_attention_ogyei"),
                },
            'weights_folder':
                {
                    "nih":
                        DATA_PATH.get_data_path("weights_fusion_network_efficient_net_v2_multi_head_attention_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("weights_fusion_network_efficient_net_v2_multi_head_attention_ogyei"),
                },
            'prediction_folder':
                {
                    "nih":
                        DATA_PATH.get_data_path(
                            "predictions_fusion_network_efficient_net_v2_multi_head_attention_nih"
                        ),
                    "ogyei":
                        DATA_PATH.get_data_path(
                            "predictions_fusion_network_efficient_net_v2_multi_head_attention_ogyei"
                        ),
                },
            'plotting_folder':
                {
                    "nih":
                        IMAGES_PATH.get_data_path(
                            "plotting_fusion_network_efficient_net_v2_multi_head_attention_nih"
                        ),
                    "ogyei":
                        IMAGES_PATH.get_data_path(
                            "plotting_fusion_network_efficient_net_v2_multi_head_attention_ogyei"
                        ),
                },
            'confusion_matrix':
                {
                    "nih":
                        IMAGES_PATH.get_data_path(
                            "conf_mtx_fusion_network_efficient_net_v2_multi_head_attention_nih"
                        ),
                    "ogyei":
                        IMAGES_PATH.get_data_path(
                            "conf_mtx_fusion_network_efficient_net_v2_multi_head_attention_ogyei"
                        ),
                },
            'ref_vectors_folder':
                {
                    "nih":
                        DATA_PATH.get_data_path(
                            "reference_vectors_fusion_network_efficient_net_v2_multi_head_attention_nih"
                        ),
                    "ogyei":
                        DATA_PATH.get_data_path(
                            "reference_vectors_fusion_network_efficient_net_v2_multi_head_attention_ogyei"
                        ),
                },
        },
        "EfficientNetV2MHAFMHA": {
            'logs_folder':
                {
                    "nih":
                        DATA_PATH.get_data_path("logs_fusion_network_efficient_net_v2_mha_fmha_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("logs_fusion_network_efficient_net_v2_mha_fmha_ogyei"),
                },
            'weights_folder':
                {
                    "nih":
                        DATA_PATH.get_data_path("weights_fusion_network_efficient_net_v2_mha_fmha_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("weights_fusion_network_efficient_net_v2_mha_fmha_ogyei"),
                },
            'prediction_folder':
                {
                    "nih":
                        DATA_PATH.get_data_path(
                            "predictions_fusion_network_efficient_net_v2_mha_fmha_nih"
                        ),
                    "ogyei":
                        DATA_PATH.get_data_path(
                            "predictions_fusion_network_efficient_net_v2_mha_fmha_ogyei"
                        ),
                },
            'plotting_folder':
                {
                    "nih":
                        IMAGES_PATH.get_data_path(
                            "plotting_fusion_network_efficient_net_v2_mha_fmha_nih"
                        ),
                    "ogyei":
                        IMAGES_PATH.get_data_path(
                            "plotting_fusion_network_efficient_net_v2_mha_fmha_ogyei"
                        ),
                },
            'confusion_matrix':
                {
                    "nih":
                        IMAGES_PATH.get_data_path(
                            "conf_mtx_fusion_network_efficient_net_v2_mha_fmha_nih"
                        ),
                    "ogyei":
                        IMAGES_PATH.get_data_path(
                            "conf_mtx_fusion_network_efficient_net_v2_mha_fmha_ogyei"
                        ),
                },
            'ref_vectors_folder':
                {
                    "nih":
                        DATA_PATH.get_data_path(
                            "reference_vectors_fusion_network_efficient_net_v2_mha_fmha_nih"
                        ),
                    "ogyei":
                        DATA_PATH.get_data_path(
                            "reference_vectors_fusion_network_efficient_net_v2_mha_fmha_ogyei"
                        ),
                },
        },
    }
    if network_type not in network_configs:
        raise ValueError(f'Invalid network type: {network_type}')

    return network_configs[network_type]


def dataset_images_path_selector():
    """
    Selects the correct directory paths based on the given operation string.

    :return: A dictionary containing directory paths for images, masks, and other related files.
    :raises ValueError: If the operation string is not "train" or "test".
    """

    path_to_images = {
        "ogyei": {
            "train": {
                "images": DATASET_PATH.get_data_path("ogyei_v2_single_splitted_train_images"),
                "masks": DATASET_PATH.get_data_path("ogyei_v2_single_splitted_gt_train_masks"),
            },
            "valid": {
                "images": DATASET_PATH.get_data_path("ogyei_v2_single_splitted_valid_images"),
                "masks": DATASET_PATH.get_data_path("ogyei_v2_single_splitted_gt_valid_masks"),
            },
            "test": {
                "images": DATASET_PATH.get_data_path("ogyei_v2_single_splitted_test_images"),
                "masks": DATASET_PATH.get_data_path("ogyei_v2_single_splitted_gt_test_masks"),
            }
        },
        "nih": {
            "train": {
                "images": DATASET_PATH.get_data_path(""),
                "masks": DATASET_PATH.get_data_path(""),

            },
            "valid": {
                "images": DATASET_PATH.get_data_path(""),
                "masks": DATASET_PATH.get_data_path(""),

            },
            "test": {
                "images": DATASET_PATH.get_data_path(""),
                "masks": IMAGES_PATH.get_data_path(""),
            },
            "ref": DATASET_PATH.get_data_path("nih_ref_images"),
            "query": DATASET_PATH.get_data_path("nih_query_images"),
            "xlsx": DATASET_PATH.get_data_path("nih_xlsx")
        },
        "cure": {
            "customer_images":
                DATASET_PATH.get_data_path("cure_customer_images"),
            "customer_segmentation_labels":
                DATASET_PATH.get_data_path("cure_customer_segmentation_labels"),
            "customer_pixel_bbox_labels":
                DATASET_PATH.get_data_path("cure_customer_pixel_bbox_labels"),

            "reference_images":
                DATASET_PATH.get_data_path("cure_reference_images"),
            "reference_masks":
                DATASET_PATH.get_data_path("cure_reference_masks"),

            "train_bbox_pixel_labels":
                DATASET_PATH.get_data_path("cure_train_bbox_pixel_labels"),
            "train_images":
                DATASET_PATH.get_data_path("cure_train_images"),
            "train_mask_images":
                DATASET_PATH.get_data_path("cure_train_mask_images"),
            "train_segmentation_labels":
                DATASET_PATH.get_data_path("cure_train_segmentation_labels"),
            "train_yolo_labels":
                DATASET_PATH.get_data_path("cure_train_yolo_labels"),

            "valid_bbox_pixel_labels":
                DATASET_PATH.get_data_path("cure_valid_bbox_pixel_labels"),
            "valid_images":
                DATASET_PATH.get_data_path("cure_valid_images"),
            "valid_mask_images":
                DATASET_PATH.get_data_path("cure_valid_mask_images"),
            "valid_segmentation_labels":
                DATASET_PATH.get_data_path("cure_valid_segmentation_labels"),
            "valid_yolo_labels":
                DATASET_PATH.get_data_path("cure_valid_yolo_labels"),

            "test_bbox_pixel_labels":
                DATASET_PATH.get_data_path("cure_test_bbox_pixel_labels"),
            "test_images":
                DATASET_PATH.get_data_path("cure_test_images"),
            "test_mask_images":
                DATASET_PATH.get_data_path("cure_test_mask_images"),
            "test_segmentation_labels":
                DATASET_PATH.get_data_path("cure_test_segmentation_labels"),
            "test_yolo_labels":
                DATASET_PATH.get_data_path("cure_test_yolo_labels")
        },
        "dtd": {
            "dataset_path": DATASET_PATH.get_data_path("dtd_images")
        }
    }

    return path_to_images
