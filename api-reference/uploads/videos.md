> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# 上传视频

> 上传视频获取 URL，用于视频生成和参考视频输入

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


> 💡 **提示**
>
> **文档 Playground 不支持文件上传**：请使用下方的 cURL、Python 或 JavaScript 代码示例进行测试。


## 为什么需要先上传视频？

1. **统一输入方式** - 本地视频先上传成公网 URL，便于后续接口复用
2. **减少重复传输** - 上传一次后可以在多个视频任务中重复使用

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

视频文件

**支持的格式：**

* MP4 (.mp4)
* WebM (.webm)
* MOV (.mov)

**限制：**

* 最大文件大小：50MB


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

视频的公开访问 URL，可直接用于视频生成接口


**`mime_type`** — `string`

视频的 MIME 类型，如 `video/mp4`


**`size`** — `integer`

视频文件大小（字节）


### 请求示例

```bash cURL 
curl --request POST \
  --url https://toapis.com/v1/uploads/videos \
  --header 'Authorization: Bearer <token>' \
  --form 'file=@/path/to/your/video.mp4'
```

```python Python 
import requests

with open('video.mp4', 'rb') as f:
    response = requests.post(
        "https://toapis.com/v1/uploads/videos",
        headers={
            "Authorization": "Bearer your-ToAPIs-key"
        },
        files={
            "file": f
        }
    )

result = response.json()
video_url = result['data']['url']
print(f"视频 URL: {video_url}")
```

```javascript JavaScript 
(async () => {
const fileInput = document.createElement('input');
fileInput.type = 'file';
fileInput.accept = 'video/mp4,video/webm,video/quicktime';
fileInput.click();
await new Promise(resolve => fileInput.onchange = resolve);

const formData = new FormData();
formData.append('file', fileInput.files[0]);

const uploadResponse = await fetch('https://toapis.com/v1/uploads/videos', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-ToAPIs-key'
  },
  body: formData
});

const uploadResult = await uploadResponse.json();
console.log('上传结果:', uploadResult);
})();
```


### 响应示例

```json 200 成功 
{
  "success": true,
  "message": "",
  "data": {
    "id": "upload_abc12345",
    "url": "https://files.toapis.com/uploads/123/videos/1737568800_abc12345.mp4",
    "mime_type": "video/mp4",
    "size": 1892345
  }
}
```

```json 400 错误请求 
{
  "success": false,
  "message": "Unsupported or invalid video file. Allowed: MP4, WebM, MOV"
}
```

```json 400 文件过大 
{
  "success": false,
  "message": "Video too large. Maximum size is 50MB"
}
```

