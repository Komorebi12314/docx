> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Cherry Studio 配置指南

> 在 Cherry Studio 中使用 ToAPIs 作为 API 后端

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


## 准备工作

在开始之前，请确保：

1. **已安装 Cherry Studio**

   从 [Cherry Studio 官网](https://cherry-ai.com) 下载并安装适合您操作系统的版本

2. **已获取 ToAPIs API 密钥**

   登录 [ToAPIs 控制台](https://toapis.com/console/token) 获取您的 API 密钥（以 `sk-` 开头）

**提示：** 如果还没有 ToAPIs 账户，请先在 [ToAPIs](https://toapis.com) 注册并获取 API 密钥。

## 配置步骤

### 第一步：打开模型提供商设置

1. 启动 Cherry Studio
2. 点击左下角的 **设置** 图标（齿轮图标）
3. 在设置页面中选择 **模型服务** 或 **提供商**

### 第二步：添加 ToAPIs 提供商

1. 点击提供商列表右上角的 **+** 按钮，添加新提供商
2. 在弹出的对话框中：
   * **名称**：填写 `ToAPIs`（或您喜欢的名称）
   * **提供商类型**：选择 **New API**（兼容 OpenAI 格式）
3. 点击 **确认** 完成创建

### 第三步：填写 API 配置

在 ToAPIs 提供商的配置页面中，填写以下信息：

| 配置项        | 填写内容                                |
| ---------- | ----------------------------------- |
| **API 密钥** | 您的 ToAPIs API 密钥（`sk-xxxxxxxxxxxx`） |
| **API 地址** | `https://toapis.com/v1/`            |

### 第四步：添加模型

1. 在提供商配置页面，点击 **添加模型** 按钮
2. 填写模型信息：
   * **模型 ID**：输入您想使用的模型 ID（见下方推荐模型列表）
   * **端点类型**：选择 **OpenAI**
3. 点击保存

**推荐模型：**

| 模型名称              | 模型 ID                                                                      | 特点             |
| ----------------- | -------------------------------------------------------------------------- | -------------- |
| Claude Opus 4.6   | [`claude-opus-4-6`](../api-reference/chat/claude-opus-4-6/chat)            | 最强大，适合复杂任务     |
| Claude Sonnet 4.6 | [`claude-sonnet-4-6`](../api-reference/chat/claude-sonnet-4-6/chat)        | 性能与速度平衡，推荐日常使用 |
| Claude Haiku 4.5  | [`claude-haiku-4-5-20251001`](../api-reference/chat/claude-haiku-4-5/chat) | 快速响应，适合简单任务    |
| GPT-5             | [`gpt-5`](../api-reference/chat/models)                                    | 最新 OpenAI 旗舰模型 |
| GPT-4o            | [`gpt-4o`](../api-reference/chat/models)                                   | 高质量对话与多模态      |
| GPT-4o Mini       | [`gpt-4o-mini`](../api-reference/chat/models)                              | 快速且经济          |
| Gemini 2.5 Pro    | [`gemini-2.5-pro`](../api-reference/chat/models)                           | Google 多模态旗舰   |

您可以重复上述步骤，按需添加多个模型。

### 第五步：启用并验证

1. 确保提供商右侧的开关处于**开启**状态
2. 点击 **检查连接** 或 **测试** 按钮，验证配置是否正确
3. 如果提示连接成功，说明配置完成

## 开始使用

配置完成后：

1. 返回 Cherry Studio 主界面
2. 在对话框顶部的模型选择器中，选择刚才添加的 ToAPIs 模型
3. 开始对话

## 常见问题

### Q1: 连接测试失败？

**解决方案：**

1. 检查 **API 密钥** 是否正确，确认以 `sk-` 开头
2. 确认 **API 地址** 填写为 `https://toapis.com/v1/`（注意末尾的斜杠）
3. 在 [ToAPIs 控制台](https://toapis.com/console/token) 确认密钥未过期且账户余额充足
4. 检查网络连接，确保能访问 `https://toapis.com`

### Q2: 模型列表中找不到我的模型？

Cherry Studio 使用手动添加模型的方式，直接在添加模型时输入模型 ID 即可。可在 [ToAPIs 模型列表](https://toapis.com/console/models) 查看所有可用模型 ID。

### Q3: 常见错误码说明

| 错误信息                        | 原因            | 解决方法         |
| --------------------------- | ------------- | ------------ |
| `401 Unauthorized`          | API Key 无效或过期 | 重新获取 API Key |
| `429 Too Many Requests`     | 请求频率超限        | 稍等片刻后重试      |
| `500 Internal Server Error` | 服务器临时故障       | 等待几分钟后重试     |
| `insufficient_quota`        | 账户余额不足        | 前往控制台充值      |

## 支持与帮助

如果您在使用过程中遇到任何问题：

* 📚 [ToAPIs 文档中心](https://docs.toapis.com)
* 📚 [Cherry Studio 官方文档](https://docs.cherry-ai.com)
* 💬 [Discord 社区](https://discord.gg/hvnszCrJ73)
* 🐦 [Twitter @toapisai](https://x.com/toapisai)

***

\[## 开始使用 ToAPIs

立即注册 ToAPIs，获取您的 API 密钥，在 Cherry Studio 中开启高效 AI 之旅！]\([https://toapis.com](https://toapis.com))
