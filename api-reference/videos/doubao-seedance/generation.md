> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Doubao SeeDance 视频生成

> 使用字节跳动豆包 Doubao SeeDance 模型生成视频

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 字节跳动豆包视频生成模型
* 通过 model 参数选择 `doubao-seedance-1-0-pro-fast` 或 `doubao-seedance-1-0-pro-quality` 模型
* 支持文本到视频生成
* 支持首帧/尾帧/参考图控制
* 异步任务管理，通过任务 ID 查询结果

> ⚠️ **注意**
>
> **重要变更**：为了更好的性能和成本控制，我们不再支持在 `image_urls` 中直接传入 base64 图片数据。请先使用 [上传图片接口](../../uploads/images) 上传图片，获取 URL 后再调用本接口。


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

`string` · 必填 · 默认值：`doubao-seedance-1-0-pro-fast`

视频生成模型名称

可用模型：

* `doubao-seedance-1-0-pro-fast` - 快速版（40-90 秒生成）
* `doubao-seedance-1-0-pro-quality` - 高质量版（90-300 秒生成）


### `private_asset_review`

`boolean` · 默认值：`false`

可选, 默认 `false`. 设为 `true` 时按所选渠道能力准备并审核素材; 不支持私有素材库的渠道跳过提审, 沿用原有生成流程.

仅用于包含以下媒体字段的异步生成请求: `image_urls`, `image_with_roles`.

纯文本或仅在 metadata 中提供素材的请求请省略或设为 `false`. 不适用于独立的 remix 或 extend 接口. 设为 `true` 时拒绝 `asset://`, 模型原有的媒体格式和数量限制不变. 详见[按需素材审核](../private-assets).


### `prompt`

`string` · 必填

视频内容描述

详细描述场景、动作、风格以获得更好的生成效果

示例：`"海滩日落，金色阳光照在海面上，海浪轻轻拍打沙滩"`


### `duration`

`integer` · 默认值：`5`

视频时长（秒）

支持范围：`2` \~ `12` 秒

默认：`5`


### `aspect_ratio`

`string` · 默认值：`16:9`

视频宽高比

可选项：

* `16:9` - 横屏
* `9:16` - 竖屏
* `1:1` - 方形
* `4:3` - 传统比例
* `3:4` - 竖向传统比例
* `21:9` - 超宽屏

默认：`16:9`


### `resolution`

`string` · 默认值：`720p`

视频分辨率

可选项：

* `480p` - 标清
* `720p` - 高清
* `1080p` - 全高清

默认：`720p`

**1080p 限制**：使用参考图（`image_with_roles` 中 `role: reference`）时，不支持 1080p 分辨率


## 分辨率与宽高比组合

| 分辨率   | 支持的宽高比                          | 备注     |
| ----- | ------------------------------- | ------ |
| 480p  | 16:9, 4:3, 1:1, 3:4, 9:16, 21:9 | 全部支持   |
| 720p  | 16:9, 4:3, 1:1, 3:4, 9:16, 21:9 | 全部支持   |
| 1080p | 16:9, 4:3, 1:1, 3:4, 9:16, 21:9 | 不支持参考图 |

### `image_urls`

`string[]`

首帧图像 URL 数组，用于图生视频

**⚠️ 仅支持 URL 格式（不再支持 base64）**

* 公开可访问的图像 URL（http\:// 或 https\://）
* 可使用 [上传图片接口](../../uploads/images) 上传本地图片获取 URL

示例：`["https://example.com/cat.png"]`

`image_urls` 和 `image_with_roles` 不能同时使用


### `image_with_roles`

`array`

带角色的图像数组，用于更精确的控制

<details>
<summary>字段说明</summary>

**`url`** — `string` · 必填

图像 URL 地址


**`role`** — `string` · 必填

图像角色

可选项：

* `first_frame` - 首帧图，作为视频起始画面（仅支持一张）
* `last_frame` - 尾帧图，作为视频结束画面（**仅 quality 版本支持**，仅支持一张）
* `reference` - 参考图，用于指导视频风格（仅支持一张）


示例：

```json 
[
  {"url": "https://example.com/start.png", "role": "first_frame"},
  {"url": "https://example.com/end.png", "role": "last_frame"}
]
```

> ⚠️ **注意**
>
> * `image_urls` 和 `image_with_roles` 不能同时使用
> * 每种角色的图片仅支持上传一张
> * `last_frame`（尾帧图）仅 `doubao-seedance-1-0-pro-quality` 版本支持，fast 版本不支持首尾帧同时使用


### `metadata`

`object`

扩展参数（可选）

<details>
<summary>字段说明</summary>

**`seed`** — `integer`

种子整数，用于控制生成内容的随机性

取值范围：`-1` \~ `2^32-1`

相同 seed 值会生成类似结果，但不保证完全一致


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


### 请求示例

```bash cURL（快速预览横屏视频） 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "doubao-seedance-1-0-pro-fast",
    "prompt": "海滩日落，金色阳光照在海面上，海浪轻轻拍打沙滩",
    "duration": 5,
    "aspect_ratio": "16:9",
    "resolution": "720p"
  }'
```

```bash cURL（高质量竖屏短视频） 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "doubao-seedance-1-0-pro-quality",
    "prompt": "女孩在樱花树下旋转，花瓣随风飘落",
    "duration": 5,
    "aspect_ratio": "9:16",
    "resolution": "1080p"
  }'
```

```bash cURL（首尾帧动态过渡） 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "doubao-seedance-1-0-pro-quality",
    "prompt": "画面从白天逐渐过渡到夜晚，城市灯光逐渐亮起",
    "duration": 5,
    "image_with_roles": [
      {"url": "https://example.com/day.png", "role": "first_frame"},
      {"url": "https://example.com/night.png", "role": "last_frame"}
    ]
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
        "model": "doubao-seedance-1-0-pro-fast",
        "prompt": "海滩日落，金色阳光照在海面上，海浪轻轻拍打沙滩",
        "duration": 5,
        "aspect_ratio": "16:9",
        "resolution": "720p"
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
    model: 'doubao-seedance-1-0-pro-fast',
    prompt: '海滩日落，金色阳光照在海面上，海浪轻轻拍打沙滩',
    duration: 5,
    aspect_ratio: '16:9',
    resolution: '720p'
  })
});

const task = await response.json();
console.log(`任务 ID: ${task.id}`);
console.log(`状态: ${task.status}`);
```


### 响应示例

```json 200 
{
  "id": "task_vid_xyz789ghi012",
  "object": "generation.task",
  "model": "doubao-seedance-1-0-pro-fast",
  "status": "queued",
  "progress": 0,
  "created_at": 1703884800,
  "metadata": {}
}
```

