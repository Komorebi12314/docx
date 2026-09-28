> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Gemini-2.5-Flash 图像生成

> 使用 Google Gemini 2.5 Flash 模型生成图像，快速高效

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* Google Gemini 2.5 Flash 高效图像生成模型 (Nano banana)
* 通过 model 参数选择 `gemini-2.5-flash-image-preview` 模型
* 支持文本到图像生成
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

`string` · 必填 · 默认值：`gemini-2.5-flash-image-preview`

图像生成模型名称

可用模型别名：`nano-banana`

示例：`"gemini-2.5-flash-image-preview"`


### `prompt`

`string` · 必填

图像生成的文本描述

最长 1000 个字符


### `size`

`string`

图像生成的尺寸比例

支持的格式：

| 值      | 说明   | 像素（参考）    |
| ------ | ---- | --------- |
| `1:1`  | 正方形  | 1024x1024 |
| `16:9` | 横向宽屏 | 1792x1024 |
| `9:16` | 竖向长图 | 1024x1792 |
| `4:3`  | 横向标准 | 1365x1024 |
| `3:4`  | 竖向标准 | 1024x1365 |
| `3:2`  | 横向相片 | 1536x1024 |
| `2:3`  | 竖向相片 | 1024x1536 |


### `n`

`integer` · 默认值：`1`

生成图像的数量

固定为 1

**⚠️ 注意：** 必须是纯数字（如 `1`），不要加引号，否则会报错


### `image_urls`

`object[]`

参考图像 URL 列表，用于图生图或图像编辑

<details>
<summary>详细字段说明</summary>

**`url`** — `string` · 必填

图像 URL 地址

**⚠️ 仅支持 URL 格式（不再支持 base64）**

* 公开可访问的图片 URL（http\:// 或 https\://）
* 示例：`https://example.com/image.jpg`
* 可使用 [上传图片接口](../../uploads/images) 上传本地图片获取 URL

**限制：**

* 单张图片不得超过 10MB
* 支持格式：.jpeg, .jpg, .png, .webp


**限制：** 最多 14 张图片


### `metadata`

`object`

元数据参数，用于传递额外的配置选项

<details>
<summary>支持的元数据字段</summary>

**`resolution`** — `string` · 默认值：`1K`

输出图像分辨率

支持的值：

* `1K` - 1K 分辨率（默认，唯一支持的选项）


**`orientation`** — `string`

图像方向

支持的值：

* `landscape` - 横向
* `portrait` - 竖向


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
    "model": "gemini-2.5-flash-image-preview",
    "prompt": "一只穿着宇航服的猫咪在月球上行走",
    "size": "1:1",
    "n": 1
  }'
```

```bash cURL (图生图示例) 
curl --request POST \
  --url https://toapis.com/v1/images/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gemini-2.5-flash-image-preview",
    "prompt": "将这只猫变成卡通风格",
    "size": "1:1",
    "n": 1,
    "image_urls": ["https://example.com/cat.jpg"]
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
        "model": "gemini-2.5-flash-image-preview",
        "prompt": "一只穿着宇航服的猫咪在月球上行走",
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
        "model": "gemini-2.5-flash-image-preview",
        "prompt": "将这只猫变成卡通风格",
        "size": "1:1",
        "n": 1,
        "image_urls": ["https://example.com/cat.jpg"]
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
    model: 'gemini-2.5-flash-image-preview',
    prompt: '一只穿着宇航服的猫咪在月球上行走',
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
    model: 'gemini-2.5-flash-image-preview',
    prompt: '将这只猫变成卡通风格',
    size: '1:1',
    n: 1,
    image_urls: ['https://example.com/cat.jpg']
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
  "model": "gemini-2.5-flash-image-preview",
  "status": "queued",
  "progress": 0,
  "created_at": 1703884800,
  "metadata": {}
}
```

