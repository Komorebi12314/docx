> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Kling v3 视频生成

> 使用官方 Kling v3 生成视频，普通参考图与首尾帧控制采用显式区分语义

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 异步任务接口，提交后返回任务 ID
* 支持文生视频、图生视频、显式首尾帧控制和有声视频
* `mode=std` 对应 720P，`mode=pro` 对应 1080P
* `audio=true` 会生成有声视频，并按 Sound 价格计费
* `duration` 支持 `3s`、`4s`、`5s`、`6s`、`7s`、`8s`、`9s`、`10s`、`11s`、`12s`、`13s`、`14s`、`15s`

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

视频生成模型名称，固定为 `kling-v3`。


### `prompt`

`string` · 必填

视频提示词。建议描述主体、动作、场景、镜头语言和风格。


### `mode`

`string` · 默认值：`std`

生成模式。

* `std` - 标准模式，720P
* `pro` - 专业模式，1080P


### `duration`

`integer` · 默认值：`5`

视频时长，单位秒。

可选值：`3`、`4`、`5`、`6`、`7`、`8`、`9`、`10`、`11`、`12`、`13`、`14`、`15`


### `aspect_ratio`

`string` · 默认值：`16:9`

视频宽高比。常用值：`16:9`、`9:16`、`1:1`


### `reference_images`

`string[]`

普通参考图。

* 这里只表示参考图语义
* 不会再自动把第二张参考图推断为尾帧
* 首尾帧请使用 `image_with_roles` 显式传入


### `image_with_roles`

`object[]`

显式图片角色数组，用于首尾帧控制或混合输入。

<details>
<summary>显示 image_with_roles 字段</summary>

**`url`** — `string` · 必填

公网可访问的图片 URL。


**`role`** — `string` · 必填

图片角色。

支持值：

* `first_frame`
* `last_frame`
* `reference`
* `reference_image`


> ⚠️ **注意**
>
> 只有在 `image_with_roles` 中显式声明 `last_frame` 时，系统才会发送尾帧控制字段；不会再从 `reference_images[1]` 自动猜测。


### `audio`

`boolean` · 默认值：`false`

是否生成有声视频。


### `metadata`

`object`

扩展参数。

<details>
<summary>显示 metadata 字段</summary>

**`negative_prompt`** — `string`

负面提示词，描述不希望出现的内容。


**`watermark`** — `boolean`

是否添加水印。


## 输入规则

| 输入形态                                                     | 行为    |
| -------------------------------------------------------- | ----- |
| 只有 `reference_images`                                    | 普通参考图 |
| 只有 `image_with_roles` 且角色仅有 `first_frame` / `last_frame` | 首尾帧控制 |
| 两者混用，或 roles 中同时含 frame/reference 语义                     | 混合模式  |

## 示例

### 文生视频

```json 
{
  "model": "kling-v3",
  "prompt": "一只金色的猫咪在阳光下的草地上奔跑，慢动作，电影质感",
  "mode": "std",
  "duration": 5,
  "aspect_ratio": "16:9"
}
```

### 普通参考图

```json 
{
  "model": "kling-v3",
  "prompt": "参考人物形象，让角色轻轻微笑",
  "reference_images": ["https://example.com/reference.jpg"],
  "mode": "std",
  "duration": 5
}
```

### 首尾帧控制

```json 
{
  "model": "kling-v3",
  "prompt": "城市从白天自然过渡到夜晚",
  "image_with_roles": [
    { "url": "https://example.com/day.jpg", "role": "first_frame" },
    { "url": "https://example.com/night.jpg", "role": "last_frame" }
  ],
  "mode": "pro",
  "duration": 5
}
```

### 参考图与首尾帧混合

```json 
{
  "model": "kling-v3",
  "prompt": "保持角色一致性，同时完成场景过渡",
  "reference_images": ["https://example.com/character-reference.jpg"],
  "image_with_roles": [
    { "url": "https://example.com/start-scene.jpg", "role": "first_frame" },
    { "url": "https://example.com/end-scene.jpg", "role": "last_frame" }
  ],
  "mode": "pro",
  "duration": 5
}
```

### 有声视频

```json 
{
  "model": "kling-v3",
  "prompt": "舞台上的歌手正在演唱，观众欢呼，灯光闪烁",
  "mode": "std",
  "duration": 5,
  "audio": true
}
```

> 💡 **提示**
>
> 视频生成为异步任务。提交后使用 [获取视频任务状态](../../tasks/video-status) 查询进度和结果。

