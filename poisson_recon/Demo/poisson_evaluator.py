import sys
sys.path.append('../open3d-manage')

from poisson_recon.Module.poisson_evaluator import PoissonEvaluator

def demo():
    eval_mesh_folder_path = '../output_mesh/'
    gt_pcd_file_path = '../output_noise_pcd/airplane_pcd.ply'
    print_progress = True

    poisson_evaluator = PoissonEvaluator()
    chamfer_dict = poisson_evaluator.evalMeshFiles(eval_mesh_folder_path, gt_pcd_file_path, print_progress)

    for key, value in chamfer_dict.items():
        print(key)
        print(value)
    return True
