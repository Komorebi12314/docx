> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# 异步任务 Webhook

> 接收并验证 ToAPIs 异步生成任务的最终成功和最终失败事件

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


ToAPIs 为异步图片和视频任务发送统一的最终状态事件。第一版只发送最终成功、最终失败和测试事件，不发送中间进度事件。

ToAPIs 提供至少一次投递，同一事件重试时 `id` 保持不变，但不保证恰好一次。接收方必须先持久化 event ID，再执行订单更新、发货等副作用；重复 event ID 应直接返回 `2xx`。

## 配置 Token

在 ToAPIs 控制台编辑 Token：

1. 配置 HTTPS 默认 callback URL。
2. 生成 32 字节签名密钥。密钥仅在生成或轮换时显示一次，请立即安全保存。
3. 启用“任务 Webhook”并保存。
4. 发送测试事件，确认接收端能验签并返回 `2xx`。

任务请求未传 `callback_url` 时，ToAPIs 使用 Token 默认地址。请求级 `callback_url` 只能覆盖路径和查询参数，协议、域名和端口必须与 Token 默认地址相同。

如果 Token 未启用 Webhook，或缺少默认地址/签名密钥，却在请求中传入 `callback_url`，ToAPIs 返回：

```json 
{
  "error": {
    "code": "webhook_not_configured",
    "message": "webhook_not_configured"
  }
}
```

## 事件类型与 Payload

`task_type` 只会是 `image` 或 `video`。`result` 与对应任务查询接口的标准化公开结果一致，不包含渠道 ID、上游任务 ID、上游密钥、内部凭证或 `PrivateData`。

图片成功事件可包含 `data.usage`，其中只包含已确认且有效的图片 token 用量字段，也可与 `tool_usage.web_search` 并存。图片和视频事件还可能包含 `data.billing`。当 `status` 为 `pending` 时不返回金额；无法确认安全公开值时会省略整个对象。字段契约见[价格与实际费用](../account/pricing)。`billing` 是否可用不会延迟投递，也不会改变重试规则。

### generation.completed

```json 
{
  "id": "evt_01abcdef",
  "type": "generation.completed",
  "api_version": "v1",
  "created_at": 1783953302,
  "data": {
    "task_id": "tsk_01abcdef",
    "client_business_id": "order_123",
    "task_type": "image",
    "model": "model-name",
    "status": "SUCCESS",
    "progress": "100%",
    "result": {
      "type": "image",
      "data": [{"url": "https://cdn.example/result.png"}]
    },
    "billing": {
      "status": "settled",
      "credits": "100",
      "cost_usd": "0.5"
    },
    "error": null,
    "submitted_at": 1783953000,
    "finished_at": 1783953300
  }
}
```

### generation.failed

只有内部重试已经结束、最终计费或退款已经完成时，ToAPIs 才会发送失败事件。暂时性失败不会触发 `generation.failed`。

```json 
{
  "id": "evt_01failure",
  "type": "generation.failed",
  "api_version": "v1",
  "created_at": 1783953302,
  "data": {
    "task_id": "tsk_01failure",
    "client_business_id": "order_456",
    "task_type": "video",
    "model": "model-name",
    "status": "FAILURE",
    "progress": "100%",
    "result": null,
    "billing": {
      "status": "refunded",
      "credits": "0",
      "cost_usd": "0"
    },
    "error": {
      "code": "generation_failed",
      "message": "Generation failed after retries"
    },
    "submitted_at": 1783953000,
    "finished_at": 1783953300
  }
}
```

### endpoint.test

```json 
{
  "id": "evt_01test",
  "type": "endpoint.test",
  "api_version": "v1",
  "created_at": 1783953302,
  "data": {
    "task_id": "endpoint_test",
    "task_type": "image",
    "status": "SUCCESS",
    "progress": "100%",
    "result": {
      "message": "ToAPIs webhook endpoint test"
    },
    "error": null,
    "submitted_at": 0,
    "finished_at": 0
  }
}
```

## 请求头与签名

```text 
User-Agent: ToAPIs-Webhook/1.0
X-ToAPIs-Webhook-Id: evt_01abcdef
X-ToAPIs-Webhook-Timestamp: 1783953302
X-ToAPIs-Webhook-Signature: v1=<current-signature>[,v1=<previous-signature>]
```

签名原文必须使用未经解析、未经重新序列化的原始请求体：

```text 
event_id + "." + timestamp + "." + raw_request_body
```

算法为 HMAC-SHA256，输出为小写十六进制。首次收到事件时，应拒绝与本地时间相差超过 5 分钟的时间戳。重试使用实际发送时间重新签名，但 event ID 不变。

密钥轮换后 24 小时内，ToAPIs 同时发送当前密钥和上一密钥的两个 `v1` 签名。接收方应拆分逗号分隔的签名，并接受任意一个有效值。

### Python

```python 
import hashlib
import hmac
import time

def verify_toapis(headers, raw_body: bytes, secrets: list[str]) -> bool:
    event_id = headers["X-ToAPIs-Webhook-Id"]
    timestamp = int(headers["X-ToAPIs-Webhook-Timestamp"])
    if abs(int(time.time()) - timestamp) > 300:
        return False

    signed = f"{event_id}.{timestamp}.".encode() + raw_body
    received = [
        value.strip()[3:]
        for value in headers["X-ToAPIs-Webhook-Signature"].split(",")
        if value.strip().startswith("v1=")
    ]
    for secret in secrets:
        expected = hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()
        if any(hmac.compare_digest(expected, signature) for signature in received):
            return True
    return False
```

### Node.js

```javascript 
import crypto from 'node:crypto';

export function verifyToAPIs(headers, rawBody, secrets) {
  const eventId = headers['x-toapis-webhook-id'];
  const timestamp = Number(headers['x-toapis-webhook-timestamp']);
  if (!Number.isFinite(timestamp) || Math.abs(Date.now() / 1000 - timestamp) > 300) {
    return false;
  }

  const signed = Buffer.concat([Buffer.from(`${eventId}.${timestamp}.`), rawBody]);
  const received = headers['x-toapis-webhook-signature']
    .split(',')
    .map((value) => value.trim())
    .filter((value) => value.startsWith('v1='))
    .map((value) => value.slice(3));

  return secrets.some((secret) => {
    const expected = crypto.createHmac('sha256', secret).update(signed).digest('hex');
    return received.some((signature) =>
      expected.length === signature.length &&
      crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(signature)),
    );
  });
}
```

### Go

```go 
package webhook

import (
    "crypto/hmac"
    "crypto/sha256"
    "encoding/hex"
    "strconv"
    "strings"
    "time"
)

func VerifyToAPIs(eventID, timestamp, signature string, body []byte, secrets []string) bool {
    ts, err := strconv.ParseInt(timestamp, 10, 64)
    if err != nil || time.Now().Unix()-ts > 300 || ts-time.Now().Unix() > 300 {
        return false
    }
    signed := append([]byte(eventID+"."+timestamp+"."), body...)
    received := strings.Split(signature, ",")
    for _, secret := range secrets {
        mac := hmac.New(sha256.New, []byte(secret))
        _, _ = mac.Write(signed)
        expected, _ := hex.DecodeString(hex.EncodeToString(mac.Sum(nil)))
        for _, value := range received {
            value = strings.TrimSpace(value)
            if !strings.HasPrefix(value, "v1=") {
                continue
            }
            actual, err := hex.DecodeString(strings.TrimPrefix(value, "v1="))
            if err == nil && hmac.Equal(expected, actual) {
                return true
            }
        }
    }
    return false
}
```

## 投递、重试与安全

* 首次投递立即执行；失败后约在 10 秒、30 秒、2 分钟、10 分钟、1 小时、6 小时和 24 小时后重试。
* 只有 `2xx` 被视为成功。`3xx` 不会自动跟随，`4xx` 和 `5xx` 都会按计划重试。
* 单次 HTTP 请求超时为 10 秒，ToAPIs 最多读取 4 KB 响应体用于脱敏后的诊断。
* callback URL 必须使用 HTTPS，禁止 userinfo、fragment、私网、回环、链路本地、保留地址和非法端口。
* 每次投递都会重新执行 DNS/IP 与 SSRF 校验，并把连接固定到已校验的公网 IP，避免 DNS rebinding。
* 回调延迟或最终失败时，请使用任务查询接口兜底；轮询应遵守[异步任务速率限制](/docs/cn/api-reference/rate-limits/async-tasks)。
* 结果 URL 可能具有有效期，请在收到事件后及时下载和保存所需文件。

Seedance 真人认证的 `callback_url`、支付 Webhook 和 OAuth callback 保持原有协议，不属于异步生成任务 Webhook。
