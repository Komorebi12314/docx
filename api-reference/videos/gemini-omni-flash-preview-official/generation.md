> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Gemini Omni Flash 视频生成

> 使用 Gemini Omni Flash 生成或编辑视频，支持文本、最多 10 张参考图或最多 3 个输入视频

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 通过 `model` 指定 `gemini-omni-flash-preview-official`
* 支持文生视频、图像/参考图生视频和视频编辑
* 最多支持 10 张参考图或 3 个输入视频；图片与视频不能混用
* 视频最长 10 秒；Playground 提供 4 / 6 / 8 / 10 秒预设
* 仅支持 `720p` 分辨率；支持 `16:9` 和 `9:16` 画幅
* 异步任务接口，提交后使用任务 ID 查询结果

> 💡 **提示**
>
> 本文档仅适用于 `gemini-omni-flash-preview-official`. 平台通过 Vertex AI Interactions API 调用它, 而不是 Vertex AI Publisher Model 的 `predictLongRunning` 接口. 它与旧版 `gemini-omni-flash` / `gemini_omni_flash` 是两个独立模型, 不会改变旧模型的路由或参数.


> ⚠️ **注意**
>
> 请先通过[图片上传 API](../../uploads/images)上传本地图片，通过[视频上传 API](../../uploads/videos)上传本地视频，再传入返回的 URL。不要直接传 base64 媒体数据。


## Authorizations

### `Authorization`

`string` · 必填

使用 Bearer Token 认证：

```
Authorization: Bearer YOUR_API_KEY
```


## Body

### `model`

`string` · 必填 · 默认值：`gemini-omni-flash-preview-official`

模型名称。使用 `gemini-omni-flash-preview-official`。


### `prompt`

`string` · 必填

视频生成提示词。


### `duration`

`integer` · 默认值：`6`

视频时长（秒），最大为 `10`。Playground 提供 `4`、`6`、`8`、`10` 秒预设。


### `aspect_ratio`

`string` · 默认值：`16:9`

视频比例，支持：

* `16:9` 横屏
* `9:16` 竖屏


### `resolution`

`string` · 默认值：`720p`

视频分辨率：

* `720p` 默认分辨率
* 仅支持 `720p`，不接受 Veo 专属参数


### `image_urls`

`string[]`

可选的参考图 URL 数组，最多 `10` 张。不传时为文生视频。不能与 `video_list` 同时使用。


### `video_list`

`object[]`

可选的视频编辑输入，最多 `3` 个。每一项必须包含 `video_url`，例如 `{ "video_url": "https://example.com/input.mp4" }`。支持 HTTPS URL、data URI 和平台上传后返回的视频 URL；后端下载的单个输入视频最大 50 MB。不能与 `image_urls` 同时使用。


### `metadata`

`object`

可选的 Interactions 生成参数。支持 `temperature`（`0.0`–`2.0`）、`topP` / `top_p`（`0.0`–`1.0`）、`candidateCount` / `candidate_count`、`previous_interaction_id`，以及 `task`（`text_to_video`、`image_to_video`、`reference_to_video` 或 `edit`）。省略 `task` 时，平台不会擅自默认；由上游根据 prompt 和媒体推断。对 `edit`（或带参考视频且未显式指定非 edit 任务）路径，平台会省略 `aspect_ratio`，因为上游拒绝在 edit 的 `response_format` 中设置宽高比。


## Response

### `id`

`string`

任务 ID，用于查询任务状态。


### `object`

`string`

对象类型，通常为 `generation.task`。


### `model`

`string`

使用的模型名称。


### `status`

`string`

任务状态：`queued`、`in_progress`、`completed`、`failed`。


### `created_at`

`integer`

任务创建时间戳。


### `video_url`

`string`

任务完成后的生成视频 URL。


## Examples

### 请求示例

```bash cURL 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gemini-omni-flash-preview-official",
    "prompt": "一支蓝色按压瓶在纯白摄影棚中轻微转动，商业产品视频",
    "duration": 6,
    "aspect_ratio": "9:16",
    "resolution": "720p",
    "image_urls": ["https://example.com/reference.jpg"]
  }'
```


视频编辑示例：

```bash 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gemini-omni-flash-preview-official",
    "prompt": "保留镜头运动，把白天场景改成雨夜",
    "duration": 8,
    "aspect_ratio": "16:9",
    "resolution": "720p",
    "video_list": [{"video_url": "https://example.com/input.mp4"}],
    "metadata": {"temperature": 1.0, "topP": 0.95}
  }'
```

### 响应示例

```json 200 
{
  "id": "video_01JZEXAMPLE",
  "object": "generation.task",
  "model": "gemini-omni-flash-preview-official",
  "status": "queued",
  "created_at": 1779247407
}
```


## 查询任务

提交接口会返回任务 ID。使用通用视频任务查询接口获取状态和结果：

```bash 
curl --request GET \
  --url https://toapis.com/v1/videos/generations/{task_id} \
  --header "Authorization: Bearer YOUR_API_KEY"
```
