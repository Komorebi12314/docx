> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# kling-3.0-turbo 视频生成

> 通过 ToAPIs 标准异步视频接口接入官方 kling-3.0-turbo 视频生成模型

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 异步任务接口，提交后返回任务 ID
* 使用新的官方 Kling Turbo 上游协议
* 支持文生视频和图生视频，但图生仅支持首帧
* `resolution` 支持 `720p` 和 `1080p`
* `duration` 支持 `3s`、`4s`、`5s`、`6s`、`7s`、`8s`、`9s`、`10s`、`11s`、`12s`、`13s`、`14s`、`15s`
* `aspect_ratio` 仅对文生视频生效
* `watermark` 仅支持布尔开关，不支持自定义水印对象

> ⚠️ **注意**
>
> 请传入公网可访问的图片 URL。不要直接传 base64 图片数据；本地图片请先使用 [上传图片接口](../../uploads/images) 获取 URL。


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

视频生成模型名称，固定为 `kling-3.0-turbo`。


### `prompt`

`string` · 必填

视频提示词。对于图生视频，该字段会转换为 Kling Turbo `contents` 中的 `prompt` 项。


### `reference_images`

`string[]`

可选输入图片。Kling Turbo 图生视频只会取第一张图作为 `first_frame`。

> ⚠️ **注意**
>
> 当前接入不支持尾帧。多余图片不会作为尾帧传给上游。


### `resolution`

`string` · 默认值：`720p`

视频分辨率。

支持值：

* `720p`
* `1080p`


### `duration`

`integer` · 默认值：`5`

视频时长，单位秒。

支持值：`3`、`4`、`5`、`6`、`7`、`8`、`9`、`10`、`11`、`12`、`13`、`14`、`15`


### `aspect_ratio`

`string` · 默认值：`16:9`

文生视频宽高比。

支持值：

* `16:9`
* `9:16`
* `1:1`


### `watermark`

`boolean` · 默认值：`false`

是否添加官方 Kling 水印。


## 示例

### 文生视频

```json 
{
  "model": "kling-3.0-turbo",
  "prompt": "A cinematic shot of a red sports car driving through rain",
  "resolution": "720p",
  "duration": 5,
  "aspect_ratio": "16:9"
}
```

### 图生视频

```json 
{
  "model": "kling-3.0-turbo",
  "prompt": "Animate the character with subtle camera motion",
  "reference_images": ["https://example.com/first-frame.png"],
  "resolution": "1080p",
  "duration": 5,
  "watermark": true
}
```

> 💡 **提示**
>
> 视频生成为异步任务。提交后使用 [获取视频任务状态](../../tasks/video-status) 查询进度和结果。

