#include "poisson_params.h"

const std::string PoissonParams::toCMDStr() {
  std::string params_str;

  params_str += " --degree " + std::to_string(degree);
  params_str += " --bType " + std::to_string(bType);
  params_str += " --depth " + std::to_string(depth);
  params_str += " --scale " + std::to_string(scale);
  params_str += " --samplesPerNode " + std::to_string(samplesPerNode);

  if (pointWeight >= 0) {
    params_str += " --pointWeight " + std::to_string(pointWeight);
  } else {
    params_str += " --pointWeight " + std::to_string(2.0 * degree);
  }

  params_str += " --iters " + std::to_string(iters);
  params_str += " --confidence " + std::to_string(confidence);
  params_str += " --confidenceBias " + std::to_string(confidenceBias);

  if (primalGrid) {
    params_str += " --primalGrid";
  }

  if (linearFit) {
    params_str += " --linearFit";
  }

  if (polygonMesh) {
    params_str += " --polygonMesh";
  }

  return params_str;
}

const std::string PoissonParams::toLogStr() {
  std::string params_str;

  params_str += "_degree-" + std::to_string(degree);
  params_str += "_bType-" + std::to_string(bType);
  params_str += "_depth-" + std::to_string(depth);
  params_str += "_scale-" + std::to_string(scale);
  params_str += "_samplesPerNode-" + std::to_string(samplesPerNode);

  if (pointWeight >= 0) {
    params_str += "_pointWeight-" + std::to_string(pointWeight);
  } else {
    params_str += "_pointWeight-" + std::to_string(2.0 * degree);
  }

  params_str += "_iters-" + std::to_string(iters);
  params_str += "_confidence-" + std::to_string(confidence);
  params_str += "_confidenceBias-" + std::to_string(confidenceBias);
  params_str += "_primalGrid-" + std::to_string(primalGrid);
  params_str += "_linearFit-" + std::to_string(linearFit);
  params_str += "_polygonMesh-" + std::to_string(polygonMesh);

  return params_str;
}
