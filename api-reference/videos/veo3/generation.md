> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Veo3 视频生成

> 使用 Google Veo3 模型生成高质量视频，支持异步任务管理

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 异步处理模式，返回任务ID用于后续查询
* 支持文本转视频、图生视频等多种生成模式
* 生成的视频链接，有效期为24小时，请尽快保存

> ⚠️ **注意**
>
> **重要变更**：为了更好的性能和成本控制，我们不再支持在 `image_urls` 中直接传入 base64 图片数据。请先使用 [上传图片接口](../../uploads/images) 上传图片，获取 URL 后再调用本接口。


## Authorizations

### `Authorization`

`string` · 必填

所有接口均需要使用Bearer Token进行认证

获取 API Key：访问 [API Key 管理页面](https://toapis.com/console/token) 获取您的 API Key

使用时在请求头中添加：

```
Authorization: Bearer YOUR_API_KEY
```


## Body

### `model`

`string` · 必填 · 默认值：`veo3.1-fast`

视频生成模型名称

可用模型：

* `veo3.1-fast` - 快速生成模型，适用于快速预览和迭代
* `veo3.1-quality` - 高质量生成模型，适用于最终制作
* `veo3.1-lite` - 轻量生成模型，适用于更低成本的快速生成

Example: `"veo3.1-fast"`


### `prompt`

`string` · 必填

视频生成的文本描述


### `duration`

`integer`

视频时长（秒）

固定值：`8`（VEO3 仅支持 8 秒时长）


### `aspect_ratio`

`string`

视频分辨率

支持的格式：

* `16:9` (横屏)
* `9:16` (竖屏)


### `image_urls`

`string[]`

用于图生视频的参考图像 URL 数组

**⚠️ 仅支持 URL 格式（不再支持 base64）**

* 公开可访问的图像 URL（http\:// 或 https\://）
* 可使用 [上传图片接口](../../uploads/images) 上传本地图片获取 URL

**限制：**

* 最大文件大小：10MB
* 支持格式：.jpeg、.jpg、.png、.webp


### `metadata`

`object`

VEO3 特有扩展参数

<details>
<summary>显示 metadata 字段</summary>

**`generation_type`** — `string`

视频生成类型

支持的类型：

* `frame` - 帧转视频（FL模式）
* `reference` - 参考图生视频

如果不传此参数，默认根据图片数量自动判断：2张为帧转视频，3张为参考图生视频

**注意：`veo3.1-quality` 模型不支持 `reference` 参考图模式**


**`resolution`** — `string`

视频分辨率

支持的值：

* `720p`（默认）
* `1080p`
* `4k`


**`enable_gif`** — `boolean`

启用 GIF 输出格式。默认：`false`

注意：GIF 和 1080p、4k 分辨率不能同时使用


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
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "veo3.1-fast",
    "prompt": "海豚在碧蓝海洋中跳跃",
    "duration": 8,
    "aspect_ratio": "16:9",
    "image_urls": ["https://example.com/start-frame.jpg", "https://example.com/end-frame.jpg"],
    "metadata": {
      "generation_type": "frame",
      "resolution": "1080p",
      "enable_gif": false
    }
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
        "model": "veo3.1-fast",
        "prompt": "海豚在碧蓝海洋中跳跃",
        "duration": 8,
        "aspect_ratio": "16:9",
        "image_urls": ["https://example.com/start-frame.jpg", "https://example.com/end-frame.jpg"],
        "metadata": {
            "generation_type": "frame",
            "resolution": "1080p",
            "enable_gif": False
        }
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
    model: 'veo3.1-fast',
    prompt: '海豚在碧蓝海洋中跳跃',
    duration: 8,
    aspect_ratio: '16:9',
    image_urls: ['https://example.com/start-frame.jpg', 'https://example.com/end-frame.jpg'],
    metadata: {
      generation_type: 'frame',
      resolution: '1080p',
      enable_gif: false
    }
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
  "model": "veo3.1-fast",
  "status": "queued",
  "progress": 0,
  "created_at": 1768380224,
  "metadata": {
    "aspect_ratio": "16:9"
  }
}
```

