from time import time

from poisson_recon.Module.poisson_reconstructor import PoissonReconstructor


def demo():
    pcd_file_path = '../open3d-manage/output/airplane_gauss_noise_0.1_0.1_pcd.ply'
    save_mesh_file_path = '../output_mesh/airplane_gauss_noise_0.1_0.1.ply'
    overwrite = False
    print_progress = True

    poisson_reconstructor = PoissonReconstructor()
    start = time()
    poisson_reconstructor.reconMeshFile(pcd_file_path, save_mesh_file_path, overwrite, print_progress)
    print('time spend:', time() - start)
    return True
