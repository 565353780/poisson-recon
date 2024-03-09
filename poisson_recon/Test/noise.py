import sys
sys.path.append('../open3d-manage/')

import os
from time import time

from open3d_manage.Method.io import loadGeometry
from open3d_manage.Method.trans import toPLYFile, toPCDFile, toGaussNoisePCDFile
from open3d_manage.Method.render import renderGeometries

from poisson_recon.Module.poisson_reconstructor import PoissonReconstructor

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
    save_poisson_recon_folder_path = '../output_mesh/'
    overwrite = False
    print_progress = True

    noise_pcd_filename_list = os.listdir(noise_pcd_folder_path)

    for noise_pcd_filename in noise_pcd_filename_list:
        if noise_pcd_filename[-8:] != '_pcd.ply':
            continue

        noise_pcd_file_path = noise_pcd_folder_path + noise_pcd_filename
        noise_pcd_file_basename = noise_pcd_filename[:-8]

        poisson_recon_file_path = save_poisson_recon_folder_path + noise_pcd_file_basename + '.ply'

        poisson_reconstructor = PoissonReconstructor()
        print('start recon:', noise_pcd_file_basename, '...')
        start = time()
        poisson_reconstructor.reconMeshFile(noise_pcd_file_path, poisson_recon_file_path, overwrite, print_progress)
        print('time spend:', time() - start)

    return True

def test():
    toNoisePCD()
    toMesh()
    return True
