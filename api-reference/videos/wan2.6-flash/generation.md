> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan2.6 Flash 视频生成

> 使用阿里云万相 Wan2.6 Flash 极速版生成视频 — 支持图生视频和参考视频，速度更快

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 阿里云万相极速版视频生成模型
* 支持**图生视频**（Image-to-Video）和**参考视频**（Reference Video，r2v）两种模式
* **不支持**纯文本生成（必须提供图片或参考视频 URL）
* 支持 720p/1080p 分辨率，有声/无声选项（影响计费）
* 生成速度更快，适合快速预览和迭代

> ⚠️ **注意**
>
> **必须提供图片或参考视频 URL**：`image_urls`（图生视频）和 `metadata.reference_urls`（参考视频）必须提供其中之一，否则接口将返回错误。


## 路由逻辑

服务端根据请求参数自动选择上游模型：

| 提供的参数                             | 上游模式               |
| --------------------------------- | ------------------ |
| `metadata.reference_urls`（视频 URL） | 参考视频极速版（r2v-flash） |
| `image_urls`（图片）                  | 图生视频极速版（i2v-flash） |
| 仅 `prompt`                        | ❌ 返回错误             |

## 认证

### `Authorization`

`string` · 必填

所有接口均需要使用 Bearer Token 进行认证

获取 API Key：访问 [API Key 管理页面](https://toapis.com/console/token) 获取您的 API Key

使用时在请求头中添加：

```
Authorization: Bearer YOUR_API_KEY
```


## 请求参数

### `model`

`string` · 必填

视频生成模型名称，固定为 `wan2.6-flash`


### `image_urls`

`string[]`

参考图片 URL 数组（图生视频模式，仅支持 1 张图片）

**与 `metadata.reference_urls` 二选一必填**

**⚠️ 仅支持 URL 格式（不再支持 base64）**

* 公开可访问的图像 URL（http\:// 或 https\://）
* 可使用 [上传图片接口](../../uploads/images) 上传本地图片获取 URL

示例：`["https://example.com/image.jpg"]`


### `prompt`

`string`

视频内容描述（可选）

描述期望的动作或风格，帮助模型理解生成意图

示例：`"画面中的人物动了起来，向镜头微笑"`


### `resolution`

`string` · 默认值：`1080p`

视频分辨率

可选值：

* `720p` - 标清
* `1080p` - 高清（默认）

默认值：`1080p`

不同分辨率计费不同，请参考模型市场价格


### `duration`

`integer` · 默认值：`5`

视频时长（秒）

支持：`5`、`10`、`15`

默认值：`5`


### `audio`

`boolean` · 默认值：`true`

是否生成有声视频

* `true` - 生成有声视频（默认）
* `false` - 生成无声视频

**⚠️ 有声/无声计费标准不同，请确认后选择**

默认值：`true`


### `watermark`

`boolean`

在生成的视频上添加阿里云水印


### `metadata`

`object`

扩展参数

<details>
<summary>展开查看 metadata 字段</summary>

**`reference_urls`** — `string[]`

**参考视频（r2v）模式** — 参考视频 URL 数组

当提供此字段时，服务端路由到参考视频极速上游（wan2.6-r2v-flash）。模型将参考这些视频生成具有一致角色或场景的新视频。

* 每个条目必须是公开可访问的视频 URL（http\:// 或 https\://）

示例：`["https://cdn.example.com/ref1.mp4"]`

**注意：** 不能与 `image_urls` 同时使用


## 有声 vs 无声计费说明

| 模式                 | 720p 单价  | 1080p 单价 |
| ------------------ | -------- | -------- |
| 有声（`audio: true`）  | 0.3 元/秒  | 0.5 元/秒  |
| 无声（`audio: false`） | 0.15 元/秒 | 0.25 元/秒 |

## 响应

### `id`

`string`

唯一任务标识符，用于后续查询状态


### `object`

`string`

对象类型，固定为 `generation.task`


### `model`

`string`

使用的模型名称


### `status`

`string`

任务状态

* `queued` - 排队等待
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


## 使用场景

### 场景一：图生视频（有声）

```json 
{
  "model": "wan2.6-flash",
  "image_urls": ["https://example.com/photo.jpg"],
  "prompt": "画面中的人活跃起来",
  "resolution": "1080p",
  "duration": 5,
  "audio": true
}
```

### 场景二：图生视频（无声，降低成本）

```json 
{
  "model": "wan2.6-flash",
  "image_urls": ["https://example.com/photo.jpg"],
  "resolution": "720p",
  "duration": 5,
  "audio": false
}
```

### 场景三：参考视频（r2v-flash）

```json 
{
  "model": "wan2.6-flash",
  "prompt": "角色在沙发上看电影",
  "metadata": {
    "reference_urls": ["https://cdn.example.com/ref-character.mp4"]
  },
  "resolution": "1080p",
  "duration": 5,
  "audio": true
}
```

> 💡 **提示**
>
> **查询任务结果**
>
> 视频生成为异步任务。提交后返回 `task_id`，使用 [获取视频任务状态](../../tasks/video-status) 接口查询生成进度和结果。


### 请求示例

```bash cURL（图生视频） 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "wan2.6-flash",
    "image_urls": ["https://example.com/photo.jpg"],
    "prompt": "画面中的人活跃起来",
    "resolution": "1080p",
    "duration": 5,
    "audio": true
  }'
```

```bash cURL（参考视频） 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "wan2.6-flash",
    "prompt": "角色在沙发上看电影",
    "metadata": {
      "reference_urls": ["https://cdn.example.com/ref-character.mp4"]
    },
    "resolution": "1080p",
    "duration": 5,
    "audio": true
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
        "model": "wan2.6-flash",
        "image_urls": ["https://example.com/photo.jpg"],
        "prompt": "画面中的人活跃起来",
        "resolution": "1080p",
        "duration": 5,
        "audio": True
    }
)

task = response.json()
print(f"Task ID: {task['id']}")
print(f"Status: {task['status']}")
```

```javascript JavaScript 
const response = await fetch('https://toapis.com/v1/videos/generations', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-ToAPIs-key',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'wan2.6-flash',
    image_urls: ['https://example.com/photo.jpg'],
    prompt: '画面中的人活跃起来',
    resolution: '1080p',
    duration: 5,
    audio: true
  })
});

const task = await response.json();
console.log(`Task ID: ${task.id}`);
console.log(`Status: ${task.status}`);
```


### 响应示例

```json 200 
{
  "id": "video_01K2ABJPQ9A0Z6JZ3V8M9W6PZ",
  "object": "generation.task",
  "model": "wan2.6-flash",
  "status": "queued",
  "progress": 0,
  "created_at": 1768380224,
  "metadata": {}
}
```

