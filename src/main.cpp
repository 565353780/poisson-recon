#include "poisson_params.h"
#include "poisson_reconstructor.h"
#include <iostream>

int main() {
  // PoissonRecon git package path
  const std::string poisson_recon_folder_path =
      "/home/chli/github/AMCAX/PoissonRecon/";

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

  const std::string pcd_file_path =
      "/home/chli/chLi/Dataset/MashPcd_Manifold/ShapeNet/02691156/"
      "2af04ef09d49221b85e5214b0d6a7.ply";
  const std::string save_mesh_file_path = "./output/recon_poisson.ply";
  const bool overwrite = true;

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
  PoissonReconstructor poisson_reconstructor(poisson_recon_folder_path,
                                             poisson_params);

  if (!poisson_reconstructor.isValid()) {
    std::cout << "poisson_reconstructor is not valid!" << std::endl;
    return -1;
  }

  // reconstruct mesh from input point cloud
  const bool success = poisson_reconstructor.reconMeshFile(
      pcd_file_path, save_mesh_file_path, overwrite);
  if (!success) {
    std::cout << "reconMesh failed!" << std::endl;
    return -1;
  }

  // get reconstructed mesh data
  const int saved_mesh_num = poisson_reconstructor.getSavedMeshNum();
  const std::vector<float> last_saved_mesh_vertices =
      poisson_reconstructor.getSavedMeshVertices(saved_mesh_num - 1);
  const std::vector<int> last_saved_mesh_faces =
      poisson_reconstructor.getSavedMeshFaces(saved_mesh_num - 1);

  std::cout << "saved mesh num: " << saved_mesh_num << std::endl;
  std::cout << "last saved mesh vertices num: "
            << int(last_saved_mesh_vertices.size() / 3) << std::endl;
  std::cout << "last saved mesh faces num: "
            << int(last_saved_mesh_faces.size() / 3) << std::endl;

  // clear all saved recon data and files
  // poisson_reconstructor.clear();

  return 1;
}
