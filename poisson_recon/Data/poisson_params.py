from typing import Union


class PoissonParams(object):
    def __init__(self,
                 degree: int=1,
                 bType: int=3,
                 depth: int=8,
                 scale: float=1.1,
                 samplesPerNode: float=1.5,
                 pointWeight: Union[float, None]=None,
                 iters: int=8,
                 confidence: float=0,
                 confidenceBias: float=0,
                 primalGrid: bool=False,
                 linearFit: bool=False,
                 polygonMesh: bool=False) -> None:
        self.degree = degree
        self.bType = bType
        self.depth = depth
        self.scale = scale
        self.samplesPerNode = samplesPerNode
        self.pointWeight = pointWeight
        self.iters = iters
        self.confidence = confidence
        self.confidenceBias = confidenceBias
        self.primalGrid = primalGrid
        self.linearFit = linearFit
        self.polygonMesh = polygonMesh
        return

    def toCMDStr(self) -> str:
        params_str = ''
        params_str += ' --degree ' + str(self.degree)
        params_str += ' --bType ' + str(self.bType)
        params_str += ' --depth ' + str(self.depth)
        params_str += ' --scale ' + str(self.scale)
        params_str += ' --samplesPerNode ' + str(self.samplesPerNode)

        if self.pointWeight is None:
            params_str += ' --pointWeight ' + str(2.0 * self.degree)
        else:
            params_str += ' --pointWeight ' + str(self.pointWeight)

        params_str += ' --iters ' + str(self.iters)
        params_str += ' --confidence ' + str(self.confidence)
        params_str += ' --confidenceBias ' + str(self.confidenceBias)

        if self.primalGrid:
            params_str += ' --primalGrid'

        if self.linearFit:
            params_str += ' --linearFit'

        if self.polygonMesh:
            params_str += ' --polygonMesh'

        return params_str

    def toLogStr(self) -> str:
        params_str = ''
        params_str += '_degree-' + str(self.degree)
        params_str += '_bType-' + str(self.bType)
        params_str += '_depth-' + str(self.depth)
        params_str += '_scale-' + str(self.scale)
        params_str += '_samplesPerNode-' + str(self.samplesPerNode)

        if self.pointWeight is None:
            params_str += '_pointWeight-' + str(2.0 * self.degree)
        else:
            params_str += '_pointWeight-' + str(self.pointWeight)

        params_str += '_iters-' + str(self.iters)
        params_str += '_confidence-' + str(self.confidence)
        params_str += '_confidenceBias-' + str(self.confidenceBias)
        params_str += '_primalGrid-' + str(int(self.primalGrid))
        params_str += '_linearFit-' + str(int(self.linearFit))
        params_str += '_polygonMesh-' + str(int(self.polygonMesh))

        return params_str
