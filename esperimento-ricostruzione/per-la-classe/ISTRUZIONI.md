# Rifare l'esperimento a lezione

Durata: circa 30 minuti (10-15 di lavoro dell'AI, il resto per il confronto e la discussione).

## Cosa serve
- Un PC con **Docker Desktop** acceso e **Claude Code**.
- Questa cartella `per-la-classe/`.

## Passi

1. **Prepara una cartella vuota** e copiaci dentro **solo** i file di `documenti/`:
   ```powershell
   New-Item -ItemType Directory C:\lezione\ricostruito
   Copy-Item documenti\*.md C:\lezione\ricostruito\
   ```
2. **Apri una sessione nuova** di Claude Code in `C:\lezione\ricostruito`
   (importante: nuova, così non sa niente del progetto).
3. **Incolla il prompt** di [prompt.md](prompt.md), con il percorso giusto.
4. **Mentre lavora**, fai leggere alla classe SPEC.md e chiedi: *"secondo voi dove dovrà indovinare?"*.
   Scrivete le ipotesi alla lavagna.
5. **Quando ha finito**, fai i controlli di [VERIFICA.md](VERIFICA.md).
6. **Leggete insieme il suo DUBBI.md** e confrontatelo con le ipotesi della lavagna
   e con [../DUBBI-del-claude-nuovo.md](../DUBBI-del-claude-nuovo.md) (il nostro risultato).
   Dividete i dubbi nei 4 tipi di [../RISULTATI.md](../RISULTATI.md):
   A buchi nella spec · B buchi nel piano · C errori · D libertà accettabili.

## Domande per la discussione
- Quali dubbi sono decisioni che doveva prendere l'utente e non l'AI? (tipo A)
- Il vostro Claude ha avuto gli stessi dubbi del nostro? Se no, perché secondo voi?
- In un progetto fatto a vibe coding, dove finiscono queste 36 decisioni?
- Cosa bisognerebbe scrivere nei documenti perché il file `dati-di-prova/esempio.json` entri al primo colpo?

## Variante: prima e dopo
Ripeti l'esperimento con i documenti **corretti** che stanno nella cartella principale del progetto
(`SPEC.md`, `PIANO.md`, ...) e confronta il numero di dubbi.
