cd ..
mkdir output_mesh

./PoissonRecon/Bin/Linux/PoissonRecon \
	--in ./open3d-manage/output/airplane_gauss_noise_0.1_0.1_pcd.ply \
	--out ./output_mesh/airplane_gauss_noise_0.1_0.1.ply
