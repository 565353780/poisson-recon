#include "poisson_reconstructor.h"
#include <iostream>
#include <vector>

int main() {
  // super params
  const std::string root_path = "../../poisson-recon/";
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
  const std::string save_mesh_folder_path = "../../poisson-recon/output/";

  // input point cloud [x1, y1, z1, x2, y2, z2, ...]
  std::vector<float> points;
  points.resize(3000);
  for (int i = 0; i < 1000; ++i) {
    points[3 * i] = 1.0 * i;
    points[3 * i + 1] = 2.0 * i;
    points[3 * i + 2] = 3.0 * i;
  }

  // construct detector module
  PoissonReconstructor poisson_reconstructor(root_path);

  // reconstruct mesh from input point cloud
  const bool success = poisson_reconstructor.reconMesh(
      points, degree, bType, depth, scale, samplesPerNode, pointWeight, iters,
      confidence, confidenceBias, primalGrid, linearFit, polygonMesh,
      save_mesh_folder_path);
  if (!success) {
    std::cout << "reconMesh failed!" << std::endl;
    return -1;
  }

  // get reconstructed mesh data
  const int saved_mesh_num = poisson_reconstructor.getSavedMeshNum();
  const std::vector<float> vertices =
      poisson_reconstructor.getVertices(saved_mesh_num - 1);
  const std::vector<float> faces =
      poisson_reconstructor.getFaces(saved_mesh_num - 1);

  std::cout << "saved mesh num: " << saved_mesh_num << std::endl;
  std::cout << "vertices num: " << int(vertices.size() / 3) << std::endl;
  std::cout << "faces num: " << int(faces.size() / 3) << std::endl;

  return 1;
}
