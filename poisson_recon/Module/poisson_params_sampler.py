from tqdm import tqdm
from typing import Union
from itertools import product

from poisson_recon.Data.poisson_params import PoissonParams

class PoissonParamsSampler(object):
    def __init__(self,
                 degree_range: list=[1, 2, 3, 4, 5, 6, 7, 8],
                 bType_range: list=[1, 2, 3],
                 depth_range: list=[5, 6, 7, 8, 9, 10, 11, 12],
                 scale_range: list=[1.0, 1.1, 1.2, 1.3, 1.4, 1.5],
                 samplesPerNode_range: list=[1.0, 1.5, 3.0, 5.0, 10.0, 15.0, 20.0],
                 pointWeight_range: list=[1, 2, 3, 4, 5, 6],
                 iters_range: list=[5, 6, 7, 8, 9, 10],
                 confidence_range: list=[0, 0.1, 0.2, 0.4, 0.8, 1.0],
                 confidenceBias_range: list=[0, 0.1, 0.2, 0.3, 0.4],
                 primalGrid_range: list=[True, False],
                 linearFit_range: list=[True, False],
                 polygonMesh_range: list=[True, False],
                 print_progress: bool=False
                 ) -> None:
        self.degree_range = degree_range
        self.bType_range = bType_range
        self.depth_range = depth_range
        self.scale_range = scale_range
        self.samplesPerNode_range = samplesPerNode_range
        self.pointWeight_range = pointWeight_range
        self.iters_range = iters_range
        self.confidence_range = confidence_range
        self.confidenceBias_range = confidenceBias_range
        self.primalGrid_range = primalGrid_range
        self.linearFit_range = linearFit_range
        self.polygonMesh_range = polygonMesh_range

        self.sample_params_list = []

        self.updateParamsIdxs(print_progress)
        return

    def updateParamsIdxs(self, print_progress: bool=False) -> bool:
        self.sample_params_list = []

        loop_val = [self.degree_range, self.bType_range, self.depth_range,  self.scale_range,
                    self.samplesPerNode_range, self.pointWeight_range, self.iters_range,
                    self.confidence_range, self.confidenceBias_range, self.primalGrid_range,
                    self.linearFit_range, self.polygonMesh_range]

        total_num = 1
        for data_range in loop_val:
            total_num *= len(data_range)

        for_data = product(*loop_val)
        if print_progress:
            print('[INFO][PoissonParamsSampler::updateParamsIdxs]')
            print('\t start update sample params...')
            for_data = tqdm(for_data, total=total_num)
        for sample_params_values in for_data:
            self.sample_params_list.append(list(sample_params_values))
        return True

    def size(self) -> int:
        return len(self.sample_params_list)

    def sampleParams(self, sample_params_idx: int) -> Union[PoissonParams, None]:
        if sample_params_idx < 0 or sample_params_idx >= self.size():
            print('[ERROR][PoissonParamsSampler::sampleParams]')
            print('\t sample params idx out of range!')
            print('\t sample_params_idx:', sample_params_idx)
            print('\t size:', self.size())
            return None

        sample_params_values = self.sample_params_list[sample_params_idx]

        sample_params = PoissonParams(*sample_params_values)

        return sample_params
