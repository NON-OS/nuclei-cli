"""Descrizione di nuclei: profili, flag vietati, formato dei risultati."""

from __future__ import annotations

from nucleicli.profili import Profilo
from nucleicli.risultati import Voce, righe_json, sotto_dict

NOME = "nuclei"
BINARIO = "nuclei"
DESCRIZIONE = "Scansione di vulnerabilità con template, scope validato, dry-run di default e audit a catena di hash."
MODO = "url"
PASSA = ("file", "-l")
UNO_EXTRA: tuple[str, ...] = ()  # solo ffuf lavora "un comando per target"
USCITA = "-o"
VERSIONE = ("-version",)
RICONOSCI = "engine version"  # testo che il binario vero stampa con {VERSIONE}: distingue da programmi omonimi
INSTALLAZIONE = "Kali/Debian: sudo apt install nuclei. Ovunque con Go: go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"
SEGRETI = frozenset({"h", "header", "sf", "secret-file", "auth"})
GRUPPO = "Severità"
NOTA_ATTIVITA = (
    "nuclei invia richieste costruite per riconoscere vulnerabilità: è attivo. I profili escludono i tag "
    "'intrusive' e 'dos' e non contattano il server interactsh (-ni). Leggi il template prima di fidarti."
)

_COMUNI = ("-exclude-tags", "intrusive,dos", "-ni")

PROFILI = {
    p.nome: p
    for p in (
        Profilo("critici", "Severità critical e high.",
                ("-severity", "critical,high", *_COMUNI, "-jsonl"), "medio",
                "Il punto di partenza: poche segnalazioni, tutte da guardare.", uscita="jsonl"),
        Profilo("cve", "Template CVE, critical e high.",
                ("-tags", "cve", "-severity", "critical,high", *_COMUNI, "-jsonl"), "medio",
                "Dopo aver identificato le tecnologie: cerca vulnerabilità note.", uscita="jsonl"),
        Profilo("esposizioni", "CVE, configurazioni errate ed esposizioni.",
                ("-tags", "cve,misconfig,exposure", "-severity", "critical,high", *_COMUNI, "-jsonl"), "medio",
                "Copre anche i pannelli esposti e i file dimenticati.", uscita="jsonl"),
        Profilo("esteso", "Aggiunge la severità medium.",
                ("-severity", "critical,high,medium", *_COMUNI, "-jsonl"), "alto",
                "Quando il cliente vuole il quadro completo. Più template, più richieste.", uscita="jsonl"),
        Profilo("prudente", "Con limiti su frequenza, concorrenza e timeout.",
                ("-severity", "critical,high", *_COMUNI, "-rl", "50", "-c", "20", "-bs", "20",
                 "-timeout", "10", "-retries", "1", "-stats", "-silent", "-jsonl"), "medio",
                "Il profilo da usare di default su infrastrutture di clienti.", uscita="jsonl"),
        Profilo("lento", "Frequenza espressa al minuto, pochi thread.",
                ("-severity", "critical,high", *_COMUNI, "-rlm", "600", "-c", "10", "-bs", "10",
                 "-timeout", "15", "-retries", "1", "-jsonl"), "basso",
                "Per servizi fragili o con rilevamento aggressivo.", uscita="jsonl"),
    )
}  # fmt: skip

_MOTIVO_TPL = "i template si scelgono tramite i profili: un template non verificato può fare quello che vuole"

VIETATI = {
    "u": "i target arrivano dal file validato contro lo scope",
    "target": "i target arrivano dal file validato contro lo scope",
    "l": "i target arrivano dal file validato contro lo scope",
    "list": "i target arrivano dal file validato contro lo scope",
    "o": "l'output lo gestisce nuclei-cli",
    "output": "l'output lo gestisce nuclei-cli",
    "t": _MOTIVO_TPL,
    "templates": _MOTIVO_TPL,
    "template-url": _MOTIVO_TPL,
    "w": _MOTIVO_TPL,
    "workflows": _MOTIVO_TPL,
    "code": "abilita template che eseguono codice sulla tua macchina",
    "dast": "il fuzzing DAST è attivo e intrusivo: usa nuclei direttamente, con un accordo esplicito",
    "etags": "l'esclusione dei tag pericolosi è fissata dai profili",
    "exclude-tags": "l'esclusione dei tag pericolosi è fissata dai profili",
    "itags": "i tag inclusi si scelgono con i profili",
    "include-tags": "i tag inclusi si scelgono con i profili",
    "im": "una specifica importata può contenere host fuori scope",
    "input-mode": "una specifica importata può contenere host fuori scope",
    "resume": "riprende un lancio che non è passato dal controllo dello scope",
    "turl": "i template si scelgono tramite i profili",
    "wurl": "i template si scelgono tramite i profili",
    "esc": "i template autonomi portano con sé i loro target: fuori scope",
    "enable-self-contained": "i template autonomi portano con sé i loro target: fuori scope",
    "targets-inline": "i target arrivano dal file validato contro lo scope",
    "ai": "manda a un servizio esterno la richiesta di generare un template",
    "prompt": "manda a un servizio esterno la richiesta di generare un template",
    "rc": "invia i risultati a servizi esterni (GitHub, Jira, Slack...)",
    "report-config": "invia i risultati a servizi esterni (GitHub, Jira, Slack...)",
    "iserver": "interactsh è spento dai profili",
    "itoken": "interactsh è spento dai profili",
    "up": "l'aggiornamento del programma si fa a parte, non dentro un lancio autorizzato",
    "update": "l'aggiornamento del programma si fa a parte, non dentro un lancio autorizzato",
}

ESEMPI_VIETATI = [
    ["-u", "x"],
    ["-l", "x"],
    ["-t", "x.yaml"],
    ["-code"],
    ["-dast"],
    ["-etags", "x"],
    ["-im", "openapi"],
    ["-esc"],
    ["-ai", "x"],
    ["-rc", "x"],
    ["-turl", "x"],
]
ESEMPI_AMMESSI = [["-H", "X-A: b"], ["-timeout", "5"], ["-severity", "critical"]]

_ORDINE = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}


def voci(testo: str) -> list[Voce]:
    out = []
    for r in righe_json(testo):
        if not isinstance(r, dict):
            continue
        tpl = str(r.get("template-id", ""))
        dove = str(r.get("matched-at") or r.get("host") or "")
        sev = str(sotto_dict(r.get("info")).get("severity", "")).lower()
        if tpl:
            out.append(Voce(f"{tpl}@{dove}", f"[{sev or '?'}] {tpl} {dove}", sev))
    return sorted(out, key=lambda v: (_ORDINE.get(v.gruppo, 9), v.chiave))


# -- lingua -------------------------------------------------------------------
# Testi tradotti, generati da l10n/. L'italiano resta quello definito sopra.
_TR_TESTI: dict[str, dict[str, str]] = {
    "en": {
        "descrizione": "Template-based vulnerability scanning with a validated scope, dry-run by default and a hash-chained audit.",
        "nota_attivita": "nuclei sends requests built to recognize vulnerabilities: it is active. The profiles exclude the 'intrusive' and 'dos' tags and do not contact the interactsh server (-ni). Read the template before you trust it.",
        "installazione": "Kali/Debian: sudo apt install nuclei. Anywhere with Go: go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
        "gruppo": "Severity",
    },
    "zh": {
        "descrizione": "基于模板的漏洞扫描，带作用域校验、默认 dry-run 以及哈希链审计。",
        "nota_attivita": "nuclei 会发送为识别漏洞而构造的请求：属于主动行为。各配置排除了 'intrusive' 和 'dos' 标签，并且不联系 interactsh 服务器（-ni）。信任模板之前，请先阅读它。",
        "installazione": "Kali/Debian：sudo apt install nuclei。任何装了 Go 的环境：go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
        "gruppo": "严重性",
    },
}
_TR_PROFILI: dict[str, dict[str, list[str]]] = {
    "en": {
        "critici": ["Critical and high severity.", "The starting point: few alerts, all worth reviewing."],
        "cve": [
            "CVE templates, critical and high.",
            "After identifying the technologies: look for known vulnerabilities.",
        ],
        "esposizioni": ["CVEs, misconfigurations and exposures.", "Also covers exposed panels and forgotten files."],
        "esteso": ["Adds medium severity.", "When the client wants the full picture. More templates, more requests."],
        "prudente": ["With rate, concurrency and timeout limits.", "The default profile on client infrastructure."],
        "lento": ["Rate expressed per minute, few threads.", "For fragile services or ones with aggressive detection."],
    },
    "zh": {
        "critici": ["critical 和 high 级别。", "起点：报告数量少，但每条都值得查看。"],
        "cve": ["CVE 模板，critical 和 high。", "在识别出所用技术之后：查找已知漏洞。"],
        "esposizioni": ["CVE、错误配置和信息暴露。", "同时覆盖暴露的管理面板和被遗忘的文件。"],
        "esteso": ["增加 medium 级别。", "当客户想要完整的全貌时使用。模板更多，请求也更多。"],
        "prudente": ["带频率、并发和超时限制。", "在客户基础设施上默认使用的配置。"],
        "lento": ["频率以每分钟计，线程很少。", "用于脆弱的服务或具有激进检测机制的服务。"],
    },
}
_TR_VIETATI: dict[str, dict[str, str]] = {
    "en": {
        "abilita template che eseguono codice sulla tua macchina": "enables templates that run code on your machine",
        "i tag inclusi si scelgono con i profili": "the included tags are chosen via the profiles",
        "i target arrivano dal file validato contro lo scope": "targets come from the file validated against the scope",
        "i template autonomi portano con sé i loro target: fuori scope": "self-contained templates carry their own targets: out of scope",
        "i template si scelgono tramite i profili": "templates are chosen via the profiles",
        "i template si scelgono tramite i profili: un template non verificato può fare quello che vuole": "templates are chosen via the profiles: an unverified template can do whatever it wants",
        "il fuzzing DAST è attivo e intrusivo: usa nuclei direttamente, con un accordo esplicito": "DAST fuzzing is active and intrusive: use nuclei directly, with an explicit agreement",
        "interactsh è spento dai profili": "interactsh is disabled by the profiles",
        "invia i risultati a servizi esterni (GitHub, Jira, Slack...)": "sends results to external services (GitHub, Jira, Slack...)",
        "l'aggiornamento del programma si fa a parte, non dentro un lancio autorizzato": "updating the program is done separately, not inside an authorized run",
        "l'esclusione dei tag pericolosi è fissata dai profili": "excluding dangerous tags is fixed by the profiles",
        "l'output lo gestisce nuclei-cli": "output is handled by nuclei-cli",
        "manda a un servizio esterno la richiesta di generare un template": "sends a template-generation request to an external service",
        "riprende un lancio che non è passato dal controllo dello scope": "resumes a run that didn't go through the scope check",
        "una specifica importata può contenere host fuori scope": "an imported spec can contain out-of-scope hosts",
    },
    "zh": {
        "abilita template che eseguono codice sulla tua macchina": "启用会在你本机上执行代码的模板",
        "i tag inclusi si scelgono con i profili": "要包含的标签由配置选择",
        "i target arrivano dal file validato contro lo scope": "目标来自经过作用域校验的文件",
        "i template autonomi portano con sé i loro target: fuori scope": "自带目标的独立模板会带来它们自己的目标：超出作用域",
        "i template si scelgono tramite i profili": "模板通过配置选择",
        "i template si scelgono tramite i profili: un template non verificato può fare quello che vuole": "模板通过配置选择：未经验证的模板可以为所欲为",
        "il fuzzing DAST è attivo e intrusivo: usa nuclei direttamente, con un accordo esplicito": "DAST 模糊测试是主动且具有侵入性的：请在有明确授权的情况下直接使用 nuclei",
        "interactsh è spento dai profili": "interactsh 已由配置关闭",
        "invia i risultati a servizi esterni (GitHub, Jira, Slack...)": "会把结果发送到外部服务（GitHub、Jira、Slack……）",
        "l'aggiornamento del programma si fa a parte, non dentro un lancio autorizzato": "程序更新应单独进行，而不是在一次授权任务中进行",
        "l'esclusione dei tag pericolosi è fissata dai profili": "危险标签的排除由配置固定",
        "l'output lo gestisce nuclei-cli": "输出由 nuclei-cli 管理",
        "manda a un servizio esterno la richiesta di generare un template": "会把生成模板的请求发送给外部服务",
        "riprende un lancio che non è passato dal controllo dello scope": "会恢复一次未经过作用域检查的任务",
        "una specifica importata può contenere host fuori scope": "导入的规格文件可能包含作用域之外的主机",
    },
}
_ORIGINALI = (DESCRIZIONE, NOTA_ATTIVITA, INSTALLAZIONE, GRUPPO, PROFILI, VIETATI)


def applica_lingua(lingua: str) -> None:
    """Passa testi, profili e motivi dei flag vietati alla lingua scelta. Ripartendo
    sempre dagli originali italiani, chiamarla più volte non accumula niente."""
    global DESCRIZIONE, NOTA_ATTIVITA, INSTALLAZIONE, GRUPPO, PROFILI, VIETATI
    from dataclasses import replace

    DESCRIZIONE, NOTA_ATTIVITA, INSTALLAZIONE, GRUPPO, PROFILI, VIETATI = _ORIGINALI
    testi = _TR_TESTI.get(lingua)
    if not testi:
        return
    DESCRIZIONE = testi["descrizione"] or DESCRIZIONE
    NOTA_ATTIVITA = testi["nota_attivita"] or NOTA_ATTIVITA
    INSTALLAZIONE = testi["installazione"] or INSTALLAZIONE
    GRUPPO = testi["gruppo"] or GRUPPO
    prof = _TR_PROFILI.get(lingua, {})
    PROFILI = {
        n: replace(p, descrizione=prof[n][0] or p.descrizione, quando=prof[n][1] or p.quando) if n in prof else p
        for n, p in PROFILI.items()
    }
    viet = _TR_VIETATI.get(lingua, {})
    VIETATI = {k: viet.get(v, v) for k, v in VIETATI.items()}
