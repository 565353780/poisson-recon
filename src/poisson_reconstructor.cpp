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
      std::filesystem::remove(save_mesh_file_path);
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

  const bool update_param_success =
      poisson_reconstructor_
          .attr("updateParams")(
              "degree"_a = degree, "bType"_a = bType, "depth"_a = depth,
              "scale"_a = scale, "samplesPerNode"_a = samplesPerNode,
              "pointWeight"_a = pointWeight, "iters"_a = iters,
              "confidence"_a = confidence, "confidenceBias"_a = confidenceBias,
              "primalGrid"_a = primalGrid, "linearFit"_a = linearFit,
              "polygonMesh"_a = polygonMesh)
          .cast<bool>();
  if (!update_param_success) {
    std::cout << "update params failed!" << std::endl;
    return false;
  }

  py::list point_list;
  for (int i = 0; i < points.size(); ++i) {
    point_list.append(points[i]);
  }

  const std::string save_mesh_file_path =
      poisson_reconstructor_
          .attr("autoReconMeshFileFromPointsList")(
              "points"_a = point_list,
              "save_mesh_folder_path"_a = save_mesh_folder_path,
              "overwrite"_a = true, "print_progress"_a = true)
          .cast<std::string>();

  if (save_mesh_file_path == "") {
    return false;
  }

  saved_mesh_file_path_vec_.emplace_back(save_mesh_file_path);

  return true;
}

const int PoissonReconstructor::getSavedMeshNum() {
  return saved_mesh_file_path_vec_.size();
}

const std::vector<float>
PoissonReconstructor::getVertices(const int &mesh_idx) {
  py::gil_scoped_acquire acquire;

  const int valid_mesh_idx = toValidMeshIdxs(mesh_idx);

  if (valid_mesh_idx < 0) {
    std::cout << "[ERROR][PoissonReconstructor::getVertices]" << std::endl;
    std::cout << "\t toValidMeshIdxs failed!" << std::endl;

    return std::vector<float>();
  }

  const bool load_mesh_success =
      poisson_reconstructor_
          .attr("loadReconMeshFile")(saved_mesh_file_path_vec_[valid_mesh_idx])
          .cast<bool>();
  if (!load_mesh_success) {
    std::cout << "load mesh failed!" << std::endl;

    return std::vector<float>();
  }

  py::list vertices_list =
      poisson_reconstructor_.attr("getLoadedVerticesList")();

  std::vector<float> vertices;
  vertices.reserve(vertices_list.size());

  for (int i = 0; i < vertices_list.size(); ++i) {
    vertices.emplace_back(vertices_list[i].cast<float>());
  }

  return vertices;
}

const std::vector<float> PoissonReconstructor::getFaces(const int &mesh_idx) {
  py::gil_scoped_acquire acquire;

  const int valid_mesh_idx = toValidMeshIdxs(mesh_idx);

  if (valid_mesh_idx < 0) {
    std::cout << "[ERROR][PoissonReconstructor::getFaces]" << std::endl;
    std::cout << "\t toValidMeshIdxs failed!" << std::endl;

    return std::vector<float>();
  }

  const bool load_mesh_success =
      poisson_reconstructor_
          .attr("loadReconMeshFile")(saved_mesh_file_path_vec_[valid_mesh_idx])
          .cast<bool>();
  if (!load_mesh_success) {
    std::cout << "load mesh failed!" << std::endl;

    return std::vector<float>();
  }

  py::list faces_list = poisson_reconstructor_.attr("getLoadedFacesList")();

  std::vector<float> faces;
  faces.reserve(faces_list.size());

  for (int i = 0; i < faces_list.size(); ++i) {
    faces.emplace_back(faces_list[i].cast<float>());
  }

  return faces;
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
