> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Azure Sora 2 视频生成

> 使用 Azure Sora 2 模型生成高质量视频

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* Azure Sora 2 视频生成模型（Azure OpenAI 官方端点）
* 通过 model 参数选择 `sora-2-official`
* 支持文本到视频、图生视频、remix
* 异步任务管理，通过任务 ID 查询结果

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

视频生成模型名称

支持的模型：

* `sora-2-official` - Azure Sora 2 官方模型

示例：`"sora-2-official"`


### `prompt`

`string` · 必填

视频生成的自然语言描述

包含镜头类型、主体、动作、场景、光线和相机运动，以减少歧义。保持描述单一目的以获得最佳效果。

示例：`"一只金毛犬在草地上奔跑，阳光明媚"`


### `duration`

`integer` · 默认值：`4`

视频时长（秒）

支持的值：

* `4` - 4 秒
* `8` - 8 秒
* `12` - 12 秒

默认值：`4`

示例：`12`


### `aspect_ratio`

`string` · 默认值：`9:16`

视频宽高比

支持的格式：

* `16:9` (横屏，1280×720)
* `9:16` (竖屏，720×1280)

默认值：`9:16`


### `image_urls`

`string[]`

用于图生视频的参考图像 URL 数组

**⚠️ 仅支持 URL 格式**

* 公开可访问的图像 URL（http\:// 或 https\://）
* 可使用 [上传图片接口](../../uploads/images) 上传本地图片获取 URL
* 仅使用第一张图片作为参考
* 支持格式：JPEG、PNG、WebP
* **图片尺寸必须为 1280×720（16:9）或 720×1280（9:16）**


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

任务元数据，包含尺寸和时长信息


### 请求示例

```bash cURL（文生视频） 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "sora-2-official",
    "prompt": "一只金毛犬在草地上奔跑，阳光明媚",
    "duration": 12,
    "aspect_ratio": "16:9"
  }'
```

```bash cURL（图生视频） 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "sora-2-official",
    "prompt": "让这只狗动起来，在草地上奔跑",
    "image_urls": ["https://example.com/dog.jpg"],
    "duration": 8,
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
        "model": "sora-2-official",
        "prompt": "一只金毛犬在草地上奔跑，阳光明媚",
        "duration": 12,
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
    model: 'sora-2-official',
    prompt: '一只金毛犬在草地上奔跑，阳光明媚',
    duration: 12,
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
  "id": "video_01K8SGYNNNVBQTXNR4MM964S7K",
  "object": "generation.task",
  "model": "sora-2-official",
  "status": "queued",
  "progress": 0,
  "created_at": 1768380224,
  "metadata": {
    "size": "1280x720",
    "seconds": "12"
  }
}
```

