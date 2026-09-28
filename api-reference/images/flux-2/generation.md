> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Flux 2.0 图像生成

> 使用 Flux 2.0 模型生成高质量图像，支持文生图和图生图

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* Flux 2.0 图像生成模型
* 通过 model 参数选择 `flux-2-flex`（速度较快，适合快速迭代）或 `flux-2-pro`（质量更高，细节更好）
* 支持文生图、图生图，最多 8 张参考图
* 按分辨率计费（1K/2K）
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

* `flux-2-flex` - 速度较快，适合快速迭代
* `flux-2-pro` - 质量更高，细节更好


### `prompt`

`string` · 必填

图像生成的文本描述


### `size`

`string` · 默认值：`1:1`

图像宽高比

支持的宽高比：

* `1:1` - 正方形（默认）
* `4:3` / `3:4` - 传统显示器比例
* `16:9` / `9:16` - 宽屏/竖屏
* `3:2` / `2:3` - 标准照片


### `image_urls`

`string[]`

参考图像 URL 数组，用于图生图

**⚠️ 仅支持 URL 格式（不支持 base64）**

* 公开可访问的图片 URL（http\:// 或 https\://）
* 可使用 [上传图片接口](../../uploads/images) 上传本地图片获取 URL

**限制：**

* 最多 8 张参考图


### `metadata`

`object`

元数据参数，用于传递额外的配置选项

<details>
<summary>支持的 metadata 字段</summary>

**`resolution`** — `string` · 默认值：`1K`

输出图像分辨率

可选值：

* `1K` - 标准分辨率（默认）
* `2K` - 高分辨率

**分辨率与宽高比对应像素尺寸：**

| 宽高比  | 1K 尺寸     | 2K 尺寸     |
| ---- | --------- | --------- |
| 1:1  | 1024×1024 | 2048×2048 |
| 4:3  | 1365×1024 | 2730×2048 |
| 3:4  | 1024×1365 | 2048×2730 |
| 16:9 | 1820×1024 | 3640×2048 |
| 9:16 | 1024×1820 | 2048×3640 |
| 3:2  | 1536×1024 | 3072×2048 |
| 2:3  | 1024×1536 | 2048×3072 |

**注意：** 不同分辨率计费不同，2K 价格高于 1K


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

### 场景一：文生图（快速迭代）

```json 
{
  "model": "flux-2-flex",
  "prompt": "一只可爱的橘猫在窗台上晒太阳",
  "size": "1:1",
  "metadata": {
    "resolution": "1K"
  }
}
```

### 场景二：文生图（高质量输出）

```json 
{
  "model": "flux-2-pro",
  "prompt": "未来城市的天际线，霓虹灯光，赛博朋克风格，电影质感",
  "size": "16:9",
  "metadata": {
    "resolution": "2K"
  }
}
```

### 场景三：图生图（多参考图）

```json 
{
  "model": "flux-2-pro",
  "prompt": "保持角色风格，生成在森林中奔跑的场景",
  "size": "1:1",
  "image_urls": [
    "https://example.com/ref1.jpg",
    "https://example.com/ref2.jpg"
  ],
  "metadata": {
    "resolution": "2K"
  }
}
```

### 场景四：竖屏海报

```json 
{
  "model": "flux-2-flex",
  "prompt": "音乐会宣传海报，简约风格，深色背景",
  "size": "9:16",
  "metadata": {
    "resolution": "1K"
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
    "model": "flux-2-flex",
    "prompt": "一只可爱的橘猫在窗台上晒太阳",
    "size": "1:1",
    "metadata": {
      "resolution": "1K"
    }
  }'
```

```bash cURL (图生图) 
curl --request POST \
  --url https://toapis.com/v1/images/generations \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "flux-2-pro",
    "prompt": "保持角色风格，生成在森林中奔跑的场景",
    "size": "1:1",
    "image_urls": ["https://example.com/ref1.jpg"],
    "metadata": {
      "resolution": "2K"
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
        "model": "flux-2-flex",
        "prompt": "一只可爱的橘猫在窗台上晒太阳",
        "size": "1:1",
        "metadata": {
            "resolution": "1K"
        }
    }
)

task = response.json()
print(f"任务 ID: {task['id']}")
print(f"状态: {task['status']}")
```

```python Python (图生图) 
import requests

response = requests.post(
    "https://toapis.com/v1/images/generations",
    headers={
        "Authorization": "Bearer your-ToAPIs-key",
        "Content-Type": "application/json"
    },
    json={
        "model": "flux-2-pro",
        "prompt": "保持角色风格，生成在森林中奔跑的场景",
        "size": "1:1",
        "image_urls": ["https://example.com/ref1.jpg"],
        "metadata": {
            "resolution": "2K"
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
    model: 'flux-2-flex',
    prompt: '一只可爱的橘猫在窗台上晒太阳',
    size: '1:1',
    metadata: {
      resolution: '1K'
    }
  })
});

const task = await response.json();
console.log(`任务 ID: ${task.id}`);
console.log(`状态: ${task.status}`);
```

```javascript JavaScript (图生图) 
const response = await fetch('https://toapis.com/v1/images/generations', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-ToAPIs-key',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'flux-2-pro',
    prompt: '保持角色风格，生成在森林中奔跑的场景',
    size: '1:1',
    image_urls: ['https://example.com/ref1.jpg'],
    metadata: {
      resolution: '2K'
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
  "model": "flux-2-flex",
  "status": "queued",
  "progress": 0,
  "created_at": 1703884800,
  "metadata": {}
}
```

