> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Kling Video O1 视频生成

> 使用可灵 Kling Video O1 推理增强模型生成最高质量视频

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 异步处理模式，返回任务 ID 供后续查询
* **推理增强模型**，生成最高质量视频
* 使用官方 Omni 引用结构，支持 `image_list`、`video_list`、`element_list`
* 支持标准模式（720P）和专业模式（1080P）
* 支持参考视频编辑和特征参考

> ⚠️ **注意**
>
> 请传入公网可访问的图片或视频 URL。不要直接传 base64 图片数据；本地图片请先使用 [上传图片接口](../../uploads/images) 获取 URL。


## 认证

### `Authorization`

`string` · 必填

所有接口均需要使用 Bearer Token 进行认证

获取 API Key：访问 [API Key 管理页面](https://toapis.com/console/token) 获取您的 API Key

使用时在请求头中添加：

```
Authorization: Bearer YOUR_API_KEY
```


## 请求参数

### `model`

`string` · 必填

视频生成模型名称，固定为 `kling-video-o1`


### `prompt`

`string` · 必填

文字提示词，支持官方 Omni 占位符，编号从 1 开始：

* `<<<image_N>>>` 引用 `metadata.image_list`
* `<<<video_N>>>` 引用 `video_list`
* `<<<element_N>>>` 引用 `metadata.element_list`

示例：`"让<<<image_1>>>中的人物向镜头挥手"`

> 💡 **提示**
>
> 引用列表顺序必须与 prompt 中对应占位符顺序一致；系统不会自动补首帧或自动插入占位符。


### `client_business_id`

`string`

客户侧业务 ID，例如订单号、流水号或您系统内的任务 ID。提交后会随任务保存，后续可用该 ID 查询状态：
`GET /v1/videos/generations/{client_business_id}`。

也兼容放在 `metadata.client_business_id` 中，但推荐使用顶层字段。


### `mode`

`string` · 默认值：`std`

生成模式

可选值：

* `std` - 标准模式（720P）
* `pro` - 专业模式（1080P）

默认值：`std`


### `duration`

`integer` · 默认值：`5`

视频时长（秒）

可选值：`3`、`4`、`5`、`6`、`7`、`8`、`9`、`10`

默认值：`5`


### `aspect_ratio`

`string` · 默认值：`16:9`

视频宽高比

可选值：

* `16:9` - 横屏（默认）
* `9:16` - 竖屏
* `1:1` - 方形

默认值：`16:9`


### `video_list`

`object[]`

参考视频列表，最多 1 段视频

每个对象包含以下字段：

<details>
<summary>显示 video_list 对象字段</summary>

**`video_url`** — `string` · 必填

视频 URL，必须公开可访问

仅支持 MP4/MOV 格式；时长不少于 3 秒；分辨率 720px-2160px；帧率 24-60fps；大小不超过 200MB


**`refer_type`** — `string` · 默认值：`base`

参考类型

可选值：

* `base` - 待编辑视频（默认）
* `feature` - 特征参考视频

默认值：`base`


**`keep_original_sound`** — `string` · 默认值：`no`

是否保留原视频声音

可选值：

* `yes` - 保留原声
* `no` - 不保留（默认）

默认值：`no`


> ⚠️ **注意**
>
> * `video_url` 不能为空，且视频 URL 需可访问
> * 当 `refer_type=base` 时：不能定义视频首尾帧；参考视频需 3–10 秒；生成视频时长以上传视频为准
> * 有视频参考时不要同时开启 `audio` / `sound`


### `metadata`

`object`

扩展参数

<details>
<summary>显示 metadata 字段</summary>

**`image_list`** — `object[]`

官方 Omni 图片列表。在 prompt 中通过 `<<<image_1>>>`、`<<<image_2>>>` 按顺序引用。

<details>
<summary>显示 image_list 对象字段</summary>

**`image_url`** — `string` · 必填

图片 URL，必须公网可访问。


**`type`** — `string`

图片类型。首尾帧可传 `first_frame`、`end_frame`；传 `end_frame` 时必须同时提供 `first_frame`。


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

是否添加水印


## Omni 引用语法

Video O1 使用官方 Omni 占位符引用输入素材：

| 语法                | 说明                                    |
| ----------------- | ------------------------------------- |
| `<<<image_1>>>`   | 引用 `metadata.image_list` 第 1 张图片      |
| `<<<video_1>>>`   | 引用 `video_list` 第 1 段视频               |
| `<<<element_1>>>` | 引用 `metadata.element_list` 第 1 个主体/角色 |

> ⚠️ **注意**
>
> `image_list`、`video_list`、`element_list` 的顺序必须分别与 prompt 中对应占位符的顺序一致。


## 响应

### `id`

`string`

任务唯一标识符，用于查询任务状态


### `client_business_id`

`string`

客户侧业务 ID。仅当请求中传入 `client_business_id` 时返回。


### `object`

`string`

对象类型，固定为 `generation.task`


### `model`

`string`

使用的模型名称


### `status`

`string`

任务状态

* `queued` - 排队等待处理
* `in_progress` - 处理中
* `completed` - 成功完成
* `failed` - 失败


### `progress`

`integer`

任务进度百分比（0-100）


### `created_at`

`integer`

任务创建时间戳（Unix 时间戳）


### `metadata`

`object`

任务元数据


## 使用场景

### 场景 1：文生视频（最高质量）

```json 
{
  "model": "kling-video-o1",
  "client_business_id": "order_20260428_001",
  "prompt": "黄金时刻的城市天际线，电影质感镜头",
  "mode": "pro",
  "duration": 5,
  "aspect_ratio": "16:9"
}
```

### 场景 2：图片引用（单张）

```json 
{
  "model": "kling-video-o1",
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

### 场景 3：多图片引用

```json 
{
  "model": "kling-video-o1",
  "prompt": "<<<image_1>>>中的角色走向<<<image_2>>>中的场景",
  "mode": "pro",
  "duration": 5,
  "metadata": {
    "image_list": [
      {"image_url": "https://example.com/character.jpg"},
      {"image_url": "https://example.com/scene.jpg"}
    ]
  }
}
```

### 场景 4：参考视频编辑（video\_list - base）

```json 
{
  "model": "kling-video-o1",
  "prompt": "将视频中的背景替换为海边日落",
  "video_list": [
    {
      "video_url": "https://example.com/source-video.mp4",
      "refer_type": "base",
      "keep_original_sound": "no"
    }
  ]
}
```

### 场景 5：特征参考视频（video\_list - feature）

```json 
{
  "model": "kling-video-o1",
  "prompt": "<<<element_1>>>中的人物模仿<<<video_1>>>中的动作",
  "video_list": [
    {
      "video_url": "https://example.com/dance-reference.mp4",
      "refer_type": "feature",
      "keep_original_sound": "no"
    }
  ],
  "mode": "std",
  "duration": 5,
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
> **查询任务结果**
>
> 视频生成为异步任务，提交后会返回任务 ID。使用 [获取任务状态](../../tasks/video-status) 接口查询生成进度和结果。


### 请求示例

```bash cURL 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "kling-video-o1",
    "prompt": "让<<<image_1>>>中的人物向镜头挥手",
    "mode": "std",
    "duration": 5,
    "aspect_ratio": "16:9",
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
        "Authorization": "Bearer your-ToAPIs-key",
        "Content-Type": "application/json"
    },
    json={
        "model": "kling-video-o1",
        "prompt": "让<<<image_1>>>中的人物向镜头挥手",
        "mode": "std",
        "duration": 5,
        "aspect_ratio": "16:9",
        "metadata": {
            "image_list": [{"image_url": "https://example.com/portrait.jpg"}],
        },
    }
)

task = response.json()
print(f"任务 ID: {task['id']}")
print(f"状态: {task['status']}")
```

```javascript JavaScript 
const response = await fetch('https://toapis.com/v1/videos/generations', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-ToAPIs-key',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'kling-video-o1',
    prompt: '让<<<image_1>>>中的人物向镜头挥手',
    mode: 'std',
    duration: 5,
    aspect_ratio: '16:9',
    metadata: {
      image_list: [{ image_url: 'https://example.com/portrait.jpg' }]
    }
  })
});

const task = await response.json();
console.log(`任务 ID: ${task.id}`);
console.log(`状态: ${task.status}`);
```


### 响应示例

```json 200 
{
  "id": "video_01J9HA7JPQ9A0Z6JZ3V8M9W6PZ",
  "object": "generation.task",
  "model": "kling-video-o1",
  "status": "queued",
  "progress": 0,
  "created_at": 1768380224,
  "metadata": {}
}
```

