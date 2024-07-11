#rm -rf build

mkdir build
cd build
cmake \
  -DOpen3D_ROOT=../../open3d-manage/3rd/open3d-devel-linux/ \
  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
  ..
make -j
