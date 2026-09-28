> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# 查询用户余额

> 查询当前用户账户的剩余额度和已使用额度

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 查询当前用户账户的总体余额
* 监控用户级别的使用情况
* 支持 CORS 跨域请求
* 实时余额监控

获取当前用户账户的剩余余额和已使用余额。此接口返回用户级别的余额信息，与具体令牌无关，用于查看用户账户的总体余额，同时会返回积分字段，固定按 `1 USD = 200 积分` 换算。

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


## 接口端点

```
GET /v1/user/balance
GET /user/balance
```

两个端点功能相同，可以任选其一使用。

### 请求示例

```bash cURL 
curl --request GET \
  --url 'https://toapis.com/v1/user/balance' \
  --header 'Authorization: Bearer <token>'
```

```python Python 
import requests

API_BASE = 'https://toapis.com'
API_KEY = 'sk-xxxxxxxxxxxxxxxxxxxxxx'

headers = {
    'Authorization': f'Bearer {API_KEY}'
}

def get_user_balance():
    response = requests.get(f'{API_BASE}/v1/user/balance', headers=headers)
    data = response.json()

    if data.get('success'):
        if data.get('unlimited_quota'):
            print("用户额度: 无限")
        else:
            print(f"用户剩余余额: {data['remain_balance']}")
            print(f"用户剩余积分: {data['remain_credits']}")
        print(f"用户已使用: {data['used_balance']}")
        print(f"用户已使用积分: {data['used_credits']}")
    else:
        print(f"查询失败: {data.get('message')}")

    return data

get_user_balance()
```

```javascript JavaScript 
const API_BASE = 'https://toapis.com';
const API_KEY = 'sk-xxxxxxxxxxxxxxxxxxxxxx';

async function getUserBalance() {
  const response = await fetch(`${API_BASE}/v1/user/balance`, {
    headers: {
      'Authorization': `Bearer ${API_KEY}`
    }
  });

  const data = await response.json();

  if (data.success) {
    if (data.unlimited_quota) {
      console.log('用户额度: 无限');
    } else {
      console.log(`用户剩余余额: ${data.remain_balance}`);
      console.log(`用户剩余积分: ${data.remain_credits}`);
    }
    console.log(`用户已使用: ${data.used_balance}`);
    console.log(`用户已使用积分: ${data.used_credits}`);
  } else {
    console.error('查询失败:', data.message);
  }

  return data;
}

getUserBalance();
```

```go Go 
package main

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
)

type UserBalanceResponse struct {
    Success        bool    `json:"success"`
    Message        string  `json:"message,omitempty"`
    RemainBalance  float64 `json:"remain_balance"`
    UsedBalance    float64 `json:"used_balance"`
    RemainCredits  float64 `json:"remain_credits"`
    UsedCredits    float64 `json:"used_credits"`
    CreditsPerUSD  float64 `json:"credits_per_usd"`
    UnlimitedQuota bool    `json:"unlimited_quota"`
}

func main() {
    url := "https://toapis.com/v1/user/balance"

    req, _ := http.NewRequest("GET", url, nil)
    req.Header.Set("Authorization", "Bearer <token>")

    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        panic(err)
    }
    defer resp.Body.Close()

    body, _ := ioutil.ReadAll(resp.Body)

    var result UserBalanceResponse
    json.Unmarshal(body, &result)

    if result.Success {
        if result.UnlimitedQuota {
            fmt.Println("额度: 无限")
        } else {
            fmt.Printf("剩余余额: %.2f\n", result.RemainBalance)
            fmt.Printf("剩余积分: %.2f\n", result.RemainCredits)
        }
        fmt.Printf("已使用: %.2f\n", result.UsedBalance)
        fmt.Printf("已使用积分: %.2f\n", result.UsedCredits)
    }
}
```

```java Java 
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;

public class Main {
    public static void main(String[] args) throws Exception {
        String url = "https://toapis.com/v1/user/balance";

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .header("Authorization", "Bearer <token>")
            .GET()
            .build();

        HttpResponse<String> response = client.send(request,
            HttpResponse.BodyHandlers.ofString());

        System.out.println(response.body());
    }
}
```

```php PHP 
<?php

$api_key = 'sk-xxxxxxxxxxxxxxxxxxxxxx';

$ch = curl_init('https://toapis.com/v1/user/balance');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "Authorization: Bearer $api_key"
]);

$response = curl_exec($ch);
curl_close($ch);

$data = json_decode($response, true);

if ($data['success']) {
    if ($data['unlimited_quota']) {
        echo "额度: 无限\n";
    } else {
        echo "剩余余额: " . $data['remain_balance'] . "\n";
    }
    echo "已使用: " . $data['used_balance'] . "\n";
} else {
    echo "查询失败: " . $data['message'] . "\n";
}
?>
```

```ruby Ruby 
require 'net/http'
require 'json'
require 'uri'

api_key = 'sk-xxxxxxxxxxxxxxxxxxxxxx'

url = URI("https://toapis.com/v1/user/balance")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Get.new(url)
request["Authorization"] = "Bearer #{api_key}"

response = http.request(request)
data = JSON.parse(response.body)

if data['success']
  if data['unlimited_quota']
    puts "额度: 无限"
  else
    puts "剩余余额: #{data['remain_balance']}"
  end
  puts "已使用: #{data['used_balance']}"
else
  puts "查询失败: #{data['message']}"
end
```

```swift Swift 
import Foundation

let apiKey = "sk-xxxxxxxxxxxxxxxxxxxxxx"
let url = URL(string: "https://toapis.com/v1/user/balance")!

var request = URLRequest(url: url)
request.httpMethod = "GET"
request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")

let task = URLSession.shared.dataTask(with: request) { data, response, error in
    if let error = error {
        print("Error: \(error)")
        return
    }

    if let data = data, let responseString = String(data: data, encoding: .utf8) {
        print(responseString)
    }
}

task.resume()
```


### 响应示例

```json 200 - 查询成功 
{
  "success": true,
  "remain_balance": 100.0,
  "used_balance": 25.5,
  "remain_credits": 20000,
  "used_credits": 5100,
  "credits_per_usd": 200,
  "unlimited_quota": false
}
```

```json 200 - 无限额度用户 
{
  "success": true,
  "remain_balance": -1,
  "used_balance": 25.5,
  "remain_credits": 20000,
  "used_credits": 5100,
  "credits_per_usd": 200,
  "unlimited_quota": true
}
```

```json 200 - 用户额度查询失败 
{
  "success": false,
  "message": "获取用户额度失败"
}
```

```json 200 - 已使用额度查询失败 
{
  "success": false,
  "message": "获取已使用额度失败"
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

```json 429 
{
  "error": {
    "code": 429,
    "message": "请求过于频繁，请稍后再试",
    "type": "rate_limit_error"
  }
}
```


## Response

### `success`

`boolean`

请求是否成功


### `message`

`string`

错误信息（仅失败时返回）


### `remain_balance`

`float`

用户剩余余额（成功时返回）。当 `unlimited_quota` 为 `true` 时，该值为 `-1`


### `used_balance`

`float`

用户已使用余额（成功时返回）


### `remain_credits`

`float`

用户剩余积分（成功时返回），固定按 `1 USD = 200 积分` 换算


### `used_credits`

`float`

用户已使用积分（成功时返回）


### `credits_per_usd`

`float`

积分换算比例，当前返回 `200`


### `unlimited_quota`

`boolean`

是否为无限额度用户。`true` 表示无限额度，`false` 表示有限额度


## 令牌余额 vs 用户余额

| 对比项  | 令牌余额 (`/v1/balance`)            | 用户余额 (`/v1/user/balance`)  |
| ---- | ------------------------------- | -------------------------- |
| 作用范围 | 单个令牌                            | 整个用户账户                     |
| 数据来源 | Token 的 RemainQuota 和 UsedQuota | User 的 quota 和 used\_quota |
| 使用场景 | 监控单个 API Key 的使用情况              | 查看用户账户总体余额                 |
| 受限于  | 令牌级别的额度限制                       | 用户级别的额度限制                  |

## 使用场景

* 查看用户账户的总体余额
* 用于充值提醒和余额告警
* 在用户控制面板显示账户余额

> 💡 **提示**
>
> **余额单位说明**
>
> 余额数值的单位取决于系统配置：
>
> * **USD** - 美元
> * **CNY** - 人民币
> * **Tokens** - Token 数量
>
> 如果需要稳定读取积分，请优先使用 `remain_credits` 和 `used_credits`。这两个字段固定按 `1 USD = 200 积分` 换算，不受余额展示配置影响。


> 💡 **小贴士**
>
> **无限额度用户**
>
> 当用户被设置为无限额度时：
>
> * `unlimited_quota` 字段返回 `true`
> * `remain_balance` 字段返回 `-1`
> * 该用户不受额度限制，可无限使用


## 常见错误

| 错误信息              | 原因                    | 解决方案                                    |
| ----------------- | --------------------- | --------------------------------------- |
| 无 Authorization 头 | 未提供 Authorization 请求头 | 添加 `Authorization: Bearer sk-xxxxx` 请求头 |
| 获取用户额度失败          | 用户不存在                 | 检查令牌关联的用户是否存在                           |
| 获取已使用额度失败         | 数据库查询错误               | 联系管理员检查系统状态                             |

> ⚠️ **注意**
>
> **安全提示**
>
> API Key 相当于密码，请妥善保管，不要泄露给他人。生产环境请务必使用 HTTPS。

