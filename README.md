# fullstack_ai
Points need to note building products powered by machine learning. A road map of skill required to quickly develop and deploy a complete ML system. 


### Deep learning Framework
;tldr, PyTorch is preferred due to its dominance in the number of models, papers, and competition winners. So there will be Pytorch and Pytorch lightling code here. Sure you can also use Tensorflow or JAX as well.


### Meta-Frameworks and Model Zoos
There are also thousands of models that already been trained on the platform to be used for free. 

1.[ONNX](https://onnx.ai/) is an open standard for saving and exchanging deep learning models

2.[Hugging Face](https://huggingface.co/) is a prominent model repository that initially focused on Natural Language Processing (NLP) tasks but has since expanded to include a wide range of tasks such as audio classification, image classification, and object detection. 

3.[TIMM](https://github.com/rwightman/pytorch-image-models) is a collection of cutting-edge computer vision models and related code.

Here I will use Hugging face as an example. 

### Distributed Training 

Distributed training is a bit like a potluck dinner. You've got multiple GPUs (guests) across different machines (houses) all ready to process data batches and model parameters (bring their own dishes). If both the data batch and model parameters (the potato salad and the apple pie) can fit on a single GPU (in one guest's car), that's what we call trivial parallelism (or a one-person potluck, which isn't much of a party).

But what if the model fits (the potato salad is small enough), but the data (the apple pie) is too big to handle? Well, that's when we call in data parallelism. It's like cutting that apple pie into slices and giving each guest a piece to bring. This is implemented in PyTorch with the DistributedDataParallel library and Horovod (our potluck coordinators).

Now, if the model can't fit on a single GPU (imagine trying to transport a whole wedding cake in a compact car), we have a few different strategies. Sharded data-parallelism is like cutting that cake into pieces and giving each guest a slice to transport. This is done by the likes of Microsoft's DeepSpeed, Facebook's FairScale, and PyTorch's Fully-Sharded DataParallel (our cake-cutting experts).

Pipelined model-parallelism is like having each guest bring a different dish, maximizing the variety (and deliciousness). Tensor-parallelism, demonstrated by NVIDIA's Megatron-LM, is like each guest bringing a different ingredient for a big, communal stew.

In conclusion, if your model and data can fit on one GPU, that's as sweet as a one-person potluck with all your favorite dishes. If not, and you want to speed up training (or get the party started faster), try DistributedDataParallel. If the model still doesn't fit, try ZeRO-3 or Full-Sharded Data Parallel. It's like calling in the caterers. For more resources to speed up model training (or potluck planning), refer to the list compiled by DeepSpeed, MosaicML, and FFCV (our party planning committee).
