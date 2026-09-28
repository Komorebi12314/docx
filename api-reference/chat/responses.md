> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Responses API

> OpenAI Responses API 格式，支持函数调用、内置工具与服务端多轮上下文管理

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


Responses API 是 OpenAI 推出的新一代 Agentic 接口，相比 Chat Completions 提供更强大的能力：

* **函数调用（Function Calling）**：模型可调用自定义函数
* **内置工具**：`web_search_preview`（联网搜索）等开箱即用
* **服务端多轮上下文**：通过 `previous_response_id` 自动维护对话历史，无需客户端传完整消息
* **推理力度控制**：通过 `reasoning.effort` 精确调节思考深度

> ⚠️ **注意**
>
> 标注为 **Responses Only** 的模型（如 `gpt-5-pro-official`、`gpt-5.3-codex-official`）仅支持此 API，不支持 Chat Completions。完整模型列表请参阅 [模型一览](./models)。


## Authorizations

### `Authorization`

`string` · 必填

使用 Bearer Token 认证

```
Authorization: Bearer YOUR_API_KEY
```

获取 API Key：访问 [API Key 管理页面](https://toapis.com/console/token)


## Body

### `model`

`string` · 必填

模型名称

示例：`"gpt-5-pro-official"`、`"gpt-5.3-codex-official"`、`"gpt-5.2-official"`


### `input`

`string | object[]` · 必填

用户输入，支持两种格式：

* **字符串**：简单文本输入
* **消息数组**：多轮对话格式

<details>
<summary>消息数组格式</summary>

**`role`** — `string` · 必填

消息角色：`user`、`assistant`、`developer`


**`content`** — `string | object[]` · 必填

消息内容，支持纯文本或包含图片的内容块数组


### `instructions`

`string`

系统指令，指导模型行为（等同于 Chat Completions 中的 system message）


### `stream`

`boolean` · 默认值：`false`

是否启用流式输出


### `max_output_tokens`

`integer`

生成内容的最大 token 数量


### `temperature`

`number` · 默认值：`1`

采样温度，范围 `0` \~ `2`


### `top_p`

`number` · 默认值：`1`

核采样概率阈值，范围 `0` \~ `1`


### `previous_response_id`

`string`

上一次响应的 ID，用于服务端自动拼接多轮上下文，无需客户端传完整历史消息


### `reasoning`

`object`

推理配置

<details>
<summary>reasoning</summary>

**`effort`** — `string`

推理力度：`high`、`medium`、`low`、`none`

值越高，模型思考越深入，消耗的 reasoning tokens 越多


### `tools`

`object[]`

可用工具列表

<details>
<summary>tools[n]</summary>

**`type`** — `string` · 必填

工具类型：`function`（自定义函数）、`web_search_preview`（联网搜索）


**`name`** — `string`

函数名称（`type` 为 `function` 时必填）


**`description`** — `string`

函数描述


**`parameters`** — `object`

函数参数的 JSON Schema


### `tool_choice`

`string` · 默认值：`auto`

工具选择策略：`auto`、`none`、`required`


## Response

### `id`

`string`

响应的唯一标识符（可用作 `previous_response_id`）


### `object`

`string`

固定为 `response`


### `status`

`string`

响应状态：`completed`、`failed`、`in_progress`


### `output`

`object[]`

输出项列表，可能包含多种类型：

* **`message`**：文本回复，包含 `content[].text`
* **`function_call`**：函数调用请求，包含 `name` 和 `arguments`
* **`reasoning`**：推理过程（当 `reasoning.effort` 非 `none` 时出现）
* **`web_search_call`**：联网搜索调用记录


### `usage`

`object`

token 消耗统计

* `usage.input_tokens`：输入 token 数
* `usage.output_tokens`：输出 token 数
* `usage.output_tokens_details.reasoning_tokens`：推理 token 数
* `usage.total_tokens`：总 token 数


### 请求示例

```bash cURL 
curl --request POST \
  --url https://toapis.com/v1/responses \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gpt-5.3-codex-official",
    "instructions": "你是一个专业的代码助手",
    "input": "用 Python 写一个快速排序"
  }'
```

```bash cURL（联网搜索） 
curl --request POST \
  --url https://toapis.com/v1/responses \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gpt-5.3-codex-official",
    "input": "2026年最流行的 AI 框架有哪些？",
    "tools": [{"type": "web_search_preview"}]
  }'
```

```bash cURL（函数调用） 
curl --request POST \
  --url https://toapis.com/v1/responses \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gpt-5-pro-official",
    "instructions": "你是一个天气助手",
    "input": "北京今天天气怎么样？",
    "tools": [
      {
        "type": "function",
        "name": "get_weather",
        "description": "获取指定城市的天气",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {"type": "string", "description": "城市名称"}
          },
          "required": ["location"]
        }
      }
    ]
  }'
```

```bash cURL（多轮对话） 
curl --request POST \
  --url https://toapis.com/v1/responses \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gpt-5.3-codex-official",
    "previous_response_id": "resp_abc123",
    "input": [
      {"role": "user", "content": "现在给这个函数加上错误处理"}
    ]
  }'
```

```python Python (openai SDK) 
from openai import OpenAI

client = OpenAI(
    api_key="your-ToAPIs-key",
    base_url="https://toapis.com/v1"
)

response = client.responses.create(
    model="gpt-5.3-codex-official",
    instructions="你是一个专业的代码助手",
    input="用 Python 写一个快速排序"
)

print(response.output[0].content[0].text)
```

```python Python（多轮对话） 
from openai import OpenAI

client = OpenAI(
    api_key="your-ToAPIs-key",
    base_url="https://toapis.com/v1"
)

response1 = client.responses.create(
    model="gpt-5.3-codex-official",
    instructions="你是一个专业的代码助手",
    input="写一个斐波那契函数"
)

response2 = client.responses.create(
    model="gpt-5.3-codex-official",
    previous_response_id=response1.id,
    input=[{"role": "user", "content": "加上输入验证"}]
)

print(response2.output[0].content[0].text)
```

```javascript JavaScript (openai SDK) 
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: "your-ToAPIs-key",
  baseURL: "https://toapis.com/v1",
});

const response = await client.responses.create({
  model: "gpt-5.3-codex-official",
  instructions: "你是一个专业的代码助手",
  input: "用 Python 写一个快速排序",
});

console.log(response.output[0].content[0].text);
```


### 响应示例

````json 200（文本响应） 
{
  "id": "resp_abc123",
  "object": "response",
  "status": "completed",
  "model": "gpt-5.3-codex-official",
  "output": [
    {
      "type": "message",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "```python\ndef quicksort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quicksort(right)\n```"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 25,
    "output_tokens": 80,
    "total_tokens": 105
  }
}
````

```json 200（函数调用） 
{
  "id": "resp_def456",
  "object": "response",
  "status": "completed",
  "model": "gpt-5-pro-official",
  "output": [
    {
      "type": "function_call",
      "name": "get_weather",
      "arguments": "{\"location\":\"Beijing\"}",
      "call_id": "call_abc123"
    }
  ],
  "usage": {
    "input_tokens": 85,
    "output_tokens": 24,
    "total_tokens": 109
  }
}
```

```json 400 
{
  "error": {
    "code": "invalid_request_error",
    "message": "The 'input' field is required.",
    "type": "invalid_request_error"
  }
}
```

