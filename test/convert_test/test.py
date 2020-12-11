import os
import sys
import torch
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from nni.retiarii.converter.graph_gen import convert_to_graph
from nni.retiarii.converter.visualize import visualize_model
from nni.retiarii.codegen.pytorch import model_to_pytorch_script

from nni.retiarii import nn
from nni.retiarii.trainer import PyTorchImageClassificationTrainer
from nni.retiarii.utils import TraceClassArguments

from base_mnasnet import MNASNet
from nni.experiment import RetiariiExperiment, RetiariiExpConfig

#from simple_strategy import SimpleStrategy
#from tpe_strategy import TPEStrategy
from nni.retiarii.strategies import TPEStrategy
from mutator import BlockMutator

if __name__ == '__main__':
    _DEFAULT_DEPTHS = [16, 24, 40, 80, 96, 192, 320]
    _DEFAULT_CONVOPS = ["dconv", "mconv", "mconv", "mconv", "mconv", "mconv", "mconv"]
    _DEFAULT_SKIPS = [False, True, True, True, True, True, True]
    _DEFAULT_KERNEL_SIZES = [3, 3, 5, 5, 3, 5, 3]
    _DEFAULT_NUM_LAYERS = [1, 3, 3, 3, 2, 4, 1]

    with TraceClassArguments() as tca:
        base_model = MNASNet(0.5, _DEFAULT_DEPTHS, _DEFAULT_CONVOPS, _DEFAULT_KERNEL_SIZES,
                        _DEFAULT_NUM_LAYERS, _DEFAULT_SKIPS)
        trainer = PyTorchImageClassificationTrainer(base_model, dataset_cls="CIFAR10",
                dataset_kwargs={"root": "data/cifar10", "download": True},
                dataloader_kwargs={"batch_size": 32},
                optimizer_kwargs={"lr": 1e-3},
                trainer_kwargs={"max_epochs": 1})

    '''script_module = torch.jit.script(base_model)
    model = convert_to_graph(script_module, base_model, tca.recorded_arguments)
    code_script = model_to_pytorch_script(model)
    print(code_script)
    print("Model: ", model)
    graph_ir = model._dump()
    print(graph_ir)
    visualize_model(graph_ir)'''

    # new interface
    applied_mutators = []
    applied_mutators.append(BlockMutator('mutable_0'))
    applied_mutators.append(BlockMutator('mutable_1'))

    simple_startegy = TPEStrategy()

    exp = RetiariiExperiment(base_model, trainer, applied_mutators, simple_startegy, tca)

    exp_config = RetiariiExpConfig.create_template('local')
    exp_config.experiment_name = 'mnasnet_search'
    exp_config.trial_concurrency = 2
    exp_config.max_trial_number = 10

    exp.run(exp_config, 8081, debug=True)
