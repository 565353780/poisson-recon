from poisson_recon.Demo.poisson_reconstructor import demo as demo_recon_poisson
from poisson_recon.Demo.evaluator import (
    demo as demo_eval_poisson,
    demo_folder as demo_eval_poisson_folder,
)
from poisson_recon.Demo.poisson_params_sampler import demo as demo_sample_poisson_params
from poisson_recon.Demo.metric_renderer import demo as demo_render_metric
from poisson_recon.Demo.server import demo as demo_server

if __name__ == "__main__":
    demo_recon_poisson()
    demo_eval_poisson()
    demo_eval_poisson_folder()
    demo_sample_poisson_params()
    demo_render_metric()
    demo_server()
