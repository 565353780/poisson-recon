#pragma once

#include <string>

class PoissonParams {
public:
  PoissonParams(){};

  const std::string toCMDStr();

  const std::string toLogStr();

public:
  int degree = 1;
  int bType = 3;
  int depth = 8;
  float scale = 1.1;
  float samplesPerNode = 1.5;
  float pointWeight = -1.0; // regard as null if < 0
  int iters = 8;
  float confidence = 0.0;
  float confidenceBias = 0.0;
  bool primalGrid = false;
  bool linearFit = false;
  bool polygonMesh = false;
  float maxMemory = -1.0;
  bool performance = false;
  bool verbose = false;
};
