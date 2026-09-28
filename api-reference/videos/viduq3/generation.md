> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Vidu Q3 视频生成

> 使用 Vidu Q3 系列模型生成视频，支持文生视频、图生视频、首尾帧、参考生成和 Subjects 生成

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 异步任务接口，提交后返回任务 ID
* 支持模型：`viduq3-pro`、`viduq3-turbo`、`viduq3`
* `viduq3-pro`：高质量模型，支持音视频同步和分镜视频生成
* `viduq3-turbo`：快速模型，支持智能场景切换，生成速度最快，性价比最高
* `viduq3`：多机位一致性最优，支持智能镜头切换和多参考图生成

> ⚠️ **注意**
>
> 请传入公网可访问的图片 URL。不要在 `image_urls` 中直接传 base64 图片数据；本地图片请先使用 [上传图片接口](../../uploads/images) 获取 URL。


## 认证

### `Authorization`

`string` · 必填

所有接口均需要使用 Bearer Token 认证。

```
Authorization: Bearer YOUR_API_KEY
```


## 请求参数

### `model`

`string` · 必填

Vidu Q3 模型名称。

可选值：

* `viduq3-pro` - 高质量模型，支持音视频同步和分镜视频生成
* `viduq3-turbo` - 快速模型，支持智能场景切换，生成速度最快
* `viduq3` - 多机位一致性最优，适用于多参考图/Subjects 生成


### `prompt`

`string` · 必填

视频提示词，最大 **5000 字符**。

描述主体、动作、场景、镜头和风格。使用 subjects 时可通过 `@name` 引用主体。

示例：`"一只猫咪在弹钢琴，镜头缓缓推近，电影质感"`


### `duration`

`integer` · 默认值：`5`

视频时长，单位秒。

* `viduq3-pro` / `viduq3-turbo`：`1` 到 `16`
* `viduq3`：`3` 到 `16`


### `resolution`

`string` · 默认值：`720p`

视频分辨率。

可选值：

* `540p`
* `720p`
* `1080p`


### `aspect_ratio`

`string`

视频宽高比。

常用值：`16:9`、`9:16`、`1:1`

Q3 系列模型支持任意宽高比。传入 `image_urls` 时，宽高比通常由参考图片决定。


### `image_urls`

`string[]`

参考图片 URL 数组。

* `viduq3-pro` / `viduq3-turbo`
  * 不传：文生视频
  * 传 1 张：图生视频，图片作为首帧
  * 传 2 张：首尾帧，第一张为首帧，第二张为尾帧
* `viduq3`
  * 必填，最多 7 张参考图片

示例：`["https://example.com/reference.jpg"]`


### `audio`

`boolean`

是否启用音视频输出。

* 所有 Q3 模型默认 `true`

设为 `true` 时，系统根据提示词生成语音和背景音效。


### `seed`

`integer`

随机种子，用于在相同参数下复现相近结果。


### `metadata`

`object`

扩展参数，用于传递官方 API 支持但未作为顶层字段暴露的参数。

<details>
<summary>显示 metadata 字段</summary>

**`subjects`** — `array`

主体列表（Subjects 模式，仅 `viduq3` 支持）。每个主体包含 `name` 和 `images` 字段。

* 最多 7 个主体
* 每个主体最多 3 张图片
* 使用时在 prompt 中通过 `@name` 引用主体

示例：

```json 
[
  {"name": "cat", "images": ["https://example.com/cat.jpg"]},
  {"name": "dog", "images": ["https://example.com/dog.jpg"]}
]
```


**`auto_subjects`** — `boolean`

是否启用智能实体库能力，默认 `false`。


**`voice_id`** — `string`

语音 ID，用于指定视频中的语音角色。系统会自动推荐合适的语音。


**`audio_type`** — `string`

音频类型，`audio` 为 `true` 时有效。

可选值：

* `all` - 音效+人声（默认）
* `speech_only` - 仅人声
* `sound-effect_only` - 仅音效


**`off_peak`** — `boolean`

闲时模式，默认 `false`。

* `true`：闲时生成，消耗更少积分
* 闲时任务将在 48 小时内生成，未完成自动取消并退还积分
* Q3 模型在 `audio=true` 时支持闲时任务


**`payload`** — `string`

透传参数，不做处理仅传递数据，最大 1048576 字符。


**`callback_url`** — `string`

ToAPIs 最终任务 Webhook。需先配置 Token URL 和签名密钥；详见 [任务 Webhook](/docs/cn/api-reference/webhooks/task-webhooks)。


## 模型选择

| 模型             | 适用场景             | 图片输入      | 分辨率                       | 时长    |
| -------------- | ---------------- | --------- | ------------------------- | ----- |
| `viduq3-pro`   | 高质量文生/图生/首尾帧     | 可选，最多 2 张 | `540p` / `720p` / `1080p` | 1-16s |
| `viduq3-turbo` | 快速文生/图生/首尾帧      | 可选，最多 2 张 | `540p` / `720p` / `1080p` | 1-16s |
| `viduq3`       | 多参考图/Subjects 生成 | 必填，最多 7 张 | `540p` / `720p` / `1080p` | 3-16s |

## 计费区分

Vidu Q3 按模型、分辨率和生成类型计费：

* `viduq3-pro`：高质量档，价格约为 turbo 的 2 倍
* `viduq3-turbo`：快速档，性价比最高
* `viduq3`：多参考图生成，按参考生成计费

## 响应

### `id`

`string`

任务 ID，用于查询任务状态。


### `object`

`string`

对象类型，通常为 `generation.task`。


### `model`

`string`

本次请求使用的模型名称。


### `status`

`string`

任务状态：`queued`、`in_progress`、`completed` 或 `failed`。


### `created_at`

`integer`

任务创建时间戳。


## 示例

### 文生视频

```json 
{
  "model": "viduq3-pro",
  "prompt": "一只猫咪在弹钢琴，镜头缓缓推近，电影质感",
  "duration": 8,
  "resolution": "1080p",
  "aspect_ratio": "16:9",
  "audio": true
}
```

### 图生视频

```json 
{
  "model": "viduq3-turbo",
  "prompt": "让图片中的人物缓缓转身并微笑",
  "image_urls": ["https://example.com/portrait.jpg"],
  "duration": 5,
  "resolution": "720p"
}
```

### 首尾帧

```json 
{
  "model": "viduq3-pro",
  "prompt": "人物从站立自然坐下，动作流畅",
  "image_urls": [
    "https://example.com/first-frame.jpg",
    "https://example.com/last-frame.jpg"
  ],
  "duration": 8,
  "resolution": "720p"
}
```

### 多参考图生成视频

```json 
{
  "model": "viduq3",
  "prompt": "保持参考图中的角色一致，在未来城市街道中行走",
  "image_urls": [
    "https://example.com/character-front.jpg",
    "https://example.com/character-side.jpg"
  ],
  "duration": 6,
  "resolution": "1080p"
}
```

### Subjects 模式

```json 
{
  "model": "viduq3",
  "prompt": "@cat 和 @dog 在公园里奔跑，阳光明媚",
  "image_urls": ["https://example.com/park-bg.jpg"],
  "duration": 8,
  "resolution": "720p",
  "audio": true,
  "metadata": {
    "subjects": [
      {"name": "cat", "images": ["https://example.com/cat.jpg"]},
      {"name": "dog", "images": ["https://example.com/dog.jpg"]}
    ],
    "audio_type": "all"
  }
}
```

> 💡 **提示**
>
> 视频生成为异步任务。提交后使用 [获取视频任务状态](../../tasks/video-status) 查询进度和结果。


### 请求示例

```bash cURL 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "viduq3-pro",
    "prompt": "一只猫咪在弹钢琴，镜头缓缓推近，电影质感",
    "duration": 8,
    "resolution": "1080p",
    "aspect_ratio": "16:9",
    "audio": true
  }'
```

```python Python 
import requests

response = requests.post(
    "https://toapis.com/v1/videos/generations",
    headers={
        "Authorization": "Bearer <token>",
        "Content-Type": "application/json",
    },
    json={
        "model": "viduq3-pro",
        "prompt": "一只猫咪在弹钢琴，镜头缓缓推近，电影质感",
        "duration": 8,
        "resolution": "1080p",
        "aspect_ratio": "16:9",
        "audio": True,
    },
)

print(response.json())
```

```javascript JavaScript 
const response = await fetch("https://toapis.com/v1/videos/generations", {
  method: "POST",
  headers: {
    Authorization: "Bearer <token>",
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    model: "viduq3-pro",
    prompt: "一只猫咪在弹钢琴，镜头缓缓推近，电影质感",
    duration: 8,
    resolution: "1080p",
    aspect_ratio: "16:9",
    audio: true
  })
});

console.log(await response.json());
```

