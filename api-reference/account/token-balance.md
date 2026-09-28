> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# 查询令牌余额

> 查询当前 API Key 的剩余额度和已使用额度

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


* 查询当前 API Key 的剩余额度和已使用额度
* 监控单个令牌的使用情况
* 支持 CORS 跨域请求
* 实时余额监控

获取当前 API Key（令牌）的剩余余额和已使用余额。此接口用于监控单个令牌的使用情况，同时会返回积分字段，固定按 `1 USD = 200 积分` 换算。

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
GET /v1/balance
GET /balance
```

两个端点功能相同，可以任选其一使用。

### 请求示例

```bash cURL 
curl --request GET \
  --url 'https://toapis.com/v1/balance' \
  --header 'Authorization: Bearer <token>'
```

```python Python 
import requests

API_BASE = 'https://toapis.com'
API_KEY = 'sk-xxxxxxxxxxxxxxxxxxxxxx'

headers = {
    'Authorization': f'Bearer {API_KEY}'
}

def get_token_balance():
    response = requests.get(f'{API_BASE}/v1/balance', headers=headers)
    data = response.json()

    if data.get('success'):
        if data.get('unlimited_quota'):
            print("令牌额度: 无限")
        else:
            print(f"令牌剩余余额: {data['remain_balance']}")
            print(f"令牌剩余积分: {data['remain_credits']}")
        print(f"令牌已使用: {data['used_balance']}")
        print(f"令牌已使用积分: {data['used_credits']}")
    else:
        print(f"查询失败: {data.get('message')}")

    return data

get_token_balance()
```

```javascript JavaScript 
const API_BASE = 'https://toapis.com';
const API_KEY = 'sk-xxxxxxxxxxxxxxxxxxxxxx';

async function getTokenBalance() {
  const response = await fetch(`${API_BASE}/v1/balance`, {
    headers: {
      'Authorization': `Bearer ${API_KEY}`
    }
  });

  const data = await response.json();

  if (data.success) {
    if (data.unlimited_quota) {
      console.log('令牌额度: 无限');
    } else {
      console.log(`令牌剩余余额: ${data.remain_balance}`);
      console.log(`令牌剩余积分: ${data.remain_credits}`);
    }
    console.log(`令牌已使用: ${data.used_balance}`);
    console.log(`令牌已使用积分: ${data.used_credits}`);
  } else {
    console.error('查询失败:', data.message);
  }

  return data;
}

getTokenBalance();
```

```go Go 
package main

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
)

type BalanceResponse struct {
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
    url := "https://toapis.com/v1/balance"

    req, _ := http.NewRequest("GET", url, nil)
    req.Header.Set("Authorization", "Bearer <token>")

    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        panic(err)
    }
    defer resp.Body.Close()

    body, _ := ioutil.ReadAll(resp.Body)

    var result BalanceResponse
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
        String url = "https://toapis.com/v1/balance";

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

$ch = curl_init('https://toapis.com/v1/balance');
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

url = URI("https://toapis.com/v1/balance")

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
let url = URL(string: "https://toapis.com/v1/balance")!

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
  "remain_balance": 10.5,
  "used_balance": 2.3,
  "remain_credits": 2100,
  "used_credits": 460,
  "credits_per_usd": 200,
  "unlimited_quota": false
}
```

```json 200 - 无限额度令牌 
{
  "success": true,
  "remain_balance": -1,
  "used_balance": 2.3,
  "remain_credits": 2100,
  "used_credits": 460,
  "credits_per_usd": 200,
  "unlimited_quota": true
}
```

```json 200 - 令牌不存在 
{
  "success": false,
  "message": "获取令牌信息失败: record not found"
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

令牌剩余余额（成功时返回）。当 `unlimited_quota` 为 `true` 时，该值为 `-1`


### `used_balance`

`float`

令牌已使用余额（成功时返回）


### `remain_credits`

`float`

令牌剩余积分（成功时返回），固定按 `1 USD = 200 积分` 换算


### `used_credits`

`float`

令牌已使用积分（成功时返回）


### `credits_per_usd`

`float`

积分换算比例，当前返回 `200`


### `unlimited_quota`

`boolean`

是否为无限额度令牌。`true` 表示无限额度，`false` 表示有限额度


## 使用场景

* 监控单个 API Key 的消耗情况
* 在应用中显示当前令牌的余额
* 设置余额告警，当余额低于阈值时通知

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
> **无限额度令牌**
>
> 当令牌被设置为无限额度时：
>
> * `unlimited_quota` 字段返回 `true`
> * `remain_balance` 字段返回 `-1`
> * 该令牌不受额度限制，可无限使用


## 常见错误

| 错误信息              | 原因                    | 解决方案                                    |
| ----------------- | --------------------- | --------------------------------------- |
| 无 Authorization 头 | 未提供 Authorization 请求头 | 添加 `Authorization: Bearer sk-xxxxx` 请求头 |
| 获取令牌信息失败          | 令牌不存在或已删除             | 检查令牌 key 是否正确                           |

> ⚠️ **注意**
>
> **安全提示**
>
> API Key 相当于密码，请妥善保管，不要泄露给他人。生产环境请务必使用 HTTPS。

