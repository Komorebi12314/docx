> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Azure Sora 2 Remix

> 使用 Azure Sora 2 模型对现有视频进行重混

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


Remix 功能允许您修改现有视频的特定方面，同时保留其核心元素。通过引用之前成功完成的视频 ID，并提供更新的提示词，系统会维持原始视频的框架、场景转换和视觉布局，同时实现您请求的更改。

> 💡 **小贴士**
>
> 为获得最佳效果，请将修改限制在一个明确的调整上。精确、聚焦的编辑能更好地保持与源素材的一致性，并最大限度地减少生成视觉缺陷的可能性。


## Authorizations

### `Authorization`

`string` · 必填

所有接口均需要使用 Bearer Token 进行认证

获取 API Key：访问 [API Key 管理页面](https://toapis.com/console/token) 获取您的 API Key

使用时在请求头中添加：

```
Authorization: Bearer YOUR_API_KEY
```


## Path Parameters

### `video_id`

`string` · 必填

之前已完成的视频 ID，用于进行 remix

示例：`"video_01K8SGYNNNVBQTXNR4MM964S7K"`


## Body

### `model`

`string` · 必填

视频生成模型名称

Azure Sora 2 remix 必须使用 `sora-2-official`

示例：`"sora-2-official"`


### `prompt`

`string` · 必填

重混视频的更新文本描述

描述您想对原始视频进行的具体更改。保持精确并专注于一个明确的修改。

示例：`"将色彩调整为青色、沙色和铁锈色，配合温暖的背光"`


## Response

### `id`

`string`

重混视频的唯一任务标识符


### `object`

`string`

对象类型，固定为 `video`


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


### `remixed_from_video_id`

`string`

被重混的原始视频 ID


### `seconds`

`string`

视频时长（秒）


### `size`

`string`

视频分辨率（如 "1280x720"）


### 请求示例

```bash cURL 
curl --request POST \
  --url https://toapis.com/v1/videos/video_01K8SGYNNNVBQTXNR4MM964S7K/remix \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "sora-2-official",
    "prompt": "将色彩调整为青色、沙色和铁锈色，配合温暖的背光"
  }'
```

```python Python 
import requests

video_id = "video_01K8SGYNNNVBQTXNR4MM964S7K"

response = requests.post(
    f"https://toapis.com/v1/videos/{video_id}/remix",
    headers={
        "Authorization": "Bearer your-ToAPIs-key",
        "Content-Type": "application/json"
    },
    json={
        "model": "sora-2-official",
        "prompt": "将色彩调整为青色、沙色和铁锈色，配合温暖的背光"
    }
)

task = response.json()
print(f"Remix 任务 ID: {task['id']}")
print(f"状态: {task['status']}")
print(f"重混自: {task.get('remixed_from_video_id')}")
```

```javascript JavaScript 
const videoId = "video_01K8SGYNNNVBQTXNR4MM964S7K";

const response = await fetch(`https://toapis.com/v1/videos/${videoId}/remix`, {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-ToAPIs-key',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'sora-2-official',
    prompt: '将色彩调整为青色、沙色和铁锈色，配合温暖的背光'
  })
});

const task = await response.json();
console.log(`Remix 任务 ID: ${task.id}`);
console.log(`状态: ${task.status}`);
console.log(`重混自: ${task.remixed_from_video_id}`);
```


### 响应示例

```json 200 
{
  "id": "video_68ff7cef76cc8190b7eab9395e936d9e",
  "object": "video",
  "model": "sora-2-official",
  "status": "queued",
  "progress": 0,
  "created_at": 1761574127,
  "remixed_from_video_id": "video_01K8SGYNNNVBQTXNR4MM964S7K",
  "seconds": "8",
  "size": "1280x720"
}
```

