import sys
sys.path.append('../open3d-manage')

from poisson_recon.Module.evaluator import Evaluator

def demo():
    eval_mesh_folder_path = '../output_mesh/spsr/airplane_gaussMean-10.0_gaussSigma-10.0/'
    gt_pcd_file_path = '../output_noise_pcd/airplane_pcd.ply'
    save_metric_folder_path = '../output_metric/spsr/airplane_gaussMean-10.0_gaussSigma-10.0/'
    print_progress = True

    evaluator = Evaluator()
    metric_dict = evaluator.evalMeshFiles(eval_mesh_folder_path, gt_pcd_file_path, save_metric_folder_path, print_progress)

    assert metric_dict is not None

    for key, value in metric_dict.items():
        print(key)
        print(value)
    return True

def demo_folder():
    eval_mesh_root_folder_path = '../output_mesh/spsr/'
    gt_pcd_file_path = '../output_noise_pcd/airplane_pcd.ply'
    save_metric_root_folder_path = '../output_metric/spsr/'
    print_progress = True

    evaluator = Evaluator()
    metric_dict = evaluator.evalMeshFolders(eval_mesh_root_folder_path, gt_pcd_file_path, save_metric_root_folder_path, print_progress)

    assert metric_dict is not None

    for key, value in metric_dict.items():
        print(key)
        for subkey, subvalue in value.items():
            print(subkey)
            print(subvalue)
    return True
