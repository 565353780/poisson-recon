import os
import json
import numpy as np
from tqdm import tqdm
from typing import Union

from open3d_manage.Method.io import loadGeometry

from poisson_recon.Method.metric import toMetricDict

class PoissonEvaluator(object):
    def __init__(self) -> None:
        return

    def evalMeshFiles(self, mesh_folder_path: str, gt_pcd_file_path: str,
                      save_metric_folder_path: str, print_progress: bool=False) -> Union[dict, None]:
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

        os.makedirs(save_metric_folder_path, exist_ok=True)

        gt_pcd = loadGeometry(gt_pcd_file_path, 'pcd', print_progress)

        name_metric_dict = {}

        mesh_file_name_list = os.listdir(mesh_folder_path)

        for_data = mesh_file_name_list
        if print_progress:
            print('[INFO][PoissonEvaluator::evalMeshFiles]')
            print('\t start eval mesh files...')
            for_data = tqdm(for_data)
        for mesh_file_name in for_data:
            if mesh_file_name[-4:] != '.ply':
                continue

            save_metric_file_path = save_metric_folder_path + mesh_file_name[:-4] + '.json'

            if os.path.exists(save_metric_file_path):
                with open(save_metric_file_path, 'r') as f:
                    metric_dict = json.load(f)
                    name_metric_dict[mesh_file_name] = metric_dict
                continue

            mesh_file_path = mesh_folder_path + mesh_file_name

            mesh = loadGeometry(mesh_file_path, 'mesh', print_progress)

            if np.asarray(mesh.vertices).shape[0] == 0:
                metric_dict = {
                    'chamfer': -1.0,
                }
                name_metric_dict[mesh_file_name] = metric_dict

                with open(save_metric_file_path, 'w') as f:
                    json.dump(metric_dict, f)
                continue

            pcd = mesh.sample_points_uniformly(np.asarray(gt_pcd.points).shape[0])

            metric_dict = toMetricDict(pcd, gt_pcd)

            name_metric_dict[mesh_file_name] = metric_dict

            with open(save_metric_file_path, 'w') as f:
                json.dump(metric_dict, f)

        return name_metric_dict

    def evalMeshFolders(self, mesh_root_folder_path: str, gt_pcd_file_path: str,
                        save_metric_root_folder_path: str, print_progress: bool=False) -> Union[dict, None]:
        if not os.path.exists(mesh_root_folder_path):
            print('[ERROR::PoissonEvaluator::evalMeshFolders]')
            print('\t mesh root folder not exist!')
            print('\t mesh_root_folder_path:', mesh_root_folder_path)
            return None

        if not os.path.exists(gt_pcd_file_path):
            print('[ERROR::PoissonEvaluator::evalMeshFiles]')
            print('\t gt pcd file not exist!')
            print('\t gt_pcd_file_path:', gt_pcd_file_path)
            return None

        mesh_folder_name_list = os.listdir(mesh_root_folder_path)

        name_metric_dict = {}

        for mesh_folder_name in mesh_folder_name_list:
            if print_progress:
                print('[INFO][PoissonEvaluator::evalMeshFolders]')
                print('\t start eval mesh folder:', mesh_folder_name, '...')

            mesh_folder_path = mesh_root_folder_path + mesh_folder_name + '/'

            if not os.path.isdir(mesh_folder_path):
                continue

            save_metric_folder_path = save_metric_root_folder_path + mesh_folder_name + '/'

            current_name_metric_dict = self.evalMeshFiles(mesh_folder_path, gt_pcd_file_path, save_metric_folder_path, print_progress)

            if current_name_metric_dict is None:
                print('[WARN][PoissonEvaluator::evalMeshFolders]')
                print('\t evalMeshFiles failed!')
                print('\t mesh_folder_name:', mesh_folder_name)
                continue

            name_metric_dict[mesh_folder_name] = current_name_metric_dict

        return name_metric_dict
