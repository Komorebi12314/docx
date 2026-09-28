> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Grok Video 1.5 视频生成

> 使用文本, 首帧或参考图生成视频

> 💡 **提示**
>
> 中国大陆用户请在示例中使用 `https://toapis.cn` 替代 `https://toapis.com`.


使用 `grok-video-1.5` 请求以下 3 种输入模式. 模式必须由兼容渠道开放后才能使用. 报价成功不代表生成渠道一定可用.

> ⚠️ **注意**
>
> 图片请使用公网可访问的 `http://` 或 `https://` URL. 本地文件先通过[上传图片接口](../../uploads/images)上传, 不要直接发送 base64. 上传后使用 JSON 传入 URL 可适配已支持的渠道; 部分渠道不接受 multipart 二进制文件上传.


## 生成模式

| 模式                           | 输入                |
| ---------------------------- | ----------------- |
| `text_to_video`              | 仅提示词, 不传图片        |
| `first_frame_image_to_video` | 恰好 1 张首帧          |
| `reference_images_to_video`  | 1-7 张参考图, 包括单张参考图 |

新请求建议显式填写 `video_generation_mode`. 未填写时沿用旧单图行为, 只传 1 张 `reference_images` 不会自动选择参考图模式. 文生视频模式不能携带图片.

## 认证

### `Authorization`

`string` · 必填

使用 API Key 进行 Bearer Token 认证.

```text 
Authorization: Bearer YOUR_API_KEY
```


## 请求参数

### `model`

`string` · 必填 · 默认值：`grok-video-1.5`

使用公共模型名 `grok-video-1.5`, 不要替换为供应商模型名.


### `prompt`

`string`

描述场景和运动. 文生视频和参考图模式必填. 部分旧单首帧请求可以省略, 其他首帧请求仍可能要求此字段. 新接入建议始终提供非空提示词.


### `video_generation_mode`

`string`

旧客户端可以省略. 按实际输入选值: 纯文本填 `text_to_video`, 恰好 1 张首帧填 `first_frame_image_to_video`, 1-7 张参考图填 `reference_images_to_video`. 模式必须与 `image`, `input_reference` 或 `reference_images` 的实际输入一致, 不匹配会被拒绝. 单张参考图必须显式指定参考图模式, 才能与旧单首帧输入区分.


### `image`

`string`

首帧 URL. 首帧模式必须填写, 也可以改用 `input_reference`. 文生视频和纯参考图模式不填写. 上游对首帧的实际处理取决于渠道.


### `input_reference`

`string`

首帧 URL 的字符串别名. 使用 `image` 或 `input_reference` 其中一个, 不要同时传入不同值. 新请求使用该别名时也应显式指定模式.


### `reference_images`

`array`

1-7 张参考图 URL, 支持字符串数组或 `{"url":"https://example.com/reference.jpg"}` 对象数组. 参考图模式必填. 保留旧 `image_urls` 和 `images` 别名, 但不要同时传入内容不同的多组列表.


### `duration`

`integer`

整数秒数, 建议显式填写. 支持 1-15 秒.


### `resolution`

`string`

参考图模式使用 `480p` 或 `720p`. 文生视频和首帧模式可在渠道支持时使用 `1080p`. 本页示例均显式指定 `720p`.


### `aspect_ratio`

`string`

视频画面比例, 如 `16:9`. 常用值为 `1:1`, `16:9`, `9:16`, `3:2` 和 `2:3`, 具体取决于渠道支持范围.


## 兼容性限制

部分渠道对单首帧和单参考图采用相同的处理方式, 模式名称不保证严格的首帧控制. 开放模式不会豁免协议限制. 不支持的输入可能在提交前被拒绝; 没有匹配且已开放的渠道时无法生成任务.

## 价格

视频价格以当前账户和 SKU 配置为准. 请查看[实时价格](https://toapis.com/pricing)以及对应参数的登录报价, 本页不承诺固定每秒价格.

## 创建视频任务

示例均明确指定模式, 时长和分辨率. 图片 URL 需替换为实际可访问的地址.

### 请求示例

```bash cURL 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
  "model": "grok-video-1.5",
  "prompt": "A cinematic product shot with a slow camera push-in",
  "video_generation_mode": "text_to_video",
  "duration": 8,
  "resolution": "720p",
  "aspect_ratio": "16:9"
}'
```

```python Python 
import requests

response = requests.post(
    "https://toapis.com/v1/videos/generations",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "model": "grok-video-1.5",
        "prompt": "A cinematic product shot with a slow camera push-in",
        "video_generation_mode": "first_frame_image_to_video",
        "image": "https://example.com/first-frame.jpg",
        "duration": 8,
        "resolution": "720p",
        "aspect_ratio": "16:9"
    },
)
response.raise_for_status()
print(response.json()["id"])
```


### 参考图示例

```json 
{
  "model": "grok-video-1.5",
  "prompt": "A cinematic product shot with a slow camera push-in",
  "video_generation_mode": "reference_images_to_video",
  "reference_images": [
    "https://example.com/reference-a.jpg",
    "https://example.com/reference-b.jpg"
  ],
  "duration": 8,
  "resolution": "720p",
  "aspect_ratio": "16:9"
}
```

## 响应

### `id`

`string`

用于轮询的任务 ID.


### `object`

`string`

对象类型为 `generation.task`.


### `model`

`string`

本次请求的公共模型名.


### `status`

`string`

任务状态: `queued`, `in_progress`, `completed` 或 `failed`.


### 响应示例

```json 200 
{
  "id": "video_abc123def456",
  "object": "generation.task",
  "model": "grok-video-1.5",
  "status": "queued",
  "progress": 0,
  "created_at": 1768380224,
  "metadata": {}
}
```


## 查询任务状态

使用返回的 `id` 调用[视频任务状态接口](../../tasks/video-status).
