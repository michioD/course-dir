# Återkoppling 1 – Diala Badra (diaba644)

Denna återkoppling avser inlämningen för **Diala Badra** i kursen *Cybersäkerhet - grunder och medvetenhet* vid Linköpings universitet, baserat på filen [`riskanalys-diaba644.xlsx`](file:///Users/lfrykman/course-dir/z.(delete-after-cybersecurity-course-is-over/grade-these/Badra%20Diala%20%28diaba644%29%20-%202026-10-09%2020-54%20-%20riskanalys-diaba644.xlsx).

---

### 1. På vems inlämning ger du återkoppling? (ange liu-id med 8 tecken, små bokstäver)
```
diaba644
```

---

### 2. I vilken utsträckning är risknivåerna rimligt formulerade i excelarket? (1 - inte alls, 5 - fullständigt)
**Betyg:** `3`

---

### 3. Är de beskrivna riskerna rimliga och tydliga? (1 - inte alls, 5 - fullständigt)
**Betyg:** `4`

---

### 4. I vilken utsträckning används begreppen rätt (tex konfidentialitet, sårbarhet, hot, risk etc)? (1 - inte alls, 5 - fullständigt)
**Betyg:** `3`

---

### 5. Motivera kortfattat dina svar på fråga 2-4.

#### Text för formulär (kopiera texten nedan):
> Sannolikhetsnivåerna är kvantifierade i antal gånger per år (>10, 5–10, 1–5, <1), vilket är mätbart även om >10 gånger per år är en mycket hög frekvens för ett litet företags incidenter. Konsekvensnivåerna har monetära belopp, men nivå 2 ("< 500 000 kr") är alldeles för bred och skapar överlapp. Dessutom saknas konkreta tidsramar för driftavbrott (t.ex. i timmar/dagar); formuleringar som "längre än verksamhet kan acceptera" är svåra att bedöma objektivt.
> 
> De 8 beskrivna riskerna uppfyller minimikravet och är relevanta för affärssystemets olika delar. Vissa bedömningar är dock överdrivna, exempelvis DDoS mot kundhanteringssystemet som satts till högsta sannolikhet (>10 ggr/år) och högsta konsekvens (>1 miljon kr), vilket inte är helt rimligt för ett internt system i ett mindre företag.
> 
> Strukturellt hålls hot, orsak och konsekvens isär väl, men kolumnen för säkerhetsegenskap blandar begrepp från både CIA och STRIDE på samma rad (t.ex. "Tampering, infomration disclouser" och "Avability, Denial of service"). Det förekommer också en hel del stavfel i begreppen som drar ner helhetsintrycket.

---

### Detaljerad granskningssammanfattning
* **Antal risker:** 8 st (Risk-001 till Risk-008).
* **Komponenter som täcks:** Databas, Kundhantering, Systemadministratör, Fakturasystem, Molntjänst, Extern tjänst (Skatteverket).
* **Positivt:** Relevanta hotscenarier som täcker både tekniska brister (behörigheter, validering) och mänskliga faktorer (nätfiske).
* **Förbättringsområden:** Sätt tydliga tidsgränser (timmar/dagar) för avbrott, specificera ekonomiska intervall utan överlapp, och använd konsekvent antingen CIA eller STRIDE utan stavfel.
