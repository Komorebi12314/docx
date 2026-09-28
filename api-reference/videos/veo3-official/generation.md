> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Veo3 Official 视频生成

> 使用 Google Veo3 官方直连模型生成高质量视频，支持音频生成、首尾帧控制等高级功能

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 异步处理模式，返回任务ID用于后续查询
* 直连 Google Vertex AI，支持 Veo 原生全部参数
* 支持文生视频、图生视频、首尾帧插值等多种生成模式
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

`string` · 必填 · 默认值：`Veo3.1-quality-official`

视频生成模型名称

可用模型：

* `Veo3.1-quality-official` - 高质量生成模型，适用于最终制作
* `Veo3.1-fast-official` - 快速生成模型，适用于快速预览和迭代
* `Veo3.1-lite-official` - Lite 720p
  Example: `"Veo3.1-quality-official"`


### `prompt`

`string` · 必填

视频生成的文本描述


### `duration`

`integer`

视频时长（秒）

支持的值：

* `4` - 4 秒
* `6` - 6 秒
* `8` - 8 秒（默认）


### `size`

`string`

视频宽高比

支持的格式：

* `16:9` (横屏，默认)
* `9:16` (竖屏)


### `resolution`

`string`

视频分辨率

支持的值：

* `720p`（默认）
* `1080p`
* `4k`（预览）


### `image_urls`

`string[]`

图生视频的**首帧参考图**，视频将从该图像开始生成。仅使用数组中的第一个 URL。

**⚠️ 仅支持 URL 格式（不再支持 base64）**

* 公开可访问的图像 URL（http\:// 或 https\://）
* 可使用 [上传图片接口](../../uploads/images) 上传本地图片获取 URL

**限制：**

* 最大文件大小：10MB
* 支持格式：.jpeg、.jpg、.png、.webp

> ⚠️ **注意**
>
> `image_urls` 与 `metadata.referenceImages` **不可同时使用**。如果同时传入，`image_urls`（首帧）优先，`referenceImages` 将被忽略。


### `metadata`

`object`

Veo3 Official 特有扩展参数

<details>
<summary>显示 metadata 字段</summary>

**`generateAudio`** — `boolean`

是否生成音频。默认：`false`

启用后视频将包含 AI 生成的音效和环境音


**`negativePrompt`** — `string`

负面提示词，描述不希望在视频中出现的内容

Example: `"模糊, 低质量, 畸变"`


**`personGeneration`** — `string`

人物生成安全设置

支持的值：

* `allow_adult` - 允许生成成年人
* `dont_allow` - 不允许生成人物


**`lastFrame`** — `string`

尾帧图片 URL，用于首尾帧插值生成视频

**必须**与 `image_urls`（首帧）配合使用，生成从首帧到尾帧的过渡视频。单独使用无效。


**`referenceImages`** — `string[]`

素材/风格参考图 URL 数组，视频内容将参考这些图片的视觉风格和元素进行生成（不作为视频起始帧）

**限制：最多 3 张**

**⚠️ 不可与 `image_urls` 同时使用**——二者在 Veo API 中互斥。如需首帧控制，请使用 `image_urls`。


**`compressionQuality`** — `string`

视频压缩质量

支持的值：

* `optimized`（默认）- 优化压缩
* `lossless` - 无损压缩


**`resizeMode`** — `string`

图生视频时的图片调整模式

支持的值：

* `pad` - 填充模式，保持原始比例
* `crop` - 裁剪模式，填满画面


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
    "model": "Veo3.1-quality-official",
    "prompt": "海豚在碧蓝海洋中跳跃，溅起水花，阳光洒在海面上",
    "duration": 8,
    "size": "16:9",
    "resolution": "1080p",
    "metadata": {
      "generateAudio": true,
      "negativePrompt": "模糊, 低质量"
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
        "model": "Veo3.1-quality-official",
        "prompt": "海豚在碧蓝海洋中跳跃，溅起水花，阳光洒在海面上",
        "duration": 8,
        "size": "16:9",
        "resolution": "1080p",
        "metadata": {
            "generateAudio": True,
            "negativePrompt": "模糊, 低质量"
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
    model: 'Veo3.1-quality-official',
    prompt: '海豚在碧蓝海洋中跳跃，溅起水花，阳光洒在海面上',
    duration: 8,
    size: '16:9',
    resolution: '1080p',
    metadata: {
      generateAudio: true,
      negativePrompt: '模糊, 低质量'
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
  "model": "Veo3.1-quality-official",
  "status": "queued",
  "progress": 0,
  "created_at": 1768380224,
  "metadata": {}
}
```

