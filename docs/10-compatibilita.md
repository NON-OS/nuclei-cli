# Compatibilità e prove

🌐 **Italiano** · [English](en/10-compatibilita.md) · [中文](zh/10-compatibilita.md)

Questa pagina dice cosa è stato verificato contro il programma vero e cosa no. Non è un elenco di promesse.

**Versione provata:** nuclei v3.11.1, binario ufficiale della release, macOS arm64.

## Cosa è stato verificato

1. **I flag dei profili esistono.** Ogni flag usato da un profilo è stato confrontato con l'output di `nuclei -h` della versione provata: nessuno sconosciuto.
2. **I flag vietati esistono.** Anche l'elenco dei vietati è stato confrontato con l'help vero, per non vietare nomi inventati e per cercare flag pericolosi che mancavano. Ne sono stati trovati e aggiunti.
3. **Il lancio vero funziona.** `nuclei-cli lancia ... --esegui` con il binario vero, e `rapporto` che legge il risultato.
4. **Stdin chiuso.** Alcuni tool leggono i target anche da stdin, e quelli non passano dallo scope. Il programma chiude stdin del processo figlio; c'è un test che lo dimostra con un eseguibile finto, e la prova con i binari veri è sotto.
5. **I formati dei risultati.** I parser leggono gli output veri, conservati in `tests/fixtures/` (vedi il README lì dentro).
6. **Il binario giusto.** `doctor` e `--esegui` controllano che l'eseguibile nel PATH sia davvero nuclei e non un programma omonimo. Provato con il binario vero (accettato) e con un finto (rifiutato, codice 5).
7. **Python e installazione.** Test passati con Python 3.11.18 e 3.13 su macOS e con 3.12.3 su Linux. Installazione pulita con `pip install .` in un venv nuovo, comando nel PATH compreso.
8. **I tipi.** `mypy --strict` non trova errori in `src/`. Non è una prova di correttezza, ma un controllo in più su cosa un parametro o un ritorno può davvero essere; è nella CI, quindi non si guasta senza che un test lo segnali.
9. **Quanto i test toccano davvero.** `coverage` misura la copertura: la CI fallisce sotto l'85%, la cifra reale è più alta. Un numero dichiarato senza averlo mai misurato non vuol dire niente.



## Cosa NON è stato verificato

Provato `prudente` con 3992 template ufficiali (scaricati il 22/11/2026) sul bersaglio locale: nessun risultato, come previsto per un semplice server. Un risultato positivo è stato letto da un template di prova eseguito direttamente, perché il wrapper vieta `-t`.

## Se usi un'altra versione

I formati di output e i flag cambiano tra una versione e l'altra. Se `nuclei-cli doctor` mostra una versione diversa, i test non lo sanno. Lancia `make check` e, soprattutto, un lancio di prova su un bersaglio tuo prima di fidarti. Se trovi un flag che aggira lo scope e non è tra i vietati, è una vulnerabilità: vedi [SECURITY.md](../SECURITY.md).
