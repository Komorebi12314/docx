> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# 集成指南

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


## 准备工作

在开始之前，请确保：

1. **已安装 ChatBox**

   从 [ChatBox GitHub](https://github.com/Bin-Huang/chatbox) 下载并安装适合您操作系统的版本，或访问 [ChatBox 官网](https://chatboxai.app/)
2. **已获取 ToAPIs API 密钥**

   登录 [ToAPIs 控制台](https://toapis.com/console/token) 获取您的 API 密钥（以 `sk-` 开头）

**提示：** 如果还没有 ToAPIs 账户，请先在 [ToAPIs](https://toapis.com) 注册并获取 API 密钥。

## 第一步：启动 ChatBox 并开始配置

首次启动 ChatBox 或添加新的 AI 提供商时：

1. 启动 ChatBox 应用
2. 如果是首次使用，会自动弹出配置向导
3. 点击 **“使用自己的 API Key 或本地模型”** 按钮
4. 如果已经配置过，可以点击左下角的 **⚙️ 设置** 图标，或使用快捷键 `Ctrl+,` (Windows/Linux) / `Cmd+,` (macOS)

<img src="https://mintcdn.com/dashlyai/gmegcqBsMOcqIUJu/docs/assets/images/cn_integrations_chatbox/a6b4b59a_main-interface.png?fit=max&auto=format&n=gmegcqBsMOcqIUJu&q=85&s=68e10e95207c9a6cdb0fc27f9bd634d4" alt="ChatBox 启动配置向导" width="1023" height="768" data-path="docs/assets/images/cn_integrations_chatbox/a6b4b59a_main-interface.png" />

## 第二步：配置 ToAPIs API

### 2.1 选择 AI 模型提供商

在设置页面中：

1. 找到 **AI 模型提供商** 或 **AI Provider** 设置项
2. 在下拉菜单中选择 **OpenAI API**（使用 GPT 系列模型）、**Claude API**（使用 Claude 系列模型）或 **Gemini API**（使用 Gemini 系列模型）

<img src="https://mintcdn.com/dashlyai/gmegcqBsMOcqIUJu/docs/assets/images/cn_integrations_chatbox/7c1a840e_settings-page.png?fit=max&auto=format&n=gmegcqBsMOcqIUJu&q=85&s=5896999ba8dc5dbf3665bc47ba06e584" alt="ChatBox 设置页面" width="1023" height="768" data-path="docs/assets/images/cn_integrations_chatbox/7c1a840e_settings-page.png" />

### 2.2 配置 API 信息

选择 **OpenAI API** 后，填写以下配置信息：

| 配置项                           | 填写内容                                |
| ----------------------------- | ----------------------------------- |
| **API Key**                   | 您的 ToAPIs API 密钥（`sk-xxxxxxxxxxxx`） |
| **API Host** 或 **API Domain** | `https://toapis.com`                |

<img src="https://mintcdn.com/dashlyai/gmegcqBsMOcqIUJu/docs/assets/images/cn_integrations_chatbox/10f0f475_api-config.png?fit=max&auto=format&n=gmegcqBsMOcqIUJu&q=85&s=5c8928de7f66a9948ab00f63452f7fde" alt="API 配置" width="1023" height="768" data-path="docs/assets/images/cn_integrations_chatbox/10f0f475_api-config.png" />

选择 **Claude API** 后，填写以下配置信息：

| 配置项                           | 填写内容                                |
| ----------------------------- | ----------------------------------- |
| **API Key**                   | 您的 ToAPIs API 密钥（`sk-xxxxxxxxxxxx`） |
| **API Host** 或 **API Domain** | `https://toapis.com/v1`             |

<img src="https://mintcdn.com/dashlyai/gmegcqBsMOcqIUJu/docs/assets/images/cn_integrations_chatbox/4ceb244f_claude.png?fit=max&auto=format&n=gmegcqBsMOcqIUJu&q=85&s=a63c42568ec8f7636a309af045945101" alt="claude模型" width="1023" height="768" data-path="docs/assets/images/cn_integrations_chatbox/4ceb244f_claude.png" />

选择 **Gemini API** 后，填写以下配置信息：

| 配置项                           | 填写内容                                |
| ----------------------------- | ----------------------------------- |
| **API Key**                   | 您的 ToAPIs API 密钥（`sk-xxxxxxxxxxxx`） |
| **API Host** 或 **API Domain** | `https://toapis.com/`               |

<img src="https://mintcdn.com/dashlyai/gmegcqBsMOcqIUJu/docs/assets/images/cn_integrations_chatbox/ac809bea_Gemini.png?fit=max&auto=format&n=gmegcqBsMOcqIUJu&q=85&s=b1895cf497120cc92b2342d8daaedab4" alt="Gemini" width="1023" height="768" data-path="docs/assets/images/cn_integrations_chatbox/ac809bea_Gemini.png" />

**重要提示：**

* 使用 OpenAI API 时，API Host 应填写 `https://toapis.com`（不包含 `/v1` 后缀）
* 使用 Claude API 时，API Host 应填写 `https://toapis.com/v1`（包含 `/v1` 后缀）
* 使用 Gemini API 时，API Host 应填写 `https://toapis.com/`（不包含 `/v1` 后缀）
* API Key 必须是从 ToAPIs 控制台获取的以 `sk-` 开头的密钥
* 确保您的 API 密钥有足够的余额

### 2.3 选择模型

配置完成后，在 **模型** 或 **Model** 下拉菜单中选择您要使用的模型：
**推荐模型：**

| 模型名称              | 模型 ID                          | 特点       |
| ----------------- | ------------------------------ | -------- |
| GPT-5             | `gpt-5`                        | 最新最强大的模型 |
| GPT-4o            | `gpt-4o` 或 `chatgpt-4o-latest` | 高质量对话    |
| GPT-4o Mini       | `gpt-4o-mini`                  | 快速且经济    |
| Claude Sonnet 4.5 | `claude-sonnet-4-5-20250929`   | 擅长代码和推理  |
| Claude Haiku 4.5  | `claude-haiku-4-5-20251001`    | 快速响应     |
| Gemini 2.0 Flash  | `gemini-2.0-flash-exp`         | 多模态支持    |

\*\*使用 Claude 模型的特殊说明：\*\*如果您选择使用 Claude 模型（如 `claude-sonnet-4-5-20250929` 或 `claude-haiku-4-5-20251001`），需要进行以下额外配置：

1. **切换到 Claude API 提供商**：
   * 在设置中将 **AI 模型提供商** 改为 **Claude API**
   * API Host 保持填写 `https://toapis.com/v1`
   * API Key 使用您的 ToAPIs API 密钥（`sk-xxxxxxxxxxxx`）
2. **或者添加自定义请求头**（如果使用 OpenAI API 提供商）：
   * 某些版本的 ChatBox 支持添加自定义 Headers
   * 在高级设置中添加请求头：`anthropic-version: 2023-06-01`

**推荐方式：** 使用 GPT 系列模型时选择 **OpenAI API**，使用 Claude 系列模型时选择 **Claude API**，使用 Gemini 系列模型时选择 **Gemini API**。
**性能建议：**

* 💰 **高性价比：** `gpt-4o-mini`、`claude-haiku-4-5-20251001`
* 🚀 **高性能：** `gpt-5`、`gpt-4o`、`claude-sonnet-4-5-20250929`
* ⚡ **快速响应：** `gemini-2.0-flash-exp`、`gpt-4o-mini`

## 第三步：开始使用

配置完成后，您就可以开始使用 ChatBox 与 AI 对话了：

1. 返回主界面
2. 在输入框中输入您的问题或需求
3. 按 `Enter` 或点击发送按钮
4. AI 将使用 ToAPIs 的模型为您生成回复

<img src="https://mintcdn.com/dashlyai/gmegcqBsMOcqIUJu/docs/assets/images/cn_integrations_chatbox/5dfc3202_chat-interface.png?fit=max&auto=format&n=gmegcqBsMOcqIUJu&q=85&s=beed007c5c26df47524ff4007f9d8034" alt="对话界面" width="1023" height="768" data-path="docs/assets/images/cn_integrations_chatbox/5dfc3202_chat-interface.png" />

### 调整模型参数（可选）

您可以根据需要调整以下参数：

| 参数              | 说明      | 推荐值              |
| --------------- | ------- | ---------------- |
| **Temperature** | 控制输出随机性 | 0.7（创意）/ 0.3（精确） |
| **Max Tokens**  | 最大输出长度  | 2000-4000        |
| **Top P**       | 核采样参数   | 0.9              |

## 高级功能

### 多会话管理

ChatBox 支持创建多个对话会话：

1. 点击 **新建对话** 按钮
2. 可以为不同的任务创建独立的会话
3. 在左侧会话列表中切换不同的对话

### 保存和导出对话

1. 右键点击对话会话
2. 选择 **导出** 选项
3. 可以导出为 Markdown、JSON 等格式

### 使用提示词模板

1. 在设置中找到 **提示词** 或 **Prompts** 设置
2. 可以保存常用的提示词模板
3. 在对话中快速调用预设的提示词

## 常见问题

### Q1: 无法连接到 ToAPIs 服务？

**解决方案：**

1. **检查 API Host**：
   * 确保填写的是 `https://toapis.com`
   * 不要添加 `/v1` 或其他路径
2. **验证 API Key**：
   * 确认 API Key 正确且以 `sk-` 开头
   * 在 [ToAPIs 控制台](https://toapis.com/console/token) 检查密钥是否有效
3. **检查网络连接**：
   * 确保能够访问 `https://toapis.com`
   * 如果在国内，可能需要配置代理

### Q2: 模型列表中没有显示 ToAPIs 的模型？

**解决方案：**

1. **手动输入模型名称**：
   * 在模型输入框中直接输入模型 ID
   * 例如：`gpt-4o`、`gpt-4o-mini`、`claude-sonnet-4-5-20250929`
2. **刷新模型列表**：
   * 重启 ChatBox 应用
   * 重新配置 API 信息

### Q3: 对话时出现错误提示？

**常见错误及解决方案：**

| 错误信息                        | 原因            | 解决方法               |
| --------------------------- | ------------- | ------------------ |
| `401 Unauthorized`          | API Key 无效或过期 | 重新获取 API Key 并更新配置 |
| `429 Too Many Requests`     | 请求频率超限        | 稍等片刻后重试            |
| `500 Internal Server Error` | 服务器临时故障       | 等待几分钟后重试           |
| `insufficient_quota`        | 账户余额不足        | 前往控制台充值            |

### Q4: 如何查看 API 使用情况和费用？

登录 [ToAPIs 控制台](https://toapis.com/console) 查看：

* 📊 API 调用统计
* 💰 费用明细
* 📈 使用趋势图表
* 🔍 详细的请求日志

### Q5: ChatBox 支持哪些平台？

ChatBox 支持多个平台：

* 🪟 **Windows** - Windows 10/11
* 🍎 **macOS** - macOS 10.15+
* 🐧 **Linux** - 各主流发行版
* 🌐 **Web** - 浏览器版本

## 使用技巧

### 1. 快捷键

充分利用 ChatBox 的快捷键提升效率：

| 快捷键                | 功能      |
| ------------------ | ------- |
| `Ctrl/Cmd + Enter` | 发送消息    |
| `Ctrl/Cmd + N`     | 新建对话    |
| `Ctrl/Cmd + K`     | 搜索对话    |
| `Ctrl/Cmd + ,`     | 打开设置    |
| `Ctrl/Cmd + /`     | 显示快捷键帮助 |

### 2. 优化提示词

编写更好的提示词以获得更好的回复：
**❌ 不好的提示：**
复制

```shiki 
帮我写代码

```

**✅ 好的提示：**
复制

```shiki 
请帮我用 Python 编写一个函数，实现以下功能：
1. 接收一个字符串列表作为输入
2. 过滤掉长度小于 3 的字符串
3. 返回按字母顺序排序的结果
请包含详细注释和示例用法

```

### 3. 利用对话历史

ChatBox 会保存对话历史：

* AI 会记住当前会话中的上下文
* 可以基于之前的回答继续提问
* 适合进行深入的探讨和迭代

### 4. 切换模型

根据不同任务切换合适的模型：

* **写作任务** - 使用 `gpt-4o` 或 `claude-sonnet-4-5`
* **代码任务** - 使用 `claude-sonnet-4-5`
* **快速问答** - 使用 `gpt-4o-mini`
* **多模态** - 使用 `gemini-2.0-flash-exp`

## 功能特性

使用 ChatBox + ToAPIs，您可以：

* 💬 **流畅对话** - 实时流式输出，体验更流畅
* 🎯 **多会话管理** - 同时管理多个独立对话
* 💾 **本地存储** - 对话记录保存在本地，保护隐私
* 📤 **导出对话** - 支持多种格式导出对话记录
* 🎨 **界面简洁** - 简洁美观的用户界面
* 🔒 **开源免费** - 完全开源，免费使用
* 🌍 **跨平台** - 支持 Windows、macOS、Linux
* 🚀 **性能优秀** - 轻量级应用，运行流畅

## 支持与帮助

如果您在使用过程中遇到任何问题：

* 📚 [ToAPIs 文档中心](https://docs.toapis.com)
* 📚 [ChatBox GitHub](https://github.com/Bin-Huang/chatbox)
* 💬 [Discord 社区](https://discord.gg/hvnszCrJ73)
* 🐦 [Twitter @toapisai](https://x.com/toapisai)
* 📧 技术支持：[zhihong@toapis.com](mailto:zhihong@toapis.com)

***

### [开始使用 ToAPIs](https://toapis.com)

立即注册 ToAPIs，获取您的 API 密钥，在 ChatBox 中开启 AI 之旅。


### [在 Cherry Studio 中使用 ToAPIs](./cherry-studio)

配置另一个 OpenAI 兼容客户端。

