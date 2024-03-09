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

    def toMetricRenderDict(self, param_name_list: list, param_metric_values: np.ndarray, metric_num, metric_names) -> dict:
        metric_render_dict = {}

        for i in range(len(param_name_list)):
            current_render_dict = {}

            param_name = param_name_list[i]
            param_unit_value_list = list(set(param_metric_values[:, i].tolist()))
            current_render_dict['param_unit_value_list'] = param_unit_value_list

            for j in range(metric_num):
                current_metric_values_list = []

                for k in range(len(param_unit_value_list)):
                    metric_mask = param_metric_values[:, i] == param_unit_value_list[k]

                    current_metrics = param_metric_values[metric_mask, len(param_name_list) + j]

                    current_metric_values_list.append(current_metrics)

                current_render_dict[metric_names[j]] = current_metric_values_list

            metric_render_dict[param_name] = current_render_dict

        return metric_render_dict

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

        metric_render_dict = self.toMetricRenderDict(param_name_list,param_metric_values, metric_num, metric_names)

        for param_name, param_render_dict in metric_render_dict.items():
            x = param_render_dict['param_unit_value_list']
            for metric_name in metric_names:
                y = param_render_dict[metric_name]

                figure, axes = plt.subplots()
                axes.boxplot(y, labels=x, patch_artist=True, showfliers=False)
                plt.show()
        return True
