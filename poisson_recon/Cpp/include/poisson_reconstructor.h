#pragma once

#include <pybind11/embed.h>
#include <string>

namespace py = pybind11;

class __attribute__((visibility("default"))) PoissonReconstructor {
public:
  PoissonReconstructor(const std::string root_path = "../../poisson-recon/");
  ~PoissonReconstructor();

  const bool reconMesh(
      const std::vector<float> &points, const int &degree = 1,
      const int &bType = 3, const int &depth = 8, const float &scale = 1.1,
      const float &samplesPerNode = 1.5, const float &pointWeight = -1,
      const int &iters = 8, const float &confidence = 0,
      const float &confidenceBias = 0, const bool &primalGrid = false,
      const bool &linearFit = false, const bool &polygonMesh = false,
      const std::string &save_mesh_folder_path = "../../poisson-recon/output/");

  const int getSavedMeshNum();
  const std::vector<float> getVertices(const int &mesh_idx = -1);
  const std::vector<float> getFaces(const int &mesh_idx = -1);

private:
  const int toValidMeshIdxs(const int &mesh_idx);

private:
  py::scoped_interpreter guard_{};

  py::object poisson_reconstructor_;

  std::vector<std::string> saved_mesh_file_path_vec_;
};
