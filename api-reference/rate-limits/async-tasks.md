> ## Documentation Index
> Fetch the complete documentation index at: https://docs.toapis.com/llms.txt
> Use this file to discover all available pages before exploring further.

# 异步任务速率限制

> ToAPIs 异步图片和视频任务的用户级提交与查询限流

> 💡 **提示**
>
> **国内用户请注意：** 中国大陆用户请使用 `https://toapis.cn` 作为接口地址（Base URL）。文档示例中的 `https://toapis.com` 请替换为 `https://toapis.cn`。


ToAPIs 为异步任务提交和状态查询使用两个独立令牌桶，不占用同步模型请求额度。

| 分组        | 提交 RPM | 持续 RPS | 10 秒突发 | 查询 RPM | 持续 RPS | 10 秒突发 |
| --------- | -----: | -----: | -----: | -----: | -----: | -----: |
| `default` |    300 |      5 |     50 |  3,000 |     50 |    500 |
| `vip`     |  1,000 |   16.7 |    167 | 10,000 |  166.7 |  1,667 |
| `svip`    |  2,000 |   33.3 |    334 | 30,000 |    500 |  5,000 |

额度按用户 ID 而不是 Token 统计，同一用户的多个 Token 共享额度。提交和查询互不影响。业务失败会计数，被 `429` 拒绝的请求不计数。批量状态查询一次计一个请求，每次最多 100 个任务 ID。

限流响应头包括 `Retry-After`、`X-RateLimit-Limit`、`X-RateLimit-Remaining`、`X-RateLimit-Reset` 和 `X-RateLimit-Category: async_submit|async_query`。

```json 429 
{"error":{"code":"rate_limit_exceeded","message":"异步任务请求频率超限"}}
```

```json 503 
{"error":{"code":"rate_limit_unavailable","message":"异步任务提交限流服务暂时不可用，请稍后重试"}}
```

提交限流服务不可用时返回 `503 rate_limit_unavailable`；查询会降级放行并记录监控。推荐以 [任务 Webhook](/docs/cn/api-reference/webhooks/task-webhooks) 为主、轮询为兜底。轮询间隔至少 5～10 秒，加入随机抖动，并在 `429`/`503` 时优先读取 `Retry-After`，没有该头时再使用指数退避。
