# Dove provarlo in sicurezza

🌐 **Italiano** · [English](en/07-lab.md) · [中文](zh/07-lab.md)

Per imparare serve qualcosa da analizzare che sia tuo.

Con il lab Docker (`lab/`): `nuclei-cli lancia critici http://172.28.0.11 --scope examples/scope.lab.toml`. Le due applicazioni sono volutamente vulnerabili, quindi nuclei troverà qualcosa: è l'occasione per provare `rapporto` e `confronta` su risultati veri.

## Il lab Docker

In `lab/` c'è un `docker-compose.yml` che avvia due bersagli volutamente vulnerabili su una rete isolata.

```mermaid
flowchart LR
    subgraph H[il tuo computer]
        T[nuclei-cli]
        subgraph N[rete docker 172.28.0.0/24]
            J[juice-shop<br/>172.28.0.10:3000]
            D[dvwa<br/>172.28.0.11:80]
        end
    end
    T --> J
    T --> D
```

Le due applicazioni sono OWASP Juice Shop e DVWA, progetti pubblici fatti apposta per essere attaccati. Non esporle mai su una rete vera.

```sh
cd lab && docker compose up -d
```

Lo scope per il lab è in `examples/scope.lab.toml`. Le date vanno aggiornate: quelle d'esempio scadono.

## Esercizi

1. Lancia lo stesso profilo con un target in scope e uno fuori. Quale codice ottieni, e perché non parte nemmeno il primo?
2. Aggiungi un host a `esclude` e rilancia. Cosa cambia?
3. Cambia `valido_fino` con una data passata.
4. Apri `nuclei-cli.audit.jsonl`, cambia a mano una lettera in una riga a metà e lancia `nuclei-cli audit`.
5. Prova a passare un flag vietato dopo `--` e leggi il messaggio.
6. Fai due lanci e confrontali con `nuclei-cli confronta`.

## Pulizia

```sh
docker compose down
```

## Nota

Il compose file non è stato provato su ogni versione di Docker. Se il comando fallisce, controlla che le immagini esistano ancora sul registro e che la rete `172.28.0.0/24` non confligga con una già in uso.
