#pragma once

#include "poisson_params.h"
#include <string>
#include <vector>

class PoissonReconstructor {
public:
  PoissonReconstructor(){};

  PoissonReconstructor(const PoissonParams &poisson_params) {
    poisson_params_ = poisson_params;
  };

  const bool
  updateParams(const int &degree = 1, const int &bType = 3,
               const int &depth = 8, const float &scale = 1.1,
               const float &samplesPerNode = 1.5, const float &pointWeight = -1,
               const int &iters = 8, const float &confidence = 0,
               const float &confidenceBias = 0, const bool &primalGrid = false,
               const bool &linearFit = false, const bool &polygonMesh = false);

  const bool estimateNormal(const std::string &pcd_file_path,
                            const std::string &save_pcd_file_path,
                            const bool &overwrite = false);

  const bool reconMeshFile(const std::string &pcd_file_path,
                           const std::string &save_mesh_file_path,
                           const bool &overwrite = false);

  const bool reconMesh(
      const std::string &save_mesh_folder_path = "../../poisson-recon/output/");

  const int getSavedMeshNum();
  const std::vector<float> getVertices(const int &mesh_idx = -1);
  const std::vector<float> getFaces(const int &mesh_idx = -1);

private:
  const int toValidMeshIdxs(const int &mesh_idx);

private:
  PoissonParams poisson_params_;
  std::vector<std::string> saved_mesh_file_path_vec_;
};
