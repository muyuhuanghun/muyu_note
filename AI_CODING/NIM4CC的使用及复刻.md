# 1.[NIM4CC][[Geek66666/nim4cc: NIM4CC 是一个面向公开使用的 NVIDIA NIM 兼容网关，目标是把 NIM 的 chat/completions 能力转换成更易接入的上层协议，并补上模型目录缓存、调用统计和健康度看板。](https://github.com/Geek66666/nim4cc)]

NIM4CC 是一个面向公开使用的 NVIDIA NIM 兼容网关，目标是把 NIM 的 `chat/completions` 能力转换成更易接入的上层协议，并补上模型目录缓存、调用统计和健康度看板。

# 2.主要能力

- 将 NVIDIA 官方 `POST /v1/chat/completions` 转换为 OpenAI 风格的 `POST /v1/responses`
- 将 NVIDIA 官方 `POST /v1/chat/completions` 转换为 Anthropic 风格的 `POST /v1/messages`
- 支持 OpenAI 风格的 tool calling / function calling
- 支持 Anthropic 风格的 `tools`、`tool_choice`、`tool_result`
- 尽量兼容 Claude Code 常见客户端工具调用形态
- 支持 `previous_response_id` 对话续写
- 支持 Anthropic SSE 风格流式事件
- 支持官方模型目录同步、本地缓存和公开展示
- 支持调用成功率聚合统计和模型健康度看板