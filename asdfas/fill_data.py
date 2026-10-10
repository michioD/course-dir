import json
import uuid
from openpyxl import load_workbook

# 1. Update JSON
with open('kundregister.json', 'r', encoding='utf-8') as f:
    model = json.load(f)

threats_data = [
    {
        "asset": "Molntjänst",
        "cia": "Tillgänglighet",
        "scenario": "En överbelastningsattack (DDoS) mot molntjänsten gör att systemet blir otillgängligt.",
        "cause": "Otillräckligt DDoS-skydd och avsaknad av rate-limiting.",
        "conseq": "Kunder kan inte lägga ordrar och personal kan inte hantera kundärenden.",
        "S": 3,
        "K": 4
    },
    {
        "asset": "Databas",
        "cia": "Konfidentialitet",
        "scenario": "Obehöriga kommer åt kund- och orderdata i databasen.",
        "cause": "Svaga åtkomstkontroller (t.ex. standardlösenord) och okrypterad lagring.",
        "conseq": "Integritetsintrång för kunder och eventuellt vite enligt GDPR.",
        "S": 2,
        "K": 4
    },
    {
        "asset": "Kundhantering",
        "cia": "Riktighet",
        "scenario": "En anställd av misstag eller medvetet ändrar fakturauppgifter innan de skickas.",
        "cause": "Bristfällig loggning och avsaknad av granskning vid ändring av känsliga fält.",
        "conseq": "Felaktiga fakturor skickas, vilket leder till ekonomisk förlust och minskat förtroende.",
        "S": 3,
        "K": 3
    },
    {
        "asset": "Databas",
        "cia": "Riktighet",
        "scenario": "Ransomware krypterar databasen vilket gör data obrukbar och kräver lösensumma.",
        "cause": "Brist på offline-backuper och dåligt uppdaterat skydd mot skadlig kod.",
        "conseq": "Totalförlust av orderhistorik och kunddata för en tid framåt.",
        "S": 2,
        "K": 4
    },
    {
        "asset": "Systemadministratör",
        "cia": "Konfidentialitet",
        "scenario": "Admin-konto kapas via ett phishing-mejl.",
        "cause": "Avsaknad av multifaktorautentisering (MFA) för administrativa konton.",
        "conseq": "Full kontroll över systemet, vilket kan leda till storskalig datastöld.",
        "S": 3,
        "K": 4
    },
    {
        "asset": "Extern enhet",
        "cia": "Riktighet",
        "scenario": "En obehörig enhet utger sig för att vara en legitim mobil enhet och skickar in falska ordrar.",
        "cause": "Svag enhetsautentisering (t.ex. endast lösenord utan certifikat).",
        "conseq": "Felaktiga leveranser och kostnader för att hantera falska beställningar.",
        "S": 2,
        "K": 2
    },
    {
        "asset": "Kontorsenhet",
        "cia": "Konfidentialitet",
        "scenario": "En stulen kontorsdator används för att komma åt affärssystemet.",
        "cause": "Datorn saknar diskkryptering (t.ex. BitLocker) och har långa sessions-timeouts.",
        "conseq": "Risk för läckage av företagshemligheter och kunddata.",
        "S": 2,
        "K": 3
    },
    {
        "asset": "Kundhantering",
        "cia": "Tillgänglighet",
        "scenario": "En uppdatering av kundhanteringsprocessen innehåller en bugg som kraschar systemet.",
        "cause": "Bristande testning innan lansering (dålig CI/CD-pipeline).",
        "conseq": "Kortvarigt driftavbrott tills systemet rullas tillbaka.",
        "S": 3,
        "K": 2
    },
    {
        "asset": "Databas",
        "cia": "Tillgänglighet",
        "scenario": "Hårdvarufel på databasservern gör att data inte kan nås.",
        "cause": "Avsaknad av hårdvaruredundans (t.ex. RAID) och långsam återställningsprocess.",
        "conseq": "Verksamhetsavbrott och risk för dataförlust om backup ej är aktuell.",
        "S": 2,
        "K": 3
    },
    {
        "asset": "Molntjänst",
        "cia": "Riktighet",
        "scenario": "Felkonfiguration i molntjänsten exponerar interna API:er öppet.",
        "cause": "Manuella konfigurationsändringar utan granskning (Infrastructure as Code används ej).",
        "conseq": "Ökad risk för obehörig åtkomst eller manipulation av data.",
        "S": 2,
        "K": 3
    }
]

# Find cells in JSON and attach threats
cells = model.get('detail', {}).get('cells', [])
for t_data in threats_data:
    asset_name = t_data['asset']
    # Find matching cell
    target_cell = next((c for c in cells if c.get('data', {}).get('name') == asset_name), None)
    if target_cell:
        threat = {
            "id": str(uuid.uuid4()),
            "title": t_data['cia'] + " brist: " + t_data['scenario'][:20] + "...",
            "status": "Open",
            "severity": "High" if t_data['K'] >= 3 else "Medium",
            "type": t_data['cia'],
            "description": t_data['scenario'] + "\nOrsak: " + t_data['cause'],
            "mitigation": "Åtgärder behövs."
        }
        if 'threats' not in target_cell['data']:
            target_cell['data']['threats'] = []
        target_cell['data']['threats'].append(threat)

with open('hotmodell-lucfr079.json', 'w', encoding='utf-8') as f:
    json.dump(model, f, indent=2, ensure_ascii=False)

# 2. Update Excel
wb = load_workbook('verktyg-analys-risk.xlsx')

# Studentdata
ws_stud = wb['Studentdata']
ws_stud['B3'] = 'Student'
ws_stud['C3'] = 'lucfr079'

# Risknivåer
ws_risk = wb['Risknivåer']
# Konsekvens (4, 3, 2, 1) -> rows 7, 8, 9, 10
ws_risk['C7'] = '> 1 000 000 kr'
ws_risk['E7'] = 'Mycket stort'
ws_risk['G7'] = '> 1 vecka'
ws_risk['I7'] = 'Lagbrott'

ws_risk['C8'] = '> 100 000 kr'
ws_risk['E8'] = 'Stort'
ws_risk['G8'] = '> 1 dag'
ws_risk['I8'] = 'Allvarlig avvikelse'

ws_risk['C9'] = '> 10 000 kr'
ws_risk['E9'] = 'Måttligt'
ws_risk['G9'] = '> 1 timme'
ws_risk['I9'] = 'Mindre avvikelse'

ws_risk['C10'] = '< 10 000 kr'
ws_risk['E10'] = 'Litet/Inget'
ws_risk['G10'] = '< 1 timme'
ws_risk['I10'] = 'Ingen avvikelse'

# Sannolikhet -> rows 14, 15, 16, 17
ws_risk['C14'] = '> 1 gång per månad'
ws_risk['C15'] = '1 gång per år'
ws_risk['C16'] = '1 gång per 5 år'
ws_risk['C17'] = '< 1 gång per 10 år'

# Riskregister
ws_reg = wb['Riskregister']
for i, t_data in enumerate(threats_data):
    row = i + 6
    ws_reg[f'B{row}'] = t_data['asset']
    ws_reg[f'C{row}'] = t_data['cia']
    ws_reg[f'D{row}'] = t_data['scenario']
    ws_reg[f'E{row}'] = t_data['cause']
    ws_reg[f'F{row}'] = t_data['conseq']
    ws_reg[f'G{row}'] = t_data['S']
    ws_reg[f'I{row}'] = t_data['K']

wb.save('riskanalys-lucfr079.xlsx')
print("Done")
