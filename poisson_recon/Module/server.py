import os
import numpy as np
import gradio as gr
import open3d as o3d
from typing import Union

from poisson_recon.Data.poisson_params import PoissonParams
from poisson_recon.Method.render import toPlotFigure
from poisson_recon.Module.poisson_reconstructor import PoissonReconstructor


def renderInputData(input_pcd_file_path: str):
    pcd = o3d.io.read_point_cloud(input_pcd_file_path)

    gt_points = np.asarray(pcd.points)

    return toPlotFigure(gt_points)


def toMesh(
    input_pcd_file_path: str,
    degree: int,
    bType: int,
    depth: int,
    scale: float,
    samplesPerNode: float,
    pointWeight: Union[float, None],
    iters: int,
    confidence: float,
    confidenceBias: float,
    primalGrid: bool,
    linearFit: bool,
    polygonMesh: bool,
):
    print("input_pcd_file_path:", input_pcd_file_path)
    if not os.path.exists(input_pcd_file_path):
        print("[ERROR][Server::fitBSplineSurface]")
        print("\t input pcd file not exist!")
        print("\t input_pcd_file_path:", input_pcd_file_path)
        return ""

    input_pcd_file_name = input_pcd_file_path.split("/")[-1]
    save_mesh_file_path = "./output/" + input_pcd_file_name
    overwrite = True
    print_progress = True

    if pointWeight == 0:
        pointWeight = None

    poisson_params = PoissonParams(
        degree,
        bType,
        depth,
        scale,
        samplesPerNode,
        pointWeight,
        iters,
        confidence,
        confidenceBias,
        bool(primalGrid),
        bool(linearFit),
        bool(polygonMesh),
    )
    poisson_reconstructor = PoissonReconstructor(poisson_params)
    recon_mesh_file_path = poisson_reconstructor.reconMeshFile(
        input_pcd_file_path, save_mesh_file_path, overwrite, print_progress
    )

    return recon_mesh_file_path


class Server(object):
    def __init__(self, port: int) -> None:
        self.port = port

        self.input_data = None
        return

    def start(self) -> bool:
        example_folder_path = "./output/input_pcd/"
        example_file_name_list = os.listdir(example_folder_path)

        examples = [
            example_folder_path + example_file_name
            for example_file_name in example_file_name_list
        ]

        with gr.Blocks() as iface:
            gr.Markdown("Surface Reconstruction Demo")

            with gr.Row():
                with gr.Column():
                    input_pcd = gr.Model3D(label="3D Data to be reconstructed")

                    gr.Examples(examples=examples, inputs=input_pcd)

                    submit_button = gr.Button("Submit to server")

                with gr.Column():
                    visual_gt_plot = gr.Plot()

                    recon_button = gr.Button("Click to start reconstructing")

            output_mesh = gr.Model3D(label="Reconstructed Surface")

            with gr.Accordion(label="Recon Params", open=False):
                degree = gr.Slider(1, 8, value=1, step=1, label="degree")
                bType = gr.Slider(1, 3, value=3, step=1, label="bType")
                depth = gr.Slider(5, 12, value=8, step=1, label="depth")
                scale = gr.Slider(1.0, 1.5, value=1.1, step=0.1, label="scale")
                samplesPerNode = gr.Slider(
                    1.0, 20.0, value=1.5, step=0.1, label="samplesPerNode"
                )
                pointWeight = gr.Slider(0, 6, value=0, step=1, label="pointWeight")
                iters = gr.Slider(5, 10, value=8, step=1, label="iters")
                confidence = gr.Slider(
                    0.0, 1.0, value=0.0, step=0.1, label="confidence"
                )
                confidenceBias = gr.Slider(
                    0.0, 0.4, value=0.0, step=0.1, label="confidenceBias"
                )
                primalGrid = gr.Slider(0, 1, value=0, step=1, label="primalGrid")
                linearFit = gr.Slider(0, 1, value=0, step=1, label="linearFit")
                polygonMesh = gr.Slider(0, 1, value=0, step=1, label="polygonMesh")

            recon_params = [
                degree,
                bType,
                depth,
                scale,
                samplesPerNode,
                pointWeight,
                iters,
                confidence,
                confidenceBias,
                primalGrid,
                linearFit,
                polygonMesh,
            ]

            submit_button.click(
                fn=renderInputData,
                inputs=[input_pcd],
                outputs=[visual_gt_plot],
            )

            recon_button.click(
                fn=toMesh,
                inputs=[input_pcd] + recon_params,
                outputs=[output_mesh],
            )

        iface.launch(
            server_name="0.0.0.0",
            server_port=self.port,
            ssl_keyfile="./ssl/key.pem",
            ssl_certfile="./ssl/cert.pem",
            ssl_verify=False,
        )
        return True
