> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# GPT-4o 图像生成

> 使用 GPT-4o 模型生成图像，支持文本到图像和图像编辑

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 统一的图像生成 API 接口
* 通过 model 参数选择 `gpt-4o-image` 模型
* 支持文本到图像、图生图和图像编辑
* 异步任务管理，通过任务 ID 查询结果

> ⚠️ **注意**
>
> **重要变更**：为了更好的性能和成本控制，我们不再支持在 `image_urls` 中直接传入 base64 图片数据。请先使用 [上传图片接口](../../uploads/images) 上传图片，获取 URL 后再调用本接口。


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

`string` · 必填 · 默认值：`gpt-4o-image`

图像生成模型名称

示例：`"gpt-4o-image"`


### `prompt`

`string` · 必填

图像生成的文本描述

最长 1000 个字符


### `size`

`string` · 默认值：`1:1`

图像生成的尺寸比例

支持的格式：

* `1:1` - 正方形（默认）
* `2:3` - 竖版
* `3:2` - 横版


### `n`

`integer` · 默认值：`1`

生成图像的数量

支持 1、2、4，会根据生成数量进行预扣费

默认：1

**⚠️ 注意：** 必须输入纯数字（如 `1`），不要加引号，否则会报错


### `image_urls`

`string[]`

参考图像 URL 列表，用于图生图或图像编辑

**⚠️ 仅支持 URL 格式（不再支持 base64）**

* 公开可访问的图片 URL（http\:// 或 https\://）
* 可使用 [上传图片接口](../../uploads/images) 上传本地图片获取 URL

**限制：**

* 最多 5 张图片
* 单张图片不超过 10MB
* 支持格式：jpeg、jpg、png、webp


### `mask_url`

`string`

蒙版图像 URL（用于图像编辑）

* 必须是 PNG 格式
* 尺寸必须与参考图像匹配
* 不得超过 4MB


## Response

### `id`

`string`

任务唯一标识符，用于查询任务状态


### `object`

`string`

对象类型，固定为 `generation.task`


### `model`

`string`

使用的模型名称


### `status`

`string`

任务状态

* `queued` - 排队等待处理
* `in_progress` - 处理中
* `completed` - 成功完成
* `failed` - 失败


### `progress`

`integer`

任务进度百分比（0-100）


### `created_at`

`integer`

任务创建时间戳（Unix 时间戳）


### `metadata`

`object`

任务元数据


### 请求示例

```bash cURL 
curl --request POST \
  --url https://toapis.com/v1/images/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gpt-4o-image",
    "prompt": "星空下的古老城堡",
    "size": "1:1",
    "n": 1
  }'
```

```bash cURL (图生图) 
curl --request POST \
  --url https://toapis.com/v1/images/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gpt-4o-image",
    "prompt": "将这张图片转换为星空下的古老城堡风格",
    "size": "1:1",
    "n": 1,
    "image_urls": [
      "https://example.com/castle.jpg"
    ]
  }'
```

```bash cURL (图像编辑) 
curl --request POST \
  --url https://toapis.com/v1/images/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gpt-4o-image",
    "prompt": "在城堡上方添加烟花",
    "size": "1:1",
    "n": 1,
    "image_urls": [
      "https://example.com/castle.jpg"
    ],
    "mask_url": "https://example.com/mask.png"
  }'
```

```python Python 
import requests

response = requests.post(
    "https://toapis.com/v1/images/generations",
    headers={
        "Authorization": "Bearer your-ToAPIs-key",
        "Content-Type": "application/json"
    },
    json={
        "model": "gpt-4o-image",
        "prompt": "星空下的古老城堡",
        "size": "1:1",
        "n": 1
    }
)

task = response.json()
print(f"任务 ID: {task['id']}")
print(f"状态: {task['status']}")
```

```python Python (图生图) 
import requests

response = requests.post(
    "https://toapis.com/v1/images/generations",
    headers={
        "Authorization": "Bearer your-ToAPIs-key",
        "Content-Type": "application/json"
    },
    json={
        "model": "gpt-4o-image",
        "prompt": "将这张图片转换为星空下的古老城堡风格",
        "size": "1:1",
        "n": 1,
        "image_urls": ["https://example.com/castle.jpg"]
    }
)

task = response.json()
print(f"任务 ID: {task['id']}")
print(f"状态: {task['status']}")
```

```javascript JavaScript 
const response = await fetch('https://toapis.com/v1/images/generations', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-ToAPIs-key',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'gpt-4o-image',
    prompt: '星空下的古老城堡',
    size: '1:1',
    n: 1
  })
});

const task = await response.json();
console.log(`任务 ID: ${task.id}`);
console.log(`状态: ${task.status}`);
```

```javascript JavaScript (图生图) 
const response = await fetch('https://toapis.com/v1/images/generations', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-ToAPIs-key',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'gpt-4o-image',
    prompt: '将这张图片转换为星空下的古老城堡风格',
    size: '1:1',
    n: 1,
    image_urls: ['https://example.com/castle.jpg']
  })
});

const task = await response.json();
console.log(`任务 ID: ${task.id}`);
console.log(`状态: ${task.status}`);
```


### 响应示例

```json 200 
{
  "id": "task_img_abc123def456",
  "object": "generation.task",
  "model": "gpt-4o-image",
  "status": "queued",
  "progress": 0,
  "created_at": 1703884800,
  "metadata": {}
}
```

```json 400 
{
  "error": {
    "code": "invalid_request",
    "message": "The 'prompt' field is required.",
    "param": "prompt",
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

