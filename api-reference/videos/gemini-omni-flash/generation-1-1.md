> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Gemini Omni 1.1 普通版

> 普通版支持文生视频和图生视频, 固定 10 秒 / 720p. 最多使用 5 张参考图.

普通版支持文生视频和图生视频, 固定 10 秒 / 720p. 最多使用 5 张参考图.

> 💡 **提示**
>
> 使用平台 API Key, 不使用上游供应商 Key. 中国大陆可将 Base URL 换为 [https://toapis.cn](https://toapis.cn).
[VIP](./generation-1-1-vip) | [Official 文档](../gemini-omni-1.1-flash-preview-official/generation)

## 请求参数

### `Authorization`

`string` · 必填

`Bearer YOUR_API_KEY`


### `model`

`string` · 必填

`gemini-omni-1.1-flash-preview`
- **`prompt`**（`string`，必填） — 必填的视频描述.
- **`duration`**（`integer`，默认 `10`） — 普通版固定 10 秒.
- **`resolution`**（`string`，默认 `720p`） — 720p
- **`aspect_ratio`**（`string`，默认 `16:9`） — 支持 16:9 或 9:16, 默认 16:9.
- **`image_urls`**（`string[]`） — 普通版最多 5 张公开图片 URL.
> ⚠️ **注意**
>
> 本地素材先通过上传接口获得公网 URL. 请勿发送 base64 或本地文件路径.
## 请求示例

```bash 
curl https://toapis.com/v1/videos \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gemini-omni-1.1-flash-preview",
    "prompt": "A cinematic tracking shot through a sunlit city",
    "duration": 10,
    "resolution": "720p",
    "aspect_ratio": "16:9",
    "image_urls": ["https://example.com/image.png"]
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
  "model": "gemini-omni-1.1-flash-preview",
  "status": "queued",
  "created_at": 1789600000
}
```

