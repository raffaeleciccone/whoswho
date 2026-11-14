"""Sorgente: LinkedIn. DA FARE dopo le risposte del prof (vedi SPEC.md sezione 7).

Due strade possibili:
- import del CSV dei collegamenti che LinkedIn fa scaricare
  (Impostazioni > Privacy dei dati > Ottieni una copia dei tuoi dati);
  contiene nome, cognome, URL profilo, azienda e ruolo attuali, ma niente foto né skill;
- scraping delle pagine profilo (vietato dai termini di LinkedIn, serve login).

In entrambi i casi questa funzione deve restituire persone nel formato di PIANO.md sezione 2.
"""


def leggi(*args, **kwargs) -> list[dict]:
    raise NotImplementedError("Sorgente LinkedIn da scrivere dopo le risposte del prof")
