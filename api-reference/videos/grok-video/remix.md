> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Grok 视频混音

> 编辑和修改已生成的 Grok 视频

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* Grok 视频混音功能
* 基于现有视频进行二次创作
* 异步任务管理，通过任务 ID 查询结果

## Path Parameters

### `video_id`

`string` · 必填

原始视频任务 ID

这是之前视频生成请求返回的任务 ID


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

`string` · 必填 · 默认值：`grok-video-1.0`

视频混音模型名称

示例：`"grok-video-1.0"`


### `prompt`

`string` · 必填

混音指令描述


### `size`

`string`

视频尺寸


### `aspect_ratio`

`string`

视频宽高比

支持的格式：

* `16:9` - 横屏
* `9:16` - 竖屏


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

```bash cURL 
curl --request POST \
  --url https://toapis.com/v1/videos/video_abc123def456/remix \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "grok-video-1.0",
    "prompt": "在场景中添加一只小狗",
    "aspect_ratio": "16:9"
  }'
```

```python Python 
import requests

video_id = "video_abc123def456"

response = requests.post(
    f"https://toapis.com/v1/videos/{video_id}/remix",
    headers={
        "Authorization": "Bearer your-ToAPIs-key",
        "Content-Type": "application/json"
    },
    json={
        "model": "grok-video-1.0",
        "prompt": "在场景中添加一只小狗",
        "aspect_ratio": "16:9"
    }
)

task = response.json()
print(f"任务 ID: {task['id']}")
print(f"状态: {task['status']}")
```

```javascript JavaScript 
const videoId = 'video_abc123def456';

const response = await fetch(`https://toapis.com/v1/videos/${videoId}/remix`, {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-ToAPIs-key',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'grok-video-1.0',
    prompt: '在场景中添加一只小狗',
    aspect_ratio: '16:9'
  })
});

const task = await response.json();
console.log(`任务 ID: ${task.id}`);
console.log(`状态: ${task.status}`);
```


### 响应示例

```json 200 
{
  "id": "video_remix_abc123",
  "object": "generation.task",
  "model": "grok-video-1.0",
  "status": "queued",
  "progress": 0,
  "created_at": 1768380224,
  "metadata": {}
}
```

