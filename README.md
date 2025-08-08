# julestest
Testing Jules features

Questo programma, scritto in Python, implementa il gioco UNO

# 🃏 Regole del Gioco di Carte UNO

## 🎯 Obiettivo del Gioco
Essere il primo giocatore a **eliminare tutte le proprie carte**. Quando ti rimane **una sola carta**, devi dire “UNO!” — altrimenti rischi una penalità.

---

## 👥 Numero di Giocatori
Da **2 a 10 giocatori**. Più si è, più il gioco diventa caotico e divertente!

---

## 🎴 Composizione del Mazzo
Il mazzo UNO contiene **108 carte** suddivise in:

### Carte Normali (colori: rosso, giallo, verde, blu)
- Numeri da **0 a 9** (ci sono due copie per ogni numero tranne lo 0)
- Carte Azione:
  - **Salta turno** (Skip): il giocatore successivo salta il turno
  - **Inverti** (Reverse): cambia il senso di gioco
  - **+2** (Pesca Due): il giocatore successivo pesca 2 carte e salta il turno

### Carte Speciali (senza colore)
- **Jolly** (Wild): puoi cambiare il colore in gioco
- **Jolly +4** (Wild Draw Four): cambia colore **e** il giocatore successivo pesca 4 carte e salta il turno  
  > ⚠️ Da usare solo se non hai carte del colore in gioco!

---

## ▶️ Come Si Gioca

1. **Distribuzione**: ogni giocatore riceve **7 carte**.
2. Si scopre la prima carta del mazzo per iniziare la pila degli scarti.
3. A turno, ogni giocatore deve:
   - Giocare una carta che **corrisponde per colore o numero** a quella in cima alla pila degli scarti.
   - Oppure giocare una **carta speciale** (se consentito).
   - Se non può giocare, deve **pescare una carta** dal mazzo. Se può giocarla, lo fa subito; altrimenti la tiene.
4. Quando un giocatore ha **una sola carta**, deve dire “UNO!”.
5. Il primo che finisce le carte **vince la partita**.

---

## ⚠️ Penalità

- Se dimentichi di dire “UNO” e vieni scoperto, devi **pescare 2 carte**.
- Se giochi un **Jolly +4** illegalmente (cioè hai carte del colore in gioco), e vieni sfidato, devi **pescare 4 carte** tu!

---

## 🧠 Varianti e Consigli

- Puoi aggiungere regole “casalinghe” come:
  - **Salto multiplo**
  - **Raddoppio delle penalità**
  - **Gioco a squadre**
- **Strategia**: conserva le carte +2 e +4 per momenti critici!

---

> ✨ Divertiti e che vinca il più astuto!
