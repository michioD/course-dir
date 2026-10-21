# Sammanfattning av uppgift: Riskhantering

Denna fil dokumenterar de åtgärder som utfördes för att slutföra riskhanteringsuppgiften.

## Filer som genererades
1. `hotmodell-lucfr079.json` - Hotmodell för OWASP Threat Dragon.
2. `riskanalys-lucfr079.xlsx` - Riskverktyg med ifylld analys och bedömning.

## 1. Hotmodellering (Threat Dragon)
Utgick från grundmodellen (`kundregister.json`) och lade till 10 relevanta hot. Hoten fördelades över olika CIA-egenskaper och tillgångar:

1. **Molntjänst (Tillgänglighet):** En överbelastningsattack (DDoS) gör att systemet blir otillgängligt.
2. **Databas (Konfidentialitet):** Obehöriga kommer åt kund- och orderdata i databasen på grund av svaga åtkomstkontroller.
3. **Kundhantering (Riktighet):** En anställd ändrar av misstag eller medvetet fakturauppgifter innan de skickas.
4. **Databas (Riktighet):** Ransomware krypterar databasen vilket gör data obrukbar och kräver lösensumma.
5. **Systemadministratör (Konfidentialitet):** Admin-konto kapas via ett phishing-mejl på grund av avsaknad av MFA.
6. **Extern enhet (Riktighet):** En obehörig enhet utger sig för att vara en legitim mobil enhet och skickar in falska ordrar.
7. **Kontorsenhet (Konfidentialitet):** En stulen kontorsdator används för att komma åt affärssystemet.
8. **Kundhantering (Tillgänglighet):** En uppdatering av processen innehåller en bugg som kraschar systemet (dålig CI/CD).
9. **Databas (Tillgänglighet):** Hårdvarufel på databasservern gör att data inte kan nås (ingen RAID/redundans).
10. **Molntjänst (Riktighet):** Felkonfiguration exponerar interna API:er öppet.

## 2. Riskverktyget (Excel)
Följande flikar fylldes i och uppdaterades i `riskanalys-lucfr079.xlsx`:

### Studentdata
* **Namn:** Lucas Frykman
* **LiU-ID:** lucfr079

### Risknivåer
Nivåerna för sannolikhet och konsekvens definierades enligt följande:

**Konsekvensnivåer:**
* **4 (Allvarlig):** > 1 000 000 kr (Ekonomisk förlust), Mycket stort (Minskat förtroende), > 1 vecka (Avbrott), Lagbrott (Regelefterlevnad).
* **3 (Betydande):** > 100 000 kr, Stort, > 1 dag, Allvarlig avvikelse.
* **2 (Måttlig):** > 10 000 kr, Måttligt, > 1 timme, Mindre avvikelse.
* **1 (Försumbar):** < 10 000 kr, Litet/Inget, < 1 timme, Ingen avvikelse.

**Sannolikhetsnivåer:**
* **4 (Mycket hög):** > 1 gång per månad
* **3 (Hög):** 1 gång per år
* **2 (Medelhög):** 1 gång per 5 år
* **1 (Låg):** < 1 gång per 10 år

### Riskregister
Samtliga 10 hot överfördes till riskregistret med tydliga riskscenarier, orsaksbeskrivningar, och konsekvensbeskrivningar. Respektive Sannolikhets- och Konsekvensvärden (S och K) fylldes i för att automatiskt generera en total Risknivå.
