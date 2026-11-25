# 配置与被禁标志

🌐 [Italiano](../04-profili.md) · [English](../en/04-profili.md) · **中文**

> ⚠️ 本页为机器翻译草稿，正式发布前需母语者校对。

| 配置 | 作用 | 噪声 | Root |
|---|---|---|---|
| `critici` | critical 和 high 级别。 | 中 | 否 |
| `cve` | CVE 模板，critical 和 high。 | 中 | 否 |
| `esposizioni` | CVE、错误配置和信息暴露。 | 中 | 否 |
| `esteso` | 增加 medium 级别。 | 高 | 否 |
| `prudente` | 带频率、并发和超时限制。 | 中 | 否 |
| `lento` | 频率以每分钟计，线程很少。 | 低 | 否 |

`nuclei-cli profili` 会打印每个配置的具体标志。

## 各配置的作用

**critici** (`-severity critical,high -exclude-tags intrusive,dos -ni -jsonl`). critical 和 high 级别。 起点：报告数量少，但每条都值得查看。

**cve** (`-tags cve -severity critical,high -exclude-tags intrusive,dos -ni -jsonl`). CVE 模板，critical 和 high。 在识别出所用技术之后：查找已知漏洞。

**esposizioni** (`-tags cve,misconfig,exposure -severity critical,high -exclude-tags intrusive,dos -ni -jsonl`). CVE、错误配置和信息暴露。 同时覆盖暴露的管理面板和被遗忘的文件。

**esteso** (`-severity critical,high,medium -exclude-tags intrusive,dos -ni -jsonl`). 增加 medium 级别。 当客户想要完整的全貌时使用。模板更多，请求也更多。

**prudente** (`-severity critical,high -exclude-tags intrusive,dos -ni -rl 50 -c 20 -bs 20 -timeout 10 -retries 1 -stats -silent -jsonl`). 带频率、并发和超时限制。 在客户基础设施上默认使用的配置。

**lento** (`-severity critical,high -exclude-tags intrusive,dos -ni -rlm 600 -c 10 -bs 10 -timeout 15 -retries 1 -jsonl`). 频率以每分钟计，线程很少。 用于脆弱的服务或具有激进检测机制的服务。

## 手动传入标志

`--` 之后写的所有内容都会追加在配置标志之后传给 nuclei，前提是不在被禁清单中。比对时不区分大小写，`-flag valore` 和 `-flag=valore` 两种写法都能识别，一个或两个短横线均可。

```sh
nuclei-cli lancia prudente https://app.example.org --scope scope.toml -- -timeout 5
```

## 被禁标志清单

| 标志 | 原因 |
|---|---|
| `-u`, `-target`, `-l`, `-list`, `-targets-inline` | 目标来自经过作用域校验的文件 |
| `-o`, `-output` | 输出由 nuclei-cli 管理 |
| `-t`, `-templates`, `-template-url`, `-w`, `-workflows` | 模板通过配置选择：未经验证的模板可以为所欲为 |
| `-code` | 启用会在你本机上执行代码的模板 |
| `-dast` | DAST 模糊测试是主动且具有侵入性的：请在有明确授权的情况下直接使用 nuclei |
| `-etags`, `-exclude-tags` | 危险标签的排除由配置固定 |
| `-itags`, `-include-tags` | 要包含的标签由配置选择 |
| `-im`, `-input-mode` | 导入的规格文件可能包含作用域之外的主机 |
| `-resume` | 会恢复一次未经过作用域检查的任务 |
| `-turl`, `-wurl` | 模板通过配置选择 |
| `-esc`, `-enable-self-contained` | 自带目标的独立模板会带来它们自己的目标：超出作用域 |
| `-ai`, `-prompt` | 会把生成模板的请求发送给外部服务 |
| `-rc`, `-report-config` | 会把结果发送到外部服务（GitHub、Jira、Slack……） |
| `-iserver`, `-itoken` | interactsh 已由配置关闭 |
| `-up`, `-update` | 程序更新应单独进行，而不是在一次授权任务中进行 |

## 过滤器做不到的事

它不是沙箱。想绕过它并不难，比如直接调用 `nuclei`。它的作用是拦住失误和坏习惯，而不是拦住一个已经能访问你终端的恶意人员。如果某项与客户约定好的活动需要用到被禁标志，请直接使用 nuclei，并在项目记录中注明这一选择。
