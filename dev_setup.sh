cd ..
git clone https://github.com/mkazhdan/PoissonRecon.git

sudo apt install libboost-dev libboost-system-dev

cd PoissonRecon
make -j

pip install -U tqdm open3d numpy matplotlib gradio plotly

cd ../poisson-recon
mkdir ssl
cd ssl
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365 -nodes
