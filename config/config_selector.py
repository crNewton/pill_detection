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
                    "cure": {
                        "anchor":
                            IMAGES_PATH.get_data_path("train_contour_stream_cure_anchor"),
                        "pos_neg":
                            IMAGES_PATH.get_data_path("contour_stream_cure_pos_neg")
                    },
                    "nih":
                        IMAGES_PATH.get_data_path("train_contour_stream_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("train_contour_stream_ogyei"),
                },
            "ref":
                {
                    "cure":
                        IMAGES_PATH.get_data_path("test_contour_stream_ref_cure"),
                    "nih":
                        IMAGES_PATH.get_data_path("test_contour_stream_ref_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("test_contour_stream_ref_ogyei"),
                },
            "query":
                {
                    "cure":
                        IMAGES_PATH.get_data_path("test_contour_stream_query_cure"),
                    "nih":
                        IMAGES_PATH.get_data_path("test_contour_stream_query_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("test_contour_stream_query_ogyei")
                },
            "model_weights_dir": {
                "EfficientNet":
                    {
                        "cure":
                            DATA_PATH.get_data_path("weights_efficient_net_contour_cure"),
                        "nih":
                            DATA_PATH.get_data_path("weights_efficient_net_contour_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("weights_efficient_net_contour_ogyei"),
                    }
            },
            "logs_dir": {
                "EfficientNet":
                    {
                        "cure":
                            DATA_PATH.get_data_path("logs_efficient_net_contour_cure"),
                        "nih":
                            DATA_PATH.get_data_path("logs_efficient_net_contour_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("logs_efficient_net_contour_ogyei"),
                    }
            },
            "learning_rate": {
                "EfficientNet":
                    cfg.learning_rate_en_con,
            }.get(cfg.type_of_net, cfg.learning_rate_en_con),
            "image_size": {
                "EfficientNet":
                    cfg.img_size_en,
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
                    "cure": {
                        "anchor":
                            IMAGES_PATH.get_data_path("train_lbp_stream_cure_anchor"),
                        "pos_neg":
                            IMAGES_PATH.get_data_path("lbp_stream_cure_pos_neg")
                    },
                    "nih":
                        IMAGES_PATH.get_data_path("train_lbp_stream_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("train_lbp_stream_ogyei"),
                },
            "ref":
                {
                    "cure":
                        IMAGES_PATH.get_data_path("test_lbp_stream_ref_cure"),
                    "nih":
                        IMAGES_PATH.get_data_path("test_lbp_stream_ref_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("test_lbp_stream_ref_ogyei"),
                },
            "query":
                {
                    "cure":
                        IMAGES_PATH.get_data_path("test_lbp_stream_query_cure"),
                    "nih":
                        IMAGES_PATH.get_data_path("test_lbp_stream_query_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("test_lbp_stream_query_ogyei")
                },
            "model_weights_dir": {
                "EfficientNet":
                    {
                        "cure":
                            DATA_PATH.get_data_path("weights_efficient_net_lbp_cure"),
                        "nih":
                            DATA_PATH.get_data_path("weights_efficient_net_lbp_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("weights_efficient_net_lbp_ogyei"),
                    }
            },
            "logs_dir": {
                "EfficientNet":
                    {
                        "cure":
                            DATA_PATH.get_data_path("logs_efficient_net_lbp_cure"),
                        "nih":
                            DATA_PATH.get_data_path("logs_efficient_net_lbp_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("logs_efficient_net_lbp_ogyei"),
                    }
            },
            "learning_rate": {
                "EfficientNet":
                    cfg.learning_rate_en_lbp
            }.get(cfg.type_of_net, cfg.learning_rate_en_lbp),
            "image_size": {
                "EfficientNet":
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
                    "cure": {
                        "anchor":
                            IMAGES_PATH.get_data_path("train_rgb_stream_cure_anchor"),
                        "pos_neg":
                            IMAGES_PATH.get_data_path("rgb_stream_cure_pos_neg")
                    },
                    "nih":
                        IMAGES_PATH.get_data_path("train_rgb_stream_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("train_rgb_stream_ogyei"),
                },
            "ref":
                {
                    "cure":
                        IMAGES_PATH.get_data_path("test_rgb_stream_ref_cure"),
                    "nih":
                        IMAGES_PATH.get_data_path("test_rgb_stream_ref_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("test_rgb_stream_ref_ogyei"),
                },
            "query":
                {
                    "cure":
                        IMAGES_PATH.get_data_path("test_rgb_stream_query_cure"),
                    "nih":
                        IMAGES_PATH.get_data_path("test_rgb_stream_query_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("test_rgb_stream_query_ogyei")
                },
            "model_weights_dir": {
                "EfficientNet":
                    {
                        "cure":
                            DATA_PATH.get_data_path("weights_efficient_net_rgb_cure"),
                        "nih":
                            DATA_PATH.get_data_path("weights_efficient_net_rgb_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("weights_efficient_net_rgb_ogyei"),
                    }
            },
            "logs_dir": {
                "EfficientNet":
                    {
                        "cure":
                            DATA_PATH.get_data_path("logs_efficient_net_rgb_cure"),
                        "nih":
                            DATA_PATH.get_data_path("logs_efficient_net_rgb_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("logs_efficient_net_rgb_ogyei"),
                    }
            },
            "learning_rate": {
                "EfficientNet":
                    cfg.learning_rate_en_rgb,
            }.get(cfg.type_of_net, cfg.learning_rate_en_rgb),
            "image_size": {
                "EfficientNet":
                    cfg.img_size_en,
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
                    "cure": {
                        "anchor":
                            IMAGES_PATH.get_data_path("train_texture_stream_cure_anchor"),
                        "pos_neg":
                            IMAGES_PATH.get_data_path("texture_stream_cure_pos_neg")
                    },
                    "nih":
                        IMAGES_PATH.get_data_path("train_texture_stream_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("train_texture_stream_ogyei"),
                },
            "ref":
                {
                    "cure":
                        IMAGES_PATH.get_data_path("test_texture_stream_ref_cure"),
                    "nih":
                        IMAGES_PATH.get_data_path("test_texture_stream_ref_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("test_texture_stream_ref_ogyei"),
                },
            "query":
                {
                    "cure":
                        IMAGES_PATH.get_data_path("test_texture_stream_query_cure"),
                    "nih":
                        IMAGES_PATH.get_data_path("test_texture_stream_query_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("test_texture_stream_query_ogyei")
                },
            "model_weights_dir": {
                "EfficientNet":
                    {
                        "cure":
                            DATA_PATH.get_data_path("weights_efficient_net_texture_cure"),
                        "nih":
                            DATA_PATH.get_data_path("weights_efficient_net_texture_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("weights_efficient_net_texture_ogyei"),
                    }
            },
            "logs_dir": {
                "EfficientNet":
                    {
                        "cure":
                            DATA_PATH.get_data_path("logs_efficient_net_texture_cure"),
                        "nih":
                            DATA_PATH.get_data_path("logs_efficient_net_texture_nih"),
                        "ogyei":
                            DATA_PATH.get_data_path("logs_efficient_net_texture_ogyei"),
                    }
            },
            "learning_rate": {
                "EfficientNet":
                    cfg.learning_rate_en_tex,
            }.get(cfg.type_of_net, cfg.learning_rate_en_tex),
            "image_size": {
                "EfficientNet":
                    cfg.img_size_en,
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
        'EfficientNet':
            {
                'prediction_folder': {
                    "cure":
                        DATA_PATH.get_data_path("predictions_efficient_net_cure"),
                    "nih":
                        DATA_PATH.get_data_path("predictions_efficient_net_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("predictions_efficient_net_ogyei")
                },
                'plotting_folder': {
                    "cure":
                        IMAGES_PATH.get_data_path("plotting_efficient_net_cure"),
                    "nih":
                        IMAGES_PATH.get_data_path("plotting_efficient_net_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("plotting_efficient_net_ogyei")
                },
                'confusion_matrix': {
                    "cure":
                        IMAGES_PATH.get_data_path("conf_mtx_efficient_net_cure"),
                    "nih":
                        IMAGES_PATH.get_data_path("conf_mtx_efficient_net_nih"),
                    "ogyei":
                        IMAGES_PATH.get_data_path("conf_mtx_efficient_net_ogyei")
                },
                'ref_vectors_folder': {
                    "cure":
                        DATA_PATH.get_data_path("reference_vectors_efficient_net_cure"),
                    "nih":
                        DATA_PATH.get_data_path("reference_vectors_efficient_net_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("reference_vectors_efficient_net_ogyei"),
                }
            }
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
        'EfficientNetMultiHeadAttention': {
            'logs_folder':
                {
                    "cure":
                        DATA_PATH.get_data_path("logs_fusion_network_efficient_net_multi_head_attention_cure"),
                    "nih":
                        DATA_PATH.get_data_path("logs_fusion_network_efficient_net_multi_head_attention_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("logs_fusion_network_efficient_net_multi_head_attention_ogyei"),
                },
            'weights_folder':
                {
                    "cure":
                        DATA_PATH.get_data_path("weights_fusion_network_efficient_net_multi_head_attention_cure"),
                    "nih":
                        DATA_PATH.get_data_path("weights_fusion_network_efficient_net_multi_head_attention_nih"),
                    "ogyei":
                        DATA_PATH.get_data_path("weights_fusion_network_efficient_net_multi_head_attention_ogyei"),
                },
            'prediction_folder':
                {
                    "cure":
                        DATA_PATH.get_data_path(
                            "predictions_fusion_network_efficient_net_multi_head_attention_cure"
                        ),
                    "nih":
                        DATA_PATH.get_data_path(
                            "predictions_fusion_network_efficient_net_multi_head_attention_nih"
                        ),
                    "ogyei":
                        DATA_PATH.get_data_path(
                            "predictions_fusion_network_efficient_net_multi_head_attention_ogyei"
                        ),
                },
            'plotting_folder':
                {
                    "cure":
                        IMAGES_PATH.get_data_path(
                            "plotting_fusion_network_efficient_net_multi_head_attention_cure"
                        ),
                    "nih":
                        IMAGES_PATH.get_data_path(
                            "plotting_fusion_network_efficient_net_multi_head_attention_nih"
                        ),
                    "ogyei":
                        IMAGES_PATH.get_data_path(
                            "plotting_fusion_network_efficient_net_multi_head_attention_ogyei"
                        ),
                },
            'confusion_matrix':
                {
                    "cure":
                        IMAGES_PATH.get_data_path(
                            "conf_mtx_fusion_network_efficient_net_multi_head_attention_cure"
                        ),
                    "nih":
                        IMAGES_PATH.get_data_path(
                            "conf_mtx_fusion_network_efficient_net_multi_head_attention_nih"
                        ),
                    "ogyei":
                        IMAGES_PATH.get_data_path(
                            "conf_mtx_fusion_network_efficient_net_multi_head_attention_ogyei"
                        ),
                },
            'ref_vectors_folder':
                {
                    "cure":
                        DATA_PATH.get_data_path(
                            "reference_vectors_fusion_network_efficient_net_multi_head_attention_cure"
                        ),
                    "nih":
                        DATA_PATH.get_data_path(
                            "reference_vectors_fusion_network_efficient_net_multi_head_attention_nih"
                        ),
                    "ogyei":
                        DATA_PATH.get_data_path(
                            "reference_vectors_fusion_network_efficient_net_multi_head_attention_ogyei"
                        ),
                }
        }
    }
    if network_type not in network_configs:
        raise ValueError(f'Invalid network type: {network_type}')

    return network_configs[network_type]


def dataset_images_path_selector(dataset_name):
    """
    Selects the correct directory paths based on the given operation string.

    :return: A dictionary containing directory paths for images, masks, and other related files.
    :raises ValueError: If the operation string is not "train" or "test".
    """

    path_to_images = {
        # --------------------------------------------------- C U R E --------------------------------------------------
        "cure": {
            "customer": {
                "customer_images":
                    DATASET_PATH.get_data_path("cure_customer_images"),
                "customer_segmentation_labels":
                    DATASET_PATH.get_data_path("cure_customer_segmentation_labels"),
                "customer_pixel_bbox_labels":
                    DATASET_PATH.get_data_path("cure_customer_pixel_bbox_labels"),
                "customer_mask_images":
                    DATASET_PATH.get_data_path("cure_customer_mask_images")
            },

            "reference": {
                "reference_images":
                    DATASET_PATH.get_data_path("cure_reference_images"),
                "reference_mask_images":
                    DATASET_PATH.get_data_path("cure_reference_mask_images"),
                "reference_labels":
                    DATASET_PATH.get_data_path("cure_reference_yolo_labels"),
            },

            "train": {
                "bbox_pixel_labels":
                    DATASET_PATH.get_data_path("cure_train_bbox_pixel_labels"),
                "images":
                    DATASET_PATH.get_data_path("cure_train_images"),
                "mask_images":
                    DATASET_PATH.get_data_path("cure_train_mask_images"),
                "segmentation_labels":
                    DATASET_PATH.get_data_path("cure_train_segmentation_labels"),
                "yolo_labels":
                    DATASET_PATH.get_data_path("cure_train_yolo_labels"),
                "aug_images":
                    DATASET_PATH.get_data_path("cure_train_aug_images"),
                "aug_yolo_labels":
                    DATASET_PATH.get_data_path("cure_train_aug_yolo_labels"),
                "aug_mask_images":
                    DATASET_PATH.get_data_path("cure_train_aug_mask_images"),
            },

            "valid": {
                "bbox_pixel_labels":
                    DATASET_PATH.get_data_path("cure_valid_bbox_pixel_labels"),
                "images":
                    DATASET_PATH.get_data_path("cure_valid_images"),
                "mask_images":
                    DATASET_PATH.get_data_path("cure_valid_mask_images"),
                "segmentation_labels":
                    DATASET_PATH.get_data_path("cure_valid_segmentation_labels"),
                "yolo_labels":
                    DATASET_PATH.get_data_path("cure_valid_yolo_labels"),
                "aug_images":
                    DATASET_PATH.get_data_path("cure_valid_aug_images"),
                "aug_yolo_labels":
                    DATASET_PATH.get_data_path("cure_valid_aug_yolo_labels"),
                "aug_mask_images":
                    DATASET_PATH.get_data_path("cure_valid_aug_mask_images"),
            },

            "test": {
                "bbox_pixel_labels":
                    DATASET_PATH.get_data_path("cure_test_bbox_pixel_labels"),
                "images":
                    DATASET_PATH.get_data_path("cure_test_images"),
                "mask_images":
                    DATASET_PATH.get_data_path("cure_test_mask_images"),
                "segmentation_labels":
                    DATASET_PATH.get_data_path("cure_test_segmentation_labels"),
                "yolo_labels":
                    DATASET_PATH.get_data_path("cure_test_yolo_labels"),
                "aug_images":
                    DATASET_PATH.get_data_path("cure_test_aug_images"),
                "aug_yolo_labels":
                    DATASET_PATH.get_data_path("cure_test_aug_yolo_labels"),
            },

            "src_stream_images": {
                "reference": {
                    "stream_images":
                        DATASET_PATH.get_data_path("stream_images_cure_reference"),
                    "stream_images_contour":
                        DATASET_PATH.get_data_path("stream_images_cure_reference_contour"),
                    "stream_images_lbp":
                        DATASET_PATH.get_data_path("stream_images_cure_reference_lbp"),
                    "stream_images_rgb":
                        DATASET_PATH.get_data_path("stream_images_cure_reference_rgb"),
                    "stream_images_texture":
                        DATASET_PATH.get_data_path("stream_images_cure_reference_texture"),
                },
                "customer": {
                    "stream_images":
                        DATASET_PATH.get_data_path("stream_images_cure_customer"),
                    "stream_images_contour":
                        DATASET_PATH.get_data_path("stream_images_cure_customer_contour"),
                    "stream_images_lbp":
                        DATASET_PATH.get_data_path("stream_images_cure_customer_lbp"),
                    "stream_images_rgb":
                        DATASET_PATH.get_data_path("stream_images_cure_customer_rgb"),
                    "stream_images_texture":
                        DATASET_PATH.get_data_path("stream_images_cure_customer_texture"),
                }
            },

            "dst_stream_images": {
                'stream_images_anchor':
                    IMAGES_PATH.get_data_path("stream_images_cure_anchor"),
                "stream_images_pos_neg":
                    IMAGES_PATH.get_data_path("stream_images_cure_pos_neg"),
                'ref':
                    IMAGES_PATH.get_data_path("test_ref_cure"),
                'query':
                    IMAGES_PATH.get_data_path("test_query_cure")
            },

            "other": {
                'k_fold':
                    DATA_PATH.get_data_path("cure_k_fold")
            },
        },
        # -------------------------------------------------- O G Y E I -------------------------------------------------
        "ogyei": {
            "unsplitted": {
                "images":
                    DATASET_PATH.get_data_path("ogyei_v2_unsplitted_images"),
                "mask_images":
                    DATASET_PATH.get_data_path("ogyei_v2_unsplitted_gt_masks"),
                "segmentation_labels":
                    DATASET_PATH.get_data_path("ogyei_v2_unsplitted_labels")
            },
            "train": {
                "bbox_pixel_labels":
                    DATASET_PATH.get_data_path("ogyei_v2_splitted_train_bbox_pixel_labels"),
                "images":
                    DATASET_PATH.get_data_path("ogyei_v2_splitted_train_images"),
                "mask_images":
                    DATASET_PATH.get_data_path("ogyei_v2_splitted_gt_train_masks"),
                "segmentation_labels":
                    DATASET_PATH.get_data_path("ogyei_v2_splitted_train_labels"),
                "yolo_labels":
                    DATASET_PATH.get_data_path("ogyei_v2_splitted_train_yolo_labels"),
                "aug_images":
                    DATASET_PATH.get_data_path("ogyei_v2_splitted_train_aug_images"),
                "aug_yolo_labels":
                    DATASET_PATH.get_data_path("ogyei_v2_splitted_train_aug_yolo_labels"),
                "aug_mask_images":
                    DATASET_PATH.get_data_path("ogyei_v2_splitted_train_aug_mask_images"),
            },
            "valid": {
                "bbox_pixel_labels":
                    DATASET_PATH.get_data_path("ogyei_v2_splitted_valid_bbox_pixel_labels"),
                "images":
                    DATASET_PATH.get_data_path("ogyei_v2_splitted_valid_images"),
                "mask_images":
                    DATASET_PATH.get_data_path("ogyei_v2_splitted_gt_valid_masks"),
                "segmentation_labels":
                    DATASET_PATH.get_data_path("ogyei_v2_splitted_valid_labels"),
                "yolo_labels":
                    DATASET_PATH.get_data_path("ogyei_v2_splitted_valid_yolo_labels"),
                "aug_images":
                    DATASET_PATH.get_data_path("ogyei_v2_splitted_valid_aug_images"),
                "aug_yolo_labels":
                    DATASET_PATH.get_data_path("ogyei_v2_splitted_valid_aug_yolo_labels"),
                "aug_mask_images":
                    DATASET_PATH.get_data_path("ogyei_v2_splitted_valid_aug_mask_images"),
            },
            "test": {
                "bbox_pixel_labels":
                    DATASET_PATH.get_data_path("ogyei_v2_splitted_test_bbox_pixel_labels"),
                "images":
                    DATASET_PATH.get_data_path("ogyei_v2_splitted_test_images"),
                "mask_images":
                    DATASET_PATH.get_data_path("ogyei_v2_splitted_gt_test_masks"),
                "segmentation_labels":
                    DATASET_PATH.get_data_path("ogyei_v2_splitted_test_labels"),
                "yolo_labels":
                    DATASET_PATH.get_data_path("ogyei_v2_splitted_test_yolo_labels"),
                "aug_images":
                    DATASET_PATH.get_data_path("ogyei_v2_splitted_test_aug_images"),
                "aug_yolo_labels":
                    DATASET_PATH.get_data_path("ogyei_v2_splitted_test_aug_yolo_labels"),
                "aug_mask_images":
                    DATASET_PATH.get_data_path("ogyei_v2_splitted_test_aug_mask_images"),
            },
            "other": {
                'k_fold':
                    DATA_PATH.get_data_path("ogye_v2_k_fold"),
                'stream_images':
                    IMAGES_PATH.get_data_path("stream_images_ogyei"),
                'stream_test_images':
                    IMAGES_PATH.get_data_path("stream_images_ogyei_test"),
                'ref':
                    IMAGES_PATH.get_data_path("test_ref_ogyei"),
                'query':
                    IMAGES_PATH.get_data_path("test_query_ogyei")
            }
        },

        # ---------------------------------------------------- N I H ---------------------------------------------------
        "nih": {
            "customer": {
                "customer_images":
                    DATASET_PATH.get_data_path("nih_customer_images"),
                "customer_csv":
                    DATASET_PATH.get_data_path("nih_customer_csv"),
                "customer_xlsx":
                    DATASET_PATH.get_data_path("nih_customer_xlsx"),
                "customer_txt":
                    DATASET_PATH.get_data_path("nih_customer_txt")
            },

            "reference": {
                "reference_images":
                    DATASET_PATH.get_data_path("nih_reference_images"),
                "reference_masks":
                    DATASET_PATH.get_data_path("nih_reference_masks"),
                "reference_labels":
                    DATASET_PATH.get_data_path("nih_reference_labels"),
                "reference_csv":
                    DATASET_PATH.get_data_path("nih_reference_csv"),
                "reference_xlsx":
                    DATASET_PATH.get_data_path("nih_reference_xlsx"),
                "reference_txt":
                    DATASET_PATH.get_data_path("nih_reference_txt")
            },

            # "train": {
            #     "images": DATASET_PATH.get_data_path(""),
            #     "masks": DATASET_PATH.get_data_path(""),
            #
            # },
            # "valid": {
            #     "images": DATASET_PATH.get_data_path(""),
            #     "masks": DATASET_PATH.get_data_path(""),
            #
            # },
            # "test": {
            #     "images": DATASET_PATH.get_data_path(""),
            #     "masks": IMAGES_PATH.get_data_path(""),
            # },
            "other": {
                "ref": DATASET_PATH.get_data_path("nih_ref_images"),
                "query": DATASET_PATH.get_data_path("nih_query_images"),
                "xlsx": DATASET_PATH.get_data_path("nih_xlsx")
            }
        },

        # ---------------------------------------------------- D T D ---------------------------------------------------
        "dtd": {
            "dataset_path": DATASET_PATH.get_data_path("dtd_images")
        }
    }

    return path_to_images[dataset_name]
