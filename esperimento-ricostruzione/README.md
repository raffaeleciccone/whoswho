# Esperimento: un Claude nuovo può ricostruire il progetto dalla sola documentazione?

## L'idea

Nello spec coding la verità sta nei documenti (SPEC.md, PIANO.md), non nel codice e non nella chat.
Se è vero, un'AI che non ha mai visto il progetto dovrebbe poterlo ricostruire leggendo solo i documenti,
senza fare domande a nessuno.

Il 14/11/2026 l'abbiamo provato:
1. abbiamo copiato **solo i 5 file .md** del progetto in una cartella vuota (nessuna riga di codice);
2. abbiamo dato a un Claude nuovo, senza memoria della conversazione in cui è nato il progetto,
   il compito di ricostruirlo, con una regola: **ogni volta che deve indovinare, lo scrive in DUBBI.md**;
3. abbiamo controllato la sua versione con i nostri dati e con i criteri della spec.

## Perché è utile

Ogni voce di DUBBI.md è qualcosa che noi davamo per scontato ma non avevamo scritto.
L'esperimento non serve a vedere se l'AI è brava: serve a **misurare quanto è completa la documentazione**.

## Cosa trovi qui

| File | Contenuto |
|---|---|
| [RISULTATI.md](RISULTATI.md) | prova 1: com'è andata, cosa abbiamo imparato e corretto |
| [DUBBI-del-claude-nuovo.md](DUBBI-del-claude-nuovo.md) | prova 1: i 36 punti in cui il Claude nuovo ha dovuto indovinare |
| [prova-2/](prova-2/) | la stessa prova rifatta con i documenti corretti: risultati e confronto con la prova 1 |
| [prova-3/](prova-3/) | la prova rifatta dopo la grafica (nginx, bozza, misura C34): risultati e confronto con le prove 1 e 2 |
| [per-la-classe/](per-la-classe/) | traccia della lezione per chi la guida, e i documenti della prova 1 per il "prima e dopo" |
| [../kit-ricostruzione/](../kit-ricostruzione/) | **il kit per gli studenti**: una cartella sola con documenti, prompt, verifica e misura; funziona con Claude Code, Antigravity e altri |
