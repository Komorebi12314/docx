> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Qwen Image 3.0 图像生成

> 使用 qwen-image-3.0 或 qwen-image-3.0-pro 进行文生图和多参考图生成

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 支持 `qwen-image-3.0` 和 `qwen-image-3.0-pro`
* 支持文生图、图生图和多图参考，最多传入 3 张参考图
* 支持 1K、2K 分辨率和 7 种常用宽高比
* 每次请求固定生成 1 张图片，`n` 必须为 `1`
* 异步执行，提交成功后通过任务 ID 查询结果

> ⚠️ **注意**
>
> `image_urls` 仅支持可公开访问的图片 URL，不支持 base64 Data URI。请先使用[上传图片接口](../../uploads/images)上传本地图片，再将返回的 URL 传给本接口。


## 支持模型

| 模型                   | 文生图 | 图生图 | 参考图上限 | 输出数量   |
| -------------------- | --- | --- | ----- | ------ |
| `qwen-image-3.0`     | 支持  | 支持  | 3 张   | 固定 1 张 |
| `qwen-image-3.0-pro` | 支持  | 支持  | 3 张   | 固定 1 张 |

## Authorizations

### `Authorization`

`string` · 必填

所有接口均需要使用 Bearer Token 认证。

访问 [API Key 管理页面](https://toapis.com/console/token) 获取 API Key，并添加到请求头：

```text 
Authorization: Bearer YOUR_API_KEY
```


## Body

### `model`

`string` · 必填

图像生成模型名称，只支持：

* `qwen-image-3.0`
* `qwen-image-3.0-pro`


### `prompt`

`string` · 必填

图像生成或编辑指令。不能是空字符串。


### `size`

`string`

输出图像的宽高比。推荐显式传入以下值之一：

`1:1`、`4:3`、`3:4`、`16:9`、`9:16`、`3:2`、`2:3`

也支持 `WIDTH*HEIGHT` 或 `WIDTHxHEIGHT` 像素格式。像素总面积必须在 `512*512` 到 `2048*2048` 之间，宽高比必须在 `1:8` 到 `8:1` 之间。

不传时由模型自动推荐尺寸。


### `resolution`

`string` · 默认值：`1K`

当 `size` 使用宽高比时，控制输出分辨率档位：

* `1K` - 默认
* `2K`

也兼容放在 `metadata.resolution` 中，推荐使用顶层 `resolution`。


### `n`

`integer` · 默认值：`1`

生成图片数量，固定为 `1`。

> ⚠️ **注意**
>
> 传入 `2` 或更大的值会返回 `400 invalid_request`。


### `image_urls`

`string[]`

参考图 URL 列表，用于图生图、图片编辑或多图参考生成。

* 最多 3 张
* 仅支持 URL，不支持 base64 Data URI
* 本地图片可先通过[上传图片接口](../../uploads/images)获取 URL


### `client_business_id`

`string`

您自己的订单号、流水号或业务任务 ID。传入后，可使用同一个图片任务查询接口按该 ID 查询结果。


### `metadata`

`object`

Qwen Image 高级参数。

<details>
<summary>metadata 属性</summary>

**`metadata.prompt_extend`** — `boolean` · 默认值：`true`

是否自动优化和扩展提示词。


**`metadata.prompt_extend_mode`** — `string`

提示词扩展模式：

* `direct` - 直接扩展
* `agent` - Agent 扩展，仅用于文生图

当请求包含 `image_urls` 时，`agent` 会自动转换为 `direct`。


**`metadata.negative_prompt`** — `string`

负面提示词，描述不希望出现在结果中的内容。


**`metadata.seed`** — `integer`

随机种子。使用相同参数和种子有助于获得相近结果，但不保证完全一致。


**`metadata.watermark`** — `boolean` · 默认值：`false`

是否添加水印。


## 分辨率与像素映射

当 `size` 传入宽高比时，ToAPIs 会按下表转换为最终像素尺寸。两个模型使用相同的映射。

| 宽高比    | 1K        | 2K        |
| ------ | --------- | --------- |
| `1:1`  | 1024×1024 | 2048×2048 |
| `4:3`  | 1152×864  | 1600×1200 |
| `3:4`  | 864×1152  | 1200×1600 |
| `16:9` | 1280×720  | 1920×1080 |
| `9:16` | 720×1280  | 1080×1920 |
| `3:2`  | 1152×768  | 1728×1152 |
| `2:3`  | 768×1152  | 1152×1728 |

## Response

### `id`

`string`

任务唯一标识符，用于查询任务状态。


### `object`

`string`

对象类型，固定为 `generation.task`。


### `model`

`string`

本次请求使用的模型。


### `status`

`string`

任务状态：`queued`、`in_progress`、`completed` 或 `failed`。


### `progress`

`integer`

任务进度百分比，范围为 0-100。


### `created_at`

`integer`

任务创建时间，Unix 时间戳。


## 请求示例

```bash cURL（文生图） 
curl --request POST \
  --url https://toapis.com/v1/images/generations \
  --header 'Authorization: Bearer <YOUR_API_KEY>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "qwen-image-3.0",
    "prompt": "一张东方奇幻电影海报，云海之上的古城，金色晨光，画面包含清晰中文标题「云上长安」",
    "size": "16:9",
    "resolution": "2K",
    "n": 1,
    "metadata": {
      "prompt_extend": true,
      "negative_prompt": "模糊，低质量，文字错误",
      "watermark": false
    }
  }'
```

```bash cURL（多图参考） 
curl --request POST \
  --url https://toapis.com/v1/images/generations \
  --header 'Authorization: Bearer <YOUR_API_KEY>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "qwen-image-3.0-pro",
    "prompt": "保留第一张图的人物和第二张图的服装设计，将场景改为现代杂志封面，增强面部和材质细节",
    "image_urls": [
      "https://example.com/person.png",
      "https://example.com/outfit.png"
    ],
    "size": "3:4",
    "resolution": "2K",
    "n": 1,
    "metadata": {
      "prompt_extend": true,
      "prompt_extend_mode": "direct",
      "watermark": false
    }
  }'
```

```python Python 
import requests

response = requests.post(
    "https://toapis.com/v1/images/generations",
    headers={
        "Authorization": "Bearer <YOUR_API_KEY>",
        "Content-Type": "application/json",
    },
    json={
        "model": "qwen-image-3.0-pro",
        "prompt": "一张高端香水产品海报，黑金配色，棚拍光影，细节清晰",
        "size": "1:1",
        "resolution": "2K",
        "n": 1,
        "metadata": {
            "prompt_extend": True,
            "watermark": False,
        },
    },
)
response.raise_for_status()
task = response.json()
print(task["id"], task["status"])
```

```javascript JavaScript 
const response = await fetch("https://toapis.com/v1/images/generations", {
  method: "POST",
  headers: {
    Authorization: "Bearer <YOUR_API_KEY>",
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    model: "qwen-image-3.0",
    prompt: "A cinematic product photo of a transparent mechanical watch",
    size: "4:3",
    resolution: "1K",
    n: 1,
    metadata: {
      prompt_extend: true,
      watermark: false
    }
  })
});

if (!response.ok) {
  throw new Error(await response.text());
}

const task = await response.json();
console.log(task.id, task.status);
```


## 提交成功响应

### 响应示例

```json 200 
{
  "id": "task_img_abc123def456",
  "object": "generation.task",
  "model": "qwen-image-3.0-pro",
  "status": "queued",
  "progress": 0,
  "created_at": 1787270400
}
```


## 查询任务

使用提交响应中的 `id` 查询任务：

```bash 
curl --request GET \
  --url https://toapis.com/v1/images/generations/task_img_abc123def456 \
  --header 'Authorization: Bearer <YOUR_API_KEY>'
```

完整字段和轮询建议请参阅[获取图片任务状态](../../tasks/image-status)。

### 任务完成响应

```json 
{
  "id": "task_img_abc123def456",
  "object": "generation.task",
  "model": "qwen-image-3.0-pro",
  "status": "completed",
  "progress": 100,
  "created_at": 1787270400,
  "completed_at": 1787270458,
  "expires_at": 1787356858,
  "result": {
    "type": "image",
    "data": [
      {
        "url": "https://files.toapis.com/generated/qwen-image-result.png"
      }
    ]
  }
}
```

> ⚠️ **注意**
>
> 生成结果 URL 的有效期为 24 小时，请在 `expires_at` 之前下载或转存图片。


## 计费说明

* 每次成功输出：`$0.03`
* 每张输入参考图：`$0.003`
* 参考图没有免费额度
* `qwen-image-3.0` 与 `qwen-image-3.0-pro` 当前使用相同计费规则
