import os
import numpy as np
from tqdm import tqdm
from typing import Union

from open3d_manage.Method.io import loadGeometry

from poisson_recon.Metric.chamfer import getPCDChamferDistance

class PoissonEvaluator(object):
    def __init__(self) -> None:
        return

    def evalMeshFiles(self, mesh_folder_path: str, gt_pcd_file_path: str, print_progress: bool=False) -> Union[dict, None]:
        if not os.path.exists(mesh_folder_path):
            print('[ERROR::PoissonEvaluator::evalMeshFiles]')
            print('\t mesh folder not exist!')
            print('\t mesh_folder_path:', mesh_folder_path)
            return None

        if not os.path.exists(gt_pcd_file_path):
            print('[ERROR::PoissonEvaluator::evalMeshFiles]')
            print('\t gt pcd file not exist!')
            print('\t gt_pcd_file_path:', gt_pcd_file_path)
            return None

        gt_pcd = loadGeometry(gt_pcd_file_path, 'pcd', print_progress)

        name_chamfer_pairs = []

        mesh_file_name_list = os.listdir(mesh_folder_path)

        for_data = mesh_file_name_list
        if print_progress:
            print('[INFO][PoissonEvaluator::evalMeshFiles]')
            print('\t start eval mesh files...')
            for_data = tqdm(for_data)
        for mesh_file_name in for_data:
            if mesh_file_name[-4:] != '.ply':
                continue

            mesh_file_path = mesh_folder_path + mesh_file_name

            mesh = loadGeometry(mesh_file_path, 'mesh', print_progress)

            pcd = mesh.sample_points_uniformly(np.asarray(gt_pcd.points).shape[0])

            chamfer_distance = getPCDChamferDistance(pcd, gt_pcd)

            name_chamfer_pairs.append([mesh_file_name, chamfer_distance])

        sorted_name_chamfer_pairs = sorted(name_chamfer_pairs, key=lambda x: x[1])

        chamfer_dict = {}

        for name_chamfer_pair in sorted_name_chamfer_pairs:
            chamfer_dict[name_chamfer_pair[0]] = name_chamfer_pair[1]

        return chamfer_dict
