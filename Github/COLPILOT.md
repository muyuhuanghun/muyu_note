*前提！你已经完成GitHub学生认证，否则copilot无法使用，见[[GitHub学生认证]]*
# 一.使用IDE中的copilot gui插件

- 1.选择账户的copilot settings
		![[Pasted image 20260514125240.png]]
- 2.选择copilot in your ide
		![[Pasted image 20260514125332.png]]
- 3.选择你所使用的ide，目前支持vscode 和 jet brain 的ide
	网页会自动打开ide并安装相应的插件，往后仅需简单登录GitHub账号操作

# 二.使用 GitHub CLI

- 选择你所使用的ide的终端，按照文档的顺序，此处默认环境中已经支持了npm 包，若无，见文档[[如何在各种ide中使用ai agent进行ai coding]]
- 执行如下命令
```
		npm install -g @github/copilot
```

- 完成安装后根据终端指示进行GitHub账户登录
- 合理认为GitHub的copilot cli 基于泄露的Claude code 改造而成，两者使用逻辑几乎一致，终端界面极其类似

- 终端直接输入copilot 唤起终端copilot cli

	![[Pasted image 20260514130953.png]]
	常驻5.3codex ，完全足矣满足使用