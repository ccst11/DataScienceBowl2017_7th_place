from collections import OrderedDict

# ------------------------------------------------------------------------------
# pipeline parameters
# ------------------------------------------------------------------------------

pipe = OrderedDict([
    ('n_patients', 0), # number of patients to process, 0 means all
# dataset origin and paths
    ('dataset_name', 'LUNA16'), # 'LUNA16' or 'dsb3'
    ('raw_data_dirs', {
        'LUNA16': '/media/niklas/qnap/DATA/LUNA16/0_raw_data/',
        'dsb3': '/media/niklas/qnap/DATA/dsb3/stage1/',
    }),
    ('write_basedir', '/media/niklas/qnap/PROJECTS/dsb3/data_pipeline/'),
# data splits
    ('random_seed', 17),
    ('tr_va_ho_split', [0.8, 0.2, 0]), # something like 0.15, 0.7, 0.15
# technical parameters
    ('n_CPUs', 10),
    ('GPU_ids', [0]),
    ('GPU_memory_fraction', 0.85),
])
# ------------------------------------------------------------------------------
# step parameters
# ------------------------------------------------------------------------------

resample_lungs = OrderedDict([
    ('new_spacing_zyx', [1, 1, 1]), # z, y, x
    ('HU_tissue_range', [-1000, 400]), # MIN_BOUND, MAX_BOUND [-1000, 400]
    ('data_type', 'int16'), # int16 or float32
    ('bounding_box_buffer_yx_px', [12, 12]), # y, x
    ('seg_max_shape_yx', [512, 512]), # y, x
    ('batch_size', 64), # 128 for new_spacing 0.5, 64 for new_spacing 1.0
    ('checkpoint_dir', './checkpoints/resample_lungs/lung_wings_segmentation'),
])

batch_size_factor = 2
gen_prob_maps = OrderedDict([
    # the following two parameters are critical for computation time and can be easily changed
    ('view_planes', 'zyx'), # a string consisting of 'y', 'x', 'z'
    ('view_angles', [0]), # per view_plane in degrees, for example, [0, 45, -45]
    # more technical parameters
    # valid shape numbers: 256, 304, 320, 352, 384, 400, 416, 448, 464, 480, 496, 512 (dividable by 16)
    ('image_shapes', [[304, 304], [320, 320], [352, 352], [384, 384], [400, 400], [416, 416],
                     [432, 432], [448, 448], [480, 480], [512, 512], [560, 560], [1024, 1024]]), # y, x
    ('batch_sizes',  [batch_size_factor*32, batch_size_factor*32, batch_size_factor*24, batch_size_factor*24, batch_size_factor*16, batch_size_factor*16, batch_size_factor*16, batch_size_factor*16, batch_size_factor*12, batch_size_factor*12, batch_size_factor*4, batch_size_factor*1]),
    ('data_type', 'uint8'), # uint8, int16 or float32
    ('image_shape_max_ratio', 0.95),
    ('checkpoint_dir', './checkpoints/gen_prob_maps/MSE_weighted100_96_stage2'),
])

gen_candidates = OrderedDict([
    ('n_candidates', 100),
    ('threshold_prob_map', 0.2),
    ('cube_shape', (32, 32, 32)), # ensure cube_edges are dividable by two -> improvement possible
])

interpolate_candidates = OrderedDict([
    ('n_candidates', 20),
    ('new_spacing_zyx', [0.5, 0.5, 0.5]), # y, x, z
    ('new_data_type', 'float32'),
    ('new_candidates_shape_zyx', [64, 64, 64]),
    ('crop_raw_scan_buffer', 10),
])

filter_candidates = OrderedDict([
    ('checkpoint_dir', './checkpoints/luna_candidate_level_mini/'),
])

gen_submission = OrderedDict([
    ('splitting', 'submission'), # 'validation' or 'submission' or 'holdout'
    ('checkpoint_dir', './checkpoints/test'),
    ('num_augmented_data', 15), # is batch size
    ('gpu_fraction', 0.85),
    ('is_training', True),
])

# ------------------------------------------------------------------------------
# nodule segmentation parameters
# ------------------------------------------------------------------------------

gen_nodule_masks = OrderedDict([
    ('ellipse_mode', False),
    ('reduced_mask_radius_fraction', 0.5),
    ('mask2pred_lower_radius_limit_px', 3),
    ('mask2pred_upper_radius_limit_px', 15),
    ('LUNA16_annotations_csv_path', '../dsb3a_assets/LIDC-annotations_2_nodule-seg_annotations/annotations_min+missing_LUNA16_patients.csv'),
    ('yx_buffer_px', 1),
    ('z_buffer_px', 2),
])

gen_nodule_seg = OrderedDict([
    ('records_extra_radius_buffer_px', 5),
    ('gen_records_num_channels', 1),
    ('gen_records_stride', 1),
    ('gen_records_crop_size', [128, 128]), # y,x
    ('ratio_nodule_nodule_free', 1.0),
    ('view_planes', 'yxz'), # 'y' enables y-plane as nodule view, 'yx' x- and y-plane,... (order is variable)
    ('view_angles', [0, 45]), # per view_plane (degree)
    ('num_negative_examples_per_nodule_free_patient_per_view_plane', 50),
# gen nodule segmentation lists
    ('data_extra_radius_buffer_px', 5),
    ('data_num_channels', 1),
    ('data_stride', 1),
    ('data_crop_size', [96, 96]), # y, x
    ('data_view_planes', 'yxz'), # 'y' enables y-plane as nodule view, 'yx' x- and y-plane, ... (order is variable)
    ('num_negative_examples_per_nodule_free_patient_per_view_plane', 40),
])

# ------------------------------------------------------------------------------
# Eval parameters
# ------------------------------------------------------------------------------

gen_candidates_eval = OrderedDict([
    ('max_n_candidates', 100),
    ('max_dist_fraction', 0.5),
    ('priority_threshold', 3), 
    ('sort_candidates_by', 'prob_sum_min_nodule_size'),
    ('all_patients', True)
])

gen_candidates_vis = OrderedDict([
    ('inspect_what', 'true_positives')
])