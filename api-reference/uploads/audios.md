> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# 上传音频

> 上传音频获取 URL,用于音频相关接口或其他需要音频 URL 的接口

> 💡 **提示**
>
> **国内用户请注意:** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址 (Base URL).文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`.


> 💡 **提示**
>
> **文档 Playground 不支持文件上传**:请使用下方的 cURL,Python 或 JavaScript 代码示例进行测试.


## 为什么需要先上传音频?

1. **统一输入方式** - 本地音频先上传成公网 URL, 便于后续接口复用
2. **减少重复传输** - 上传一次后可以在多个请求中重复使用

## Authorizations

### `Authorization`

`string` · 必填

使用 Bearer Token 进行认证

获取 API Key: 访问 [API Key 管理页面](https://toapis.com/console/token)

```
Authorization: Bearer YOUR_API_KEY
```


## Body

### `file`

`file` · 必填

音频文件

**支持的格式:**

* MP3 (.mp3)
* WAV (.wav)
* M4A (.m4a)

**限制:**

* 最大文件大小: 50MB


### `purpose`

`string`

上传目的 (可选)

默认值: `generation`


## Response

### `success`

`boolean`

请求是否成功


### `data`

`object`

<details>
<summary>返回数据</summary>

**`id`** — `string`

上传记录 ID, 用于追踪


**`url`** — `string`

音频的公开访问 URL


**`mime_type`** — `string`

音频的 MIME 类型, 如 `audio/mpeg`


**`size`** — `integer`

音频文件大小 (字节)


### 请求示例

```bash cURL 
curl --request POST \
  --url https://toapis.com/v1/uploads/audios \
  --header 'Authorization: Bearer <token>' \
  --form 'file=@/path/to/your/audio.mp3'
```

```python Python 
import requests

with open('audio.mp3', 'rb') as f:
    response = requests.post(
        "https://toapis.com/v1/uploads/audios",
        headers={
            "Authorization": "Bearer your-ToAPIs-key"
        },
        files={
            "file": f
        }
    )

result = response.json()
audio_url = result['data']['url']
print(f"音频 URL: {audio_url}")
```

```javascript JavaScript 
(async () => {
const fileInput = document.createElement('input');
fileInput.type = 'file';
fileInput.accept = 'audio/mpeg,audio/wav,audio/mp4';
fileInput.click();
await new Promise(resolve => fileInput.onchange = resolve);

const formData = new FormData();
formData.append('file', fileInput.files[0]);

const uploadResponse = await fetch('https://toapis.com/v1/uploads/audios', {
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
    "url": "https://files.toapis.com/uploads/123/audios/1737568800_abc12345.mp3",
    "mime_type": "audio/mpeg",
    "size": 1892345
  }
}
```

```json 400 错误请求 
{
  "success": false,
  "message": "Unsupported or invalid audio file. Allowed: MP3, WAV, M4A"
}
```

