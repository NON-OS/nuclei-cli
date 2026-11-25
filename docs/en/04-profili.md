# Profiles and forbidden flags

🌐 [Italiano](../04-profili.md) · **English** · [中文](../zh/04-profili.md)

| Profile | What it does | Noise | Root |
|---|---|---|---|
| `critici` | Critical and high severity. | medium | no |
| `cve` | CVE templates, critical and high. | medium | no |
| `esposizioni` | CVEs, misconfigurations and exposures. | medium | no |
| `esteso` | Adds medium severity. | high | no |
| `prudente` | With rate, concurrency and timeout limits. | medium | no |
| `lento` | Rate expressed per minute, few threads. | low | no |

`nuclei-cli profili` prints the exact flags of each one.

## What each profile does

**critici** (`-severity critical,high -exclude-tags intrusive,dos -ni -jsonl`). Critical and high severity. The starting point: few alerts, all worth reviewing.

**cve** (`-tags cve -severity critical,high -exclude-tags intrusive,dos -ni -jsonl`). CVE templates, critical and high. After identifying the technologies: look for known vulnerabilities.

**esposizioni** (`-tags cve,misconfig,exposure -severity critical,high -exclude-tags intrusive,dos -ni -jsonl`). CVEs, misconfigurations and exposures. Also covers exposed panels and forgotten files.

**esteso** (`-severity critical,high,medium -exclude-tags intrusive,dos -ni -jsonl`). Adds medium severity. When the client wants the full picture. More templates, more requests.

**prudente** (`-severity critical,high -exclude-tags intrusive,dos -ni -rl 50 -c 20 -bs 20 -timeout 10 -retries 1 -stats -silent -jsonl`). With rate, concurrency and timeout limits. The default profile on client infrastructure.

**lento** (`-severity critical,high -exclude-tags intrusive,dos -ni -rlm 600 -c 10 -bs 10 -timeout 15 -retries 1 -jsonl`). Rate expressed per minute, few threads. For fragile services or ones with aggressive detection.

## Passing flags by hand

Everything you write after `--` goes to nuclei, after the profile flags, provided it is not on the forbidden list. The check is case-insensitive and accepts both `-flag valore` and `-flag=valore`, with one or two dashes.

```sh
nuclei-cli lancia prudente https://app.example.org --scope scope.toml -- -timeout 5
```

## Forbidden list

| Flag | Why |
|---|---|
| `-u`, `-target`, `-l`, `-list`, `-targets-inline` | targets come from the file validated against the scope |
| `-o`, `-output` | output is handled by nuclei-cli |
| `-t`, `-templates`, `-template-url`, `-w`, `-workflows` | templates are chosen via the profiles: an unverified template can do whatever it wants |
| `-code` | enables templates that run code on your machine |
| `-dast` | DAST fuzzing is active and intrusive: use nuclei directly, with an explicit agreement |
| `-etags`, `-exclude-tags` | excluding dangerous tags is fixed by the profiles |
| `-itags`, `-include-tags` | the included tags are chosen via the profiles |
| `-im`, `-input-mode` | an imported spec can contain out-of-scope hosts |
| `-resume` | resumes a run that didn't go through the scope check |
| `-turl`, `-wurl` | templates are chosen via the profiles |
| `-esc`, `-enable-self-contained` | self-contained templates carry their own targets: out of scope |
| `-ai`, `-prompt` | sends a template-generation request to an external service |
| `-rc`, `-report-config` | sends results to external services (GitHub, Jira, Slack...) |
| `-iserver`, `-itoken` | interactsh is disabled by the profiles |
| `-up`, `-update` | updating the program is done separately, not inside an authorized run |

## What the filter does not do

It is not a sandbox. If you want to get around it you can, for example by calling `nuclei` directly. It is there to stop mistakes and bad habits, not an attacker who already has access to your terminal. If you need a forbidden flag for an activity agreed with the client, use nuclei directly and record the decision in the engagement.
