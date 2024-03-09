import sys
sys.path.append('../open3d-manage/')

from time import time

from open3d_manage.Method.io import loadGeometry
from open3d_manage.Method.trans import toPLYFile, toPCDFile, toGaussNoisePCDFile
from open3d_manage.Method.render import renderGeometries

from poisson_recon.Module.poisson_reconstructor import PoissonReconstructor

def test():
    geometry_file_path = "/Users/fufu/Downloads/Airplane without texture.stl/Airplane without texture.stl"
    geometry_type = "mesh"
    ply_file_path = "../output_noise_pcd/airplane.ply"

    sample_point_num = 1000000
    pcd_file_path = "../output_noise_pcd/airplane_pcd.ply"

    gauss_mean = 100.0
    gauss_sigma = 100.0
    save_gauss_noise_pcd_folder_path = '../output_noise_pcd/'

    save_poisson_recon_folder_path = '../output_mesh/'

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

    for noise_params in [[0.1, 0.1], [1.0, 1.0], [10.0, 10.0], [100.0, 100.0]]:
        gauss_mean, gauss_sigma = noise_params

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

        poisson_recon_file_path = save_poisson_recon_folder_path + gauss_noise_pcd_file_basename + '.ply'

        poisson_reconstructor = PoissonReconstructor()
        print('start recon:', gauss_noise_pcd_file_basename, '...')
        start = time()
        poisson_reconstructor.reconMeshFile(gauss_noise_pcd_file_path, poisson_recon_file_path, overwrite, print_progress)
        print('time spend:', time() - start)

    return True
