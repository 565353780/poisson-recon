#include "normal_estimate.h"
#include "path.h"
#include <filesystem>
#include <iostream>
#include <open3d/Open3D.h>

const bool estimateNormal(const std::string &pcd_file_path,
                          const std::string &save_pcd_file_path,
                          const bool &overwrite) {
  if (!std::filesystem::exists(pcd_file_path)) {
    std::cout << "[ERROR][PoissonReconstructor::estimateNormal]" << std::endl;
    std::cout << "\t pcd file not exist!" << std::endl;
    std::cout << "\t pcd_file_path: " << pcd_file_path << std::endl;

    return false;
  }

  if (std::filesystem::exists(save_pcd_file_path)) {
    if (!overwrite) {
      std::cout << "[ERROR][PoissonReconstructor::estimateNormal]" << std::endl;
      std::cout << "\t save pcd file already exist!" << std::endl;
      std::cout << "\t save_pcd_file_path: " << save_pcd_file_path << std::endl;

      return false;
    } else {
      std::filesystem::remove(save_pcd_file_path);
    }
  }

  std::shared_ptr<open3d::geometry::PointCloud> pcd(
      new open3d::geometry::PointCloud);

  if (!open3d::io::ReadPointCloud(pcd_file_path, *pcd)) {
    std::cout << "[ERROR][PoissonReconstructor::estimateNormal]" << std::endl;
    std::cout << "\t ReadPointCloud failed!" << std::endl;
    std::cout << "\t pcd_file_path: " << pcd_file_path << std::endl;

    return false;
  }

  if (!pcd->HasNormals()) {
    std::cout << "[INFO][PoissonReconstructor::estimateNormal]" << std::endl;
    std::cout << "\t pcd does not have normals! start estimate for it..."
              << std::endl;
    pcd->EstimateNormals();
  }

  pcd->NormalizeNormals();

  if (!createFileFolder(save_pcd_file_path)) {
    std::cout << "[ERROR][PoissonReconstructor::estimateNormal]" << std::endl;
    std::cout << "\t createFileFolder failed!" << std::endl;

    return false;
  }

  if (!open3d::io::WritePointCloud(save_pcd_file_path, *pcd)) {
    std::cout << "[ERROR][PoissonReconstructor::estimateNormal]" << std::endl;
    std::cout << "\t WritePointCloud failed!" << std::endl;
    std::cout << "\t save_pcd_file_path: " << save_pcd_file_path << std::endl;

    return false;
  }

  return true;
}
