> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# 上传图片

> 上传图片获取 URL，用于图像/视频生成接口

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


> 💡 **提示**
>
> **文档 Playground 不支持文件上传**：请使用下方的 cURL、Python 或 JavaScript 代码示例进行测试。


> ⚠️ **注意**
>
> **重要变更**：为了更好的性能和成本控制，我们不再支持在生成接口中直接传入 base64 图片数据。请使用本接口上传图片，获取 URL 后再调用生成接口。


## 为什么需要先上传图片？

1. **性能优化** - base64 编码会使数据膨胀 33%，先上传可显著减少请求体大小
2. **复用图片** - 上传一次，URL 可多次使用，无需重复传输

## 使用流程

```mermaid 
sequenceDiagram
    participant 客户端
    participant ToAPIs
    participant 存储
    
    客户端->>ToAPIs: POST /v1/uploads/images (上传图片文件)
    ToAPIs->>存储: 保存图片
    存储-->>ToAPIs: 返回存储路径
    ToAPIs-->>客户端: 返回图片 URL
    客户端->>ToAPIs: POST /v1/images/generations (使用图片 URL)
```

## Authorizations

### `Authorization`

`string` · 必填

使用 Bearer Token 进行认证

获取 API Key：访问 [API Key 管理页面](https://toapis.com/console/token)

```
Authorization: Bearer YOUR_API_KEY
```


## Body

### `file`

`file` · 必填

图片文件

**支持的格式：**

* JPEG (.jpg, .jpeg)
* PNG (.png)
* WebP (.webp)
* GIF (.gif)

**限制：**

* 最大文件大小：10MB


### `purpose`

`string`

上传目的（可选）

默认值：`generation`


## Response

### `success`

`boolean`

请求是否成功


### `data`

`object`

<details>
<summary>返回数据</summary>

**`id`** — `string`

上传记录 ID，用于追踪


**`url`** — `string`

图片的公开访问 URL，可直接用于生成接口


**`mime_type`** — `string`

图片的 MIME 类型，如 `image/jpeg`


**`size`** — `integer`

图片文件大小（字节）


### 请求示例

```bash cURL 
curl --request POST \
  --url https://toapis.com/v1/uploads/images \
  --header 'Authorization: Bearer <token>' \
  --form 'file=@/path/to/your/image.jpg'
```

```python Python 
import requests

# 上传图片
with open('image.jpg', 'rb') as f:
    response = requests.post(
        "https://toapis.com/v1/uploads/images",
        headers={
            "Authorization": "Bearer your-ToAPIs-key"
        },
        files={
            "file": f
        }
    )

result = response.json()
image_url = result['data']['url']
print(f"图片 URL: {image_url}")

# 使用上传的图片进行生成
response = requests.post(
    "https://toapis.com/v1/images/generations",
    headers={
        "Authorization": "Bearer your-ToAPIs-key",
        "Content-Type": "application/json"
    },
    json={
        "model": "gemini-3-pro-image-preview",
        "prompt": "基于这张图片创作变体",
        "image_urls": [{"url": image_url}]
    }
)
```

```javascript JavaScript 
(async () => {
const fileInput = document.createElement('input');
fileInput.type = 'file';
fileInput.accept = 'image/*';
fileInput.click();
await new Promise(resolve => fileInput.onchange = resolve);

// 上传图片（已验证成功）
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const uploadResponse = await fetch('https://toapis.com/v1/uploads/images', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-ToAPIs-key' // 替换为你的实际API密钥
  },
  body: formData
});

const uploadResult = await uploadResponse.json();
const imageUrl = uploadResult.data.url;
console.log(`图片 URL: ${imageUrl}`);

// 使用上传的图片进行生成（仅修改image_urls格式，解决400）
const genResponse = await fetch('https://toapis.com/v1/images/generations', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-ToAPIs-key', // 替换为你的实际API密钥
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'gemini-3-pro-image-preview',
    prompt: '基于这张图片创作变体',
    image_urls: [imageUrl] 
  })
});

const genResult = await genResponse.json();
console.log('生成结果:', genResult);
})();
```


### 响应示例

```json 200 成功 
{
  "success": true,
  "message": "",
  "data": {
    "id": "upload_abc12345",
    "url": "https://files.toapis.com/uploads/123/1737568800_abc12345.jpg",
    "mime_type": "image/jpeg",
    "size": 89234
  }
}
```

```json 400 错误请求 
{
  "success": false,
  "message": "Unsupported image type. Allowed: JPEG, PNG, WebP, GIF"
}
```

```json 400 文件过大 
{
  "success": false,
  "message": "Image too large. Maximum size is 10MB"
}
```


## 完整示例：图生图工作流

以下是一个完整的图生图工作流示例：

```python Python 完整示例 
import requests
import time
import os

API_KEY = os.getenv(
    "TOAPIS_API_KEY", "your-ToAPIs-key"
)
BASE_URL = "https://toapis.com"


def _raise_api_error(resp: requests.Response, payload: dict) -> None:
    if resp.ok:
        return
    msg = payload.get("message") or payload.get("error")
    if isinstance(msg, dict):
        msg = msg.get("message") or str(msg)
    raise RuntimeError(f"HTTP {resp.status_code}: {msg or payload}")


def _require_api_key() -> None:
    if not API_KEY:
        raise RuntimeError("缺少 TOAPIS_API_KEY 环境变量")


def upload_image(file_path: str) -> str:
    _require_api_key()
    with open(file_path, "rb") as f:
        resp = requests.post(
            f"{BASE_URL}/v1/uploads/images",
            headers={"Authorization": f"Bearer {API_KEY}"},
            files={"file": f},
        )
    body = resp.json()
    _raise_api_error(resp, body)
    if not body.get("success"):
        raise RuntimeError(body.get("message") or str(body))
    return body["data"]["url"]


def create_generation(image_url: str, prompt: str) -> str:
    _require_api_key()
    resp = requests.post(
        f"{BASE_URL}/v1/images/generations",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gemini-3-pro-image-preview",
            "prompt": prompt,
            "image_urls": [image_url],
            "size": "16:9",
        },
    )
    body = resp.json()
    _raise_api_error(resp, body)
    task_id = body.get("id") or body.get("task_id")
    if not task_id:
        raise RuntimeError(f"创建任务响应缺少 id: {body}")
    return task_id


def wait_for_result(task_id: str) -> str:
    _require_api_key()
    while True:
        resp = requests.get(
            f"{BASE_URL}/v1/images/generations/{task_id}",
            headers={"Authorization": f"Bearer {API_KEY}"},
        )
        result = resp.json()
        _raise_api_error(resp, result)

        status = result.get("status")
        if status == "completed":
            r = result.get("result") or {}
            items = r.get("data") or []
            if not items or not items[0].get("url"):
                raise RuntimeError(f"completed 但无 URL: {result}")
            return items[0]["url"]
        if status == "failed":
            err = result.get("error") or {}
            raise RuntimeError(
                f"生成失败: {err.get('message') or result.get('fail_reason') or result}"
            )

        time.sleep(2)


if __name__ == "__main__":
    image_url = upload_image("reference.jpg")
    print(f"✅ 图片已上传: {image_url}")

    task_id = create_generation(image_url, "将这张照片转换为赛博朋克风格")
    print(f"✅ 任务已创建: {task_id}")

    result_url = wait_for_result(task_id)
    print(f"✅ 生成完成: {result_url}")

```
