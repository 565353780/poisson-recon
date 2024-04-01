import os
import open3d as o3d

from poisson_recon.Data.poisson_params import PoissonParams
from poisson_recon.Method.cmd import runCMD
from poisson_recon.Method.path import createFileFolder, removeFile, renameFile


class PoissonReconstructor(object):
    def __init__(self, poisson_params: PoissonParams = PoissonParams()) -> None:
        self.poisson_params = poisson_params
        return

    def reconMeshFile(
        self,
        pcd_file_path: str,
        save_mesh_file_path: str,
        overwrite: bool = False,
        print_progress: bool = False,
    ) -> str:
        if not os.path.exists(pcd_file_path):
            print("[ERROR][PoissonReconstructor::reconMeshFile]")
            print("\t pcd file not exist!")
            print("\t pcd_file_path:", pcd_file_path)
            return False

        full_save_mesh_file_path = (
            save_mesh_file_path[:-4] + self.poisson_params.toLogStr() + ".ply"
        )

        if os.path.exists(full_save_mesh_file_path):
            if overwrite:
                removeFile(full_save_mesh_file_path)
            else:
                print("[ERROR][PoissonReconstructor::reconMeshFile]")
                print("\t full save mesh file already exist!")
                print("\t full_save_mesh_file_path:", full_save_mesh_file_path)
                return False

        createFileFolder(save_mesh_file_path)

        tmp_save_mesh_file_path = full_save_mesh_file_path[:-4] + "_tmp.ply"

        cmd = (
            "../PoissonRecon/Bin/Linux/PoissonRecon"
            + " --in "
            + pcd_file_path
            + " --out "
            + tmp_save_mesh_file_path
            + self.poisson_params.toCMDStr()
        )

        if print_progress:
            print("[INFO][PoissonReconstructor::reconMeshFile]")
            print("\t start PoissonRecon...")
            print("\t cmd:")
            print(cmd)
        if not runCMD(cmd):
            print("[ERROR][PoissonReconstructor::reconMeshFile]")
            print("\t runCMD failed!")
            print("\t cmd:", cmd)
            return False

        if not os.path.exists(tmp_save_mesh_file_path):
            print("[ERROR][PoissonReconstructor::reconMeshFile]")
            print("\t mesh file save failed!")
            print("\t save_mesh_file_path:", save_mesh_file_path)
            return False

        renameFile(tmp_save_mesh_file_path, full_save_mesh_file_path)
        return full_save_mesh_file_path

    def reconMesh(self, pcd: o3d.geometry.PointCloud) -> o3d.geometry.TriangleMesh:
        return
