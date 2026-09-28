> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Chat Completions

> 兼容 OpenAI 格式的文字对话接口，支持全部文字模型

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 兼容 OpenAI Chat Completions API 格式
* 通过 `model` 参数指定模型，所有支持的模型请参阅 [模型一览](./models)
* 支持流式输出（SSE）
* 支持多轮对话、系统提示词
* 部分模型支持视觉输入（图片）和深度思考模式

## 新增官方文本模型

可在此接口使用 `gemini-3.7-flash-official` 和 `gemini-3.8-flash-official`. 两者按 token 计费, 每百万输入 token $1.20, 输出 token $6.00, 缓存读取 token \$0.12 (USD). 分组或账户折扣以实际报价为准.

## Authorizations

### `Authorization`

`string` · 必填

所有接口均需要使用 Bearer Token 进行认证

获取 API Key：访问 [API Key 管理页面](https://toapis.com/console/token) 获取您的 API Key

使用时在请求头中添加：

```
Authorization: Bearer YOUR_API_KEY
```


## Body

### `model`

`string` · 必填

模型名称，所有支持的模型请参阅 [模型一览](./models)

示例：`"claude-sonnet-4-6"`、`"gpt-5"`、`"qwen3-max"`


### `messages`

`object[]` · 必填

对话消息列表，按时间顺序排列

<details>
<summary>messages[n]</summary>

**`role`** — `string` · 必填

消息角色，可选值 `system`、`user`、`assistant`


**`content`** — `string | object[]` · 必填

消息内容，两种格式：

* **字符串**：纯文本消息，适用于所有模型
* **内容块数组**：混合文本与图片，仅支持视觉输入的模型可用

<details>
<summary>内容块数组格式（content[n]）</summary>

**`type`** — `string` · 必填

内容块类型，可选值 `text` 或 `image_url`


**`text`** — `string`

文本内容，`type` 为 `text` 时必填


**`image_url`** — `object`

图片信息，`type` 为 `image_url` 时必填

<details>
<summary>image_url</summary>

**`url`** — `string` · 必填

图片 URL 或 Base64 数据（格式：`data:image/jpeg;base64,...`）


### `stream`

`boolean` · 默认值：`false`

是否启用流式输出（Server-Sent Events）

* `true`：逐 token 流式返回
* `false`：等待完整响应后一次性返回


### `max_tokens`

`integer`

生成内容的最大 token 数量

不设置时使用模型默认上限。GPT-5 系列会由网关兼容转换为 `max_completion_tokens`。


### `max_completion_tokens`

`integer`

GPT-5 系列推荐使用的最大输出 token 参数。


### `reasoning_effort`

`string`

推理力度。GPT-5.6 支持 `none`、`low`、`medium`、`high`、`xhigh`、`max`，默认 `medium`。


### `temperature`

`number` · 默认值：`1`

采样温度，控制输出随机性

* 范围：`0` \~ `2`
* 值越低输出越稳定，值越高输出越随机


### `top_p`

`number` · 默认值：`1`

核采样概率阈值

范围：`0` \~ `1`，建议不要同时修改 `temperature` 和 `top_p`


> ⚠️ **注意**
>
> GPT-5 系列请求会忽略 `temperature` 和 `top_p`。使用 GPT-5.6 时，请通过 `reasoning_effort`、提示词和输出格式约束结果。


### `stop`

`string | string[]`

停止序列，遇到指定字符串时停止生成

最多 4 个停止序列


## Response

### `id`

`string`

本次请求的唯一标识符


### `object`

`string`

对象类型，固定为 `chat.completion`


### `created`

`integer`

请求创建时间（Unix 时间戳）


### `model`

`string`

实际使用的模型名称


### `choices`

`object[]`

生成结果列表

* `choices[].message.role`：消息角色，固定为 `assistant`
* `choices[].message.content`：生成的文本内容
* `choices[].finish_reason`：结束原因，`stop` / `length` / `content_filter`
* `choices[].index`：结果索引


### `usage`

`object`

本次请求的 token 消耗统计

* `usage.prompt_tokens`：输入 token 数
* `usage.completion_tokens`：输出 token 数
* `usage.total_tokens`：总 token 数


### 请求示例

```bash cURL 
curl --request POST \
  --url https://toapis.com/v1/chat/completions \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "claude-sonnet-4-6",
    "messages": [
      {
        "role": "user",
        "content": "你好，请介绍一下你自己"
      }
    ]
  }'
```

```bash cURL（流式输出） 
curl --request POST \
  --url https://toapis.com/v1/chat/completions \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gpt-5",
    "messages": [
      {
        "role": "system",
        "content": "你是一个专业的代码助手"
      },
      {
        "role": "user",
        "content": "用 Python 写一个快速排序"
      }
    ],
    "stream": true
  }'
```

```bash cURL（图片输入） 
curl --request POST \
  --url https://toapis.com/v1/chat/completions \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "claude-sonnet-4-6",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "这张图片里有什么？"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "https://www.gstatic.com/webp/gallery/1.jpg"
            }
          }
        ]
      }
    ],
    "max_tokens": 300
  }'
```

```python Python (openai SDK) 
from openai import OpenAI

client = OpenAI(
    api_key="your-ToAPIs-key",
    base_url="https://toapis.com/v1"
)

response = client.chat.completions.create(
    model="claude-sonnet-4-6",  # 替换为任意支持的模型
    messages=[
        {"role": "user", "content": "你好，请介绍一下你自己"}
    ]
)

print(response.choices[0].message.content)
```

```python Python（流式输出） 
from openai import OpenAI

client = OpenAI(
    api_key="your-ToAPIs-key",
    base_url="https://toapis.com/v1"
)

stream = client.chat.completions.create(
    model="gpt-5",  # 替换为任意支持的模型
    messages=[
        {"role": "system", "content": "你是一个专业的代码助手"},
        {"role": "user", "content": "用 Python 写一个快速排序"}
    ],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

```javascript JavaScript (openai SDK) 
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: "your-ToAPIs-key",
  baseURL: "https://toapis.com/v1",
});

const response = await client.chat.completions.create({
  model: "claude-sonnet-4-6", // 替换为任意支持的模型
  messages: [{ role: "user", content: "你好，请介绍一下你自己" }],
});

console.log(response.choices[0].message.content);
```


### 响应示例

```json 200 
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1703884800,
  "model": "claude-sonnet-4-6",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "你好！我是 Claude，由 Anthropic 开发的 AI 助手。我可以帮助你回答问题、分析信息、编写代码、创作内容等。有什么我可以帮你的吗？"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 42,
    "total_tokens": 57
  }
}
```

```json 400 
{
  "error": {
    "code": "invalid_request_error",
    "message": "The 'messages' field is required.",
    "param": "messages",
    "type": "invalid_request_error"
  }
}
```

```json 401 
{
  "error": {
    "code": "unauthorized",
    "message": "Invalid API key",
    "type": "authentication_error"
  }
}
```

