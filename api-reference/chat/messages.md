> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Anthropic Messages API

> 使用 Anthropic Messages API 原生格式与 Claude 系列模型对话

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 兼容 Anthropic Messages API 原生格式
* 支持 Anthropic 官方 SDK（Python / JavaScript）直接对接，仅需修改 `base_url`
* 支持流式输出（SSE）
* 支持多轮对话、系统提示词、视觉输入、工具调用

> 💡 **提示**
>
> 如果你已经在使用 OpenAI SDK，建议使用 [OpenAI 格式接口](./chat)。
> 如果你在使用 Anthropic SDK 或 Claude Code，推荐使用本接口。


## Authorizations

### `Authorization`

`string`

Bearer Token 认证，适用于直接 HTTP 调用

```
Authorization: Bearer YOUR_API_KEY
```


### `x-api-key`

`string`

API Key 认证，与 Anthropic SDK 兼容

```
x-api-key: YOUR_API_KEY
```


### `anthropic-version`

`string` · 默认值：`2023-06-01`

Anthropic API 版本号，使用 Anthropic SDK 时自动传入

推荐值：`2023-06-01`


## Body

### `model`

`string` · 必填

模型名称

支持所有 Claude 系列模型，例如：

* `claude-opus-4-6`
* `claude-sonnet-4-6`
* `claude-haiku-4-5`


### `messages`

`object[]` · 必填

对话消息列表，按时间顺序排列。只支持 `user` 和 `assistant` 角色，系统提示词请使用顶层 `system` 字段

<details>
<summary>messages[n]</summary>

**`role`** — `string` · 必填

消息角色，可选值：`user`、`assistant`


**`content`** — `string | object[]` · 必填

消息内容，字符串或内容块数组

<details>
<summary>内容块（content block）</summary>

**`type`** — `string` · 必填

内容类型：`text`（文本）或 `image`（图片）


**`text`** — `string`

文本内容，`type` 为 `text` 时必填


**`source`** — `object`

图片来源，`type` 为 `image` 时必填

<details>
<summary>source</summary>

**`type`** — `string` · 必填

图片来源类型：`base64` 或 `url`


**`media_type`** — `string`

MIME 类型，`type` 为 `base64` 时必填，例如 `image/jpeg`、`image/png`


**`data`** — `string`

Base64 编码的图片数据，`type` 为 `base64` 时必填


**`url`** — `string`

图片 URL，`type` 为 `url` 时必填


### `max_tokens`

`integer` · 必填

生成内容的最大 token 数量

* Claude Sonnet 4-6 最大支持 `64000`
* Claude Opus 4-6 最大支持 `32000`


### `system`

`string | object[]`

系统提示词，在顶层设置（不放在 `messages` 中）

支持字符串或内容块数组格式


### `stream`

`boolean` · 默认值：`false`

是否启用流式输出（Server-Sent Events）

* `true`：逐 token 流式返回，事件格式遵循 Anthropic SSE 规范
* `false`：等待完整响应后一次性返回


### `temperature`

`number` · 默认值：`1`

采样温度，控制输出随机性

范围：`0` \~ `1`


### `top_p`

`number`

核采样概率阈值

范围：`0` \~ `1`，建议不要同时设置 `temperature` 和 `top_p`


### `stop_sequences`

`string[]`

停止序列，遇到指定字符串时停止生成


## Response

### `id`

`string`

本次请求的唯一标识符，格式为 `msg_*`


### `type`

`string`

对象类型，固定为 `message`


### `role`

`string`

响应角色，固定为 `assistant`


### `content`

`object[]`

生成的内容块列表

* `content[].type`：内容类型，通常为 `text`
* `content[].text`：生成的文本内容


### `model`

`string`

实际使用的模型名称


### `stop_reason`

`string`

停止原因

* `end_turn`：模型正常结束
* `max_tokens`：达到 `max_tokens` 限制
* `stop_sequence`：触发了停止序列


### `usage`

`object`

本次请求的 token 消耗统计

* `usage.input_tokens`：输入 token 数
* `usage.output_tokens`：输出 token 数


### 请求示例

```bash cURL 
curl --request POST \
  --url https://toapis.com/v1/messages \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "claude-sonnet-4-6",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": "你好，请介绍一下你自己"
      }
    ]
  }'
```

```bash cURL（系统提示词） 
curl --request POST \
  --url https://toapis.com/v1/messages \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "claude-sonnet-4-6",
    "max_tokens": 1024,
    "system": "你是一个专业的代码助手，擅长 Python 和 Go 语言。",
    "messages": [
      {
        "role": "user",
        "content": "用 Python 写一个快速排序"
      }
    ]
  }'
```

```bash cURL（流式输出） 
curl --request POST \
  --url https://toapis.com/v1/messages \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "claude-sonnet-4-6",
    "max_tokens": 1024,
    "stream": true,
    "messages": [
      {
        "role": "user",
        "content": "解释一下什么是递归"
      }
    ]
  }'
```

```python Python (Anthropic SDK) 
import anthropic

client = anthropic.Anthropic(
    api_key="your-ToAPIs-key",
    base_url="https://toapis.com"
)

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "你好，请介绍一下你自己"}
    ]
)

print(message.content[0].text)
```

```python Python（带系统提示词） 
import anthropic

client = anthropic.Anthropic(
    api_key="your-ToAPIs-key",
    base_url="https://toapis.com"
)

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system="你是一个专业的代码助手，擅长 Python 和 Go 语言。",
    messages=[
        {"role": "user", "content": "用 Python 写一个快速排序"}
    ]
)

print(message.content[0].text)
```

```python Python（流式输出） 
import anthropic

client = anthropic.Anthropic(
    api_key="your-ToAPIs-key",
    base_url="https://toapis.com"
)

with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "解释一下什么是递归"}
    ]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

```javascript JavaScript (Anthropic SDK) 
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
  apiKey: "your-ToAPIs-key",
  baseURL: "https://toapis.com",
});

const message = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  messages: [{ role: "user", content: "你好，请介绍一下你自己" }],
});

console.log(message.content[0].text);
```

```javascript JavaScript（流式输出） 
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
  apiKey: "your-ToAPIs-key",
  baseURL: "https://toapis.com",
});

const stream = await client.messages.stream({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  messages: [{ role: "user", content: "解释一下什么是递归" }],
});

for await (const chunk of stream) {
  if (
    chunk.type === "content_block_delta" &&
    chunk.delta.type === "text_delta"
  ) {
    process.stdout.write(chunk.delta.text);
  }
}
```


### 响应示例

```json 200 
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "你好！我是 Claude，由 Anthropic 开发的 AI 助手。我可以帮助你回答问题、分析信息、编写代码、创作内容等。有什么我可以帮你的吗？"
    }
  ],
  "model": "claude-sonnet-4-6",
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 12,
    "output_tokens": 38
  }
}
```

```json 200（流式，SSE 事件示例） 
data: {"type":"message_start","message":{"id":"msg_01abc","type":"message","role":"assistant","content":[],"model":"claude-sonnet-4-6","stop_reason":null,"usage":{"input_tokens":12,"output_tokens":0}}}

data: {"type":"content_block_start","index":0,"content_block":{"type":"text","text":""}}

data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"你好"}}

data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"！我是"}}

data: {"type":"content_block_stop","index":0}

data: {"type":"message_delta","delta":{"stop_reason":"end_turn"},"usage":{"output_tokens":38}}

data: {"type":"message_stop"}
```

```json 400 
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "messages: field required"
  }
}
```

```json 401 
{
  "type": "error",
  "error": {
    "type": "authentication_error",
    "message": "Invalid API key"
  }
}
```

```json 429 
{
  "type": "error",
  "error": {
    "type": "rate_limit_error",
    "message": "Rate limit exceeded"
  }
}
```

