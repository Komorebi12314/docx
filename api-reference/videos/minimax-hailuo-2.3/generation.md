> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# MiniMax-Hailuo-2.3 视频生成

> 使用 MiniMax Hailuo 2.3 系列模型生成视频，支持文生视频和图生视频，可选 Fast 快速模式

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 异步任务接口，提交后返回任务 ID
* 支持模型：`MiniMax-Hailuo-2.3`、`MiniMax-Hailuo-2.3-Fast`
* `MiniMax-Hailuo-2.3`：支持文生视频和图生视频，画质最优
* `MiniMax-Hailuo-2.3-Fast`：**仅支持图生视频**（必须传入首帧图片），生成速度更快

> ⚠️ **注意**
>
> 请传入公网可访问的图片 URL。不要在 `image_urls` 中直接传 base64 图片数据；本地图片请先使用 [上传图片接口](../../uploads/images) 获取 URL。


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

模型名称。

可选值：

* `MiniMax-Hailuo-2.3` - 支持文生视频和图生视频
* `MiniMax-Hailuo-2.3-Fast` - 仅支持图生视频（必须传入 `image_urls`）


### `prompt`

`string` · 必填

视频内容描述，最大 **2000 字符**。

支持 15 种运镜指令（如 `[推进]`、`[拉远]`、`[左摇,上升]` 等），详见下方运镜指令表。

示例：`"一只猫咪在花园中奔跑 [推进]，然后停下来看向镜头 [固定]"`


### `duration`

`integer` · 默认值：`6`

视频时长（秒）。

可选值：`6` 或 `10`

> ⚠️ **注意**
>
> 使用 `1080P` 分辨率时，仅支持 `6` 秒时长。


### `resolution`

`string` · 默认值：`768P`

视频分辨率。

可选值：

* `768P` - 高清（默认）
* `1080P` - 全高清（仅支持 6 秒时长）


### `image_urls`

`string[]`

首帧图片 URL 数组。

* 不传：文生视频（`MiniMax-Hailuo-2.3-Fast` 不支持，必须传入）
* 传 1 张：图生视频，图片作为视频起始帧

图片要求：

* 格式：JPG、JPEG、PNG、WebP
* 大小：小于 20MB
* 尺寸：短边 > 300px，长宽比在 2:5 \~ 5:2 之间

示例：`["https://example.com/first-frame.jpg"]`


### `metadata`

`object`

扩展参数。

<details>
<summary>显示 metadata 字段</summary>

**`prompt_optimizer`** — `boolean` · 默认值：`true`

是否自动优化 prompt。设为 `false` 可进行更精确的控制。


**`fast_pretreatment`** — `boolean` · 默认值：`false`

是否缩短 prompt 优化耗时。启用后可加快处理速度。


**`aigc_watermark`** — `boolean` · 默认值：`false`

是否在生成的视频中添加水印。


**`callback_url`** — `string`

ToAPIs 最终任务 Webhook。需先配置 Token URL 和签名密钥；详见 [任务 Webhook](/docs/cn/api-reference/webhooks/task-webhooks)。


## 模型对比

| 模型                        | 文生视频 |   图生视频  | 分辨率              | 时长       |
| ------------------------- | :--: | :-----: | ---------------- | -------- |
| `MiniMax-Hailuo-2.3`      |   ✅  |    ✅    | `768P` / `1080P` | 6s / 10s |
| `MiniMax-Hailuo-2.3-Fast` |   ❌  | ✅（必传首帧） | `768P` / `1080P` | 6s / 10s |

## 分辨率与时长组合

| 分辨率   | 支持的时长    | 备注       |
| ----- | -------- | -------- |
| 768P  | 6 秒、10 秒 | 默认分辨率    |
| 1080P | 6 秒      | 不支持 10 秒 |

## 运镜指令

在 `prompt` 中使用 `[指令]` 语法控制运镜效果：

| 类别  | 指令                   |
| --- | -------------------- |
| 平移  | `[左移]` `[右移]`        |
| 左右摇 | `[左摇]` `[右摇]`        |
| 推拉  | `[推进]` `[拉远]`        |
| 升降  | `[上升]` `[下降]`        |
| 上下摇 | `[上摇]` `[下摇]`        |
| 变焦  | `[变焦推近]` `[变焦拉远]`    |
| 其他  | `[晃动]` `[跟随]` `[固定]` |

**使用规则**：

* 组合运镜：同一 `[]` 内多个指令同时生效，如 `[左摇,上升]`，建议不超过 3 个
* 顺序运镜：prompt 中前后出现的指令依次生效，如 `"...[推进]，然后...[拉远]"`

## 响应

### `id`

`string`

任务 ID，用于查询任务状态。


### `object`

`string`

对象类型，固定为 `generation.task`。


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
  "model": "MiniMax-Hailuo-2.3",
  "prompt": "一只猫咪在花园中奔跑，镜头缓缓推近，电影质感",
  "duration": 6,
  "resolution": "1080P"
}
```

### 图生视频

```json 
{
  "model": "MiniMax-Hailuo-2.3",
  "prompt": "让图片中的人物缓缓转身并微笑",
  "image_urls": ["https://example.com/portrait.jpg"],
  "duration": 6,
  "resolution": "1080P"
}
```

### 图生视频（Fast 快速模式）

```json 
{
  "model": "MiniMax-Hailuo-2.3-Fast",
  "prompt": "人物从静止开始缓慢行走",
  "image_urls": ["https://example.com/person.jpg"],
  "duration": 6,
  "resolution": "768P"
}
```

### 运镜控制

```json 
{
  "model": "MiniMax-Hailuo-2.3",
  "prompt": "一个人拿起一本书 [上升]，然后开始阅读 [固定]",
  "duration": 6,
  "resolution": "768P"
}
```

### 10 秒长视频

```json 
{
  "model": "MiniMax-Hailuo-2.3",
  "prompt": "海浪拍打沙滩，日落时分，金色光芒洒在海面上",
  "duration": 10,
  "resolution": "768P",
  "metadata": {
    "prompt_optimizer": true,
    "fast_pretreatment": true
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
    "model": "MiniMax-Hailuo-2.3",
    "prompt": "一只猫咪在花园中奔跑，镜头缓缓推近，电影质感",
    "duration": 6,
    "resolution": "1080P"
  }'
```

```python Python 
import requests

response = requests.post(
    "https://toapis.com/v1/videos/generations",
    headers={
        "Authorization": "Bearer your-ToAPIs-key",
        "Content-Type": "application/json",
    },
    json={
        "model": "MiniMax-Hailuo-2.3",
        "prompt": "一只猫咪在花园中奔跑，镜头缓缓推近，电影质感",
        "duration": 6,
        "resolution": "1080P",
    },
)

print(response.json())
```

```javascript JavaScript 
const response = await fetch("https://toapis.com/v1/videos/generations", {
  method: "POST",
  headers: {
    Authorization: "Bearer your-ToAPIs-key",
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    model: "MiniMax-Hailuo-2.3",
    prompt: "一只猫咪在花园中奔跑，镜头缓缓推近，电影质感",
    duration: 6,
    resolution: "1080P"
  })
});

console.log(await response.json());
```


### 响应示例

```json 200 
{
  "id": "vid_01J9HA7JPQ9A0Z6JZ3V8M9W6PZ",
  "object": "generation.task",
  "model": "MiniMax-Hailuo-2.3",
  "status": "queued",
  "progress": 0,
  "created_at": 1768380224,
  "metadata": {}
}
```

