> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# 获取视频任务状态

> 查询视频生成任务的状态和结果

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 查询异步视频生成任务的执行状态和结果
* 实时状态更新和进度跟踪
* 任务完成时获取生成的视频
* 支持多语言返回（zh/en/ko/ja）

所有视频生成任务都是异步执行的。提交任务后，您需要通过查询接口获取任务状态和结果。

> 💡 **提示**
>
> 使用[按需素材审核](../videos/private-assets)创建的视频任务也通过本接口查询. `queued` 可能包含素材准备和审核等待, 返回任务不表示视频已经开始生成. 默认每轮准备期限为 20 分钟, 后续视频生成另计; 失败原因查看 `error.message`. 无需单独轮询旧素材接口.


## 创建任务时传入业务 ID

创建视频任务时，可以在请求体顶层传入 `client_business_id`。该字段用于保存您系统内的订单号、流水号或业务任务 ID，方便后续按业务 ID 查询生成结果。

```json 
{
  "model": "sora-2",
  "client_business_id": "order_20260428_002",
  "prompt": "海浪拍打着海岸",
  "duration": 15,
  "aspect_ratio": "16:9"
}
```

也兼容放在 `metadata.client_business_id` 中，但推荐使用顶层字段。

## Authorizations

### `Authorization`

`string` · 必填

所有接口均需要使用 Bearer Token 进行认证

获取 API Key：

访问 [API Key 管理页面](https://toapis.com/console/token) 获取您的 API Key

使用时在请求头中添加：

```
Authorization: Bearer YOUR_API_KEY
```


## Path Parameters

### `task_id`

`string` · 必填

视频生成 API 返回的任务 ID。也可以传创建任务时提交的 `client_business_id`，用于按客户侧业务 ID 查询任务状态和结果。


> 💡 **提示**
>
> 如果创建视频任务时传入 `client_business_id`，可直接使用同一个状态查询接口：
> `GET /v1/videos/generations/{client_business_id}`。业务 ID 会限定在当前 API Key 所属用户下查询。


### 请求示例

```bash cURL 
curl --request GET \
  --url 'https://toapis.com/v1/videos/generations/task_01K9S419324DREZFBWNSVXYR6H' \
  --header 'Authorization: Bearer <token>'
```

```python Python 
import requests
import time

API_BASE = 'https://toapis.com'
API_KEY = 'sk-xxxxxxxxxxxxxxxxxxxxxx'

headers = {
    'Authorization': f'Bearer {API_KEY}'
}

def get_video_status(task_id):
    response = requests.get(f'{API_BASE}/v1/videos/generations/{task_id}', headers=headers)
    return response.json()

def wait_for_video(task_id, max_attempts=60, interval=10):
    for _ in range(max_attempts):
        result = get_video_status(task_id)
        status = result.get('status')
        progress = result.get('progress', 0)

        print(f"状态: {status}, 进度: {progress}%")

        if status == 'completed':
            return result
        elif status == 'failed':
            raise Exception(f"任务失败: {result}")

        time.sleep(interval)

    raise Exception("任务超时")

# 使用示例
task_id = "video_7497f4d5-3a88-44c7-923a-967fa7d941a0"
result = wait_for_video(task_id)
print(f"视频URL: {result['result']['data'][0]['url']}")
```

```javascript JavaScript 
const API_BASE = 'https://toapis.com';
const API_KEY = 'sk-xxxxxxxxxxxxxxxxxxxxxx';

async function getVideoStatus(taskId) {
  const response = await fetch(`${API_BASE}/v1/videos/generations/${taskId}`, {
    headers: {
      'Authorization': `Bearer ${API_KEY}`
    }
  });
  return response.json();
}

async function waitForVideo(taskId, maxAttempts = 60, interval = 10000) {
  for (let i = 0; i < maxAttempts; i++) {
    const result = await getVideoStatus(taskId);
    const status = result.status;
    const progress = result.progress || 0;

    console.log(`状态: ${status}, 进度: ${progress}%`);

    if (status === 'completed') {
      return result;
    } else if (status === 'failed') {
      throw new Error(`任务失败: ${JSON.stringify(result)}`);
    }

    await new Promise(r => setTimeout(r, interval));
  }

  throw new Error('任务超时');
}

// 使用示例
const taskId = 'video_7497f4d5-3a88-44c7-923a-967fa7d941a0';
waitForVideo(taskId).then(result => {
  console.log('视频URL:', result.result.data[0].url);
  console.log('格式:', result.result.data[0].format);
});
```

```go Go 
package main

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
    "time"
)

func getVideoStatus(taskId string) (map[string]interface{}, error) {
    url := fmt.Sprintf("https://toapis.com/v1/videos/generations/%s", taskId)

    req, _ := http.NewRequest("GET", url, nil)
    req.Header.Set("Authorization", "Bearer <token>")

    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    body, _ := ioutil.ReadAll(resp.Body)

    var result map[string]interface{}
    json.Unmarshal(body, &result)

    return result, nil
}

func main() {
    taskId := "video_7497f4d5-3a88-44c7-923a-967fa7d941a0"

    for i := 0; i < 60; i++ {
        result, _ := getVideoStatus(taskId)
        status := result["status"].(string)
        progress := int(result["progress"].(float64))

        fmt.Printf("状态: %s, 进度: %d%%\n", status, progress)

        if status == "completed" {
            fmt.Println("视频生成完成!")
            resultData := result["result"].(map[string]interface{})
            dataArray := resultData["data"].([]interface{})
            videoData := dataArray[0].(map[string]interface{})
            fmt.Println("视频URL:", videoData["url"])
            break
        }

        time.Sleep(10 * time.Second)
    }
}
```


### 响应示例

```json 200 - 排队中 
{
  "id": "video_7497f4d5-3a88-44c7-923a-967fa7d941a0",
  "object": "generation.task",
  "model": "sora-2",
  "status": "queued",
  "progress": 0,
  "created_at": 1768380222
}
```

```json 200 - 处理中 
{
  "id": "video_7497f4d5-3a88-44c7-923a-967fa7d941a0",
  "object": "generation.task",
  "model": "sora-2",
  "status": "in_progress",
  "progress": 65,
  "created_at": 1768380222
}
```

```json 200 - 已完成 
{
  "id": "video_7497f4d5-3a88-44c7-923a-967fa7d941a0",
  "client_business_id": "order_20260428_001",
  "object": "generation.task",
  "model": "sora-2",
  "status": "completed",
  "progress": 100,
  "created_at": 1768380222,
  "completed_at": 1768380514,
  "expires_at": 1768466914,
  "result": {
    "type": "video",
    "data": [
      {
        "url": "https://files.toapis.com/sora/7712af45-ca35-4a15-b800-f20ea623665b.mp4",
        "format": "mp4"
      }
    ]
  },
  "billing": {
    "status": "settled",
    "credits": "100",
    "cost_usd": "0.5"
  }
}
```

```json 200 - 失败 
{
  "id": "video_7497f4d5-3a88-44c7-923a-967fa7d941a0",
  "object": "generation.task",
  "model": "sora-2",
  "status": "failed",
  "progress": 0,
  "created_at": 1768380222,
  "error": {
    "code": "generation_failed",
    "message": "生成失败: 内容违反了内容政策"
  }
}
```

```json 404 
{
  "error": {
    "code": 404,
    "message": "任务不存在",
    "type": "not_found_error"
  }
}
```

```json 401 
{
  "error": {
    "code": 401,
    "message": "身份验证失败，请检查您的API密钥",
    "type": "authentication_error"
  }
}
```


## Response

### `id`

`string`

任务唯一标识符


### `client_business_id`

`string`

客户侧业务 ID。仅当创建任务时传入 `client_business_id` 时返回。


### `object`

`string`

对象类型，固定为 `generation.task`


### `model`

`string`

使用的视频生成模型


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

任务创建时间（Unix 时间戳）


### `completed_at`

`integer`

任务完成时间（Unix 时间戳，仅完成时返回）


### `expires_at`

`integer`

视频 URL 过期时间（Unix 时间戳，仅完成时返回）


### `result`

`object`

任务结果（仅成功时返回）

<details>
<summary>属性</summary>

**`type`** — `string`

结果类型，固定为 `video`


**`data`** — `array`

视频数据数组

<details>
<summary>数组元素</summary>

**`url`** — `string`

生成的视频 URL


**`format`** — `string`

视频格式（如 `mp4`）


**`last_frame_url`** — `string`

生成视频的尾帧图像 URL。仅当创建任务时设置 `return_last_frame: true` 且模型返回尾帧时出现。


### `usage`

`object`

模型工具用量。Seedance 2 启用 `tools: [{ "type": "web_search" }]` 时，`usage.tool_usage.web_search` 表示实际联网搜索次数；`0` 表示未搜索。


### `billing`

`object`

可选的平台计费状态和已确认费用。`status` 为 `pending`、`settled` 或 `refunded`。`credits` 和 `cost_usd` 是十进制字符串，仅在净费用已确认时返回。缺少该对象不代表任务免费。详见[价格与实际费用](../account/pricing)。


### `error`

`object`

错误信息（仅失败时返回）

<details>
<summary>属性</summary>

**`code`** — `string`

错误代码


**`message`** — `string`

错误描述


## 任务状态说明

| 状态            | 说明       | 是否终态 | 建议操作                       |
| ------------- | -------- | ---- | -------------------------- |
| `queued`      | 任务排队等待处理 | ❌    | 等待 5-10 秒后重试查询             |
| `in_progress` | 任务正在处理中  | ❌    | 等待 10-15 秒后重试查询            |
| `completed`   | 任务成功完成   | ✅    | 从 result.data\[0].url 获取视频 |
| `failed`      | 任务处理失败   | ✅    | 检查 error 信息                |

## 轮询策略建议

```
初始等待: 5 秒
轮询间隔: 10 秒
最大等待: 600 秒（10分钟）
典型耗时: 1-5 分钟
```

### Python 轮询示例

```python 
import time
import random
import requests

def poll_video_task(task_id, api_key, max_wait=600):
    """轮询视频生成任务直到完成或超时"""
    start_time = time.time()
    interval = 10  # 10秒间隔
    
    # 首次等待5秒
    time.sleep(5)
    
    while time.time() - start_time < max_wait:
        response = requests.get(
            f'https://toapis.com/v1/videos/generations/{task_id}',
            headers={'Authorization': f'Bearer {api_key}'}
        )
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', interval))
            time.sleep(retry_after + random.uniform(0, 1))
            interval = min(interval * 2, 120)
            continue
        response.raise_for_status()
        data = response.json()
        
        print(f"状态: {data['status']}, 进度: {data.get('progress', 0)}%")
        
        if data['status'] == 'completed':
            return {
                'url': data['result']['data'][0]['url'],
                'format': data['result']['data'][0].get('format'),
                'expires_at': data.get('expires_at')
            }
        elif data['status'] == 'failed':
            raise Exception(f"生成失败: {data['error']['message']}")
        
        time.sleep(interval + random.uniform(0, 1))
    
    raise TimeoutError("任务超时")
```

## 视频资源有效期

> ⚠️ **注意**
>
> 生成的视频 URL 有效期为 **24 小时**
>
> * 请在有效期内下载保存视频
> * `expires_at` 字段标识视频过期时间（Unix 时间戳）
> * 视频过期后无法访问，如需重新获取，需要重新提交生成任务
> * 缩略图与视频同步过期


## 常见错误

| 错误码 | 错误类型                       | 说明              |
| --- | -------------------------- | --------------- |
| 400 | `invalid_request`          | 请求参数无效          |
| 401 | `unauthorized`             | 认证失败，检查 API Key |
| 402 | `insufficient_quota`       | 余额不足            |
| 404 | `task_not_found`           | 任务不存在           |
| 422 | `content_policy_violation` | 内容违规            |
| 429 | `rate_limit_exceeded`      | 请求频率超限          |
| 500 | `internal_error`           | 服务器内部错误         |

## 性能建议

> 💡 **提示**
>
> 视频生成耗时较长，建议：
>
> 1. **使用 ToAPIs 统一任务 Webhook**：以 [Webhook](/docs/cn/api-reference/webhooks/task-webhooks) 为主，轮询为兜底
> 2. **合理设置轮询间隔**：至少5～10秒并加入随机抖动；遇到429读取 `Retry-After` 后指数退避
> 3. **设置超时时间**：长视频生成可能需要5-10分钟，请设置合理的超时
> 4. **及时下载保存**：视频24小时后过期，请务必及时保存到自己的存储


查询限流和响应头见 [异步任务速率限制](/docs/cn/api-reference/rate-limits/async-tasks)。批量查询最多 100 个任务 ID。
