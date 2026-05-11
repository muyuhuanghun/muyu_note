
# 一.本地运行

- llama.cpp支持终端和简易网页前端的交互模式，接下来以 Qwen3.5-9B-IQ4 模型和
gemma-4-E4B-it-IQ4作为示例
## 1.终端交互

- 在llama.cpp文件夹下启动终端，输入如下命令
	./llama-cli -m Qwen3.5-9B-IQ4_NL.gguf -ngl 99 -c 8192 -cnv

- -ngl 99 将模型的所有层装载到gpu上进行推理
- -c 8192 支持8k上下文能力
- -cnv 开启对话模式
- 随后可以看到如下界面
- ![[Pasted image 20260511205541.png|537]]
- 接下来就可以正常和你本地部署的大模型进行简单的对话操作了

## 2.server浏览器监听端口

- 依旧在llama.cpp文件夹下启动终端，输入如下命令
    ./llama-server -m Qwen3.5-9B-IQ4_NL.gguf -ngl 99 -c 8192

- 打开浏览器监听端口[http://localhost:8080]，可进入llama.cpp自带的简易server前端界面
- 可以看到如下界面![[Pasted image 20260511215433.png|556]]
- 操作逻辑和gpt等ai的网页端一致，但是支持更多的可能性

## 3.基于gemma4本地部署的越过模型防火墙操作

- 和qwen3本地部署的前期操作一致，将gemma4的gguf包放入llama.cpp文件夹下后使用命令激活
- ./llama-server -m gemma-4-E4B-it-IQ4_NL.gguf -ngl 99 --flash-attn on -c 8192 --port 8080 --host 0.0.0.0
- port 8080 启用8080端口监听
- host 0.0.0.0允许局域网内其他设备访问api
- flash-attn on 显著降低缓存占用，提升长文本处理能力，gemma4采用了混合注意力技术(本地滑动窗口+全局注意力)
- 在浏览器内监听[http://127.0.0.1:8080]