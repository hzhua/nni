# NNI 客户端

NNI client 是 `nnictl` 的python API，提供了对常用命令的实现。 相比于命令行，用户可以通过此 API 来在 python 代码中直接操控实验，收集实验结果并基于实验结果进行更加高级的分析。 示例如下：

```
from nni.experiment import Experiment

# create an experiment instance
exp = Experiment() 

# start an experiment, then connect the instance to this experiment
# you can also use `resume_experiment`, `view_experiment` or `connect_experiment`
# only one of them should be called in one instance
exp.start_experiment('nni/examples/trials/mnist-pytorch/config.yml', port=9090)

# update the experiment's concurrency
exp.update_concurrency(3)

# get some information about the experiment
print(exp.get_experiment_status())
print(exp.get_job_statistics())
print(exp.list_trial_jobs())

# stop the experiment, then disconnect the instance from the experiment.
exp.stop_experiment()
```

## 参考

```eval_rst
..  autoclass:: nni.experiment.Experiment
    :members:
..  autoclass:: nni.experiment.TrialJob
    :members:
..  autoclass:: nni.experiment.TrialHyperParameters
    :members:
..  autoclass:: nni.experiment.TrialMetricData
    :members:
..  autoclass:: nni.experiment.TrialResult
    :members:
```
