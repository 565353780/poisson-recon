from poisson_recon.Module.metric_renderer import MetricRenderer

def demo():
    metric_folder_path = '../output_metric/spsr/airplane/'
    print_progress = True

    metric_renderer = MetricRenderer()
    metric_renderer.renderMetricFolder(metric_folder_path, print_progress)
    return True
