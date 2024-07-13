#include "path.h"
#include <filesystem>
#include <iostream>

const bool createFileFolder(const std::string &file_path) {
  const size_t pos = file_path.rfind('/');

  if (pos == std::string::npos) {
    return true;
  }

  const std::string folder_path = file_path.substr(0, pos + 1);

  if (std::filesystem::exists(folder_path)) {
    return true;
  }

  if (!std::filesystem::create_directories(folder_path)) {
    std::cout << "[ERROR][path::createFileFolder]" << std::endl;
    std::cout << "\t create_directories failed!" << std::endl;
    std::cout << "\t folder_path: " << folder_path << std::endl;

    return false;
  }

  return true;
}
