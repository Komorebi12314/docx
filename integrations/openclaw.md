> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# 在 OpenClaw 中使用 ToAPIs

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


## 准备工作

在开始之前，请确保：

1. **已安装 OpenClaw**

   下载并安装 OpenClaw，安装完成后可在终端中运行 `openclaw` 命令

2. **已获取 ToAPIs API 密钥**

   登录 [ToAPIs 控制台](https://toapis.com/console/token) 获取您的 API 密钥（以 `sk-` 开头）

**提示：** 如果还没有 ToAPIs 账户，请先在 [ToAPIs](https://toapis.com) 注册并获取 API 密钥。

## 配置步骤

在终端中运行以下命令启动初始化向导：

```bash 
openclaw onboard
```

按照提示依次填写以下信息：

### 第一步：选择模型/认证提供商

```
Model/auth provider:
```

使用**方向键**选择 **Custom Provider**，然后按回车确认。

### 第二步：填写 API Base URL

```
API Base URL:
```

输入以下地址：

```
https://toapis.com/v1
```

### 第三步：填写 API Key

```
API Key:
```

粘贴您从 [ToAPIs 控制台](https://toapis.com/console/token) 获取的 API 密钥（`sk-xxxxxxxxxxxx`）。

### 第四步：选择端点兼容性

```
Endpoint compatibility:
```

使用**方向键**选择 **OpenAI-compatible**，然后按回车确认。

### 第五步：填写模型 ID

```
Model ID:
```

输入您要使用的模型 ID，例如：

```
claude-sonnet-4-6
```

## 推荐模型

| 模型名称              | 模型 ID               | 特点                    |
| ----------------- | ------------------- | --------------------- |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 性能与成本最佳平衡，适合大多数场景     |
| Claude Opus 4.6   | `claude-opus-4-6`   | 最强大的 Claude 模型，适合复杂任务 |
| Claude Haiku 4.5  | `claude-haiku-4-5`  | 快速且经济，适合轻量任务          |
| Qwen3 Max         | `qwen3-max`         | 阿里云旗舰推理模型             |
| Kimi K2.5         | `kimi-k2.5`         | 月之暗面长上下文模型            |

## 配置完成

完成以上步骤后，OpenClaw 将使用 ToAPIs 作为后端服务。您可以直接开始使用 AI 对话功能，所有请求将通过 ToAPIs 路由到对应的模型。

## 常见问题

### 认证失败？

* 确认 API Key 正确且以 `sk-` 开头
* 在 [ToAPIs 控制台](https://toapis.com/console/token) 检查密钥是否有效
* 确保账户余额充足

### 模型不可用？

* 确认 API Base URL 填写为 `https://toapis.com/v1`（包含 `/v1` 后缀）
* 确认 Endpoint compatibility 选择了 **OpenAI-compatible**
* 检查模型 ID 是否拼写正确

## 支持与帮助

如果您在使用过程中遇到任何问题：

* 📚 [ToAPIs 文档中心](https://docs.toapis.com)
* 💬 [Discord 社区](https://discord.gg/hvnszCrJ73)
* 🐦 [Twitter @toapisai](https://x.com/toapisai)
* 📧 技术支持：[zhihong@toapis.com](mailto:zhihong@toapis.com)

***

\[## 开始使用 ToAPIs

立即注册 ToAPIs，获取您的 API 密钥，在 OpenClaw 中开启 AI 之旅！]\([https://toapis.com](https://toapis.com))
