> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Gemini Omni Flash 视频生成

> 使用非官方 Gemini Omni Flash 渠道生成视频，支持文本和最多 3 张参考图

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 通过 `model` 指定 `gemini-omni-flash`（部分渠道配置使用 `gemini_omni_flash` 别名）
* 支持文生视频和参考图生视频
* 支持 4 / 6 / 10 秒时长
* 支持 `720p` 和 `1080p`；`1080p` 仅支持横屏
* 异步任务接口，提交后使用任务 ID 查询结果

> 💡 **提示**
>
> 本文档适用于非官方的旧版 `gemini-omni-flash`. 它不使用 Vertex AI Interactions API. 不同旧版接入的限制可能不同; 官方 Vertex AI 接入版本请参阅 `gemini-omni-flash-preview-official` 页面.


> ⚠️ **注意**
>
> 请先通过[图片上传 API](../../uploads/images) 上传本地图片，再把返回的 URL 放入 `image_urls`。不要直接传 base64 图片。


## Authorizations

### `Authorization`

`string` · 必填

使用 Bearer Token 认证：

```
Authorization: Bearer YOUR_API_KEY
```


## Body

### `model`

`string` · 必填 · 默认值：`gemini-omni-flash`

模型名称。旧版渠道使用 `gemini-omni-flash`；部分渠道配置使用等价的 `gemini_omni_flash` 别名。


### `prompt`

`string` · 必填

视频生成提示词。


### `duration`

`integer` · 默认值：`6`

视频时长，支持 `4`、`6`、`10` 秒。


### `aspect_ratio`

`string` · 默认值：`16:9`

视频比例，支持：

* `16:9` 横屏
* `9:16` 竖屏


### `resolution`

`string` · 默认值：`720p`

视频分辨率，支持 `720p` 或 `1080p`；旧版渠道的 `1080p` 仅输出横屏。


### `image_urls`

`string[]`

可选的公开参考图 URL 数组，最多 `3` 张。不传时为文生视频。此渠道不支持 base64/data URI，也不支持视频输入。


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
    "model": "gemini-omni-flash",
    "prompt": "一支蓝色按压瓶在纯白摄影棚中轻微转动，商业产品视频",
    "duration": 6,
    "aspect_ratio": "9:16",
    "resolution": "720p",
    "image_urls": ["https://example.com/reference.jpg"]
  }'
```


### 响应示例

```json 200 
{
  "id": "video_01JZEXAMPLE",
  "object": "generation.task",
  "model": "gemini-omni-flash",
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
