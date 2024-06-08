import os
import numpy as np
import open3d as o3d
from typing import Union

from poisson_recon.Data.poisson_params import PoissonParams
from poisson_recon.Method.cmd import runCMD
from poisson_recon.Method.time import getCurrentTime
from poisson_recon.Method.path import createFileFolder, removeFile, renameFile


class PoissonReconstructor(object):
    def __init__(self, poisson_params: PoissonParams = PoissonParams()) -> None:
        self.poisson_params = poisson_params

        self.loaded_mesh_file_path = ""
        self.loaded_vertices_list = []
        self.loaded_faces_list = []
        return

    def updateParams(self,
                     degree: int=1,
                     bType: int=3,
                     depth: int=8,
                     scale: float=1.1,
                     samplesPerNode: float=1.5,
                     pointWeight: Union[float, None]=None,
                     iters: int=8,
                     confidence: float=0,
                     confidenceBias: float=0,
                     primalGrid: bool=False,
                     linearFit: bool=False,
                     polygonMesh: bool=False) -> bool:
        self.poisson_params.degree = degree
        self.poisson_params.bType = bType
        self.poisson_params.depth = depth
        self.poisson_params.scale = scale
        self.poisson_params.samplesPerNode = samplesPerNode
        self.poisson_params.pointWeight = pointWeight
        self.poisson_params.iters = iters
        self.poisson_params.confidence = confidence
        self.poisson_params.confidenceBias = confidenceBias
        self.poisson_params.primalGrid = primalGrid
        self.poisson_params.linearFit = linearFit
        self.poisson_params.polygonMesh = polygonMesh
        return True

    def estimateNormal(self, pcd_file_path: str, save_pcd_file_path: str) -> bool:
        if not os.path.exists(pcd_file_path):
            print("[ERROR][PoissonReconstructor::reconMeshFile]")
            print("\t pcd file not exist!")
            print("\t pcd_file_path:", pcd_file_path)
            return False

        createFileFolder(save_pcd_file_path)

        pcd = o3d.io.read_point_cloud(pcd_file_path)

        if not pcd.has_normals():
            pcd.estimate_normals()

        pcd.normalize_normals()
        o3d.io.write_point_cloud(save_pcd_file_path, pcd)

        return True

    def reconMeshFile(
        self,
        pcd_file_path: str,
        save_mesh_file_path: str,
        overwrite: bool = False,
        print_progress: bool = False,
    ) -> Union[str, None]:
        if not os.path.exists(pcd_file_path):
            print("[ERROR][PoissonReconstructor::reconMeshFile]")
            print("\t pcd file not exist!")
            print("\t pcd_file_path:", pcd_file_path)
            return None

        normal_pcd_file_path = "./output/normal_pcd.ply"

        self.estimateNormal(pcd_file_path, normal_pcd_file_path)

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
                return None

        createFileFolder(save_mesh_file_path)

        tmp_save_mesh_file_path = full_save_mesh_file_path[:-4] + "_tmp.ply"

        cmd = (
            "../PoissonRecon/Bin/Linux/PoissonRecon"
            + " --in "
            + normal_pcd_file_path
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
            return None

        if not os.path.exists(tmp_save_mesh_file_path):
            print("[ERROR][PoissonReconstructor::reconMeshFile]")
            print("\t mesh file save failed!")
            print("\t save_mesh_file_path:", save_mesh_file_path)
            return None

        renameFile(tmp_save_mesh_file_path, full_save_mesh_file_path)
        return full_save_mesh_file_path

    def reconMeshFileFromPoints(self,
                                points: Union[np.ndarray, list],
                                save_mesh_file_path: str,
                                overwrite: bool=False,
                                print_progress: bool = False) -> Union[str, None]:
        if isinstance(points, list):
            points = np.array(points)

        is_flatten = len(points.shape) == 1
        if is_flatten:
            points = points.reshape(-1, 3)

        tmp_pcd_file_path = './output/tmp_pcd_generated_by_poisson_recon.ply'
        createFileFolder(tmp_pcd_file_path)
        
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        o3d.io.write_point_cloud(tmp_pcd_file_path, pcd, write_ascii=True)

        return self.reconMeshFile(tmp_pcd_file_path, save_mesh_file_path, overwrite, print_progress)


    def autoReconMeshFileFromPointsList(self,
                                        points: list,
                                        save_mesh_folder_path: str,
                                        overwrite: bool=False,
                                        print_progress: bool=False) -> str:
        if save_mesh_folder_path[-1] != '/':
            save_mesh_folder_path += '/'

        save_mesh_file_path = save_mesh_folder_path + getCurrentTime() + '_poisson_recon.ply'

        final_save_mesh_file_path = self.reconMeshFileFromPoints(points,
                                                                 save_mesh_file_path,
                                                                 overwrite,
                                                                 print_progress)
        if final_save_mesh_file_path is None:
            return ""

        return final_save_mesh_file_path

    def loadReconMeshFile(self, mesh_file_path: str) -> bool:
        if self.loaded_mesh_file_path == mesh_file_path:
            return True

        self.loaded_mesh_file_path = ""
        self.loaded_vertices_list = []
        self.loaded_faces_list = []

        if not os.path.exists(mesh_file_path):
            print('[ERROR][PoissonReconstructor::loadReconMeshFile]')
            print('\t mesh file not exist!')
            return False

        mesh = o3d.io.read_triangle_mesh(mesh_file_path)
        self.loaded_vertices_list = np.asarray(mesh.vertices).reshape(-1).tolist()
        self.loaded_faces_list = np.asarray(mesh.triangles).reshape(-1).tolist()
        return True

    def getLoadedVerticesList(self) -> list:
        return self.loaded_vertices_list

    def getLoadedFacesList(self) -> list:
        return self.loaded_faces_list
