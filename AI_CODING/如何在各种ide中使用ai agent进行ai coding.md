# 一.CODEX

相对最推荐，不需要anthropic的认证和封号的风险

## 方案1

- 配置过程

## 1.安装codex插件及codex cli

电脑本地需要npm包管理器，以及node.js[[Node.js — 在任何地方运行 JavaScript](https://nodejs.org/zh-cn)

npm直安装

```
curl -qL https://www.npmjs.com/install.sh | sh
```


在vscode或者其他ide中安装codex插件，打开cmd确认npm正确安装

```
node -v
npm -v
```

在cmd终端输入

```
npm install -g @openai/codex
```

安装coedx cli

输入

```
codex --version
```

确认安装成功

## 2.配置codex

推荐使用cc switch进行配置以及配置的统一管理

- 1.安装[cc switch ][[farion1231/cc-switch: A cross-platform desktop All-in-One assistant for Claude Code, Codex, OpenCode, OpenClaw, Gemini CLI & Hermes Agent. Only official website: ccswitch.io](https://github.com/farion1231/cc-switch)
		在release中选择符合自己系统的cc switch 版本并下载，图表如下
		![[Pasted image 20260513190912.png]]
- 2.在自己的无论是官方api或者中转站，先以中转站为例
		市面上常见中转站使用的都是sub2api的统一管理，所以操作基本一致
		打开你的中转站，选择创建codex分类的apikey，其他选项通常选择默认，在api密钥下找到生成的apikey，点击导出到ccs
		![[Pasted image 20260513191535.png]]
		浏览器会自动打开ccs
		![[Pasted image 20260513191630.png]]
		选择导入则第一阶段完成
- 进入vscode的codex插件，选择使用apikey登录并将你刚刚生成的apikey输入，则可进入codex插件
- 官方api直接在插件中填写apikey即可
- 由于gptcodex是闭源模型，所以很难将其他第三方api接入codex中使用，但是存在一种可能即通过兼容网关的方式伪装以供codex使用，正在尝试复刻[[NIM4CC的使用及复刻]][nim4cc][[Geek66666/nim4cc: NIM4CC 是一个面向公开使用的 NVIDIA NIM 兼容网关，目标是把 NIM 的 chat/completions 能力转换成更易接入的上层协议，并补上模型目录缓存、调用统计和健康度看板。](https://github.com/Geek66666/nim4cc)


# 二.COPILOT

专供学生使用的GitHub出品的ai coding 插件，支持大量主流模型 codex，gemini，opus的免费使用，cli版本类似Claude Code，但是使用和配置比Claude Code更简单，需要GitHub完成学生认证的账号

## 1.[[GitHub学生认证]]
- 详见该篇笔记内部

## 2.COPILOT使用
- 设置及登录操作见[[COLPILOT]]
- copilot cli界面和Claude code 近乎一致，合理认为copilot cli基于泄露的Claude code源码魔改得到



# 三.CLAUDE CODE+DEEPSEEK

## 1 从0安装claudecode

	1.需要node.js 18+
	2.确保你已经安装git for windows
	3.建议power shell 17+
在命令行界面下执行
```
npm install -g @anthropic-ai/claude-code
```
安装完成后执行
```
claude --version
```
确认Claude版本

## 2 配置

依旧建议使用ccswitch进行统一的api管理

供应商名称：DeepSeek
官网链接：https://platform.deepseek.com
请求地址：https://api.deepseek.com/anthropic
API 格式选择：Anthropic Messages(原生)
认证字段选择：ANTHROPIC_AUTH_TOKEN(默认)

配置模型映射
![[模型映射.png]]

配置json，开启写入通用配置：
```
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "deepseek-v4-flash",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_MODEL": "deepseek-v4-pro[1m]"
  },
  "theme": "dark"
}
```

deepseek原生支持claudecode的websearch功能，可以直接要求搜索网页






