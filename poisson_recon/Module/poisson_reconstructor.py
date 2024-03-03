import os
import open3d as o3d

from poisson_recon.Method.cmd import runCMD
from poisson_recon.Method.path import removeFile, renameFile


class PoissonReconstructor(object):
    def __init__(self) -> None:
        return

    def reconMeshFile(self, pcd_file_path: str, save_mesh_file_path: str, overwrite: bool=False, print_progress: bool=False) -> bool:
        if not os.path.exists(pcd_file_path):
            print('[ERROR][PoissonReconstructor::reconMeshFile]')
            print('\t pcd file not exist!')
            print('\t pcd_file_path:', pcd_file_path)
            return False

        if os.path.exists(save_mesh_file_path):
            if overwrite:
                removeFile(save_mesh_file_path)
            else:
                print('[ERROR][PoissonReconstructor::reconMeshFile]')
                print('\t save mesh file already exist!')
                print('\t save_mesh_file_path:', save_mesh_file_path)
                return False

        tmp_save_mesh_file_path = save_mesh_file_path[:-4] + '_tmp.ply'

        cmd = '../PoissonRecon/Bin/Linux/PoissonRecon' + \
            ' --in ' + pcd_file_path + \
            ' --out ' + tmp_save_mesh_file_path

        if print_progress:
            print('[INFO][PoissonReconstructor::reconMeshFile]')
            print('\t start PoissonRecon...')
        if not runCMD(cmd):
            print('[ERROR][PoissonReconstructor::reconMeshFile]')
            print('\t runCMD failed!')
            print('\t cmd:', cmd)
            return False

        if not os.path.exists(tmp_save_mesh_file_path):
            print('[ERROR][PoissonReconstructor::reconMeshFile]')
            print('\t mesh file save failed!')
            print('\t save_mesh_file_path:', save_mesh_file_path)
            return False


        renameFile(tmp_save_mesh_file_path, save_mesh_file_path)
        return True

    def reconMesh(self, pcd: o3d.geometry.PointCloud) -> o3d.geometry.TriangleMesh:
        return
