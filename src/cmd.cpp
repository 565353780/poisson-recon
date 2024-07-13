#include "cmd.h"
#include <iostream>

const bool runCMD(const std::string &command) {
  const int result = system(command.c_str());

  if (result != 0) {
    std::cout << "[ERROR][cmd::runCMD]" << std::endl;
    std::cout << "\t system call failed!" << std::endl;
    std::cout << "\t command: " << command << std::endl;

    return false;
  }

  return true;
}
