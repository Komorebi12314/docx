> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Vidu 图片生成

> 使用 Vidu 图片系列模型生成图片或基于参考图生成图片，返回统一 generation.task。

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


## 接口地址

`POST /v1/images/generations`

## 支持模型

* `vidu-image`
* `viduq3-fast`
* `viduq2-pro`
* `viduq2-fast`

## 模型说明

| 模型            | 类型                 | 分辨率                | 比例                                                      |
| ------------- | ------------------ | ------------------ | ------------------------------------------------------- |
| `vidu-image`  | 通用参考图生图            | `1K` / `2K` / `4K` | `1:1` / `4:3` / `3:4` / `16:9` / `9:16` / `3:2` / `2:3` |
| `viduq3-fast` | Vidu Q3 Fast 参考图生图 | `1K` / `2K` / `4K` | 同上                                                      |
| `viduq2-pro`  | Vidu Q2 Pro 参考图生图  | `1K` / `2K` / `4K` | 同上                                                      |
| `viduq2-fast` | Vidu Q2 Fast 参考图生图 | `1K`               | 同上                                                      |

## 请求参数

### `model`

`string` · 必填

只支持这 4 个模型名：

* `vidu-image`
* `viduq3-fast`
* `viduq2-pro`
* `viduq2-fast`


### `prompt`

`string` · 必填

文本提示词


### `image_urls`

`string[]`

参考图 URL，支持 0-7 张


### `n`

`integer` · 默认值：`1`

仅支持 `1`


### `size`

`string` · 默认值：`1:1`

支持比例值，也支持像素值，例如 `1024*1024`

支持的比例值：

* `1:1`
* `4:3`
* `3:4`
* `16:9`
* `9:16`
* `3:2`
* `2:3`


### `metadata.resolution`

`string` · 默认值：`1K`

当 `size` 传比例值时可选分辨率：

* `1K`
* `2K`
* `4K`

`viduq2-fast` 仅支持 `1K`。当 `size` 使用比例值且 `metadata.resolution` 为 `2K` 或 `4K` 时会直接报错。


### `seed`

`integer`

随机种子


### `metadata.watermark`

`boolean` · 默认值：`false`

是否加水印


## 请求示例

```bash cURL 
curl --request POST \
  --url https://toapis.com/v1/images/generations \
  --header 'Authorization: Bearer <YOUR_API_KEY>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "viduq3-fast",
    "prompt": "生成一张电影级产品海报，保持参考图主体结构一致，背景更干净。",
    "image_urls": [
      "https://example.com/reference-1.png",
      "https://example.com/reference-2.png"
    ],
    "size": "1:1",
    "metadata": {
      "resolution": "2K",
      "watermark": false
    },
    "seed": 42,
    "n": 1
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
        "model": "viduq3-fast",
        "prompt": "生成一张电影级产品海报，保持参考图主体结构一致，背景更干净。",
        "image_urls": [
            "https://example.com/reference-1.png",
            "https://example.com/reference-2.png",
        ],
        "size": "1:1",
        "metadata": {
            "resolution": "2K",
            "watermark": False,
        },
        "seed": 42,
        "n": 1,
    },
)

task = response.json()
print(task["id"])
print(task["status"])
```

```javascript JavaScript 
const response = await fetch('https://toapis.com/v1/images/generations', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer <YOUR_API_KEY>',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'viduq3-fast',
    prompt: '生成一张电影级产品海报，保持参考图主体结构一致，背景更干净。',
    image_urls: [
      'https://example.com/reference-1.png',
      'https://example.com/reference-2.png'
    ],
    size: '1:1',
    metadata: {
      resolution: '2K',
      watermark: false
    },
    seed: 42,
    n: 1
  })
});

const task = await response.json();
console.log(task.id);
console.log(task.status);
```


## 提交成功响应

### 响应示例

```json 200 
{
  "id": "task_01KABCDEF1234567890",
  "object": "generation.task",
  "model": "viduq3-fast",
  "status": "queued",
  "progress": 0,
  "created_at": 1784169600
}
```


如果请求中带了 `client_business_id`，响应顶层也会带出该字段。

## 查询任务

`GET /v1/images/generations/{task_id}`

### 处理中

```json 
{
  "id": "task_01KABCDEF1234567890",
  "object": "generation.task",
  "model": "viduq3-fast",
  "status": "in_progress",
  "progress": 50,
  "created_at": 1784169600
}
```

### 成功

```json 
{
  "id": "task_01KABCDEF1234567890",
  "object": "generation.task",
  "model": "viduq3-fast",
  "status": "completed",
  "progress": 100,
  "created_at": 1784169600,
  "completed_at": 1784169660,
  "expires_at": 1784256060,
  "result": {
    "type": "image",
    "data": [
      {
        "url": "https://cdn.toapis.com/images/task_01KABCDEF1234567890/0.png"
      }
    ]
  }
}
```

### 失败

```json 
{
  "id": "task_01KABCDEF1234567890",
  "object": "generation.task",
  "model": "viduq2-fast",
  "status": "failed",
  "progress": 100,
  "created_at": 1784169600,
  "completed_at": 1784169620,
  "error": {
    "code": "InvalidParameter",
    "message": "resolution 4K is not supported for viduq2-fast"
  }
}
```

## 计费与行为说明

* 这 4 个模型都走统一图片异步任务接口：`POST /v1/images/generations`
* 返回值中的 `object` 固定为 `generation.task`
* 结果完成后通过 `result.data[].url` 返回图片地址
* `viduq2-fast` 是轻量规格，只保留 `1K`
* 如需更高分辨率，优先使用 `vidu-image`、`viduq3-fast` 或 `viduq2-pro`

## 说明

* Vidu 图片渠道会先在上游创建任务，再轮询上游任务状态。
* 成功结果会镜像到 ToAPIs 自有 R2，再返回统一图片任务响应。
* `expires_at` 为 `completed_at + 24h`。
