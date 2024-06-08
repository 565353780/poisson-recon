#include "poisson_reconstructor.h"
#include <iostream>
#include <vector>

using namespace pybind11::literals;

PoissonReconstructor::PoissonReconstructor(const std::string root_path) {
  py::gil_scoped_acquire acquire;

  py::object sys = py::module_::import("sys");

  sys.attr("path").attr("append")(root_path);

  py::object PoissonReconstructor =
      py::module_::import("poisson_recon.Module.poisson_reconstructor");

  poisson_reconstructor_ = PoissonReconstructor.attr("PoissonReconstructor")();

  return;
}

PoissonReconstructor::~PoissonReconstructor() {}

const bool PoissonReconstructor::reconMesh(
    const std::vector<float> &points, const int &degree, const int &bType,
    const int &depth, const float &scale, const float &samplesPerNode,
    const float &pointWeight, const int &iters, const float &confidence,
    const float &confidenceBias, const bool &primalGrid, const bool &linearFit,
    const bool &polygonMesh, const std::string &save_mesh_folder_path) {
  py::gil_scoped_acquire acquire;

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
