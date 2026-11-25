# nuclei-cli

🌐 **Italiano** · [English](README.en.md) · [中文](README.zh.md)

[![ci](https://github.com/NON-OS/nuclei-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/NON-OS/nuclei-cli/actions/workflows/ci.yml)
![License MIT](https://img.shields.io/badge/License-MIT-yellow)
![python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![Kali · Parrot · Linux](https://img.shields.io/badge/Kali%20%C2%B7%20Parrot%20%C2%B7%20Linux-primario-1793d1)
![nuclei](https://img.shields.io/badge/wrapper%20di-nuclei-green)
![dipendenze 0](https://img.shields.io/badge/dipendenze-0-lightgrey)

```
  ┌─ scope ─┐   ┌─ dry-run ─┐   ┌─ conferma ─┐   ┌─ nuclei ─┐   ┌─ audit ─┐   ┌─ rapporto ─┐
  │ valida  │ → │ mostra    │ → │ riferimento│ → │ parte   │ → │ catena  │ → │ riepilogo  │
  └─────────┘   └───────────┘   └────────────┘   └─────────┘   └─────────┘   └────────────┘
```

Scansione di vulnerabilità con template, scope validato, dry-run di default e audit a catena di hash. Solo target autorizzati.

> **Solo sistemi tuoi o con autorizzazione scritta.** Leggi [DISCLAIMER.md](DISCLAIMER.md) prima di lanciare qualsiasi cosa.

## Cos'è

`nuclei-cli` è un orchestratore sottile attorno a nuclei di ProjectDiscovery. Non lo sostituisce. Controlla che ogni target sia nello scope, esclude di default i template intrusivi, blocca i flag che farebbero eseguire codice non verificato, e registra ogni lancio.

Nuclei è potente perché i template sono dati, e per lo stesso motivo è rischioso: un template scaricato da internet può contenere qualsiasi richiesta, e con `-code` può eseguire comandi sulla tua macchina. Qui `-t`, `-w`, `-tu` e `-code` sono vietati: i template li sceglie il profilo, e i tag `intrusive` e `dos` restano esclusi. Viene disattivato anche interactsh (`-ni`), che altrimenti contatterebbe un server di terzi con dati del test.

## In azione

![nuclei-cli in modalità guidata su Kali Linux](docs/img/guida-kali.png)

*Modalità guidata (`nuclei-cli guida`) eseguita su Kali Linux: logo, scelta del profilo, validazione dello scope, anteprima del comando. Screenshot reale.*

```console
$ nuclei-cli lancia prudente https://app.example.org --scope scope.toml
Ingaggio : ACME-2026 (ACME-2026-014)
Profilo  : prudente - Con limiti su frequenza, concorrenza e timeout. [rumore medio]
  ok  https://app.example.org  (host app.example.org: combacia con app.example.org)
Comando  : nuclei -severity critical,high -exclude-tags intrusive,dos -ni -rl 50 -c 20 -bs 20 -timeout 10 -retries 1 -stats -silent -jsonl -l out/esempio/target.txt -o out/esempio/risultati.jsonl
Attività: nuclei invia richieste costruite per riconoscere vulnerabilità: è attivo. I profili escludono i tag 'intrusive' e 'dos' e non contattano il server interactsh (-ni). Leggi il template prima di fidarti.

Dry-run: non ho lanciato niente. Aggiungi --esegui per partire davvero.
```

Con un target fuori scope, anche in mezzo a target validi, non parte niente:

```console
$ nuclei-cli lancia prudente https://app.example.org https://evil.example --scope scope.toml
nuclei-cli: target fuori scope, non eseguo nulla:
  https://evil.example: host evil.example: hostname non presente tra gli inclusi
$ echo $?
3
```

Il comando `lancia` non parte mai senza `--esegui`. Quello che vedi sopra è un'anteprima.

L'output parla la lingua che scegli: `--lang it|en|zh` oppure la variabile `NONOS_LANG` (comoda per impostarla a livello di sistema). Si parte sempre in italiano. Il README è anche in [English](README.en.md) e [中文](README.zh.md).

## Cosa fa

| | |
|---|---|
| Scope | Dominio, host o URL (modalità `url`), con esclusioni e date di validità. Nel dubbio rifiuta. |
| Dry-run | Di default non parte niente. `--esegui` chiede conferma. |
| Profili | 6, con indicazione di rumore e di quando usarli. |
| Filtro flag | I flag che aggirano lo scope o rubano il controllo dell'output sono bloccati. |
| Filtro liste | `filtra` legge una lista da stdin e lascia passare solo ciò che è nello scope. |
| Scope firmato | Il cliente firma lo scope con la sua chiave SSH. Se il file cambia dopo la firma, non parte niente. |
| Audit | Registro a catena di hash. Hash dello scope e firmatario inclusi, valori sensibili oscurati. |
| Rapporto | Riepilogo dei risultati in testo, Markdown o JSON. |
| Confronto | Cosa è cambiato tra due lanci, con codice di uscita per la CI. |
| Dipendenze | Nessuna: solo la libreria standard di Python. |

## Piattaforma

Pensato per **Kali**, **Parrot** e Linux in generale: è lì che questi strumenti vivono e dove `nuclei-cli` viene usato. Gira anche su macOS. Windows non è provato, e lì alcuni controlli sui privilegi (`os.geteuid`) non valgono.

## Installazione

Serve Python 3.11 o più recente e nuclei nel `PATH`. Kali/Debian: sudo apt install nuclei. Ovunque con Go: go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

```sh
git clone git@github.com:NON-OS/nuclei-cli.git
cd nuclei-cli
python3 -m venv .venv && . .venv/bin/activate
pip install -e .
nuclei-cli doctor
```

## Primo uso

### Il modo più semplice: modalità guidata

`nuclei-cli guida` ti fa le domande una alla volta — scope, profilo, target — mostra l'anteprima del comando e non lancia niente senza la tua conferma finale. È il modo consigliato per iniziare:

```sh
nuclei-cli guida
```

### Oppure a comandi

```sh
nuclei-cli init scope.toml          # crea il modello
$EDITOR scope.toml               # compilalo con il cliente
nuclei-cli verifica https://app.example.org --scope scope.toml
nuclei-cli lancia prudente https://app.example.org --scope scope.toml            # dry-run
nuclei-cli lancia prudente https://app.example.org --scope scope.toml --esegui   # parte davvero
```

In un terminale `--esegui` ti chiede di scrivere il riferimento dell'ingaggio. In uno script usa `--conferma`. Altri flag di nuclei si passano dopo `--`, se non sono tra i vietati ([docs/04-profili.md](docs/04-profili.md)).

Un flusso completo:

```sh
httpx-cli lancia vivi https://app.example.org --scope scope.toml --esegui
nuclei-cli lancia prudente https://app.example.org --scope scope.toml --esegui
nuclei-cli rapporto out/*-prudente/ --formato markdown > vulnerabilita.md
```

## Comandi

| Comando | Cosa fa |
|---|---|
| `guida` | modalità interattiva passo per passo: scope → profilo → target → conferma |
| `lancia <profilo> <target...>` | valida e costruisce (o lancia) nuclei. Con `-` legge i target da stdin |
| `filtra` | legge target da stdin e stampa solo quelli nello scope |
| `verifica <target...>` | dice se i target sono nello scope, senza lanciare |
| `scope-firma <file>` / `scope-verifica <file>` | firma e controlla lo scope con una chiave SSH |
| `rapporto <file_o_cartella>` | riepilogo dei risultati: vulnerabilità trovate |
| `confronta <vecchio> <nuovo>` | differenze tra due lanci |
| `profili` | elenca i profili con i flag esatti |
| `audit [file]` | verifica la catena del registro |
| `init [file]` | crea un file di scope da compilare |
| `doctor` | controlla nuclei, versione, privilegi |

## Profili

| Profilo | Cosa fa | Rumore | Root |
|---|---|---|---|
| `critici` | Severità critical e high. | medio | no |
| `cve` | Template CVE, critical e high. | medio | no |
| `esposizioni` | CVE, configurazioni errate ed esposizioni. | medio | no |
| `esteso` | Aggiunge la severità medium. | alto | no |
| `prudente` | Con limiti su frequenza, concorrenza e timeout. | medio | no |
| `lento` | Frequenza espressa al minuto, pochi thread. | basso | no |

![nuclei-cli doctor e profili su Kali Linux](docs/img/info-kali.png)

*`nuclei-cli doctor` (trova il binario reale di nuclei in `/usr/bin/`) e l'elenco dei profili, su Kali Linux.*

## Codici di uscita

| Codice | Significato |
|---|---|
| 0 | tutto a posto |
| 1 | `confronta --exit-code` ha trovato differenze |
| 2 | argomenti sbagliati o flag vietato |
| 3 | almeno un target fuori scope |
| 4 | scope illeggibile, malformato o scaduto |
| 5 | nuclei assente |
| 6 | esecuzione senza conferma, o profilo che richiede root senza sudo |
| 7 | nuclei è uscito con errore, o la catena di audit è spezzata |

## La catena di strumenti

Questo repository è uno di otto, pensati per lavorare insieme. Ognuno controlla lo scope per conto suo.

```mermaid
flowchart LR
    subfinder[subfinder-cli]
    dnsx[dnsx-cli]
    subfinder --> dnsx
    naabu[naabu-cli]
    dnsx --> naabu
    httpx[httpx-cli]
    naabu --> httpx
    katana[katana-cli]
    httpx --> katana
    ffuf[ffuf-cli]
    katana --> ffuf
    nuclei[nuclei-cli]
    ffuf --> nuclei
    style nuclei stroke-width:3px
```

- [subfinder-cli](https://github.com/NON-OS/subfinder-cli): enumerazione di sottodomini
- [dnsx-cli](https://github.com/NON-OS/dnsx-cli): risoluzione dns
- [naabu-cli](https://github.com/NON-OS/naabu-cli): scansione di porte
- [httpx-cli](https://github.com/NON-OS/httpx-cli): sonde http
- [katana-cli](https://github.com/NON-OS/katana-cli): crawling web
- [ffuf-cli](https://github.com/NON-OS/ffuf-cli): fuzzing di percorsi
- [nmap-cli](https://github.com/NON-OS/nmap-cli): scansione di porte e servizi con nmap

## Documentazione

1. [Introduzione e filosofia](docs/01-introduzione.md)
2. [Autorizzazione: cosa serve prima di toccare un target](docs/02-autorizzazione.md)
3. [Il file di scope](docs/03-scope.md)
4. [Profili e flag vietati](docs/04-profili.md)
5. [Il registro di audit](docs/05-audit.md)
6. [Architettura](docs/06-architettura.md)
7. [Dove provarlo in sicurezza](docs/07-lab.md)
8. [Rapporti e confronti](docs/08-rapporti.md)
9. [Scope firmato](docs/09-firma.md)
10. [Compatibilità e prove](docs/10-compatibilita.md)

Il cheatsheet shell da cui è nato il progetto è in [scripts/](scripts/).

## Cosa non fa

Non scopre se hai il permesso: lo dichiari tu nel file di scope, e il programma ti crede. Non protegge da chi lancia `nuclei` direttamente. Il filtro sui flag è una rete di sicurezza contro gli errori, non una sandbox. I dettagli sono in [docs/06-architettura.md](docs/06-architettura.md).

## Sviluppo

```sh
make check     # ruff (lint + format), mypy --strict, test e coverage
```

Nessuna dipendenza a runtime (solo la libreria standard). Gli strumenti di sviluppo si installano con `pip install -e ".[dev]"`. Vedi [CONTRIBUTING.md](CONTRIBUTING.md) e [SECURITY.md](SECURITY.md).

## Licenza

MIT, vedi [LICENSE](LICENSE). La licenza copre il codice, non autorizza nessuna attività.
