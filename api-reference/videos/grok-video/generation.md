> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Grok 视频生成

> 使用 Grok Video 模型生成高质量视频

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* Grok Video 视频生成模型
* 通过 model 参数选择 `grok-video-1.0` 模型
* 支持文本到视频、图生视频
* 异步任务管理，通过任务 ID 查询结果

> ⚠️ **注意**
>
> **重要变更**：为了更好的性能和成本控制，我们不再支持在 `reference_images` 中直接传入 base64 图片数据。请先使用 [上传图片接口](../../uploads/images) 上传图片，获取 URL 后再调用本接口。


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

`string` · 必填 · 默认值：`grok-video-1.0`

视频生成模型名称

支持的模型：

* `grok-video-1.0` - Grok 视频生成模型

示例：`"grok-video-1.0"`


### `prompt`

`string` · 必填

视频生成的文本描述


### `duration`

`integer` · 默认值：`8`

视频时长（秒）

支持范围：`1`–`15` 秒


### `resolution`

`string` · 默认值：`720p`

视频分辨率

支持的值：`480p`、`720p`


### `aspect_ratio`

`string`

视频宽高比

支持的格式：

* `16:9` (横屏)
* `9:16` (竖屏)
* `3:2` (横屏)
* `2:3` (竖屏)
* `1:1` (方形)


### `image`

`string`

可选主图 URL。仅支持公网可访问的 `http://` 或 `https://` 地址。


### `reference_images`

`string[]`

可选参考图 URL 数组，可用于人物、服装和场景一致性参考。

* 仅支持公网 URL，不支持 base64
* `image` 与 `reference_images` 合计最多 8 张
* 可使用 [上传图片接口](../../uploads/images) 上传本地图片获取 URL


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


### `created_at`

`integer`

任务创建时间戳（Unix 时间戳）


### `progress`

`integer`

任务进度，提交成功时通常为 `0`


### `metadata`

`object`

任务元数据


### 请求示例

```bash cURL（文生视频） 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "grok-video-1.0",
    "prompt": "一只金毛犬在草地上奔跑，阳光明媚",
    "duration": 10,
    "resolution": "720p",
    "aspect_ratio": "16:9"
  }'
```

```bash cURL（图生视频） 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "grok-video-1.0",
    "prompt": "让这只狗动起来，在草地上奔跑",
    "image": "https://example.com/dog.jpg",
    "reference_images": [
      "https://example.com/clothes.jpg",
      "https://example.com/scene.jpg"
    ],
    "duration": 10,
    "resolution": "480p",
    "aspect_ratio": "16:9"
  }'
```

```python Python 
import requests

response = requests.post(
    "https://toapis.com/v1/videos/generations",
    headers={
        "Authorization": "Bearer your-ToAPIs-key",
        "Content-Type": "application/json"
    },
    json={
        "model": "grok-video-1.0",
        "prompt": "一只金毛犬在草地上奔跑，阳光明媚",
        "duration": 10,
        "resolution": "720p",
        "aspect_ratio": "16:9"
    }
)

task = response.json()
print(f"任务 ID: {task['id']}")
print(f"状态: {task['status']}")
```

```javascript JavaScript 
const response = await fetch('https://toapis.com/v1/videos/generations', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-ToAPIs-key',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'grok-video-1.0',
    prompt: '一只金毛犬在草地上奔跑，阳光明媚',
    duration: 10,
    resolution: '720p',
    aspect_ratio: '16:9'
  })
});

const task = await response.json();
console.log(`任务 ID: ${task.id}`);
console.log(`状态: ${task.status}`);
```


### 响应示例

```json 200 
{
  "id": "video_abc123def456",
  "object": "generation.task",
  "model": "grok-video-1.0",
  "status": "queued",
  "progress": 0,
  "created_at": 1768380224,
  "metadata": {}
}
```

