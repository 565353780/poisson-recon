import open3d as o3d

from poisson_recon.Metric.chamfer import getPCDChamferDistance

def toMetricDict(eval_pcd: o3d.geometry.PointCloud, gt_pcd: o3d.geometry.PointCloud) -> dict:
    chamfer_distance = getPCDChamferDistance(eval_pcd, gt_pcd)

    metric_dict = {
        'chamfer': chamfer_distance,
    }

    return metric_dict
