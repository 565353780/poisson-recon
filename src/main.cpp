#include "poisson_params.h"
#include "poisson_reconstructor.h"
#include <iostream>
#include <vector>

int main() {
  // super params
  const int degree = 1;
  const int bType = 3;
  const int depth = 8;
  const float scale = 1.1;
  const float samplesPerNode = 1.5;
  const float pointWeight = -1;
  const int iters = 8;
  const float confidence = 0;
  const float confidenceBias = 0;
  const bool primalGrid = false;
  const bool linearFit = false;
  const bool polygonMesh = false;

  const std::string pcd_file_path = "./output/pcd.ply";
  const std::string save_mesh_file_path = "./output/recon_poisson.ply";
  const bool overwrite = true;

  // input point cloud [x1, y1, z1, x2, y2, z2, ...]
  std::vector<float> points;
  points.resize(3000);
  for (int i = 0; i < 1000; ++i) {
    points[3 * i] = 1.0 * i;
    points[3 * i + 1] = 2.0 * i;
    points[3 * i + 2] = 3.0 * i;
  }

  // construct detector module
  PoissonParams poisson_params;
  poisson_params.degree = degree;
  poisson_params.bType = bType;
  poisson_params.depth = depth;
  poisson_params.scale = scale;
  poisson_params.samplesPerNode = samplesPerNode;
  poisson_params.pointWeight = pointWeight;
  poisson_params.iters = iters;
  poisson_params.confidence = confidence;
  poisson_params.confidenceBias = confidenceBias;
  poisson_params.primalGrid = primalGrid;
  poisson_params.linearFit = linearFit;
  poisson_params.polygonMesh = polygonMesh;

  // construct detector module
  PoissonReconstructor poisson_reconstructor(poisson_params);

  // reconstruct mesh from input point cloud
  const bool success = poisson_reconstructor.reconMeshFile(
      pcd_file_path, save_mesh_file_path, overwrite);
  if (!success) {
    std::cout << "reconMesh failed!" << std::endl;
    return -1;
  }

  // get reconstructed mesh data
  const int saved_mesh_num = poisson_reconstructor.getSavedMeshNum();

  std::cout << "saved mesh num: " << saved_mesh_num << std::endl;

  return 1;
}
