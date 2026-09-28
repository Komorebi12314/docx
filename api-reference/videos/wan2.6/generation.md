> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan2.6 视频生成

> 使用阿里云万相 Wan2.6 模型生成高质量视频 — 支持文生视频、图生视频和参考视频

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 阿里云万相视频生成模型
* 支持**三种模式**：文生视频（Text-to-Video）、图生视频（Image-to-Video）、参考视频（Reference Video，r2v）
* 服务端根据请求参数自动路由到合适的上游模型
* 支持 720p/1080p 分辨率，5/10/15 秒时长
* 非 Flash 版本视频默认带有声音

> ⚠️ **注意**
>
> **重要变更**：为了更好的性能和成本控制，我们不再支持在 `image_urls` 中直接传入 base64 图片数据。请先使用 [上传图片接口](../../uploads/images) 上传图片，获取 URL 后再调用本接口。


## 路由逻辑

服务端根据请求参数自动选择上游模型：

| 提供的参数                             | 上游模式      |
| --------------------------------- | --------- |
| `metadata.reference_urls`（视频 URL） | 参考视频（r2v） |
| `image_urls`（图片）                  | 图生视频（i2v） |
| 仅 `prompt`                        | 文生视频（t2v） |

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

视频生成模型名称，固定为 `wan2.6`


### `prompt`

`string` · 必填

视频内容描述

文生视频模式下必填；图生视频和参考视频模式下可选（描述期望的动作或风格）

示例：`"一只可爱的猫咪在阳光下伸懒腰"`


### `image_urls`

`string[]`

参考图片 URL 数组（图生视频模式，仅支持 1 张图片）

**⚠️ 仅支持 URL 格式（不再支持 base64）**

* 公开可访问的图像 URL（http\:// 或 https\://）
* 可使用 [上传图片接口](../../uploads/images) 上传本地图片获取 URL

示例：`["https://example.com/image.jpg"]`

**注意：** 不能与 `metadata.reference_urls` 同时使用


### `aspect_ratio`

`string` · 默认值：`16:9`

视频宽高比（适用于文生视频和参考视频模式）

可选值：

* `16:9` - 横屏（默认）
* `9:16` - 竖屏
* `1:1` - 方形
* `4:3` - 横屏
* `3:4` - 竖屏

默认值：`16:9`

**注意：** 图生视频模式不支持此参数


### `resolution`

`string` · 默认值：`1080p`

视频分辨率

可选值：

* `720p` - 标清
* `1080p` - 高清（默认）

默认值：`1080p`

不支持 480p。按秒计费，不同分辨率价格不同，详见模型市场


### `duration`

`integer` · 默认值：`5`

视频时长（秒）

支持：`5`、`10`、`15`

默认值：`5`


### `negative_prompt`

`string`

负面提示词，描述不希望出现的内容

示例：`"模糊, 低质量, 变形"`


### `seed`

`integer`

随机种子，用于复现结果

示例：`12345`


### `prompt_extend`

`boolean` · 默认值：`true`

自动扩展提示词

开启后系统会自动优化并丰富您的提示词，**默认已启用**，设为 `false` 可禁用


### `audio`

`boolean`

在视频中添加音频

非 Flash 的 Wan2.6 模型默认输出有声视频，设为 `true` 可显式启用


### `shot_type`

`string`

镜头类型（适用于文生视频和参考视频模式）

可选值：

* `single` - 单镜头
* `multi` - 多镜头（电影式剪辑）


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

当提供此字段时，服务端路由到参考视频上游（wan2.6-r2v）。模型将参考这些视频生成具有一致角色或场景的新视频。

* 每个条目必须是公开可访问的视频 URL（http\:// 或 https\://）

示例：`["https://cdn.example.com/ref-character.mp4"]`

**注意：** 不能与 `image_urls` 同时使用


## 分辨率与宽高比组合

| 宽高比  | 说明     | 720p 尺寸  | 1080p 尺寸  |
| ---- | ------ | -------- | --------- |
| 16:9 | 横屏（默认） | 1280×720 | 1920×1080 |
| 9:16 | 竖屏     | 720×1280 | 1080×1920 |
| 1:1  | 方形     | 960×960  | 1440×1440 |
| 4:3  | 横屏     | 1088×832 | 1632×1248 |
| 3:4  | 竖屏     | 832×1088 | 1248×1632 |

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

### 场景一：文生视频

```json 
{
  "model": "wan2.6",
  "prompt": "一只可爱的猫咪在草地上奔跑，阳光明媚",
  "aspect_ratio": "16:9",
  "resolution": "1080p",
  "duration": 5
}
```

### 场景二：图生视频

```json 
{
  "model": "wan2.6",
  "prompt": "猫咪开心地跑起来",
  "image_urls": ["https://example.com/cat.jpg"],
  "resolution": "1080p",
  "duration": 10
}
```

### 场景三：参考视频（r2v）

```json 
{
  "model": "wan2.6",
  "prompt": "角色挥手并向镜头微笑",
  "metadata": {
    "reference_urls": ["https://cdn.example.com/ref-character.mp4"]
  },
  "shot_type": "single",
  "resolution": "1080p",
  "duration": 5
}
```

### 场景四：文生视频（完整参数）

```json 
{
  "model": "wan2.6",
  "prompt": "一只金毛犬在向日葵田里奔跑",
  "negative_prompt": "模糊, 低质量, 变形",
  "aspect_ratio": "16:9",
  "resolution": "1080p",
  "duration": 10,
  "seed": 12345,
  "prompt_extend": true,
  "shot_type": "multi",
  "watermark": false
}
```

> 💡 **提示**
>
> **查询任务结果**
>
> 视频生成为异步任务。提交后返回 `task_id`，使用 [获取视频任务状态](../../tasks/video-status) 接口查询生成进度和结果。


### 请求示例

```bash cURL（文生视频） 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "wan2.6",
    "prompt": "一只可爱的猫咪在草地上奔跑",
    "aspect_ratio": "16:9",
    "resolution": "1080p",
    "duration": 5
  }'
```

```bash cURL（图生视频） 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "wan2.6",
    "prompt": "猫咪开心地跑起来",
    "image_urls": ["https://example.com/cat.jpg"],
    "resolution": "1080p",
    "duration": 10
  }'
```

```bash cURL（参考视频） 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "wan2.6",
    "prompt": "角色挥手并向镜头微笑",
    "metadata": {
      "reference_urls": ["https://cdn.example.com/ref-character.mp4"]
    },
    "resolution": "1080p",
    "duration": 5
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
        "model": "wan2.6",
        "prompt": "一只可爱的猫咪在草地上奔跑",
        "aspect_ratio": "16:9",
        "resolution": "1080p",
        "duration": 5
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
    model: 'wan2.6',
    prompt: '一只可爱的猫咪在草地上奔跑',
    aspect_ratio: '16:9',
    resolution: '1080p',
    duration: 5
  })
});

const task = await response.json();
console.log(`Task ID: ${task.id}`);
console.log(`Status: ${task.status}`);
```


### 响应示例

```json 200 
{
  "id": "video_01J9HA7JPQ9A0Z6JZ3V8M9W6PZ",
  "object": "generation.task",
  "model": "wan2.6",
  "status": "queued",
  "progress": 0,
  "created_at": 1768380224,
  "metadata": {
    "aspect_ratio": "16:9"
  }
}
```

