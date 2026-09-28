> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Gemini Omni 1.1 VIP

> VIP 支持文生视频, 图生视频和参考视频. 支持 4 / 6 / 8 / 10 秒和 360p / 720p / 1080p / 4k, 默认 6 秒 / 720p. 提供参考视频时省略时长参数.

VIP 支持文生视频, 图生视频和参考视频. 支持 4 / 6 / 8 / 10 秒和 360p / 720p / 1080p / 4k, 默认 6 秒 / 720p. 提供参考视频时省略时长参数.

> 💡 **提示**
>
> 使用平台 API Key, 不使用上游供应商 Key. 中国大陆可将 Base URL 换为 [https://toapis.cn](https://toapis.cn).
[普通版](./generation-1-1) | [Official 文档](../gemini-omni-1.1-flash-preview-official/generation)

## 请求参数

### `Authorization`

`string` · 必填

`Bearer YOUR_API_KEY`


### `model`

`string` · 必填

`gemini-omni-1.1-flash-preview-vip`
- **`prompt`**（`string`，必填） — 必填的视频描述.
- **`duration`**（`integer`，默认 `6`） — VIP 支持 4 / 6 / 8 / 10 秒, 默认 6 秒. VIP 提供 video\_urls 时必须省略 duration 和 seconds.
- **`resolution`**（`string`，默认 `720p`） — VIP 支持 360p / 720p / 1080p / 4k, 默认 720p, 不区分大小写.
- **`aspect_ratio`**（`string`，默认 `16:9`） — 支持 16:9 或 9:16, 默认 16:9.
- **`image_urls`**（`string[]`） — VIP 首帧模式 frame 仅 1 张, 参考模式 reference 为 1 或 3 张. 不支持 2 张首尾帧. 无图片时省略 generation\_type.
- **`generation_type`**（`string`） — 仅 VIP. frame 表示首帧, reference 表示参考图. 省略时 1 张按首帧, 3 张按参考图处理.
- **`video_urls`**（`string[]`） — 仅 VIP, 最多 1 个公开 HTTP(S) 视频 URL, 可与图片同时提供. 参考视频模式不传 duration 或 seconds. 输出时长以实际生成结果为准, 不保证与源视频一致.
> ⚠️ **注意**
>
> 本地素材先通过上传接口获得公网 URL. 请勿发送 base64 或本地文件路径.
## 请求示例

#### VIP

```bash 
curl https://toapis.com/v1/videos \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gemini-omni-1.1-flash-preview-vip",
    "prompt": "A cinematic tracking shot through a sunlit city",
    "duration": 8,
    "resolution": "360p",
    "aspect_ratio": "9:16",
    "generation_type": "reference",
    "image_urls": [
      "https://example.com/a.png",
      "https://example.com/b.png",
      "https://example.com/c.png"
    ]
  }'
```


#### VIP VIDREF

```bash 
curl https://toapis.com/v1/videos \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gemini-omni-1.1-flash-preview-vip",
    "prompt": "The same scene at night with neon lights",
    "resolution": "4k",
    "aspect_ratio": "16:9",
    "generation_type": "reference",
    "image_urls": ["https://example.com/image.png"],
    "video_urls": ["https://example.com/video.mp4"]
  }'
```


## 查询结果

提交返回平台任务 id. 通过 GET /v1/videos/{id} 查询, 完成后读取视频结果. 不要使用供应商 task\_id 或直接访问供应商查询接口.

```bash 
curl https://toapis.com/v1/videos/YOUR_TASK_ID \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

### 响应示例

```json 
{
  "id": "vid_example",
  "object": "generation.task",
  "model": "gemini-omni-1.1-flash-preview-vip",
  "status": "queued",
  "created_at": 1789600000
}
```


## 参数错误

非法分辨率或时长, VIP 图片数量不符合模式, 多个参考视频, 或参考视频与时长同时传入, 均应修正请求后再提交.
