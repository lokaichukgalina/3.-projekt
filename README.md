# 3.-projekt
## Popis projektu
Tento projekt automaticky stahuje a zpracovává výsledky hlasování pro vybraný okres z webu [volby.cz](https://www.volby.cz).  
Skript stáhne seznam obcí, detailní výsledky hlasování a uloží je do CSV souboru.  

Knihovny, které jsou použity v kódu, jsou uložené v souboru `requirements.txt`. Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následující příkazy:

```bash
pip3 --version       # ověříme verzi manažeru
pip3 install -r requirements.txt  # nainstalujeme potřebné knihovny
```

## Spuštění skriptu
Spuštění souboru `main.py` vyžaduje dva povinné argumenty:

```bash
python main.py <odkaz-uzemniho-celku> <vysledny-soubor>
```

Následně se vám stáhnou výsledky jako CSV soubor.

### Ukázka projektu
Výsledky hlasování pro okres Liberec:  
- Argument 1: `https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=7&xnumnuts=5103`  
- Argument 2: `vysledky_liberec.csv`

Spuštění programu:

```bash
python main.py https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=7&xnumnuts=5103 vysledky_liberec.csv
```

Průběh stahování:

```
STAHUJI DATA Z VYBRANEHO URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=7&xnumnuts=5103
UKLADAM DO SOUBORU: vysledky_liberec.csv
UKONCUJI main
```

Částečný výstup CSV:

```
Kód obce,Název obce,Voliči v seznamu,Vydané obálky,Platné hlasy,Blok proti islam.-Obran.domova,CESTA ODPOVĚDNÉ SPOLEČNOSTI,Komunistická str.Čech a Moravy,Občanská demokratická aliance,Občanská demokratická strana,"ROZUMNÍ-stop migraci,diktát.EU",STAROSTOVÉ A NEZÁVISLÍ,Strana svobodných občanů,Strana zelených,Česká pirátská strana,Česká str.sociálně demokrat.,Řád národa - Vlastenecká unie
563901,Bílá,718,452,449,0,0,23,1,30,1,71,7,5,51,37,1
563919,Bílý Kostel nad Nisou,785,523,518,0,1,49,0,24,4,138,12,3,34,9,7
546631,Bílý Potok,571,273,272,1,0,15,0,19,0,28,0,7,27,21,1
563935,Bulovka,694,307,307,0,0,44,0,15,5,40,3,0,14,27,0
563943,Cetenov,90,59,59,0,0,3,0,6,0,10,0,0,4,2,0
545996,Černousy,255,122,121,0,0,15,0,8,1,15,0,2,3,5,0
```

## Postup tvorby projektu

### 1️⃣ Vytvoření virtuálního prostředí
1. Otevři **Visual Studio Code → File → Open Folder** (vyber složku projektu) → **Terminal → New Terminal**
2. Vytvoř virtuální prostředí:

```bash
python -m venv main
```

*(main je název složky, která se vytvoří)*

3. Aktivace prostředí (PowerShell):

```bash
.\main\Scripts\Activate.ps1
```

Po aktivaci se zobrazí název `(main)` v závorce.

### 2️⃣ Instalace požadovaných knihoven
```bash
pip install requests beautifulsoup4
```

Uložíme seznam balíčků do souboru `requirements.txt`:

```bash
pip freeze > requirements.txt
```

### 3️⃣ Struktura skriptu `main.py`
1. Import knihoven
2. Kontrola argumentů
3. Funkce pro:
   - načtení stránky,
   - čištění dat,
   - vytvoření seznamu s kódem, názvem obce a odkazy,
   - procházení detailu každé obce a získání detailů hlasování:

   - První tabulka → `Voliči_v_seznamu`, `Vydané_obálky`, `Platné_hlasy`  
   - Druhá tabulka → hlasy pro jednotlivé strany

4. Vytvoření kompletního seznamu s údaji o všech obcích
5. Uložení do CSV – pomocí `csv.DictWriter`
