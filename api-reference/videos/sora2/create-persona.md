> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Sora2 创建角色

> 从视频中提取角色，用于后续视频生成

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


## 功能概述

Sora2 角色创建功能允许您从现有视频中提取角色，创建后可在后续视频生成中复用该角色，实现角色一致性。

> 💡 **提示**
>
> **重要提示：**
>
> * 视频必须包含**声音**和**可识别的角色**
> * 时间范围限制：**最小 1 秒，最大 3 秒**
> * `url` 和 `from_task` 二选一，必须提供其中一个
> * 此模式下**不需要** `prompt` 参数
> * 创建完成后，角色任务 ID 可用于后续视频生成


## 认证

### `Authorization`

`string` · 必填

Bearer Token 认证

```
Authorization: Bearer YOUR_API_KEY
```

获取 API Key：访问 [API Key 管理页面](https://toapis.com/console/token)


## 请求参数

### `model`

`string` · 必填 · 默认值：`sora-2`

视频生成模型名称

支持的模型：

* `sora-2` - 标准版本
* `sora-2-pro` - 专业版本（更高质量）
* `sora-2-vip` - VIP版，更高优先级


### `timestamps`

`string` · 必填

角色出现的时间戳范围

单位为秒，格式为 `"起始秒,结束秒"`

**限制：**

* 时间范围差值最小 **1 秒**
* 时间范围差值最大 **3 秒**

示例：`"1,3"` 表示视频中第 1 秒到第 3 秒出现的角色


### `url`

`string`

包含需要创建角色的视频 URL

**要求：**

* 视频必须包含声音
* 视频必须包含可识别的角色

**说明：** 与 `from_task` 二选一

示例：`"https://example.com/my-video.mp4"`


### `from_task`

`string`

已生成的视频任务 ID

可以根据已经生成的视频任务 ID 来创建角色

**说明：** 与 `url` 二选一

示例：`"task_01KBYT59JDHB4A3KDDR9N9JVWP"`


## 响应字段

### `id`

`string`

任务唯一标识符，用于查询角色创建状态

创建完成后，可使用此角色任务 ID 在视频生成时通过 `character_url` 参数引用该角色


### `object`

`string`

对象类型，固定为 `generation.task`


### `model`

`string`

使用的模型名称


### `status`

`string`

任务状态：

* `queued` - 排队等待处理
* `in_progress` - 处理中
* `completed` - 成功完成
* `failed` - 失败


### `progress`

`integer`

任务进度百分比（0-100）


### `created_at`

`integer`

任务创建时间（Unix 时间戳）


### `completed_at`

`integer`

任务完成时间（Unix 时间戳，仅完成后有值）


### `result`

`object`

角色创建结果（仅完成后有值）

包含创建的角色信息，如角色 ID、名称、头像等


### 请求示例

```bash cURL（从视频 URL 创建） 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "sora-2",
    "url": "https://example.com/character-video.mp4",
    "timestamps": "1,3"
  }'
```

```bash cURL（从已生成任务创建） 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "sora-2",
    "from_task": "task_01KBYT59JDHB4A3KDDR9N9JVWP",
    "timestamps": "1,3"
  }'
```

```python Python 
import requests

# 从视频 URL 创建角色
response = requests.post(
    "https://toapis.com/v1/videos/generations",
    headers={
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    },
    json={
        "model": "sora-2",
        "url": "https://example.com/character-video.mp4",
        "timestamps": "1,3"
    }
)

task = response.json()
print(f"任务 ID: {task['id']}")
print(f"状态: {task['status']}")

# 从已生成任务创建角色
response = requests.post(
    "https://toapis.com/v1/videos/generations",
    headers={
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    },
    json={
        "model": "sora-2",
        "from_task": "task_01KBYT59JDHB4A3KDDR9N9JVWP",
        "timestamps": "1,3"
    }
)
```

```javascript JavaScript 
// 从视频 URL 创建角色
const response = await fetch('https://toapis.com/v1/videos/generations', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'sora-2',
    url: 'https://example.com/character-video.mp4',
    timestamps: '1,3'
  })
});

const task = await response.json();
console.log(`任务 ID: ${task.id}`);
console.log(`状态: ${task.status}`);
```

```go Go 
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
)

func main() {
    url := "https://toapis.com/v1/videos/generations"

    payload := map[string]interface{}{
        "model":      "sora-2",
        "url":        "https://example.com/character-video.mp4",
        "timestamps": "1,3",
    }

    jsonData, _ := json.Marshal(payload)

    req, _ := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
    req.Header.Set("Authorization", "Bearer YOUR_API_KEY")
    req.Header.Set("Content-Type", "application/json")

    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        panic(err)
    }
    defer resp.Body.Close()

    body, _ := io.ReadAll(resp.Body)
    fmt.Println(string(body))
}
```


### 响应示例

```json 200（提交成功） 
{
  "id": "task_01KBYT59JDHB4A3KDDR9N9JVWP",
  "object": "generation.task",
  "model": "sora-2",
  "status": "queued",
  "progress": 0,
  "created_at": 1703884800,
  "metadata": {}
}
```

```json 200（创建完成 - 查询结果） 
{
  "id": "task_01KC0JZCMTMQ70D68XTM56Q5D0",
  "object": "generation.task",
  "model": "sora-2",
  "status": "completed",
  "progress": 100,
  "created_at": 1765251461,
  "completed_at": 1765251507,
  "result": {
    "type": "character",
    "data": {
      "characters": [
        {
          "id": "ch_6937998961208191a45ef08447a554df",
          "display_name": "Turbo Whiskers",
          "profile_picture_url": "https://upload.toapis.com/f/image/character_task_xxx.jpg",
          "username": "duksvfkf.turbo_whis"
        }
      ]
    }
  },
  "metadata": {}
}
```

```json 400（请求参数无效） 
{
  "error": {
    "code": 400,
    "message": "请求参数无效：timestamps 时间范围必须在 1-3 秒之间",
    "type": "invalid_request_error"
  }
}
```

```json 401（认证失败） 
{
  "error": {
    "code": 401,
    "message": "身份验证失败，请检查您的 API 密钥",
    "type": "authentication_error"
  }
}
```

```json 402（余额不足） 
{
  "error": {
    "code": 402,
    "message": "账户余额不足，请充值后再试",
    "type": "payment_required"
  }
}
```


## 使用流程

1. **提交角色创建请求**
   调用此接口，提供包含角色的视频 URL 或已有任务 ID，以及角色出现的时间范围


2. **获取任务 ID**
   接口返回任务 ID，状态为 `queued` 或 `in_progress`


3. **查询任务状态**
   使用 [查询视频任务状态](../../tasks/video-status) 接口轮询任务进度


4. **使用角色生成视频**
   角色创建完成后，在后续视频生成中使用 `character_url` 参数引用该角色任务 ID


## 最佳实践

1. **选择清晰的角色片段**：选择视频中角色特征最明显的 1-3 秒片段
2. **确保视频质量**：高清视频能够更好地提取角色特征
3. **包含声音**：视频必须包含音频轨道
4. **避免多角色**：选择的时间范围内最好只有一个主要角色
