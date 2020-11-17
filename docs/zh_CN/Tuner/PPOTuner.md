# NNI 中的 PPO Tuner

## PPOTuner

这是一个用于 NNI 神经网络架构搜索（NAS）接口的 Tuner。 它使用了 [ppo 算法](https://arxiv.org/abs/1707.06347)。 此实现继承了 [OpenAI 的 ppo2 实现](https://github.com/openai/baselines/tree/master/baselines/ppo2)的主要逻辑，并为 NAS 场景做了适配。

mnist-nas 示例已调优，并得到以下结果： **注意：此示例正在重构中，以支持最新的 NAS 接口，完成后会重新发布示例代码。**

![](../../img/ppo_mnist.png)

We also tune [the macro search space for image classification in the enas paper](https://github.com/microsoft/nni/tree/v1.9/examples/trials/nas_cifar10) (with a limited epoch number for each trial, i.e., 8 epochs), which is implemented using the NAS interface and tuned with PPOTuner. [enas 论文](https://arxiv.org/pdf/1802.03268.pdf)中的图 7 展示了搜索空间：

![](../../img/enas_search_space.png)

上图是所选的结构。 每个方块是一层，可从 6 个操作中选择。 每条虚线是直通连接，每个方块都可以有 0 或 1 条直通连接获得前面层的输出。 **注意**，在原始的宏搜索空间中，每个方块层可选择任意条直通连接，在此实现中，仅允许 0 或 1条。

The results are shown in figure below (see the experimenal config [here](https://github.com/microsoft/nni/blob/v1.9/examples/trials/nas_cifar10/config_ppo.yml):

![](../../img/ppo_cifar10.png)