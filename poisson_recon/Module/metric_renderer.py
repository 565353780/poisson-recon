import os
import json
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from typing import Union

class MetricRenderer(object):
    def __init__(self) -> None:
        return

    def toJsonFileNum(self, metric_file_name_list: list) -> int:
        json_file_num = 0

        for metric_file_name in metric_file_name_list:
            if metric_file_name[-5:] != '.json':
                continue
            json_file_num += 1

        return json_file_num

    def toParamNameList(self, metric_file_name_list: list) -> Union[list, None]:
        param_name_list = []

        for metric_file_name in metric_file_name_list:
            if metric_file_name[-5:] != '.json':
                continue

            param_list = metric_file_name_list[0].split('.json')[0].split('_')

            for param in param_list:
                if '-' not in param:
                    continue

                param_name = param.split('-')[0]
                param_name_list.append(param_name)

            return param_name_list

        print('[ERROR][MetricRenderer::toParamNameList]')
        print('\t json file not found!')
        return None

    def toParamMetricValues(self, metric_folder_path: str, metric_file_name_list: list, param_name_list: list, metric_num: int, metric_names: list, print_progress: bool=False) -> np.ndarray:
        json_file_num = self.toJsonFileNum(metric_file_name_list)

        param_metric_values = np.ones([json_file_num, len(param_name_list) + metric_num], dtype=float) * -1.0

        current_row_idx = 0
        for_data = metric_file_name_list
        if print_progress:
            print('[INFO][MetricRenderer::renderMetricFolder]')
            print('\t start collect metric data...')
            for_data = tqdm(for_data)
        for metric_file_name in for_data:
            if metric_file_name[-5:] != '.json':
                continue

            param_str = metric_file_name.split('.json')[0]

            for i in range(len(param_name_list)):
                param_value = param_str.split(param_name_list[i] + '-')[1].split('_')[0]
                param_metric_values[current_row_idx, i] = param_value

            with open(metric_folder_path + metric_file_name, 'r') as f:
                metric_dict = json.load(f)

            for i in range(metric_num):
                param_metric_values[current_row_idx, len(param_name_list) + i] = metric_dict[metric_names[i]]

            current_row_idx += 1

        return param_metric_values

    def renderMetricFolder(self, metric_folder_path: str, print_progress: bool=False) -> bool:
        metric_num = 1
        metric_names = ['chamfer']

        if not os.path.exists(metric_folder_path):
            print('[ERROR][MetricRenderer::renderMetricFolder]')
            print('\t metric folder not exist!')
            print('\t metric_folder_path:', metric_folder_path)
            return False

        metric_file_name_list = os.listdir(metric_folder_path)


        param_name_list = self.toParamNameList(metric_file_name_list)

        if param_name_list is None:
            print('[ERROR][MetricRenderer::renderMetricFolder]')
            print('\t toParamNameList failed!')
            return False

        param_metric_values = self.toParamMetricValues(metric_folder_path, metric_file_name_list, param_name_list, metric_num, metric_names, print_progress)

        print(param_metric_values)
        print(param_metric_values.shape)
        return True
