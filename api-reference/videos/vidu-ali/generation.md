> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Vidu Q3 视频生成

> 使用 Vidu Q3 视频模型生成异步视频任务。

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 异步任务接口，提交后返回统一 `generation.task`
* 当前对外模型：`viduq3-pro-fast`、`viduq3-ad`、`viduq3-drama`、`viduq3-mix`

> ⚠️ **注意**
>
> `viduq3-ad`、`viduq3-drama`、`viduq3-mix` 不是纯文生视频模型。不要只传 `prompt`；至少需要参考素材。否则上游通常会返回 `InvalidParameter`，例如 `Missing required field 'subjects' in request body`。


## 认证

### `Authorization`

`string` · 必填

所有接口均需要使用 Bearer Token 认证。

```http 
Authorization: Bearer YOUR_API_KEY
```


## 支持模型

| 模型                | 上游模型                                | 生成类型      | 推荐输入       | 推荐分辨率            |
| ----------------- | ----------------------------------- | --------- | ---------- | ---------------- |
| `viduq3-pro-fast` | `vidu/viduq3-pro-fast_img2video`    | 首帧图生视频    | 1 张参考图     | `720P` / `1080P` |
| `viduq3-ad`       | `vidu/viduq3-ad_reference2video`    | 参考视频生成    | 参考视频 + 参考图 | `720P` / `1080P` |
| `viduq3-drama`    | `vidu/viduq3-drama_reference2video` | 剧情型参考视频生成 | 参考视频 + 参考图 | `1080P`          |
| `viduq3-mix`      | `vidu/viduq3-mix_reference2video`   | 混合参考生成    | 参考视频 + 参考图 | `720P` / `1080P` |

## 请求参数

### `model`

`string` · 必填

只支持以下 4 个对外模型名：

* `viduq3-pro-fast`
* `viduq3-ad`
* `viduq3-drama`
* `viduq3-mix`


### `prompt`

`string` · 必填

提示词。

即使是参考生成模型也建议始终填写 `prompt`，用于描述镜头、动作、节奏和风格。


### `image_urls`

`string[]`

参考图片 URL 列表。

* `viduq3-pro-fast`：只使用第 1 张图片，作为首帧
* `viduq3-ad` / `viduq3-drama` / `viduq3-mix`：建议传 1 张或多张主体/风格参考图

兼容字段：

* `input_reference`
* `reference_images`
* `images`
* `image`


### `url`

`string`

参考视频 URL。

仅 `viduq3-ad` / `viduq3-drama` / `viduq3-mix` 推荐传入。等价于传入一个主参考视频。


### `video_list`

`array`

参考视频列表。

仅 `viduq3-ad` / `viduq3-drama` / `viduq3-mix` 使用。每一项支持：

* `video_url`
* `refer_type`（可选）
* `keep_original_sound`（可选）


### `duration`

`integer` · 默认值：`5`

视频时长，单位秒。默认 `5`。


### `resolution`

`string` · 默认值：`720P`

分辨率，支持 `720P`、`1080P`。

建议：

* `viduq3-drama` 优先使用 `1080P`


### `audio`

`boolean`

是否生成音频。

当前服务端默认行为：

* `viduq3-pro-fast`：默认 `true`
* `viduq3-ad`：默认 `true`
* `viduq3-mix`：默认 `true`
* `viduq3-drama`：建议显式传值，不要依赖默认值


### `watermark`

`boolean` · 默认值：`false`

是否添加水印。


### `seed`

`integer`

随机种子。


### `metadata`

`object`

扩展参数，会按阿里视频请求结构尝试透传。

常见用法：

* `metadata.input.first_frame_url`
* `metadata.input.last_frame_url`
* `metadata.input.audio_url`
* `metadata.parameters.audio`
* `metadata.parameters.watermark`

> ⚠️ **注意**
>
> `viduq3-ad` / `viduq3-drama` / `viduq3-mix` 在上游侧可能要求主体结构化输入（如 `subjects`）。如果只传纯文本 prompt，通常会直接失败。


## 输入规则

### 1. `viduq3-pro-fast`

* 这是首帧图生视频模型
* 至少传 1 张图
* 多张图时当前只会取第 1 张
* 适合“让静态图片动起来”的场景

### 2. `viduq3-ad` / `viduq3-drama` / `viduq3-mix`

* 这是参考视频生成模型，不建议纯 prompt 调用
* 推荐至少传：
  * 1 个参考视频：`url` 或 `video_list`
  * 1 张参考图：`image_urls` 或兼容图片字段
* 如果缺少主体/参考素材，上游可能返回：
  * `InvalidParameter`
  * `Missing required field 'subjects' in request body`

## 请求示例

### `viduq3-pro-fast` 首帧图生视频

```bash 
curl --request POST \
  --url 'https://toapis.com/v1/videos/generations' \
  --header 'Authorization: Bearer <YOUR_API_KEY>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "viduq3-pro-fast",
    "prompt": "让角色自然抬头微笑，镜头轻微推进，保留原画风格。",
    "image_urls": [
      "https://example.com/first-frame.png"
    ],
    "duration": 5,
    "resolution": "720P",
    "audio": true,
    "watermark": false
  }'
```

### `viduq3-ad` 参考视频生成

```bash 
curl --request POST \
  --url 'https://toapis.com/v1/videos/generations' \
  --header 'Authorization: Bearer <YOUR_API_KEY>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "viduq3-ad",
    "prompt": "延续参考视频中的节奏与镜头语言，让主角走入商场中庭并面向镜头挥手。",
    "url": "https://example.com/reference-video.mp4",
    "image_urls": [
      "https://example.com/subject-reference.png"
    ],
    "duration": 5,
    "resolution": "1080P",
    "audio": true
  }'
```

### `viduq3-drama` 剧情型参考生成

```bash 
curl --request POST \
  --url 'https://toapis.com/v1/videos/generations' \
  --header 'Authorization: Bearer <YOUR_API_KEY>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "viduq3-drama",
    "prompt": "保持角色一致性，情绪逐步递进，镜头由中景切到近景。",
    "video_list": [
      {
        "video_url": "https://example.com/reference-scene.mp4"
      }
    ],
    "image_urls": [
      "https://example.com/character.png"
    ],
    "duration": 5,
    "resolution": "1080P",
    "watermark": false
  }'
```

### `viduq3-mix` 混合参考生成

```bash 
curl --request POST \
  --url 'https://toapis.com/v1/videos/generations' \
  --header 'Authorization: Bearer <YOUR_API_KEY>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "viduq3-mix",
    "prompt": "融合参考视频动作与参考图角色设定，生成一个更具广告感的过场镜头。",
    "url": "https://example.com/reference-action.mp4",
    "image_urls": [
      "https://example.com/brand-character.png"
    ],
    "duration": 5,
    "resolution": "720P",
    "audio": true
  }'
```

## 提交成功响应

```json 
{
  "id": "vid_01KABCDEF1234567890",
  "object": "generation.task",
  "model": "viduq3-pro-fast",
  "status": "queued",
  "progress": 0,
  "created_at": 1784169600
}
```

## 查询任务

`GET /v1/videos/generations/{task_id}`

处理中：

```json 
{
  "id": "vid_01KABCDEF1234567890",
  "object": "generation.task",
  "model": "viduq3-pro-fast",
  "status": "in_progress",
  "progress": 60,
  "created_at": 1784169600
}
```

成功：

```json 
{
  "id": "vid_01KABCDEF1234567890",
  "object": "generation.task",
  "model": "viduq3-pro-fast",
  "status": "completed",
  "progress": 100,
  "created_at": 1784169600,
  "completed_at": 1784169660,
  "expires_at": 1784256060,
  "result": {
    "type": "video",
    "data": [
      {
        "url": "https://files.toapis.com/videos/vid_01KABCDEF1234567890.mp4",
        "format": "mp4"
      }
    ]
  }
}
```

失败：

```json 
{
  "id": "vid_01KABCDEF1234567890",
  "object": "generation.task",
  "model": "viduq3-ad",
  "status": "failed",
  "progress": 100,
  "created_at": 1784169600,
  "completed_at": 1784169620,
  "error": {
    "code": "InvalidParameter",
    "message": "Missing required field 'subjects' in request body"
  }
}
```

## 说明

* 提交后由 ToAPIs 统一轮询上游任务状态，再返回标准视频任务结果。
* `viduq3-pro-fast` 是当前最稳定的接入形态，适合首帧图生视频。
* `viduq3-ad`、`viduq3-drama`、`viduq3-mix` 对参考素材要求更严格，接入前建议先按上面的示例准备完整素材，不要只传 prompt。
