import sys
sys.path.append('../open3d-manage')

import os
from tqdm import tqdm
from time import time

from open3d_manage.Method.trans import toPLYFile, toPCDFile, toGaussNoisePCDFile

from poisson_recon.Module.poisson_reconstructor import PoissonReconstructor
from poisson_recon.Module.poisson_params_sampler import PoissonParamsSampler

def toNoisePCD():
    geometry_file_path = "/Users/fufu/Downloads/Airplane without texture.stl/Airplane without texture.stl"
    geometry_type = "mesh"
    ply_file_path = "../output_noise_pcd/airplane.ply"

    sample_point_num = 1000000
    pcd_file_path = "../output_noise_pcd/airplane_pcd.ply"

    gauss_noise_params_list = [[0.1, 0.1], [1.0, 1.0], [10.0, 10.0], [100.0, 100.0]]
    save_gauss_noise_pcd_folder_path = '../output_noise_pcd/'

    overwrite = False
    print_progress = True

    toPLYFile(
        geometry_file_path, geometry_type, ply_file_path, overwrite, print_progress
    )

    toPCDFile(
        ply_file_path,
        geometry_type,
        sample_point_num,
        pcd_file_path,
        overwrite,
        print_progress,
    )

    for gauss_noise_params in gauss_noise_params_list:
        gauss_mean, gauss_sigma = gauss_noise_params

        gauss_noise_pcd_file_basename = "airplane_gaussMean-" + str(gauss_mean) + "_gaussSigma-" + str(gauss_sigma)

        gauss_noise_pcd_file_path = save_gauss_noise_pcd_folder_path + gauss_noise_pcd_file_basename + "_pcd.ply"

        toGaussNoisePCDFile(
            pcd_file_path,
            gauss_mean,
            gauss_sigma,
            gauss_noise_pcd_file_path,
            overwrite,
            print_progress,
        )

    return True

def toMesh():
    noise_pcd_folder_path = '../output_noise_pcd/'
    save_poisson_recon_folder_path = '../output_mesh/spsr/'
    degree_range = [1, 2, 3, 4, 5, 6, 7, 8]
    bType_range = [1, 2, 3]
    depth_range = [5, 6, 7, 8, 9, 10, 11, 12]
    scale_range = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
    samplesPerNode_range = [1.0, 1.5, 3.0, 5.0, 10.0, 15.0, 20.0]
    pointWeight_range = [1, 2, 3, 4, 5, 6]
    iters_range = [5, 6, 7, 8, 9, 10]
    confidence_range = [0, 0.1, 0.2, 0.4, 0.8, 1.0]
    confidenceBias_range = [0, 0.1, 0.2, 0.3, 0.4]
    primalGrid_range = [True, False]
    linearFit_range = [True, False]
    polygonMesh_range = [True, False]
    sample_one_only = True

    overwrite = False
    print_progress = True

    poisson_params_sampler = PoissonParamsSampler(
        degree_range,
        bType_range,
        depth_range,
        scale_range,
        samplesPerNode_range,
        pointWeight_range,
        iters_range,
        confidence_range,
        confidenceBias_range,
        primalGrid_range,
        linearFit_range,
        polygonMesh_range,
        sample_one_only,
        print_progress
    )

    params_num = poisson_params_sampler.size()

    noise_pcd_filename_list = os.listdir(noise_pcd_folder_path)

    for noise_pcd_filename in noise_pcd_filename_list:
        if noise_pcd_filename[-8:] != '_pcd.ply':
            continue

        noise_pcd_file_path = noise_pcd_folder_path + noise_pcd_filename
        noise_pcd_file_basename = noise_pcd_filename[:-8]

        poisson_recon_file_path = save_poisson_recon_folder_path + noise_pcd_file_basename + '/spsr.ply'

        for i in tqdm(range(params_num)):
            sample_params = poisson_params_sampler.sampleParams(i)
            poisson_reconstructor = PoissonReconstructor(sample_params)
            poisson_reconstructor.reconMeshFile(noise_pcd_file_path, poisson_recon_file_path, overwrite, print_progress)

    return True

def test():
    toNoisePCD()
    toMesh()
    return True
