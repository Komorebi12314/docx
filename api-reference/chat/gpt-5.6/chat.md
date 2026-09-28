> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# GPT-5.6 系列对话

> 通过 OpenAI 兼容 Chat Completions API 使用 GPT-5.6 Sol、Terra 和 Luna

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


GPT-5.6 是按质量、成本和吞吐量划分的模型家族。ToAPIs 当前提供以下明确模型 ID：

| 模型 ID           | 定位      | 推荐场景                  |
| --------------- | ------- | --------------------- |
| `gpt-5.6-sol`   | 旗舰质量    | 复杂推理、高价值代码任务、长上下文分析   |
| `gpt-5.6-terra` | 性能与成本均衡 | 通用生产流量、Agent 工作流、内容生成 |
| `gpt-5.6-luna`  | 高吞吐轻量模型 | 分类、抽取、路由、批处理和延迟敏感任务   |

> 💡 **提示**
>
> OpenAI 官方的 `gpt-5.6` 别名指向 Sol。ToAPIs 文档使用当前模型列表中可直接选择的明确 ID；如需别名，请先通过 [模型列表接口](../list-models) 确认账户是否已开放。


## 关键参数

### `model`

`string` · 必填

可选 `gpt-5.6-sol`、`gpt-5.6-terra` 或 `gpt-5.6-luna`。


### `messages`

`object[]` · 必填

OpenAI Chat Completions 消息数组，支持 `system`、`user` 和 `assistant` 角色。


### `reasoning_effort`

`string` · 默认值：`medium`

推理力度：`none`、`low`、`medium`、`high`、`xhigh`、`max`。

建议从 `medium` 开始，再用真实任务比较同等级和低一级配置。`max` 适合质量优先的困难任务，不建议作为所有请求的默认值。


### `max_completion_tokens`

`integer`

最大输出 token 数。GPT-5.6 最大可输出 128K token，实际可用量仍受账户、渠道和输入上下文限制。


### `stream`

`boolean` · 默认值：`false`

设为 `true` 时通过 SSE 流式返回结果。


> ⚠️ **注意**
>
> 当前 GPT-5 网关会忽略 `temperature` 和 `top_p`。请通过提示词、`reasoning_effort` 和明确的输出格式控制结果。


## 请求示例

```bash cURL 
curl --request POST \
  --url https://toapis.com/v1/chat/completions \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gpt-5.6-sol",
    "messages": [
      {"role": "system", "content": "你是一个严谨的代码审查助手。"},
      {"role": "user", "content": "检查这个数据库迁移方案的主要风险。"}
    ],
    "reasoning_effort": "high",
    "max_completion_tokens": 8192,
    "stream": true
  }'
```

```python Python 
from openai import OpenAI

client = OpenAI(
    api_key="your-ToAPIs-key",
    base_url="https://toapis.com/v1"
)

response = client.chat.completions.create(
    model="gpt-5.6-terra",
    messages=[
        {"role": "user", "content": "把这份需求整理成实施计划。"}
    ],
    reasoning_effort="medium",
    max_completion_tokens=4096
)

print(response.choices[0].message.content)
```


## 迁移建议

* GPT-5.5 或 GPT-5.4 旗舰任务优先评估 `gpt-5.6-sol`。
* 原本强调成本或延迟的任务先评估 Terra 或 Luna，不要全部切换到 Sol。
* 保留原有推理力度作为首轮基线，再测试低一级配置。
* Chat Completions 使用函数工具时，将有效推理力度设为 `none`；需要推理与工具协同时，应先确认账户的 Responses API 支持情况。

完整通用字段和响应格式参阅 [Chat Completions API](../chat)。
