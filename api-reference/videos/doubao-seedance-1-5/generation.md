> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Doubao SeeDance 1.5 Pro 视频生成

> 使用字节跳动豆包 Doubao SeeDance 1.5 Pro 模型生成视频

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 字节跳动豆包视频生成模型 1.5 Pro 版本
* 支持文本到视频生成
* 支持首帧/尾帧图控制
* 不支持参考图模式
* 支持音频生成（1.5 Pro 独有功能）
* 异步任务管理，通过任务 ID 查询结果

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

`string` · 必填 · 默认值：`doubao-seedance-1-5-pro`

视频生成模型名称

可用模型：

* `doubao-seedance-1-5-pro` - 1.5 Pro 版，支持音频生成和首帧/尾帧控制


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

支持范围：`4` \~ `12` 秒

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


## 分辨率与宽高比组合

| 分辨率   | 支持的宽高比                          | 备注       |
| ----- | ------------------------------- | -------- |
| 480p  | 16:9, 4:3, 1:1, 3:4, 9:16, 21:9 | 全部支持     |
| 720p  | 16:9, 4:3, 1:1, 3:4, 9:16, 21:9 | 全部支持（默认） |
| 1080p | 16:9, 4:3, 1:1, 3:4, 9:16, 21:9 | 全部支持     |

### `image_urls`

`string[]`

兼容图片 URL 数组，用于首尾帧图生视频

兼容规则：

* 1 张图片：作为 `first_frame`
* 2 张图片：分别作为 `first_frame` 和 `last_frame`
* 超过 2 张：仅使用前两张，其余忽略

建议优先使用 `image_with_roles` 显式指定首帧和尾帧

示例：`["https://example.com/first.png", "https://example.com/last.png"]`

`image_urls` 和 `image_with_roles` 不能同时使用


### `image_with_roles`

`array`

带角色的图像数组，用于显式首尾帧控制

<details>
<summary>字段说明</summary>

**`url`** — `string` · 必填

图像 URL 地址


**`role`** — `string` · 必填

图像角色

可选项：

* `first_frame` - 首帧图，作为视频起始画面（仅支持一张）
* `last_frame` - 尾帧图，作为视频结束画面（仅支持一张）


示例：

```json 
[
  {"url": "https://example.com/first.png", "role": "first_frame"},
  {"url": "https://example.com/last.png", "role": "last_frame"}
]
```

> ⚠️ **注意**
>
> * `image_urls` 和 `image_with_roles` 不能同时使用
> * 首帧和尾帧仅支持各一张
> * 1.5 Pro 不支持 `reference_image`（参考图）角色，如需参考图功能请使用 Seedance 2.0


### `metadata`

`object`

扩展参数

<details>
<summary>字段说明</summary>

**`resolution`** — `string` · 默认值：`720p`

视频分辨率

可选项：

* `480p` - 标清
* `720p` - 高清（默认）
* `1080p` - 全高清


**`seed`** — `integer`

种子整数，用于控制生成内容的随机性

取值范围：`-1` \~ `2^32-1`

相同 seed 值会生成类似结果，但不保证完全一致


**`audio`** — `boolean` · 默认值：`false`

是否生成音频

设置为 `true` 时，视频将包含 AI 生成的配套音频

**1.5 Pro 独有功能**


**`camerafixed`** — `boolean` · 默认值：`false`

是否固定摄像头

设置为 `true` 时，摄像头位置保持固定


## 与 1.0 版本的差异

| 特性     | 1.0 fast/quality | 1.5 Pro                                |
| ------ | ---------------- | -------------------------------------- |
| 默认分辨率  | 1080p            | **720p**                               |
| 支持分辨率  | 480p/720p/1080p  | **480p/720p/1080p**                    |
| 时长范围   | 2-12秒            | **4-12秒**                              |
| 音频生成   | 不支持              | **支持**                                 |
| 图片控制模式 | `reference` 单参考图 | **`first_frame` / `last_frame` 首尾帧模式** |

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

```bash cURL（带音频的文生视频） 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "doubao-seedance-1-5-pro",
    "prompt": "海滩日落，金色阳光照在海面上，海浪轻轻拍打沙滩",
    "duration": 5,
    "aspect_ratio": "16:9",
    "metadata": {
      "resolution": "720p",
      "audio": true
    }
  }'
```

```bash cURL（首帧图生视频） 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "doubao-seedance-1-5-pro",
    "prompt": "猫在草地上追逐一条蛇，镜头快速跟随",
    "image_with_roles": [
      {"url": "https://example.com/first.png", "role": "first_frame"}
    ],
    "metadata": {
      "resolution": "720p",
      "audio": true
    }
  }'
```

```bash cURL（首尾帧图生视频） 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "doubao-seedance-1-5-pro",
    "prompt": "女孩在樱花树下旋转，花瓣随风飘落，最后慢慢停下",
    "image_with_roles": [
      {"url": "https://example.com/first.png", "role": "first_frame"},
      {"url": "https://example.com/last.png", "role": "last_frame"}
    ],
    "duration": 5,
    "aspect_ratio": "9:16",
    "metadata": {
      "resolution": "720p",
      "audio": true
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
        "model": "doubao-seedance-1-5-pro",
        "prompt": "海滩日落，金色阳光照在海面上，海浪轻轻拍打沙滩",
        "duration": 5,
        "aspect_ratio": "16:9",
        "metadata": {
            "resolution": "720p",
            "audio": True
        }
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
    model: 'doubao-seedance-1-5-pro',
    prompt: '海滩日落，金色阳光照在海面上，海浪轻轻拍打沙滩',
    duration: 5,
    aspect_ratio: '16:9',
    metadata: {
      resolution: '720p',
      audio: true
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
  "id": "task_vid_xyz789ghi012",
  "object": "generation.task",
  "model": "doubao-seedance-1-5-pro",
  "status": "queued",
  "progress": 0,
  "created_at": 1703884800,
  "metadata": {}
}
```

