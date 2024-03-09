import numpy as np
import open3d as o3d

def getPCDChamferDistance(pcd1, pcd2):
    dists1 = np.array(pcd1.compute_point_cloud_distance(pcd2))
    dists2 = np.array(pcd2.compute_point_cloud_distance(pcd1))

    return np.mean(dists1) + np.mean(dists2)

def getChamferDistance(pts1:np.ndarray, pts2:np.ndarray):
    if pts1.shape[0] == 0 or pts2.shape[0] == 0:
        print('[WARN][chamfer_distance::getChamferDistance]')
        print('\t input pts contains empty set!')
        print('\t pts1.shape =', pts1.shape, ', pts2.shape =', pts2.shape)
        return 0

    pcd1 = o3d.geometry.PointCloud()
    pcd1.points = o3d.utility.Vector3dVector(pts1)
    pcd2 = o3d.geometry.PointCloud()
    pcd2.points = o3d.utility.Vector3dVector(pts2)

    return getPCDChamferDistance(pcd1, pcd2)
