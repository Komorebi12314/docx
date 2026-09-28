> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Flux Kontext 图像生成

> 使用 Flux Kontext 模型进行图片编辑和生成，支持文生图和图片编辑

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* Flux Kontext 图像生成与编辑模型
* 通过 model 参数选择 `flux-kontext-pro`（Pro）或 `flux-kontext-max`（Max，更高质量）
* 支持文生图、图片编辑两种模式
* 有参考图时为图片编辑，无参考图时为文生图
* 按请求固定计费
* 异步任务模式，返回 `task_id` 用于查询结果

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

`string` · 必填

图像生成模型名称

可选值：

* `flux-kontext-pro` - Pro 版本
* `flux-kontext-max` - Max 版本，更高质量


### `prompt`

`string` · 必填

图像生成的文本描述


### `size`

`string`

图像宽高比

默认值：

* 有参考图时：`match_input_image`（匹配输入图片）
* 无参考图时：`16:9`

支持的宽高比：

| 值                   | 说明               |
| ------------------- | ---------------- |
| `match_input_image` | 匹配输入图片比例（仅图片编辑时） |
| `1:1`               | 正方形              |
| `4:3` / `3:4`       | 传统显示器比例          |
| `16:9` / `9:16`     | 宽屏/竖屏            |
| `3:2` / `2:3`       | 标准照片             |
| `21:9` / `9:21`     | 超宽屏/超窄屏          |


### `image_urls`

`string[]`

参考图像 URL 数组，用于图片编辑

**⚠️ 仅支持 URL 格式（不支持 base64）**

* 公开可访问的图片 URL（http\:// 或 https\://）
* 可使用 [上传图片接口](../../uploads/images) 上传本地图片获取 URL

**限制：**

* 最多 1 张图片
* 传入图片时为图片编辑模式，不传时为文生图模式


### `metadata`

`object`

元数据参数，用于传递额外的配置选项

<details>
<summary>支持的 metadata 字段</summary>

**`response_format`** — `string` · 默认值：`png`

输出图像格式

可选值：`png`、`jpg`


**`safety_tolerance`** — `integer` · 默认值：`2`

安全过滤容忍度

取值范围：`0` - `6`，数值越高容忍度越高


**`prompt_upsampling`** — `boolean` · 默认值：`false`

是否启用提示词增强

* `true`：自动优化/扩展提示词
* `false`：使用原始提示词（默认）


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


## 使用场景

### 场景一：文生图

```json 
{
  "model": "flux-kontext-pro",
  "prompt": "赛博朋克风格的城市夜景，霓虹灯闪烁",
  "size": "16:9",
  "metadata": {
    "response_format": "png",
    "safety_tolerance": 2
  }
}
```

### 场景二：图片编辑

```json 
{
  "model": "flux-kontext-max",
  "prompt": "将这张照片改为水彩画风格",
  "size": "match_input_image",
  "image_urls": ["https://example.com/photo.jpg"],
  "metadata": {
    "response_format": "jpg",
    "prompt_upsampling": true
  }
}
```

### 场景三：高质量文生图（Max 模型）

```json 
{
  "model": "flux-kontext-max",
  "prompt": "一只可爱的橘猫在窗台上晒太阳，写实风格",
  "size": "1:1",
  "metadata": {
    "response_format": "png",
    "safety_tolerance": 3
  }
}
```

> 💡 **提示**
>
> **查询任务结果**
>
> 图像生成为异步任务，提交后会返回任务 ID。使用 [获取图像任务状态](../../tasks/image-status) 接口查询生成进度和结果。


### 请求示例

```bash cURL 
curl --request POST \
  --url https://toapis.com/v1/images/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "flux-kontext-pro",
    "prompt": "赛博朋克风格的城市夜景，霓虹灯闪烁",
    "size": "16:9",
    "metadata": {
      "response_format": "png"
    }
  }'
```

```bash cURL (图片编辑) 
curl --request POST \
  --url https://toapis.com/v1/images/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "flux-kontext-max",
    "prompt": "将这张照片改为水彩画风格",
    "size": "match_input_image",
    "image_urls": ["https://example.com/photo.jpg"],
    "metadata": {
      "response_format": "jpg"
    }
  }'
```

```python Python 
import requests

response = requests.post(
    "https://toapis.com/v1/images/generations",
    headers={
        "Authorization": "Bearer your-ToAPIs-key",
        "Content-Type": "application/json"
    },
    json={
        "model": "flux-kontext-pro",
        "prompt": "赛博朋克风格的城市夜景，霓虹灯闪烁",
        "size": "16:9",
        "metadata": {
            "response_format": "png"
        }
    }
)

task = response.json()
print(f"任务 ID: {task['id']}")
print(f"状态: {task['status']}")
```

```python Python (图片编辑) 
import requests

response = requests.post(
    "https://toapis.com/v1/images/generations",
    headers={
        "Authorization": "Bearer your-ToAPIs-key",
        "Content-Type": "application/json"
    },
    json={
        "model": "flux-kontext-max",
        "prompt": "将这张照片改为水彩画风格",
        "size": "match_input_image",
        "image_urls": ["https://example.com/photo.jpg"],
        "metadata": {
            "response_format": "jpg"
        }
    }
)

task = response.json()
print(f"任务 ID: {task['id']}")
print(f"状态: {task['status']}")
```

```javascript JavaScript 
const response = await fetch('https://toapis.com/v1/images/generations', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-ToAPIs-key',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'flux-kontext-pro',
    prompt: '赛博朋克风格的城市夜景，霓虹灯闪烁',
    size: '16:9',
    metadata: {
      response_format: 'png'
    }
  })
});

const task = await response.json();
console.log(`任务 ID: ${task.id}`);
console.log(`状态: ${task.status}`);
```

```javascript JavaScript (图片编辑) 
const response = await fetch('https://toapis.com/v1/images/generations', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-ToAPIs-key',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'flux-kontext-max',
    prompt: '将这张照片改为水彩画风格',
    size: 'match_input_image',
    image_urls: ['https://example.com/photo.jpg'],
    metadata: {
      response_format: 'jpg'
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
  "id": "task_img_abc123def456",
  "object": "generation.task",
  "model": "flux-kontext-pro",
  "status": "queued",
  "progress": 0,
  "created_at": 1703884800,
  "metadata": {}
}
```

