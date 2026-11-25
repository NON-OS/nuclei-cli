# Profili e flag vietati

🌐 **Italiano** · [English](en/04-profili.md) · [中文](zh/04-profili.md)

| Profilo | Cosa fa | Rumore | Root |
|---|---|---|---|
| `critici` | Severità critical e high. | medio | no |
| `cve` | Template CVE, critical e high. | medio | no |
| `esposizioni` | CVE, configurazioni errate ed esposizioni. | medio | no |
| `esteso` | Aggiunge la severità medium. | alto | no |
| `prudente` | Con limiti su frequenza, concorrenza e timeout. | medio | no |
| `lento` | Frequenza espressa al minuto, pochi thread. | basso | no |

`nuclei-cli profili` stampa i flag esatti di ciascuno.

## Cosa fa ciascun profilo

**critici** (`-severity critical,high -exclude-tags intrusive,dos -ni -jsonl`). Severità critical e high. Il punto di partenza: poche segnalazioni, tutte da guardare.

**cve** (`-tags cve -severity critical,high -exclude-tags intrusive,dos -ni -jsonl`). Template CVE, critical e high. Dopo aver identificato le tecnologie: cerca vulnerabilità note.

**esposizioni** (`-tags cve,misconfig,exposure -severity critical,high -exclude-tags intrusive,dos -ni -jsonl`). CVE, configurazioni errate ed esposizioni. Copre anche i pannelli esposti e i file dimenticati.

**esteso** (`-severity critical,high,medium -exclude-tags intrusive,dos -ni -jsonl`). Aggiunge la severità medium. Quando il cliente vuole il quadro completo. Più template, più richieste.

**prudente** (`-severity critical,high -exclude-tags intrusive,dos -ni -rl 50 -c 20 -bs 20 -timeout 10 -retries 1 -stats -silent -jsonl`). Con limiti su frequenza, concorrenza e timeout. Il profilo da usare di default su infrastrutture di clienti.

**lento** (`-severity critical,high -exclude-tags intrusive,dos -ni -rlm 600 -c 10 -bs 10 -timeout 15 -retries 1 -jsonl`). Frequenza espressa al minuto, pochi thread. Per servizi fragili o con rilevamento aggressivo.

## Passare flag a mano

Tutto ciò che scrivi dopo `--` finisce a nuclei, dopo i flag del profilo, a patto che non sia nell'elenco dei vietati. Il confronto non distingue maiuscole e minuscole e accetta sia `-flag valore` sia `-flag=valore`, con uno o due trattini.

```sh
nuclei-cli lancia prudente https://app.example.org --scope scope.toml -- -timeout 5
```

## Elenco dei vietati

| Flag | Perché |
|---|---|
| `-u`, `-target`, `-l`, `-list`, `-targets-inline` | i target arrivano dal file validato contro lo scope |
| `-o`, `-output` | l'output lo gestisce nuclei-cli |
| `-t`, `-templates`, `-template-url`, `-w`, `-workflows` | i template si scelgono tramite i profili: un template non verificato può fare quello che vuole |
| `-code` | abilita template che eseguono codice sulla tua macchina |
| `-dast` | il fuzzing DAST è attivo e intrusivo: usa nuclei direttamente, con un accordo esplicito |
| `-etags`, `-exclude-tags` | l'esclusione dei tag pericolosi è fissata dai profili |
| `-itags`, `-include-tags` | i tag inclusi si scelgono con i profili |
| `-im`, `-input-mode` | una specifica importata può contenere host fuori scope |
| `-resume` | riprende un lancio che non è passato dal controllo dello scope |
| `-turl`, `-wurl` | i template si scelgono tramite i profili |
| `-esc`, `-enable-self-contained` | i template autonomi portano con sé i loro target: fuori scope |
| `-ai`, `-prompt` | manda a un servizio esterno la richiesta di generare un template |
| `-rc`, `-report-config` | invia i risultati a servizi esterni (GitHub, Jira, Slack...) |
| `-iserver`, `-itoken` | interactsh è spento dai profili |
| `-up`, `-update` | l'aggiornamento del programma si fa a parte, non dentro un lancio autorizzato |

## Quello che il filtro non fa

Non è una sandbox. Se vuoi aggirarlo ci riesci, per esempio chiamando `nuclei` direttamente. Serve a fermare gli errori e le abitudini sbagliate, non un malintenzionato che ha già accesso al tuo terminale. Se ti serve un flag vietato per un'attività concordata con il cliente, usa nuclei direttamente e annota la scelta nell'ingaggio.
