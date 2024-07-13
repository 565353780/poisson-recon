#include "poisson_reconstructor.h"
#include "cmd.h"
#include "normal.h"
#include <filesystem>
#include <iostream>
#include <open3d/Open3D.h>
#include <string>

const bool PoissonReconstructor::clear() {
  if (std::filesystem::exists("./output/normal_pcd.ply")) {
    std::filesystem::remove("./output/normal_pcd.ply");
  }

  for (size_t i = 0; i < saved_mesh_file_path_vec_.size(); ++i) {
    const std::string &mesh_file_path = saved_mesh_file_path_vec_[i];

    if (std::filesystem::exists(mesh_file_path)) {
      std::filesystem::remove(mesh_file_path);
    }
  }

  saved_mesh_file_path_vec_.clear();
  loaded_mesh_file_path_ = "";
  loaded_vertices_.clear();
  loaded_faces_.clear();

  return true;
}

const bool PoissonReconstructor::isValid() {
  if (poisson_recon_bin_file_path_ == "") {
    return false;
  }

  return true;
}

const bool PoissonReconstructor::setPoissonReconFolderPath(
    const std::string &poisson_recon_folder_path) {
  poisson_recon_bin_file_path_ = "";

  if (!std::filesystem::exists(poisson_recon_folder_path)) {
    std::cout << "[ERROR][PoissonReconstructor::setPoissonReconFolderPath]"
              << std::endl;
    std::cout << "\t poisson recon bin folder not exist!" << std::endl;
    std::cout << "\t poisson_recon_folder_path: " << poisson_recon_folder_path
              << std::endl;

    return false;
  }

  const std::string poisson_recon_bin_file_path_linux =
      poisson_recon_folder_path + "Bin/Linux/PoissonRecon";

  if (std::filesystem::exists(poisson_recon_bin_file_path_linux)) {
    poisson_recon_bin_file_path_ = poisson_recon_bin_file_path_linux;

    return true;
  }

  std::cout << "[ERROR][PoissonReconstructor::setPoissonReconFolderPath]"
            << std::endl;
  std::cout << "\t poisson recon bin file for linux not exist!" << std::endl;
  std::cout << "\t poisson_recon_bin_file_path_linux: "
            << poisson_recon_bin_file_path_linux << std::endl;

  return false;
}

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

  const std::string full_save_mesh_file_basepath =
      save_mesh_file_path.substr(0, save_mesh_file_path.length() - 4) +
      poisson_params_.toLogStr();

  std::string full_save_mesh_file_path;

  int save_mesh_idx = 0;

  while (true) {
    full_save_mesh_file_path = full_save_mesh_file_basepath + "_" +
                               std::to_string(save_mesh_idx) + ".ply";

    if (std::filesystem::exists(full_save_mesh_file_path)) {
      ++save_mesh_idx;
      continue;
    }

    break;
  }

  const std::string tmp_save_mesh_file_path =
      full_save_mesh_file_path.substr(0,
                                      full_save_mesh_file_path.length() - 4) +
      "_tmp.ply";

  if (std::filesystem::exists(tmp_save_mesh_file_path)) {
    std::filesystem::remove(tmp_save_mesh_file_path);
  }

  std::string command = poisson_recon_bin_file_path_ + " --in " +
                        normal_pcd_file_path + " --out " +
                        tmp_save_mesh_file_path + poisson_params_.toCMDStr();

  std::cout << "[INFO][PoissonReconstructor::reconMeshFile]" << std::endl;
  std::cout << "\t start recon mesh from points by PoissonRecon..."
            << std::endl;
  if (!runCMD(command)) {
    std::cout << "[ERROR][PoissonReconstructor::reconMeshFile]" << std::endl;
    std::cout << "\t runCMD failed!" << std::endl;

    return false;
  }

  if (!std::filesystem::exists(tmp_save_mesh_file_path)) {
    std::cout << "[ERROR][PoissonReconstructor::reconMeshFile]" << std::endl;
    std::cout << "\t mesh file save failed!" << std::endl;
    std::cout << "\t save_mesh_file_path: " << tmp_save_mesh_file_path
              << std::endl;

    return false;
  }

  try {
    std::filesystem::rename(tmp_save_mesh_file_path, full_save_mesh_file_path);
  } catch (const std::filesystem::filesystem_error &e) {
    std::cout << "[ERROR][PoissonReconstructor::reconMeshFile]" << std::endl;
    std::cout << "\t rename mesh file failed!" << std::endl;
    std::cout << "\t error: " << e.what() << std::endl;

    return false;
  }

  saved_mesh_file_path_vec_.emplace_back(full_save_mesh_file_path);

  return true;
}

const int PoissonReconstructor::getSavedMeshNum() {
  return saved_mesh_file_path_vec_.size();
}

const std::string
PoissonReconstructor::getSavedMeshFilePath(const int &saved_mesh_idx) {
  const int valid_mesh_idx = toValidMeshIdxs(saved_mesh_idx);
  if (valid_mesh_idx == -1) {
    std::cout << "[ERROR][PoissonReconstructor::getSavedMeshFilePath]"
              << std::endl;
    std::cout << "\t toValidMeshIdxs failed!" << std::endl;

    return "";
  }

  return saved_mesh_file_path_vec_[valid_mesh_idx];
}

const std::vector<float>
PoissonReconstructor::getSavedMeshVertices(const int &saved_mesh_idx) {
  if (!loadMeshFile(saved_mesh_idx)) {
    std::cout << "[ERROR][PoissonReconstructor::getSavedMeshVertices]"
              << std::endl;
    std::cout << "\t loadMeshFile failed!" << std::endl;

    return std::vector<float>();
  }

  return loaded_vertices_;
}

const std::vector<int>
PoissonReconstructor::getSavedMeshFaces(const int &saved_mesh_idx) {
  if (!loadMeshFile(saved_mesh_idx)) {
    std::cout << "[ERROR][PoissonReconstructor::getSavedMeshFaces]"
              << std::endl;
    std::cout << "\t loadMeshFile failed!" << std::endl;

    return std::vector<int>();
  }

  return loaded_faces_;
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

const bool PoissonReconstructor::loadMeshFile(const int &mesh_idx) {
  const int valid_mesh_idx = toValidMeshIdxs(mesh_idx);
  if (valid_mesh_idx == -1) {
    std::cout << "[ERROR][PoissonReconstructor::loadMeshFile]" << std::endl;
    std::cout << "\t toValidMeshIdxs failed!" << std::endl;

    return false;
  }

  const std::string &mesh_file_path = saved_mesh_file_path_vec_[valid_mesh_idx];

  if (mesh_file_path == loaded_mesh_file_path_) {
    return true;
  }

  loaded_mesh_file_path_ = "";
  loaded_vertices_.clear();
  loaded_faces_.clear();

  open3d::geometry::TriangleMesh mesh;
  if (!open3d::io::ReadTriangleMesh(mesh_file_path, mesh)) {
    std::cout << "[ERROR][PoissonReconstructor::loadMeshFile]" << std::endl;
    std::cout << "\t ReadTriangleMesh failed!" << std::endl;
    std::cout << "\t mesh_file_path: " << mesh_file_path << std::endl;

    return false;
  }

  loaded_vertices_.reserve(mesh.vertices_.size() * 3);

  for (const Eigen::Vector3d &vertex : mesh.vertices_) {
    loaded_vertices_.emplace_back(static_cast<float>(vertex(0)));
    loaded_vertices_.emplace_back(static_cast<float>(vertex(1)));
    loaded_vertices_.emplace_back(static_cast<float>(vertex(2)));
  }

  loaded_faces_.reserve(mesh.triangles_.size() * 3);
  for (const Eigen::Vector3i &triangle : mesh.triangles_) {
    loaded_faces_.emplace_back(static_cast<int>(triangle(0)));
    loaded_faces_.emplace_back(static_cast<int>(triangle(1)));
    loaded_faces_.emplace_back(static_cast<int>(triangle(2)));
  }

  loaded_mesh_file_path_ = mesh_file_path;

  return true;
}
