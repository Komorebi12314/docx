> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Grok Imagine 1.0 图像编辑

> 使用 grok-imagine-1.0-edit 基于参考图进行异步图像编辑

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 统一图像编辑接口
* 异步任务模式，返回任务 ID
* 通过 `model` 指定为 `grok-imagine-1.0-edit`

## Authorizations

### `Authorization`

`string` · 必填

所有接口均使用 Bearer Token 认证

获取 API Key：访问 [API Key 管理页面](https://toapis.com/console/token)

请求头示例：

```
Authorization: Bearer YOUR_API_KEY
```


## Body

### `model`

`string` · 必填

模型名称，固定使用：

* `grok-imagine-1.0-edit`


### `prompt`

`string` · 必填

图像编辑提示词，支持多语言


### `image_urls`

`string[]` · 必填

待编辑的原图 URL 数组，至少 1 张

示例：

* `["https://example.com/original.png"]`

建议先使用 [图片上传接口](../../uploads/images) 上传后再传 URL


### `n`

`integer` · 默认值：`1`

生成数量，建议范围 1-10


## Response

### `id`

`string`

任务唯一 ID


### `object`

`string`

固定为 `generation.task`


### `status`

`string`

任务状态：`queued` / `in_progress` / `completed` / `failed`


### 请求示例

```bash cURL 
curl --request POST \
  --url https://toapis.com/v1/images/edits \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "grok-imagine-1.0-edit",
    "prompt": "把背景改成星空，主体保持不变",
    "image_urls": ["https://example.com/original.png"],
    "n": 1
  }'
```

```python Python 
import requests

resp = requests.post(
    "https://toapis.com/v1/images/edits",
    headers={
        "Authorization": "Bearer your-ToAPIs-key",
        "Content-Type": "application/json",
    },
    json={
        "model": "grok-imagine-1.0-edit",
        "prompt": "把背景改成星空，主体保持不变",
        "image_urls": ["https://example.com/original.png"],
        "n": 1,
    },
)

print(resp.status_code)
print(resp.json())
```

```javascript JavaScript 
const resp = await fetch('https://toapis.com/v1/images/edits', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-ToAPIs-key',
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'grok-imagine-1.0-edit',
    prompt: '把背景改成星空，主体保持不变',
    image_urls: ['https://example.com/original.png'],
    n: 1,
  }),
});

console.log(resp.status);
console.log(await resp.json());
```


### 响应示例

```json 200 
{
  "id": "task_01JNXXXXXXXXXXXXXXXXXX",
  "object": "generation.task",
  "model": "grok-imagine-1.0-edit",
  "status": "queued",
  "progress": 0,
  "created_at": 1768380224,
  "metadata": {}
}
```

