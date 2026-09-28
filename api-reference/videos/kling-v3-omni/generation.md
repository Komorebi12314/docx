> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Kling v3 Omni 视频生成

> 使用 Kling v3 Omni 生成视频，支持图片引用、有声视频和参考视频输入

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 异步任务接口，提交后返回任务 ID
* 支持官方 Omni 引用结构：`image_list`、`video_list`、`element_list`
* `mode=std` 对应 720P，`mode=pro` 对应 1080P
* `audio=true` 会生成有声视频，并按 Sound 价格计费
* 传入 `video_list` 会按 Video 价格计费
* `audio` 与 `video_list` 互斥

> ⚠️ **注意**
>
> 请传入公网可访问的图片或视频 URL。不要直接传 base64 图片数据；本地图片请先使用 [上传图片接口](../../uploads/images) 获取 URL。


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

视频生成模型名称，固定为 `kling-v3-omni`。


### `prompt`

`string` · 必填

视频提示词。可使用官方占位符引用 Omni 输入，编号从 1 开始：

* `<<<image_N>>>` 引用 `metadata.image_list` 中的图片
* `<<<video_N>>>` 引用 `video_list` 中的视频
* `<<<element_N>>>` 引用 `metadata.element_list` 中的主体/角色

示例：`"让<<<image_1>>>中的人物向镜头挥手"`

> 💡 **提示**
>
> 引用列表顺序必须与 prompt 中的占位符顺序一致；系统不会自动补首帧或自动插入占位符。


### `client_business_id`

`string`

客户侧业务 ID，例如订单号、流水号或您系统内的任务 ID。提交后会随任务保存，后续可用该 ID 查询状态：
`GET /v1/videos/generations/{client_business_id}`。

也兼容放在 `metadata.client_business_id` 中，但推荐使用顶层字段。


### `mode`

`string` · 默认值：`std`

生成模式，同时决定计费分辨率。

* `std` - 标准模式，720P
* `pro` - 专业模式，1080P


### `duration`

`integer` · 默认值：`5`

视频时长，单位秒。

可选值：`3`、`4`、`5`、`6`、`7`、`8`、`9`、`10`、`11`、`12`、`13`、`14`、`15`


### `aspect_ratio`

`string` · 默认值：`16:9`

视频宽高比。

常用值：`16:9`、`9:16`、`1:1`


### `audio`

`boolean` · 默认值：`false`

是否生成有声视频。

* `false` - 普通视频
* `true` - 有声视频，按 Sound 价格计费

> ⚠️ **注意**
>
> `audio` 与 `video_list` 互斥。传入 `video_list` 时不要同时传 `audio=true`。


### `video_list`

`object[]`

参考视频列表，最多 1 段视频。传入后按 Video 价格计费。

<details>
<summary>显示 video_list 对象字段</summary>

**`video_url`** — `string` · 必填

参考视频 URL，必须公网可访问。


**`refer_type`** — `string` · 默认值：`base`

参考类型。

* `base` - 待编辑视频
* `feature` - 特征参考视频


**`keep_original_sound`** — `string` · 默认值：`no`

是否保留原视频声音。

* `yes`
* `no`


### `metadata`

`object`

扩展参数。

<details>
<summary>显示 metadata 字段</summary>

**`image_list`** — `object[]`

官方 Omni 图片列表。在 prompt 中通过 `<<<image_1>>>`、`<<<image_2>>>` 按顺序引用。

<details>
<summary>显示 image_list 对象字段</summary>

**`image_url`** — `string` · 必填

图片 URL，必须公网可访问。


**`type`** — `string`

图片类型。可用于官方首尾帧语义，例如 `first_frame`、`end_frame`。传 `end_frame` 时必须同时提供 `first_frame`。


**`element_list`** — `object[]`

官方 Omni 主体/角色引用列表。在 prompt 中通过 `<<<element_1>>>`、`<<<element_2>>>` 按顺序引用。

<details>
<summary>显示 element_list 对象字段</summary>

**`url`** — `string` · 必填

主体图片、角色资产或其他官方支持的素材 URL。


**`type`** — `string`

元素类型，例如 `image`、`video`。


**`role`** — `string`

角色语义，可按官方能力传入。


**`watermark`** — `boolean`

是否添加水印。


## 计费映射

| 请求参数                                      | 计费规格        |
| ----------------------------------------- | ----------- |
| `mode=std`, `audio=false`, 无 `video_list` | 720P        |
| `mode=pro`, `audio=false`, 无 `video_list` | 1080P       |
| `mode=std`, `audio=true`                  | 720P+Sound  |
| `mode=pro`, `audio=true`                  | 1080P+Sound |
| `mode=std`, 有 `video_list`                | 720P+Video  |
| `mode=pro`, 有 `video_list`                | 1080P+Video |

## Omni 引用语法

| 语法                | 说明                                    |
| ----------------- | ------------------------------------- |
| `<<<image_1>>>`   | 引用 `metadata.image_list` 第 1 张图片      |
| `<<<video_1>>>`   | 引用 `video_list` 第 1 段视频               |
| `<<<element_1>>>` | 引用 `metadata.element_list` 第 1 个主体/角色 |

> ⚠️ **注意**
>
> `image_list`、`video_list`、`element_list` 的顺序必须分别与 prompt 中对应占位符的顺序一致。有视频参考时不要同时开启 `audio`。


## 响应

### `id`

`string`

任务 ID，用于查询任务状态。


### `client_business_id`

`string`

客户侧业务 ID。仅当请求中传入 `client_business_id` 时返回。


### `object`

`string`

对象类型，通常为 `generation.task`。


### `model`

`string`

本次请求使用的模型名称。


### `status`

`string`

任务状态：`queued`、`in_progress`、`completed` 或 `failed`。


### `created_at`

`integer`

任务创建时间戳。


## 示例

### 文生视频

```json 
{
  "model": "kling-v3-omni",
  "client_business_id": "order_20260428_001",
  "prompt": "一只金毛犬在沙滩上奔跑，日落，电影质感",
  "mode": "std",
  "duration": 5,
  "aspect_ratio": "16:9"
}
```

### 图片引用

```json 
{
  "model": "kling-v3-omni",
  "prompt": "让<<<image_1>>>中的人物向镜头挥手",
  "mode": "pro",
  "duration": 5,
  "metadata": {
    "image_list": [
      {
        "image_url": "https://example.com/portrait.jpg"
      }
    ]
  }
}
```

### 有声视频

```json 
{
  "model": "kling-v3-omni",
  "prompt": "一只黄色小鸟在树枝上鸣叫，清晨阳光",
  "mode": "std",
  "duration": 5,
  "audio": true
}
```

### 参考视频输入

```json 
{
  "model": "kling-v3-omni",
  "prompt": "将视频中的背景替换为海边日落",
  "mode": "std",
  "video_list": [
    {
      "video_url": "https://example.com/source-video.mp4",
      "refer_type": "base",
      "keep_original_sound": "no"
    }
  ]
}
```

### 特征参考视频

```json 
{
  "model": "kling-v3-omni",
  "prompt": "<<<element_1>>>中的人物模仿<<<video_1>>>中的动作",
  "mode": "pro",
  "video_list": [
    {
      "video_url": "https://example.com/motion-reference.mp4",
      "refer_type": "feature",
      "keep_original_sound": "no"
    }
  ],
  "metadata": {
    "element_list": [
      {
        "url": "https://example.com/character.jpg",
        "type": "image",
        "role": "subject"
      }
    ]
  }
}
```

> 💡 **提示**
>
> 视频生成为异步任务。提交后使用 [获取视频任务状态](../../tasks/video-status) 查询进度和结果。


### 请求示例

```bash cURL 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "kling-v3-omni",
    "prompt": "让<<<image_1>>>中的人物向镜头挥手",
    "mode": "std",
    "duration": 5,
    "metadata": {
      "image_list": [{"image_url": "https://example.com/portrait.jpg"}]
    }
  }'
```

```python Python 
import requests

response = requests.post(
    "https://toapis.com/v1/videos/generations",
    headers={
        "Authorization": "Bearer <token>",
        "Content-Type": "application/json",
    },
    json={
        "model": "kling-v3-omni",
        "prompt": "让<<<image_1>>>中的人物向镜头挥手",
        "mode": "std",
        "duration": 5,
        "metadata": {
            "image_list": [{"image_url": "https://example.com/portrait.jpg"}],
        },
    },
)

print(response.json())
```

```javascript JavaScript 
const response = await fetch("https://toapis.com/v1/videos/generations", {
  method: "POST",
  headers: {
    Authorization: "Bearer <token>",
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    model: "kling-v3-omni",
    prompt: "让<<<image_1>>>中的人物向镜头挥手",
    mode: "std",
    duration: 5,
    metadata: {
      image_list: [{ image_url: "https://example.com/portrait.jpg" }]
    }
  })
});

console.log(await response.json());
```

