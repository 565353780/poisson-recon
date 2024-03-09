from poisson_recon.Module.poisson_params_sampler import PoissonParamsSampler

def demo():
    degree_range = [1, 2, 3, 4, 5, 6, 7, 8]
    bType_range = [1, 2, 3]
    depth_range = [5, 6, 7, 8, 9, 10, 11, 12]
    scale_range = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
    samplesPerNode_range = [1.0, 1.5, 3.0, 5.0, 10.0, 15.0, 20.0]
    pointWeight_range = [1, 2, 3, 4, 5, 6]
    iters_range = [5, 6, 7, 8, 9, 10]
    confidence_range = [0, 0.1, 0.2, 0.4, 0.8, 1.0]
    confidenceBias_range = [0, 0.1, 0.2, 0.3, 0.4]
    primalGrid_range = [True, False]
    linearFit_range = [True, False]
    polygonMesh_range = [True, False]
    sample_one_only = True
    print_progress = True

    poisson_params_sampler = PoissonParamsSampler(
        degree_range,
        bType_range,
        depth_range,
        scale_range,
        samplesPerNode_range,
        pointWeight_range,
        iters_range,
        confidence_range,
        confidenceBias_range,
        primalGrid_range,
        linearFit_range,
        polygonMesh_range,
        sample_one_only,
        print_progress
    )

    params_num = poisson_params_sampler.size()

    sample_params = poisson_params_sampler.sampleParams(params_num - 1)

    print('params_num =', params_num)
    print('sample_params :', sample_params)
    return True
