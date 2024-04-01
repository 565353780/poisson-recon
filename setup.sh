cd ..
git clone https://github.com/mkazhdan/PoissonRecon.git

sudo apt install libboost-dev

cd PoissonRecon
make -j

pip install -U tqdm open3d numpy matplotlib gradio plotly
