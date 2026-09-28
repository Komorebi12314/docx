> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# HappyHorse 1.1 视频生成

> 使用 HappyHorse 1.1 生成、参考图生成或编辑视频

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 对外模型固定为 `happyhorse-1.1`
* 通过 `action` 区分文生视频、首帧图生视频、参考图生视频和视频编辑
* 未传 `action` 时，存在首帧图会自动按图生视频处理，否则按文生视频处理
* 异步任务管理，通过任务 ID 查询结果

## Authorizations

### `Authorization`

`string` · 必填

所有接口均需要使用 Bearer Token 进行认证。

```
Authorization: Bearer YOUR_API_KEY
```


## Body

### `model`

`string` · 必填 · 默认值：`happyhorse-1.1`

视频生成模型名称，固定为 `happyhorse-1.1`。


### `action`

`string` · 默认值：`text-to-video`

生成模式。

可选项：

* `text-to-video` - 文生视频
* `image-to-video` - 首帧图生视频
* `reference-to-video` - 参考图生视频
* `video-edit` - 视频编辑

如果省略该字段，服务端会根据是否传入首帧图自动判断。


### `prompt`

`string`

视频内容描述。

文生视频、参考图生视频和视频编辑必填。首帧图生视频可选，但建议填写以控制画面运动和风格。


### `image_urls`

`string[]`

图生视频首帧图片 URL。仅使用第一张图片。

也可以使用兼容字段 `input_reference`、`images`、`image` 或 `image_with_roles[{ role: "first_frame" }]`。

图片要求：

* 格式：`JPEG`、`JPG`、`PNG`、`BMP`、`WEBP`
* 文件大小：不超过 `10MB`
* 宽高：不小于 `300px`
* 宽高比：`1:2.5` 到 `2.5:1`


### `reference_images`

`string[]`

参考图片 URL 列表。

`reference-to-video` 必填，支持 `1` 到 `9` 张；`video-edit` 可选，最多 `5` 张。


### `url`

`string`

视频编辑的输入视频 URL。`action=video-edit` 时必填。


### `audio_setting`

`string` · 默认值：`auto`

视频编辑的声音控制。仅 `action=video-edit` 有效。

可选项：

* `auto`
* `origin`


### `duration`

`integer` · 默认值：`5`

视频时长，单位秒。可选范围：`3` 到 `15`。


### `resolution`

`string` · 默认值：`1080P`

视频分辨率。

可选项：

* `720P`
* `1080P`


### `aspect_ratio`

`string` · 默认值：`16:9`

文生视频宽高比。图生视频会根据首帧图决定画幅。

可选项：

* `16:9`
* `9:16`
* `1:1`
* `4:3`
* `3:4`

也可以使用兼容字段 `size`。


### `seed`

`integer`

随机种子，用于控制生成结果的确定性。


### `watermark`

`boolean` · 默认值：`true`

是否添加水印。


## 文生视频示例

```bash 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "happyhorse-1.1",
    "action": "text-to-video",
    "prompt": "夜晚的铁路桥下，一个涂鸦少年从墙上活过来，一边快速演唱英文 rap，一边做出充满活力的说唱动作。",
    "duration": 10,
    "resolution": "1080P",
    "aspect_ratio": "16:9",
    "seed": 42,
    "watermark": true
  }'
```

## 图生视频示例

```bash 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "happyhorse-1.1",
    "action": "image-to-video",
    "prompt": "让图片中的角色自然动起来，保持原始画面风格。",
    "image_urls": ["https://example.com/first-frame.png"],
    "duration": 5,
    "resolution": "1080P"
  }'
```

## 参考图生视频示例

```bash 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "happyhorse-1.1",
    "action": "reference-to-video",
    "prompt": "图 1 中的主角在图 2 的场景中奔跑，随后拿起图 3 中的道具。画面保持 3D 卡通风格。",
    "reference_images": [
      "https://example.com/image-01.jpg",
      "https://example.com/image-02.png",
      "https://example.com/image-03.jpeg"
    ],
    "duration": 5,
    "resolution": "1080P",
    "aspect_ratio": "16:9",
    "watermark": false
  }'
```

## 视频编辑示例

```bash 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "happyhorse-1.1",
    "action": "video-edit",
    "prompt": "让视频中的场景更有电影感，保留主体动作。",
    "url": "https://example.com/input.mp4",
    "reference_images": ["https://example.com/reference.png"],
    "resolution": "1080P",
    "audio_setting": "origin",
    "seed": 42
  }'
```

## 查询任务

提交接口会返回任务 ID。使用通用视频任务查询接口获取状态和结果：

```bash 
curl --request GET \
  --url https://toapis.com/v1/videos/generations/{task_id} \
  --header "Authorization: Bearer YOUR_API_KEY"
```
