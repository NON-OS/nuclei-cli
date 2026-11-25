#!/usr/bin/env bash
# nuclei_workflow_v2.sh
# Riferimento operativo completo. Solo target autorizzati.
# Le note spiegano il perché e il quando, non solo il cosa.

TARGET="<HOST_O_URL>"
TARGETS_FILE="<FILE_CON_LISTA_TARGET>"
OUT="<PREFISSO_OUTPUT>"

# ---------------------------------------------------------------
# Aggiornamento e versione
# ---------------------------------------------------------------
nuclei -update-templates
nuclei -version

# ---------------------------------------------------------------
# Template non tuoi
# Un template è un dato che dice a nuclei cosa fare. Uno scaricato
# a caso può mandare qualunque richiesta e, con -code, eseguire
# comandi sulla tua macchina. Leggilo prima di usarlo, e tieni
# nuclei aggiornato: controlla le note di rilascio ufficiali.
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# Scansione base (solo per capire cosa fa)
# NON usare in produzione senza filtri. Lancia tutto il set,
# inclusi intrusive e dos. Su target reale è un modo per
# farsi bannare o far cadere un servizio.
# ---------------------------------------------------------------
nuclei -u "$TARGET"
nuclei -u "$TARGET" -jsonl -o "$OUT.jsonl"

# ---------------------------------------------------------------
# Filtri di sicurezza (OBBLIGATORI su produzione)
# I template intrusive e dos possono modificare dati o far
# crashare servizi. Su produzione si escludono sempre.
# ---------------------------------------------------------------

# Solo severità alta e critica.
nuclei -u "$TARGET" -severity critical,high -jsonl -o "$OUT.jsonl"

# Escludo intrusive e dos. Obbligatorio su target reale.
nuclei -u "$TARGET" -severity critical,high,medium -exclude-tags intrusive,dos -jsonl -o "$OUT.jsonl"

# Solo CVE note.
nuclei -u "$TARGET" -tags cve -severity critical,high -jsonl -o "$OUT.jsonl"

# -ni disabilita interactsh/OAST. Usalo quando la rete non
# permette callback in uscita, o quando vuoi evitare rumore
# verso oast.fun. Senza -ni, i template time-based e OOB
# generano callback verso l'esterno.
nuclei -u "$TARGET" -severity critical,high -ni -jsonl -o "$OUT.jsonl"

# ---------------------------------------------------------------
# Scan strategy: la parte che nessuno mette
#
# -ss controlla come Nuclei distribuisce il lavoro.
# Default = auto = template-spray.
#
# template-spray: un template su molti target. Meno carico
#   su un singolo target, più memoria (ogni template ha il
#   suo chunk di target in input).
# host-spray: tutti i template su un target, poi il successivo.
#   Più carico sul target, meno memoria.
#
# -c e -bs cambiano SIGNIFICATO in base a -ss:
#
# In template-spray (default):
#   -c  = quanti template in parallelo (globale)
#   -bs = quanti target in parallelo per ogni template
#   Regola pratica: -c < -bs. Esempio: -c 10 -bs 200.
#
# In host-spray:
#   -c  = quanti template in parallelo per ogni target
#   -bs = quanti target in parallelo (globale)
#   Regola pratica: -c > -bs. Esempio: -c 200 -bs 10.
#
# Se non specifichi -ss, sei in template-spray. Il tuning
# che segue assume template-spray.
# ---------------------------------------------------------------

# Forzo esplicitamente template-spray per chiarezza.
nuclei -l "$TARGETS_FILE" -ss template-spray -severity critical,high -exclude-tags intrusive,dos -jsonl -o "$OUT.jsonl"

# Forzo host-spray quando voglio concentrarmi su un target
# alla volta (utile per target singoli o pochi target).
nuclei -l "$TARGETS_FILE" -ss host-spray -severity critical,high -exclude-tags intrusive,dos -jsonl -o "$OUT.jsonl"

# ---------------------------------------------------------------
# Rate limiting e performance
# Ordine di tuning quando la scan è troppo aggressiva:
# 1. Abbassa -c (template in parallelo) PRIMA di -rl
# 2. Poi abbassa -bs (target in parallelo per template)
# 3. -rl è il cap globale: non supera mai quel numero di req/s
#
# -rl default 150 req/s. -rlm (req/min) è alternativo e
# mutuamente esclusivo con -rl.
# ---------------------------------------------------------------

# Conservativo per produzione.
nuclei -l "$TARGETS_FILE" -severity critical,high \
  -exclude-tags intrusive,dos \
  -rl 50 -c 20 -bs 20 -timeout 10 -retries 1 \
  -jsonl -o "$OUT.jsonl"

# Alternativa con -rlm per target molto delicati.
nuclei -l "$TARGETS_FILE" -severity critical,high \
  -exclude-tags intrusive,dos \
  -rlm 600 -c 10 -bs 10 -timeout 15 -retries 1 \
  -jsonl -o "$OUT.jsonl"

# ---------------------------------------------------------------
# Debug: quando i finding sono zero
# Prima cosa da fare: -stats per vedere se le richieste partono.
# Se stats mostra 0 richieste, il problema è template selection
# o rete, non il target.
# ---------------------------------------------------------------
nuclei -u "$TARGET" -severity critical,high -stats -jsonl -o "$OUT.jsonl"

# -mhe (max-host-error): default 30. Se un host rifiuta troppe
# connessioni, Nuclei lo salta. Se vedi "skipping host" e non
# sai perché, alza -mhe o rallenta.
nuclei -u "$TARGET" -severity critical,high -mhe 50 -stats -jsonl -o "$OUT.jsonl"

# ---------------------------------------------------------------
# -as (automatic-scan) e i suoi limiti
# -as fingerprinta le tech e lancia solo i template rilevanti.
# Ma se il fingerprinting fallisce, puoi ottenere zero finding
# anche su target vulnerabile. Verifica sempre che -as abbia
# mappato almeno una tecnologia, altrimenti passa a -tags o -t
# espliciti.
# ---------------------------------------------------------------
nuclei -u "$TARGET" -as -severity critical,high -exclude-tags intrusive,dos -stats -jsonl -o "$OUT.jsonl"

# Fallback quando -as non mappa nulla: tag espliciti.
nuclei -u "$TARGET" -tags cve,misconfig,exposure -severity critical,high -exclude-tags intrusive,dos -jsonl -o "$OUT.jsonl"

# ---------------------------------------------------------------
# Input da lista, OpenAPI, Burp
# ---------------------------------------------------------------
nuclei -l "$TARGETS_FILE" -severity critical,high -exclude-tags intrusive,dos -jsonl -o "$OUT.jsonl"
nuclei -l openapi.yaml -im openapi -severity critical,high -jsonl -o "$OUT.jsonl"
nuclei -l burp_export.xml -im burp -severity high,critical -jsonl -o "$OUT.jsonl"

# ---------------------------------------------------------------
# DAST (attivo e intrusivo: leggi i template prima, e concordalo con il cliente)
# -fa low è il default sicuro. -fa high manda molti più payload.
# -cs limita lo scope del fuzzing.
# ---------------------------------------------------------------
nuclei -u "$TARGET" -dast -fa low -severity high,critical -jsonl -o "$OUT.jsonl"
nuclei -u "$TARGET" -dast -fa low -cs '.*target\.com/api/.*' -jsonl -o "$OUT.jsonl"

# ---------------------------------------------------------------
# Autenticazione
# -H si applica a TUTTE le richieste, anche verso domini
# esterni (CDN, font, analytics). Se metti un Bearer token
# in -H, lo stai inviando anche a terze parti.
# Per ambienti multi-dominio, usa -sf con un file di secrets
# che limita l'header ai domini specifici.
# ---------------------------------------------------------------

# Header singolo (solo per target singolo, dove sai che non
# carica risorse da domini terzi).
nuclei -u "$TARGET" -H "Authorization: Bearer <TOKEN>" -severity critical,high -jsonl -o "$OUT.jsonl"

# Secrets file (raccomandato per scan multi-target).
nuclei -l "$TARGETS_FILE" -sf secrets.yaml -ps -severity critical,high -jsonl -o "$OUT.jsonl"

# ---------------------------------------------------------------
# Template custom
# ---------------------------------------------------------------
nuclei -u "$TARGET" -t custom-templates/ -severity critical,high -jsonl -o "$OUT.jsonl"
nuclei -validate -t custom-templates/mio-template.yaml

# ---------------------------------------------------------------
# Output
# ---------------------------------------------------------------
nuclei -l "$TARGETS_FILE" -severity critical,high -jsonl -o "$OUT.jsonl"
MARKDOWN_EXPORT_SORT_MODE=severity nuclei -u "$TARGET" -severity critical,high -markdown-export "$OUT.md"
nuclei -l "$TARGETS_FILE" -severity critical,high -silent -jsonl -o "$OUT.jsonl"

# ---------------------------------------------------------------
# Comando di produzione completo
# Severità alta/critica, esclusione intrusive/dos, no OAST,
# rate limitato, template-spray (default), stats per debug.
# ---------------------------------------------------------------
nuclei -l "$TARGETS_FILE" \
  -ss template-spray \
  -severity critical,high \
  -exclude-tags intrusive,dos \
  -ni \
  -rl 50 -c 20 -bs 20 -timeout 10 -retries 1 \
  -stats \
  -silent -jsonl -o "$OUT.jsonl"
