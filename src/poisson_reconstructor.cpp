#include "poisson_reconstructor.h"
#include <filesystem>
#include <open3d/Open3D.h>

const bool PoissonReconstructor::updateParams(
    const int &degree, const int &bType, const int &depth, const float &scale,
    const float &samplesPerNode, const float &pointWeight, const int &iters,
    const float &confidence, const float &confidenceBias,
    const bool &primalGrid, const bool &linearFit, const bool &polygonMesh) {
  poisson_params_.degree = degree;
  poisson_params_.bType = bType;
  poisson_params_.depth = depth;
  poisson_params_.scale = scale;
  poisson_params_.samplesPerNode = samplesPerNode;
  poisson_params_.pointWeight = pointWeight;
  poisson_params_.iters = iters;
  poisson_params_.confidence = confidence;
  poisson_params_.confidenceBias = confidenceBias;
  poisson_params_.primalGrid = primalGrid;
  poisson_params_.linearFit = linearFit;
  poisson_params_.polygonMesh = polygonMesh;
  return true;
}

const bool
PoissonReconstructor::estimateNormal(const std::string &pcd_file_path,
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

  if (!open3d::io::WritePointCloud(save_pcd_file_path, *pcd)) {
    std::cout << "[ERROR][PoissonReconstructor::estimateNormal]" << std::endl;
    std::cout << "\t WritePointCloud failed!" << std::endl;
    std::cout << "\t save_pcd_file_path: " << save_pcd_file_path << std::endl;

    return false;
  }

  return true;
}

const bool
PoissonReconstructor::reconMeshFile(const std::string &pcd_file_path,
                                    const std::string &save_mesh_file_path,
                                    const bool &overwrite) {
  if (!std::filesystem::exists(pcd_file_path)) {
    std::cout << "[ERROR][PoissonReconstructor::reconMeshFile]" << std::endl;
    std::cout << "\t pcd file not exist!" << std::endl;
    std::cout << "\t pcd_file_path: " << pcd_file_path << std::endl;

    return false;
  }

  if (std::filesystem::exists(save_mesh_file_path)) {
    if (!overwrite) {
      std::cout << "[ERROR][PoissonReconstructor::reconMeshFile]" << std::endl;
      std::cout << "\t save mesh file already exist!" << std::endl;
      std::cout << "\t save_mesh_file_path: " << save_mesh_file_path
                << std::endl;

      return false;
    } else {
      std::filesystem::remove(save_mesh_file_path);
    }
  }

  const std::string normal_pcd_file_path = "./output/normal_pcd.ply";

  if (!estimateNormal(pcd_file_path, normal_pcd_file_path, true)) {
    std::cout << "[ERROR][PoissonReconstructor::reconMeshFile]" << std::endl;
    std::cout << "\t estimateNormal failed!" << std::endl;

    return false;
  }

  std::string full_save_mesh_file_path =
      save_mesh_file_path.substr(0, save_mesh_file_path.length() - 4) +
      poisson_params_.toLogStr() + ".ply";

  std::cout << save_mesh_file_path << std::endl;
  std::cout << full_save_mesh_file_path << std::endl;
  exit(0);

  return true;

  if (save_mesh_file_path == "") {
    return false;
  }

  saved_mesh_file_path_vec_.emplace_back(save_mesh_file_path);

  return true;
}

const int PoissonReconstructor::getSavedMeshNum() {
  return saved_mesh_file_path_vec_.size();
}

const int PoissonReconstructor::toValidMeshIdxs(const int &mesh_idx) {
  int valid_mesh_idx = mesh_idx;

  if (valid_mesh_idx < 0) {
    valid_mesh_idx += saved_mesh_file_path_vec_.size();
  }

  if (valid_mesh_idx >= saved_mesh_file_path_vec_.size()) {
    std::cout << "given mesh idx [" << valid_mesh_idx << "] out of range!"
              << std::endl;
    std::cout << "the valid range is [0 - "
              << saved_mesh_file_path_vec_.size() - 1 << "]" << std::endl;

    return -1;
  }

  return valid_mesh_idx;
}
