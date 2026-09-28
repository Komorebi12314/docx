> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan 3.0 全能视频生成

> 使用 Wan 3.0 All-in-One 模型生成视频，支持文生视频、首尾帧控制和图片、视频、音频等多模态参考

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


Wan 3.0 的公共模型名为 `wan3.0-video`。同一个模型支持以下生成方式：

* 文生视频
* 首帧或首尾帧控制
* 参考图片、参考视频和参考音频联合生成
* 文件或公开网页内容参考

接口为异步任务。提交成功后返回任务 ID，再通过[视频任务状态接口](../../tasks/video-status)查询进度和结果。

> ⚠️ **注意**
>
> **首尾帧模式与参考素材模式互斥。**
>
> 只要请求中包含 `first_frame` 或 `last_frame`，就不能同时传入参考图片、参考视频、参考音频、文件或网页链接。参考图片、参考视频和参考音频之间可以组合使用。


## 认证

### `Authorization`

`string` · 必填

使用 Bearer Token 认证：

```text 
Authorization: Bearer YOUR_API_KEY
```


## 请求参数

### `model`

`string` · 必填 · 默认值：`wan3.0-video`

模型名称，固定为 `wan3.0-video`。


### `prompt`

`string`

视频内容、主体动作、镜头和声音描述。`prompt` 与媒体素材至少提供一项。

使用多模态参考时，可以按数组顺序在提示词中写“图片1”“视频1”“音频1”。


### `duration`

`integer` · 默认值：`5`

输出时长，支持 `2` 至 `30` 秒。


### `ratio`

`string` · 默认值：`adaptive`

输出宽高比，支持：

* `adaptive`，根据参考素材自适应
* `16:9`
* `9:16`
* `1:1`
* `4:3`
* `3:4`

兼容字段 `aspect_ratio` 也可以使用。无需同时传入两个字段。


### `resolution`

`string` · 默认值：`1080p`

输出分辨率，支持 `480p`、`720p` 和 `1080p`。


### `audio`

`boolean` · 默认值：`true`

是否生成音频，默认开启。


### `watermark`

`boolean` · 默认值：`false`

是否添加水印，默认关闭。


### `seed`

`integer`

可选随机种子。相同参数和种子有助于复现相近结果。


### `image_with_roles`

`object[]`

首尾帧控制数组。每项包含：

* `url`：公开可访问的图片 URL
* `role`：`first_frame` 或 `last_frame`

最多提供一个首帧和一个尾帧。使用 `last_frame` 时必须同时提供 `first_frame`。


### `reference_images`

`string[]`

参考图片 URL 数组，最多 `10` 张。不能与 `image_with_roles` 中的首尾帧混用。


### `video_list`

`object[]`

参考视频数组，最多 `5` 段，总时长不超过 `15` 秒。每项使用以下结构：

```json 
{
  "video_url": "https://example.com/reference.mp4"
}
```


### `audio_with_roles`

`object[]`

参考音频数组，最多 `5` 段，总时长不超过 `15` 秒。每项包含：

* `url`：公开可访问的音频 URL
* `role`：固定为 `reference_audio`


### `metadata`

`object`

文件或网页参考通过 `metadata.media` 传入。

<details>
<summary>展开 metadata.media 结构</summary>

`media` 是对象数组，每项包含 `type` 和 `url`：

* 文件：`{ "type": "file", "url": "https://example.com/brief.pdf" }`
* 网页：`{ "type": "link", "url": "https://example.com/article" }`

单次请求最多提供一个文件或一个网页，二者不能同时使用。文件和网页也不能与首尾帧模式混用。


> 💡 **提示**
>
> 本地图片或视频需要先上传并取得公开 URL。不要在生成请求中直接传入本地文件路径或 base64 数据。


## 素材组合规则

| 请求内容       | 是否支持 | 说明             |
| ---------- | ---: | -------------- |
| 仅提示词       |    是 | 文生视频           |
| 仅首帧        |    是 | 首帧控制           |
| 首帧和尾帧      |    是 | 尾帧不能单独使用       |
| 参考图片和参考视频  |    是 | 可联合参考          |
| 参考图片、视频和音频 |    是 | 可联合参考          |
| 首帧和参考视频    |    否 | 首尾帧模式与参考素材模式互斥 |
| 首尾帧和参考图片   |    否 | 首尾帧模式与参考素材模式互斥 |
| 文件和网页链接    |    否 | 两者互斥           |

如果收到以下错误：

```text 
Wan 3.0 不能在同一请求中混用首尾帧与参考素材/文件/网页。
```

请删除首帧/尾帧，保留参考素材；或者删除全部参考素材，只保留首帧/尾帧。

## 请求示例

### 文生视频

```bash 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "wan3.0-video",
    "prompt": "一只橘猫在雨后的东京街道奔跑，电影感运镜",
    "duration": 5,
    "ratio": "16:9",
    "resolution": "1080p",
    "audio": true,
    "watermark": false
  }'
```

### 首尾帧生成视频

```bash 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "wan3.0-video",
    "prompt": "镜头自然推进，人物从站立状态过渡到微笑挥手",
    "duration": 8,
    "ratio": "adaptive",
    "resolution": "1080p",
    "image_with_roles": [
      {
        "url": "https://example.com/first-frame.png",
        "role": "first_frame"
      },
      {
        "url": "https://example.com/last-frame.png",
        "role": "last_frame"
      }
    ]
  }'
```

### 参考视频生成视频

不要在此请求中同时传入 `first_frame` 或 `last_frame`。

```bash 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "wan3.0-video",
    "prompt": "参考视频1的运镜和人物动作，生成一段新的街舞视频",
    "duration": 10,
    "ratio": "adaptive",
    "resolution": "720p",
    "audio": true,
    "video_list": [
      {
        "video_url": "https://example.com/reference-video.mp4"
      }
    ]
  }'
```

### 图片、视频和音频联合参考

```bash 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "wan3.0-video",
    "prompt": "使用图片1中的人物形象、视频1中的动作和音频1的节奏生成视频",
    "duration": 10,
    "ratio": "16:9",
    "resolution": "720p",
    "audio": true,
    "reference_images": [
      "https://example.com/character.png"
    ],
    "video_list": [
      {
        "video_url": "https://example.com/motion.mp4"
      }
    ],
    "audio_with_roles": [
      {
        "url": "https://example.com/music.mp3",
        "role": "reference_audio"
      }
    ]
  }'
```

### 文件参考

```bash 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "wan3.0-video",
    "prompt": "根据文件内容生成一段简洁的产品介绍视频",
    "duration": 10,
    "ratio": "16:9",
    "resolution": "1080p",
    "metadata": {
      "media": [
        {
          "type": "file",
          "url": "https://example.com/product-brief.pdf"
        }
      ]
    }
  }'
```

## 响应

### `id`

`string`

视频任务 ID，用于查询任务状态。


### `object`

`string`

对象类型，通常为 `generation.task`。


### `model`

`string`

本次请求使用的模型名称。


### `status`

`string`

任务状态：`queued`、`in_progress`、`completed` 或 `failed`。


### `progress`

`integer`

任务进度，范围为 `0` 至 `100`。


### `created_at`

`integer`

任务创建时间戳。


### 响应示例

```json 200 
{
  "id": "tsk_vid_xxx",
  "object": "generation.task",
  "model": "wan3.0-video",
  "status": "in_progress",
  "progress": 10,
  "created_at": 1781577600
}
```

