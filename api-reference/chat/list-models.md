> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# 列出模型

> 查询当前 API Key 可用的模型列表，兼容 OpenAI Models API

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 兼容 OpenAI Models API 格式
* 返回当前 API Key 与用户组可用的模型
* 默认返回文字模型，可通过 `type=all` 获取全部类型模型
* 可按模型类型筛选文字、图片、视频或音频模型

获取当前 API Key 可访问的模型列表。返回结果会根据令牌模型限制、用户组、可用渠道和模型计费配置动态过滤。

## Authorizations

### `Authorization`

`string` · 必填

所有接口均需要使用 Bearer Token 进行认证

获取 API Key：访问 [API Key 管理页面](https://toapis.com/console/token) 获取您的 API Key

使用时在请求头中添加：

```
Authorization: Bearer YOUR_API_KEY
```


## Query Parameters

### `type`

`string` · 默认值：`text`

模型类型筛选。

可选值：

* `text` 或 `chat`：仅返回文字对话模型
* `image`：仅返回图片模型
* `video`：仅返回视频模型
* `audio`：仅返回音频模型
* `all`：返回全部可用模型

不传时默认只返回文字模型。


## Response

### `success`

`boolean`

请求是否成功。


### `object`

`string`

列表对象类型，固定为 `list`。


### `data`

`object[]`

模型列表。

<details>
<summary>data[n]</summary>

**`id`** — `string`

模型 ID，用于请求其他接口时的 `model` 参数。


**`object`** — `string`

对象类型，固定为 `model`。


**`created`** — `integer`

模型创建时间戳。部分自定义模型会返回平台默认时间戳。


**`owned_by`** — `string`

模型所属供应商或渠道名称。


**`supported_endpoint_types`** — `string[]`

模型支持的接口类型。不同模型可能支持 Chat Completions、Responses、图片、视频等不同端点。


### 请求示例

```bash cURL 
curl --request GET \
  --url 'https://toapis.com/v1/models' \
  --header 'Authorization: Bearer <token>'
```

```bash cURL（获取全部类型） 
curl --request GET \
  --url 'https://toapis.com/v1/models?type=all' \
  --header 'Authorization: Bearer <token>'
```

```python Python 
import requests

API_BASE = 'https://toapis.com'
API_KEY = 'sk-xxxxxxxxxxxxxxxxxxxxxx'

headers = {
    'Authorization': f'Bearer {API_KEY}'
}

response = requests.get(f'{API_BASE}/v1/models', headers=headers)
data = response.json()

if data.get('success'):
    for model in data.get('data', []):
        print(model['id'])
else:
    print(data)
```

```javascript JavaScript 
const API_BASE = 'https://toapis.com';
const API_KEY = 'sk-xxxxxxxxxxxxxxxxxxxxxx';

async function listModels(type = 'text') {
  const url = new URL('/v1/models', API_BASE);
  if (type) url.searchParams.set('type', type);

  const response = await fetch(url, {
    headers: {
      Authorization: `Bearer ${API_KEY}`,
    },
  });

  const data = await response.json();
  console.log(data.data?.map((model) => model.id));
  return data;
}

listModels('all');
```


### 响应示例

```json 
{
  "success": true,
  "object": "list",
  "data": [
    {
      "id": "claude-sonnet-4-6",
      "object": "model",
      "created": 1626777600,
      "owned_by": "anthropic",
      "supported_endpoint_types": ["chat_completions", "responses"]
    },
    {
      "id": "gpt-5",
      "object": "model",
      "created": 1626777600,
      "owned_by": "openai",
      "supported_endpoint_types": ["chat_completions"]
    }
  ]
}
```


## 说明

* 如果 API Key 配置了模型限制，只会返回该令牌允许访问的模型。
* 如果不传 `type`，视频和音频等异步任务模型不会出现在默认结果中。
* 如果需要获取图片、视频、音频等全部可用模型，请使用 `GET /v1/models?type=all`。
