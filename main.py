import requests
from bs4 import BeautifulSoup
import csv
import sys

URL, CSV_FILE = sys.argv[1], sys.argv[2]
BASE = "https://www.volby.cz/pls/ps2017nss/"

def nacti_soup(URL):
    """Načte stránku a vrátí objekt BeautifulSoup."""
    try:
        r = requests.get(URL)
        r.raise_for_status()
        return BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print("Chyba při načítání:", URL, e)
        return None

def cisti_cislo_nebo_text(text):
    """Vyčistí číslo nebo vrátí text."""
    if not text or text.strip() == "":
        return ""
    cisty_text = text.replace("\xa0", "").replace(" ", "").replace(".", "")
    try:
        if "," in cisty_text:
            return float(cisty_text.replace(",", "."))
        else:
            return int(cisty_text)
    except ValueError:
        return cisty_text

def ziskej_obce_s_odkazy(URL, BASE):
    """Načte seznam obcí a vrátí list slovníků s odkazem na detail."""
    soup = nacti_soup(URL)
    if not soup:
        return []

    obce_list = []
    for tr in soup.select("tr"):
        kod_td = tr.select_one("td.cislo a")
        nazev_td = tr.select_one("td.overflow_name")
        if kod_td and nazev_td:
            kod = kod_td.text.strip()
            nazev = nazev_td.text.strip()
            href = kod_td.get("href", "").strip()
            obce_list.append({
                "Kód obce": kod,
                "Název obce": nazev,
                "odkaz": BASE + href if href else ""
            })
    return obce_list

def ziskej_detaily_obci_bez_odkazu(obce_list):
    """Načte detailní výsledky všech obcí (bez klíče 'odkaz')."""
    vysledky = []
    for obec in obce_list:
        url = obec.get("odkaz")
        if not url:
            continue
        soup = nacti_soup(url)
        if not soup:
            continue

        data = {k: v for k, v in obec.items() if k != "odkaz"}
        tabulky = soup.find_all("table", {"class": "table"})

        if len(tabulky) >= 2:
            tab1 = tabulky[0]
            rows = tab1.find_all("tr")
            if len(rows) >= 3:
                hodnoty = [cisti_cislo_nebo_text(td.text) for td in rows[2].find_all("td", class_="cislo")][-6:]
                if len(hodnoty) >= 5:
                    data["Voliči v seznamu"] = hodnoty[0]
                    data["Vydané obálky"] = hodnoty[1]
                    data["Platné hlasy"] = hodnoty[4]

            tab2 = tabulky[1]
            for tr in tab2.find_all("tr")[2:]:
                tds = tr.find_all("td")
                if len(tds) >= 3:
                    nazev_strany = tds[1].text.strip()
                    hlasy = cisti_cislo_nebo_text(tds[2].text)
                    data[nazev_strany] = hlasy

        vysledky.append(data)

    return vysledky

# ---- hlavní část skriptu ----
print("\nSTAHUJI DATA Z VYBRANEHO URL:", URL)
obce_list = ziskej_obce_s_odkazy(URL, BASE)
vysledky = ziskej_detaily_obci_bez_odkazu(obce_list)

print("UKLADAM DO SOUBORU:", CSV_FILE)

# pevné hlavičky na začátku
hlavicky_zacatek = ["Kód obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"]

# dynamicky doplníme názvy stran
strany = set()
for data in vysledky:
    for klic in data.keys():
        if klic not in hlavicky_zacatek:
            strany.add(klic)

hlavicky = hlavicky_zacatek + sorted(strany)

# zápis do CSV
with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=hlavicky)
    writer.writeheader()
    for data in vysledky:
        radek = {}
        for col in hlavicky:
            hodnota = data.get(col)
            if hodnota is None:
                radek[col] = "" if col in ["Kód obce", "Název obce"] else 0
            else:
                radek[col] = hodnota
        writer.writerow(radek)

print("UKONCUJI main\n")
