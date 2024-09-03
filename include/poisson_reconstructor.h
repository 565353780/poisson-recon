#pragma once

#include "poisson_params.h"
#include <string>
#include <vector>

class PoissonReconstructor {
public:
  PoissonReconstructor(const std::string &poisson_recon_folder_path) {
    setPoissonReconFolderPath(poisson_recon_folder_path);
  };

  PoissonReconstructor(const std::string &poisson_recon_folder_path,
                       const PoissonParams &poisson_params) {
    setPoissonReconFolderPath(poisson_recon_folder_path);
    poisson_params_ = poisson_params;
  };

  const bool clear();

  const bool isValid();

  const bool
  setPoissonReconFolderPath(const std::string &poisson_recon_folder_path);

  const bool
  updateParams(const int &degree = 1, const int &bType = 3,
               const int &depth = 8, const float &scale = 1.1,
               const float &samplesPerNode = 1.5, const float &pointWeight = -1,
               const int &iters = 8, const float &confidence = 0,
               const float &confidenceBias = 0, const bool &primalGrid = false,
               const bool &linearFit = false, const bool &polygonMesh = false,
               const float &maxMemory = -1.0, const bool &performance = false,
               const bool &verbose = false);

  const bool reconMeshFile(const std::string &pcd_file_path,
                           const std::string &save_mesh_file_path,
                           const bool &overwrite = false,
                           const bool &rename_with_params = false);

  const bool reconMesh(
      const std::string &save_mesh_folder_path = "../../poisson-recon/output/");

  const int getSavedMeshNum();
  const std::string getSavedMeshFilePath(const int &saved_mesh_idx = -1);
  const std::vector<float> getSavedMeshVertices(const int &saved_mesh_idx = -1);
  const std::vector<int> getSavedMeshFaces(const int &saved_mesh_idx = -1);

private:
  const int toValidMeshIdxs(const int &mesh_idx);

  const bool loadMeshFile(const int &mesh_idx);

private:
  std::string poisson_recon_bin_file_path_ = "";

  PoissonParams poisson_params_;
  std::vector<std::string> saved_mesh_file_path_vec_;

  std::string loaded_mesh_file_path_ = "";
  std::vector<float> loaded_vertices_;
  std::vector<int> loaded_faces_;
};
