# Återkoppling 1 – Mary Tecle (marte668)

Denna återkoppling avser inlämningen för **Mary Tecle** i kursen *Cybersäkerhet - grunder och medvetenhet* vid Linköpings universitet, baserat på filen [`Riskanalys-marte668.xlsx`](file:///Users/lfrykman/course-dir/z.(delete-after-cybersecurity-course-is-over/grade-these/Tecle%20Mary%20%28marte668%29%20-%202026-10-06%2009-49%20-%20Riskanalys-marte668.xlsx).

---

### 1. På vems inlämning ger du återkoppling? (ange liu-id med 8 tecken, små bokstäver)
```
marte668
```

---

### 2. I vilken utsträckning är risknivåerna rimligt formulerade i excelarket? (1 - inte alls, 5 - fullständigt)
**Betyg:** `3`

---

### 3. Är de beskrivna riskerna rimliga och tydliga? (1 - inte alls, 5 - fullständigt)
**Betyg:** `4`

---

### 4. I vilken utsträckning används begreppen rätt (tex konfidentialitet, sårbarhet, hot, risk etc)? (1 - inte alls, 5 - fullständigt)
**Betyg:** `4`

---

### 5. Motivera kortfattat dina svar på fråga 2-4.

#### Text för formulär (kopiera texten nedan):
> Sannolikhetsnivåerna är tydligt definierade i mätbara frekvensintervall per år (1–10, 0,5–1, 0,05–0,5, <0,05). Konsekvensnivåerna saknar däremot helt kvantifiering. Det finns inga belopp i kronor och inga tidsangivelser för driftavbrott i timmar eller dygn, utan endast kvalitativa beskrivningar som "mycket stor", "längre avbrott" och "begränsad". Detta gör konsekvensbedömningen svår att tillämpa konsekvent och objektivt.
> 
> De 11 beskrivna riskerna är realistiska, väl valda och täcker modellens komponenter väl. Riskscenarier och konsekvenser är tydliga. Orsaksbeskrivningarna är dock i flera fall i kortaste laget (t.ex. endast "Obehörig autentisering" eller "Felet skulle till exempel kunna bero på en bugg"), vilket inte specificerar den bakomliggande sårbarheten. Detta kompenseras dock av mycket välskrivna kommentarer med källhänvisningar till bl.a. ENISA, NIST och nationella säkerhetsrekommendationer.
> 
> Säkerhetsegenskaperna (CIA) används konsekvent och korrekt (på engelska: Confidentiality, Integrity, Availability). Förståelsen för begreppen hot, sårbarhet och konsekvens är god, även om orsakskolumnen ibland beskriver själva händelsen snarare än den sårbarhet som möjliggjorde den.

---

### Detaljerad granskningssammanfattning
* **Antal risker:** 11 st (Risk-001 till Risk-011).
* **Komponenter som täcks:** Databas, Systemadministratör, Fakturasystem, Kundhantering, Kontorsenhet, Molntjänst, Extern enhet.
* **Positivt:** Mycket ambitiösa motiveringar i kommentarskolumnen med explicita litteraturreferenser. Bra spridning över tillgångar och CIA-triaden.
* **Förbättringsområden:** Kvantifiera konsekvensnivåerna i kronor och timmar/dygn. Fördjupa orsaksbeskrivningarna så att den konkreta sårbarheten (t.ex. svagt lösenord, saknad indatavalidering) framgår direkt i registret.
