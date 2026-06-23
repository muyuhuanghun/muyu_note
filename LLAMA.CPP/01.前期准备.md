
# 一.前置准备

## 1.CUDA

- 根据gpu型号确定所需安装的cuda版本，通常为cuda13.x，使用 nvcc --version 确定cuda是否安装及其对应版本[CUDA Platform for Accelerated Computing | NVIDIA Developer](https://developer.nvidia.com/cuda?hl=zh-cn)

## 2.CMAKE

- 通常在[cmake][https://github.com/ggml-org/llama.cpp/releases]中下载的llama.cpp是已经预编译过的二进制文件，如果下载的不是如下图所示
![[Pasted image 20260511202449.png|370]]
那么则需要使用cmake进行编译处理

cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release

## 3.模型选择

- 使用llama.cpp强制需要模型为gguf的压缩模式，可以在以下开源社区找到所需要的模型gguf
	[1.]hugging face
		国际最大的ai开源社区[huggingface][https://huggingface.co/]
	[2.]modelscope
		国内源[模型库首页 · 魔搭社区](https://www.modelscope.cn/models)

- gguf下载成功后将下载的模型gguf包移动到你的llama.cpp文件夹下

全部前置准备工作完成

[[如何用llama.cpp本地运行大模型(开始体验)]]
