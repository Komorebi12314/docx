> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Sora2 查询角色状态

> 查询角色创建任务的状态和结果

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


## 功能概述

查询角色创建任务的状态和结果，获取已创建角色的详细信息（角色 ID、显示名称、用户名等），用于后续视频生成。

> 💡 **提示**
>
> **使用说明：**
>
> * 角色创建是异步任务，需要轮询此接口获取结果
> * 任务完成后返回角色详细信息
> * 角色 `username` 可在 prompt 中使用 `@username` 格式引用
> * 角色任务 ID 可通过 `character_url` 参数在视频生成中使用


## 路径参数

### `task_id`

`string` · 必填

角色创建任务 ID

这是从 [创建角色](./create-persona) API 返回的任务 ID

示例：`"task_01KBZ0TZZ7C7M3WS1TJM0PH8J4"`


## 认证

### `Authorization`

`string` · 必填

Bearer Token 认证

```
Authorization: Bearer YOUR_API_KEY
```

获取 API Key：访问 [API Key 管理页面](https://toapis.com/console/token)


## 响应字段

### `id`

`string`

任务唯一标识符（角色创建任务 ID）


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


### `expires_at`

`integer`

结果资源过期时间（Unix 时间戳，仅完成后有值）


### `result`

`object`

任务结果（仅 status 为 completed 时有值）

`result.type` 固定为 `character`，`result.data.characters` 为角色列表


### `error`

`object`

错误信息（仅 status 为 failed 时有值）


### 请求示例

```bash cURL 
curl --request GET \
  --url 'https://toapis.com/v1/characters_tasks/task_01KBZ0TZZ7C7M3WS1TJM0PH8J4' \
  --header 'Authorization: Bearer YOUR_API_KEY'
```

```python Python 
import requests
import time

def query_character_task(task_id):
    """查询角色创建任务状态"""
    url = f"https://toapis.com/v1/characters_tasks/{task_id}"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}

    response = requests.get(url, headers=headers)
    return response.json()

def wait_for_character(task_id, max_wait=300, interval=5):
    """轮询等待角色创建完成"""
    start_time = time.time()

    while time.time() - start_time < max_wait:
        result = query_character_task(task_id)

        status = result['status']
        progress = result.get('progress', 0)
        print(f"状态: {status}, 进度: {progress}%")

        if status == 'completed':
            characters = result['result']['data']['characters']
            for char in characters:
                print(f"角色 ID: {char['id']}")
                print(f"显示名称: {char['display_name']}")
                print(f"用户名: {char['username']}")
            return result

        if status == 'failed':
            raise Exception("角色创建失败")

        time.sleep(interval)

    raise Exception("等待超时")

# 使用示例
task_id = "task_01KBZ0TZZ7C7M3WS1TJM0PH8J4"
result = wait_for_character(task_id)
```

```javascript JavaScript 
async function queryCharacterTask(taskId) {
  const response = await fetch(
    `https://toapis.com/v1/characters_tasks/${taskId}`,
    {
      method: 'GET',
      headers: {
        'Authorization': 'Bearer YOUR_API_KEY'
      }
    }
  );
  return await response.json();
}

async function waitForCharacter(taskId, maxWait = 300000, interval = 5000) {
  const startTime = Date.now();

  while (Date.now() - startTime < maxWait) {
    const result = await queryCharacterTask(taskId);

    const { status, progress } = result;
    console.log(`状态: ${status}, 进度: ${progress}%`);

    if (status === 'completed') {
      const characters = result.result.data.characters;
      characters.forEach(char => {
        console.log(`角色 ID: ${char.id}`);
        console.log(`显示名称: ${char.display_name}`);
        console.log(`用户名: ${char.username}`);
      });
      return result;
    }

    if (status === 'failed') {
      throw new Error('角色创建失败');
    }

    await new Promise(resolve => setTimeout(resolve, interval));
  }

  throw new Error('等待超时');
}

// 使用示例
const taskId = 'task_01KBZ0TZZ7C7M3WS1TJM0PH8J4';
waitForCharacter(taskId).then(result => console.log(result));
```

```go Go 
package main

import (
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "time"
)

type CharacterResponse struct {
    ID        string `json:"id"`
    Object    string `json:"object"`
    Model     string `json:"model"`
    Status    string `json:"status"`
    Progress  int    `json:"progress"`
    CreatedAt int64  `json:"created_at"`
    Result    struct {
        Type string `json:"type"`
        Data struct {
            Characters []struct {
                ID                string `json:"id"`
                DisplayName       string `json:"display_name"`
                ProfilePictureURL string `json:"profile_picture_url"`
                Username          string `json:"username"`
            } `json:"characters"`
        } `json:"data"`
    } `json:"result"`
}

func queryCharacterTask(taskID string) (*CharacterResponse, error) {
    url := "https://toapis.com/v1/characters_tasks/" + taskID

    req, _ := http.NewRequest("GET", url, nil)
    req.Header.Set("Authorization", "Bearer YOUR_API_KEY")

    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    body, _ := io.ReadAll(resp.Body)

    var result CharacterResponse
    json.Unmarshal(body, &result)
    return &result, nil
}

func main() {
    taskID := "task_01KBZ0TZZ7C7M3WS1TJM0PH8J4"

    for i := 0; i < 60; i++ {
        result, err := queryCharacterTask(taskID)
        if err != nil {
            panic(err)
        }

        fmt.Printf("状态: %s, 进度: %d%%\n", result.Status, result.Progress)

        if result.Status == "completed" {
            for _, char := range result.Result.Data.Characters {
                fmt.Printf("角色 ID: %s\n", char.ID)
                fmt.Printf("显示名称: %s\n", char.DisplayName)
                fmt.Printf("用户名: %s\n", char.Username)
            }
            break
        }

        time.Sleep(5 * time.Second)
    }
}
```


### 响应示例

```json 200（进行中） 
{
  "id": "task_01KC0JZCMTMQ70D68XTM56Q5D0",
  "object": "generation.task",
  "model": "sora-2",
  "status": "in_progress",
  "progress": 45,
  "created_at": 1765251461,
  "metadata": {}
}
```

```json 200（创建完成） 
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
    "message": "请求参数无效",
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

```json 404（任务不存在） 
{
  "error": {
    "code": 404,
    "message": "任务不存在",
    "type": "not_found_error"
  }
}
```

```json 429（请求频率限制） 
{
  "error": {
    "code": 429,
    "message": "请求过于频繁，请稍后再试",
    "type": "rate_limit_error"
  }
}
```


## 使用角色生成视频

角色创建完成后，可以在视频生成中使用角色。有两种引用方式：

### 方式一：使用 @username 在 prompt 中引用

```bash 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "sora-2",
    "prompt": "@duksvfkf.turbo_whis is dancing in the rain"
  }'
```

### 方式二：使用 character\_url 参数

```bash 
curl --request POST \
  --url https://toapis.com/v1/videos/generations \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "sora-2",
    "prompt": "A cute cat is dancing in the rain",
    "character_url": "task_01KC0JZCMTMQ70D68XTM56Q5D0"
  }'
```

> 💡 **小贴士**
>
> **提示：** `username` 从查询结果的 `characters[].username` 字段获取，`character_url` 使用角色创建任务的 `task_id`。


## 轮询建议

| 参数     | 建议值         |
| ------ | ----------- |
| 轮询间隔   | 5 秒         |
| 最大等待时间 | 5 分钟        |
| 超时处理   | 重新提交任务或联系支持 |
