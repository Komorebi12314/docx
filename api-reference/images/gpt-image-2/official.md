> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# GPT-Image-2 官方渠道 图像生成

> 使用 OpenAI 官方 gpt-image-2-official 模型生成图像，支持文生图 / 图生图 / 局部重绘（mask）三合一，1K / 2K / 4K 分辨率档位

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* OpenAI 官方 `gpt-image-2-official` 模型
* 异步处理模式，返回任务 ID 用于后续查询
* 支持文生图、多参考图图生图、遮罩局部重绘（inpainting）
* 支持 13 种宽高比，可选 1K / 2K / 4K 三档分辨率
* 单次最多生成 4 张图，参考图最多 16 张

## Authorizations

### `Authorization`

`string` · 必填

所有接口均需要使用 Bearer Token 进行认证

获取 API Key：访问 [API Key 管理页面](https://toapis.com/console/token) 获取您的 API Key

使用时在请求头中添加：

```
Authorization: Bearer YOUR_API_KEY
```


## Body

### `model`

`string` · 必填 · 默认值：`gpt-image-2-official`

图像生成模型名称

固定填写 `gpt-image-2-official`


### `prompt`

`string` · 必填

图像生成的文本描述

支持中英文，建议详细描述场景、风格和构图


### `size`

`string` · 默认值：`1:1`

画面宽高比

支持以下预设比例，也可传 `auto` 由上游自动选择：

`1:1` · `3:2` · `2:3` · `4:3` · `3:4` · `5:4` · `4:5` · `16:9` · `9:16` · `2:1` · `1:2` · `21:9` · `9:21`

也支持使用 `宽:高` 格式传入任意比例，例如 `1:3`、`7:4`。任意比例必须满足下方的尺寸约束。

使用 `auto` 时，最终宽高比和像素尺寸由上游决定，无法保证固定输出。


### `resolution`

`string` · 默认值：`1k`

分辨率档位

* `1k` — 1024 基准，速度快，日常够用（默认）
* `2k` — 2048 基准，适合海报 / 高清需求
* `4k` — 3840 基准，`high` 质量下耗时可能超过 120 秒


### 尺寸对照表

| size   | 1K          | 2K          | 4K          |
| ------ | ----------- | ----------- | ----------- |
| `1:1`  | `1024x1024` | `2048x2048` | `2880x2880` |
| `3:2`  | `1536x1024` | `2048x1360` | `3520x2336` |
| `2:3`  | `1024x1536` | `1360x2048` | `2336x3520` |
| `4:3`  | `1024x768`  | `2048x1536` | `3312x2480` |
| `3:4`  | `768x1024`  | `1536x2048` | `2480x3312` |
| `5:4`  | `1280x1024` | `2560x2048` | `3216x2576` |
| `4:5`  | `1024x1280` | `2048x2560` | `2576x3216` |
| `16:9` | `1536x864`  | `2048x1152` | `3840x2160` |
| `9:16` | `864x1536`  | `1152x2048` | `2160x3840` |
| `2:1`  | `2048x1024` | `2688x1344` | `3840x1920` |
| `1:2`  | `1024x2048` | `1344x2688` | `1920x3840` |
| `21:9` | `2016x864`  | `2688x1152` | `3840x1648` |
| `9:21` | `864x2016`  | `1152x2688` | `1648x3840` |

### 任意分辨率

除上述预设比例外，可以通过 `size` 的 `宽:高` 格式请求任意比例。服务端会根据 `resolution` 档位计算实际像素尺寸。请求的宽高必须满足：

* 宽和高都必须是 16 像素的倍数
* 长边最大可达 3,840 像素（4K）
* 宽高比最大可达 3:1
* 像素总数范围为 655,360–8,294,400

例如：

* `size: "1:3"`、`resolution: "2k"` → `1024x3072`
* `size: "7:4"`、`resolution: "1k"` → `1344x768`

```bash 
curl --request POST \
  --url https://toapis.com/v1/images/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gpt-image-2-official",
    "prompt": "白色背景上的红色圆形，简洁测试图",
    "size": "7:4",
    "resolution": "1k",
    "quality": "medium",
    "n": 1
  }'
```

### `quality`

`string` · 默认值：`high`

图片质量

* `low` — 快速省钱，适合草稿/预览
* `medium` — 平衡速度与质量
* `high` — 最高精度，默认值（4K + high 耗时可达 120s+）


### `background`

`string` · 默认值：`auto`

生成图像的背景样式

* `auto` — 由模型自动决定（默认）
* `transparent` — 透明背景
* `opaque` — 不透明背景

> 💡 **提示**
>
> 透明背景建议搭配 PNG 输出使用。
### `output_format`

`string` · 默认值：`png`

输出格式

* `png` — 默认
* `jpeg` — 文件更小（支持压缩）

> 💡 **提示**
>
> Azure OpenAI 不支持 `webp` 格式。
### `output_compression`

`integer` · 默认值：`100`

JPEG 压缩强度，范围 `0–100`（`0` 不压缩，`100` 最大压缩，默认 `100`）

仅对 `output_format: "jpeg"` 有效


### `n`

`integer` · 默认值：`1`

生成图片张数

取值范围：`1 ~ 10`


### `image_urls`

`string[]`

参考图 URL 数组，用于图生图

* 最多 **16 张**，须为公网可访问的稳定 URL
* 可先使用 [上传图片接口](../../uploads/images) 获取 URL


### `mask_url`

`string`

遮罩图 URL，用于局部重绘（inpainting）

需搭配 `image_urls` 使用，遮罩图尺寸须与首张参考图一致，且需包含 Alpha 通道（透明区域为待重绘区域）


## Response

### `id`

`string`

任务唯一标识符，用于查询任务状态


### `object`

`string`

对象类型，固定为 `generation.task`


### `model`

`string`

使用的模型名称


### `status`

`string`

任务状态

* `queued` — 排队等待处理
* `in_progress` — 处理中
* `completed` — 成功完成
* `failed` — 失败


### `progress`

`integer`

任务进度百分比（0-100）


### `created_at`

`integer`

任务创建时间戳（Unix 时间戳）


### 请求示例

```bash 文生图 
curl --request POST \
  --url https://toapis.com/v1/images/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gpt-image-2-official",
    "prompt": "星空下的古老城堡，电影感光影，超写实风格",
    "size": "16:9",
    "resolution": "2k",
    "quality": "high",
    "n": 1
  }'
```

```bash 4K 壁纸 
curl --request POST \
  --url https://toapis.com/v1/images/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gpt-image-2-official",
    "prompt": "雪山日出全景，极致细节",
    "size": "16:9",
    "resolution": "4k",
    "quality": "high",
    "output_format": "jpeg",
    "output_compression": 90
  }'
```

```bash 图生图（多参考图） 
curl --request POST \
  --url https://toapis.com/v1/images/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gpt-image-2-official",
    "prompt": "将两张参考图融合成一张插画海报，保留主体轮廓",
    "size": "1:1",
    "quality": "high",
    "image_urls": [
      "https://example.com/input-a.png",
      "https://example.com/input-b.png"
    ]
  }'
```

```bash 局部重绘（mask） 
curl --request POST \
  --url https://toapis.com/v1/images/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gpt-image-2-official",
    "prompt": "把背景换成沙漠日落",
    "size": "1:1",
    "quality": "medium",
    "image_urls": ["https://example.com/photo.png"],
    "mask_url": "https://example.com/mask.png"
  }'
```

```javascript JavaScript 
const response = await fetch('https://toapis.com/v1/images/generations', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-ToAPIs-key',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'gpt-image-2-official',
    prompt: '星空下的古老城堡，电影感光影，超写实风格',
    size: '16:9',
    resolution: '2k',
    quality: 'high',
    n: 1
  })
});

const task = await response.json();
console.log(task.id, task.status);
```


### 响应示例

```json 200 
{
  "id": "tsk_img_01KPTXXXXXXXXXXXXXXX",
  "object": "generation.task",
  "model": "gpt-image-2-official",
  "status": "queued",
  "progress": 0,
  "created_at": 1703884800,
  "metadata": {}
}
```

