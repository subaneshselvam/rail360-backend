from fastapi import FastAPI
import requests
import os
from datetime import datetime

app = FastAPI(
    title="Rail 360 Backend",
    description="Real-time train status + weather API",
    version="1.0.0",
)

# ------------------------
# CONFIG – API KEYS
# ------------------------

# 1) OpenWeatherMap – direct (FREE)
# For local testing – hard-code your key
OPENWEATHER_API_KEY = "e91c6fd924313ba0b6905b5d69b8a68f"

# 2) IRCTC RapidAPI – Indian Railway IRCTC
RAPID_RAIL_KEY = os.getenv(
    "RAPID_RAIL_KEY",
    "a06373a2f1msh54eabd13036fcb8p172ba3jsne82a30f201bf"
)
RAPID_RAIL_HOST = "indian-railway-irctc.p.rapidapi.com"

# Exact URL from your RapidAPI snippet
IRCTC_URL = "https://indian-railway-irctc.p.rapidapi.com/api/trains/v1/train/status"

# ------------------------
# STATION → CITY MAP (for weather)
# ------------------------

STATION_TO_CITY = {
    "NDLS": "New Delhi",
    "HWH": "Howrah",
    "BCT": "Mumbai",
    "CSMT": "Mumbai",
    "MAS": "Chennai",
    "SBC": "Bengaluru",
    "HYB": "Hyderabad",
    "SC": "Secunderabad",
    "SDAH": "Sealdah",
    "ADI": "Ahmedabad",
    "PUNE": "Pune",
    "PNBE": "Patna",
    "CNB": "Kanpur",
    "PRYJ": "Prayagraj",
    "JP": "Jaipur",
    "LKO": "Lucknow",
    "GKP": "Gorakhpur",
    "BSB": "Varanasi",
    "GHY": "Guwahati",
    "CDG": "Chandigarh",
    "BPL": "Bhopal",
    "GWL": "Gwalior",
    "JBP": "Jabalpur",
    "CBE": "Coimbatore",
    "TVC": "Thiruvananthapuram",
    "ERS": "Ernakulam",
    "MDU": "Madurai",
    "TPJ": "Tiruchirappalli",
    "VSKP": "Visakhapatnam",
    "BZA": "Vijayawada",
    "BBS": "Bhubaneswar",
    "CTC": "Cuttack",
    "R": "Raipur",
    "BSP": "Bilaspur",
    "NGP": "Nagpur",
    "ASR": "Amritsar",
    "LDH": "Ludhiana",
    "JUC": "Jalandhar City",
    "JAT": "Jammu Tawi",
    "UDZ": "Udaipur",
    "AII": "Ajmer",
    "JU": "Jodhpur",
    "KOTA": "Kota",
    "ST": "Surat",
    "BRC": "Vadodara",
    "RJT": "Rajkot",
    "BVC": "Bhavnagar",
    "MAO": "Madgaon",
    "MAJN": "Mangaluru",
    "UBL": "Hubballi",
    "MYS": "Mysuru",
    "SA": "Salem",
    "ED": "Erode",
    "NLR": "Nellore",
    "TPTY": "Tirupati",
    "GNT": "Guntur",
    "WL": "Warangal",
    "KZJ": "Kazipet",
    "REWA": "Rewa",
    "ET": "Itarsi",
    "RTM": "Ratlam",
    "JHS": "Jhansi",
    "AGC": "Agra",
    "MTJ": "Mathura",
    "ALJN": "Aligarh",
    "MTC": "Meerut City",
    "FD": "Faizabad",
    "AY": "Ayodhya Dham",
    "BE": "Bareilly",
    "MB": "Moradabad",
    "DDN": "Dehradun",
    "HW": "Haridwar",
    "KGM": "Kathgodam",
    "RKSH": "Rishikesh",
    "TATA": "Tatanagar",
    "ASN": "Asansol",
    "DHN": "Dhanbad",
    "RNC": "Ranchi",
    "HTE": "Hatia",
    "GAYA": "Gaya",
    "BGP": "Bhagalpur",
    "MFP": "Muzaffarpur",
    "DBG": "Darbhanga",
    "SV": "Siwan",
    "SPJ": "Samastipur",
    "BJU": "Barauni",
    "BXR": "Buxar",
    "ARA": "Arrah",
    "DURG": "Durg",
    "UMB": "Ambala",
    "ROK": "Rohtak",
    "HSR": "Hisar",
    "RE": "Rewari",
    "DEE": "Delhi Sarai Rohilla",
    "ANVT": "Anand Vihar",
    "BDTS": "Bandra",
    "LTT": "Lokmanya Tilak",
    "DR": "Dadar",
    "CCG": "Churchgate",
    "VSH": "Vashi",
    "PNVL": "Panvel",
    "VR": "Virar",
    "BSR": "Vasai",
    "NK": "Nashik",
    "BSL": "Bhusaval",
    "JL": "Jalgaon",
    "AK": "Akola",
    "AMI": "Amravati",
    "WR": "Wardha",
    "CD": "Chandrapur",
    "BPQ": "Ballarshah",
    "G": "Gondia",
    "DGR": "Durgapur",
    "MLDT": "Malda Town",
    "NJP": "New Jalpaiguri",
    "SGUJ": "Siliguri",
    "APDJ": "Alipurduar",
    "KNE": "Kishanganj",
    "KIR": "Katihar",
    "PRNA": "Purnia",
    "SHC": "Saharsa",
    "FBG": "Forbesganj",
    "SMI": "Sitamarhi",
    "BTH": "Bettiah",
    "MTR": "Motihari",
    "GD": "Gonda",
    "BST": "Basti",
    "BRK": "Bahraich",
    "BLP": "Balrampur",
    "SVSI": "Shravasti",
    "SPN": "Shahjahanpur",
    "LMP": "Lakhimpur",
    "PBE": "Pilibhit",
    "FBD": "Farrukhabad",
    "ETW": "Etawah",
    "FZD": "Firozabad",
    "MNQ": "Mainpuri",
    "KJN": "Kannauj",
    "BNDA": "Banda",
    "MBA": "Mahoba",
    "CKTD": "Chitrakoot",
    "LAR": "Lalitpur",
    "SGO": "Sagar",
    "DMO": "Damoh",
    "KTE": "Katni",
    "STA": "Satna",
    "SDL": "Shahdol",
    "APR": "Anuppur",
    "UMR": "Umaria",
    "BZU": "Betul",
    "SEY": "Seoni",
    "BTC": "Balaghat",
    "KRBA": "Korba",
    "RIG": "Raigarh",
    "CPH": "Champa",
    "JSG": "Jharsuguda",
    "SBP": "Sambalpur",
    "ROU": "Rourkela",
    "ANGL": "Angul",
    "TLHR": "Talcher",
    "BLS": "Balasore",
    "BHC": "Bhadrak",
    "JJKR": "Jajpur Keonjhar",
    "DNKL": "Dhenkanal",
    "VZM": "Vizianagaram",
    "CHE": "Srikakulam",
    "RJY": "Rajahmundry",
    "EE": "Eluru",
    "CCT": "Kakinada Town",
    "COA": "Kakinada Port",
    "OGL": "Ongole",
    "CLX": "Chirala",
    "TEL": "Tenali",
    "NLDA": "Nalgonda",
    "NED": "Nanded",
    "LUR": "Latur",
    "LTRR": "Latur",
    "PBN": "Parbhani",
    "BUU": "Buldhana",
    "J": "Jalna",
    "AWB": "Aurangabad",
    "SUR": "Solapur",
    "MRJ": "Miraj",
    "KOP": "Kolhapur",
    "KRD": "Karad",
    "STR": "Satara",
    "RN": "Ratnagiri",
    "KUDL": "Kudal",
    "SWV": "Sawantwadi",
    "BGM": "Belgavi",
    "BGK": "Bagalkot",
    "GDG": "Gadag",
    "BAY": "Bellary",
    "HPT": "Hosapete",
    "RC": "Raichur",
    "KLBG": "Kalaburagi",
    "BDR": "Bidar",
    "TEN": "Tirunelveli",
    "NCJ": "Nagercoil",
    "CAPE": "Kanyakumari",
    "PGT": "Palakkad",
    "CAN": "Kannur",
    "CLT": "Kozhikode",
    "KGQ": "Kasaragod",
    "QLN": "Kollam",
    "ALLP": "Alappuzha",
    "KTYM": "Kottayam",
    "TCR": "Thrissur",
    "CKI": "Chalakkudy",
    "AFK": "Angamaly",
    "HSRA": "Hosur",
    "DPJ": "Dharmapuri",
    "KPD": "Katpadi",
    "AJJ": "Arakkonam",
    "CGL": "Chengalpattu",
    "TBM": "Tambaram",
    "VM": "Villupuram",
    "VRI": "Virudhachalam",
    "TNM": "Tiruvannamalai",
    "CUPJ": "Cuddalore Port",
    "NGT": "Nagapattinam",
    "KIK": "Karaikal",
    "MV": "Mayiladuthurai",
    "KMU": "Kumbakonam",
    "MQ": "Mannargudi",
    "TJ": "Thanjavur",
    "PDKT": "Pudukkottai",
    "SVGA": "Sivaganga",
    "RMD": "Ramanathapuram",
    "RMM": "Rameswaram",
    "DG": "Dindigul",
    "PLNI": "Palani",
    "POY": "Pollachi",
    "TUP": "Tiruppur",
    "KRR": "Karur",
    "NMKL": "Namakkal",
    "KGI": "Krishnagiri",
    "SVPR": "Srivilliputhur",
    "VPT": "Virudhunagar",
    "SRT": "Sattur",
    "TN": "Tuticorin",
    "APK": "Aruppukkottai",
    "SVKS": "Sivakasi",
    "TCN": "Tiruchendur",
    "CVP": "Kovilpatti",
    "KZY": "Kayalpattinam",
    "AB": "Ambur",
    "GYM": "Gudiyatham",
    "NVL": "Neyveli",
    "BNC": "Bangalore",
    "YNK": "Yelahanka",
    "CBP": "Chikkaballapur",
    "KQZ": "Kolar",
    "HUP": "Hindupur",
    "DMM": "Dharmavaram",
    "ATP": "Anantapur",
    "HX": "Kadapa",
    "PRDT": "Proddatur",
    "NDL": "Nandyal",
    "KRNT": "Kurnool City",
    "MBNR": "Mahbubnagar",
    "KCG": "Kacheguda",
    "MCI": "Mancherial",
    "RDM": "Ramagundam",
    "BDCR": "Bhadrachalam",
    "KMT": "Khammam",
    "STPT": "Suryapet",
    "MRGA": "Miryalaguda",
    "GLP": "Gollaprolu",
    "MRK": "Markapur",
    "DKD": "Donakonda",
    "NRT": "Narasaraopet",
    "PGRL": "Piduguralla",
    "BVRM": "Bhimavaram",
    "TNKU": "Tanuku",
    "NS": "Narsapur",
    "MTM": "Machilipatnam",
    "GDV": "Gudivada",
    "AVD": "Avadi",
    "PER": "Perambur",
    "SPE": "Sullurupeta",
    "NLS": "Nellore South",
    "RU": "Renigunta",
    "PAK": "Pakala",
    "KPN": "Kuppam",
    "BWT": "Bangarpet",
    "MYA": "Mandya",
    "RMGM": "Ramanagaram",
    "CPT": "Channapatna",
    "MAD": "Maddur",
    "TK": "Tumakuru",
    "ASK": "Arsikere",
    "HAS": "Hassan",
    "SKLR": "Sakleshpur",
    "SBHR": "Subrahmanya",
    "KUDA": "Kundapura",
    "UD": "Udupi",
    "BYNR": "Byndoor",
    "ANND": "Anand",
    "ND": "Nadiad",
    "BH": "Bharuch",
    "AKV": "Ankleshwar",
    "VAPI": "Vapi",
    "BL": "Valsad",
    "NVS": "Navsari",
    "DHD": "Dahod",
    "GDA": "Godhra",
    "PNU": "Palanpur",
    "MSH": "Mehsana",
    "PTN": "Patan",
    "GIMB": "Gandhidham",
    "BHUJ": "Bhuj",
    "SIOB": "Samakhiali",
    "AI": "Adipur",
    "MDRA": "Mundra",
    "SUNR": "Surendranagar",
    "BTD": "Botad",
    "AML": "Amreli",
    "JND": "Junagadh",
    "VRL": "Veraval",
    "OKHA": "Okha",
    "DWK": "Dwarka",
    "JAM": "Jamnagar",
    "PBR": "Porbandar",
    "BVP": "Bhavnagar East",
    "PIT": "Palitana",
    "SOJN": "Sihor",
    "GDL": "Gondal",
    "JLR": "Jetalsar",
    "SMNH": "Somnath",
    "UNAG": "Una Gujarat",
    "VDG": "Vadnagar",
    "KLL": "Kalol",
    "MDSA": "Modasa",
    "BIH": "Bhopal Bairagarh",
    "SEH": "Sehore",
    "UJN": "Ujjain",
    "DWX": "Dewas",
    "SFY": "Shajapur",
    "MKC": "Maksi",
    "BIX": "Bhind",
    "MRA": "Morena",
    "ETAH": "Etah",
    "HRS": "Hathras",
    "TDL": "Tundla",
    "KSJ": "Kasganj",
    "AWR": "Alwar",
    "BTE": "Bharatpur",
    "SWM": "Sawai Madhopur",
    "TNK": "Tonk",
    "BUDI": "Bundi",
    "BAZ": "Baran",
    "JLWC": "Jhalawar",
    "BHL": "Bhilwara",
    "COR": "Chittorgarh",
    "GGC": "Gangapur",
    "BXN": "Bayana",
    "DO": "Dausa",
    "NGO": "Nagaur",
    "SIKR": "Sikar",
    "JJN": "Jhunjhunu",
    "BNW": "Bhiwani",
    "PWL": "Palwal",
    "HDL": "Hodal",
    "MRT": "Mathura",
    "HTJ": "Hathras",
    "BLNR": "Gwalior Birlanagar",
    "DAA": "Datia",
    "DBA": "Dabra",
    "SOH": "Sirohi",
    "ABR": "Abu",
    "FA": "Falna",
    "PMY": "Pali Marwar",
    "RANI": "Rani",
    "MJ": "Marwar",
    "LUNI": "Luni",
    "PAP": "Pithapuram",
    "KTV": "Kothavalasa",
    "VBL": "Bobbili",
    "PVPT": "Parvatipuram Town",
    "SALR": "Salur",
    "KRPU": "Koraput",
    "RGDA": "Rayagada",
    "TIG": "Titlagarh",
    "KSNG": "Kesinga",
    "KBJ": "Kantabanji",
    "BLGR": "Balangir",
    "BRGA": "Bargarh",
    "JSGR": "Jharsuguda",
    "SDGH": "Sundargarh",
    "CMU": "Champua",
    "BPO": "Baripada",
    "BGY": "Bangriposi",
    "JER": "Jaleswar",
    "KGP": "Kharagpur",
    "SRC": "Santragachi",
    "SHM": "Shalimar",
    "BDC": "Bandel",
    "BWN": "Barddhaman",
    "TAK": "Tarakeswar",
    "DKAE": "Dankuni",
    "BP": "Barrackpore",
    "NH": "Naihati",
    "KYI": "Kalyani",
    "KNJ": "Krishnanagar",
    "RHA": "Ranaghat",
    "BNJ": "Bangaon",
    "HB": "Habra",
    "BSHT": "Basirhat",
    "SHE": "Seoraphuli",
    "SRP": "Serampore",
    "UPA": "Uttarpara",
    "BLY": "Bally",
    "BRMH": "Belur Math",
    "DDJ": "Dum Dum",
    "BT": "Barasat",
    "BRT": "Birati",
    "MMG": "Madhyamgram",
    "NBP": "New Barrackpore",
    "KPA": "Kanchrapara",
    "KNZ": "Kalna",
    "KWAE": "Katwa",
    "BHP": "Bolpur Shantiniketan",
    "RPH": "Rampurhat",
    "NHT": "Nalhati",
    "AZ": "Azimganj",
    "MBB": "Murshidabad",
    "JRLE": "Jangipur",
    "FKK": "Farakka",
    "KDPR": "Kumedpur",
    "SM": "Samsi",
    "HCR": "Harishchandrapur",
    "NFK": "New Farakka",
    "PKR": "Pakur",
    "SBG": "Sahibganj",
    "BHW": "Barharwa",
    "RJL": "Rajmahal",
    "GODA": "Godda",
    "DGHR": "Deoghar",
    "JSME": "Jasidih",
    "MDP": "Madhupur",
    "GRD": "Giridih",
    "DUMK": "Dumka",
    "JMT": "Jamtara",
    "VDSR": "Vidyasagar",
    "CRJ": "Chittaranjan",
    "ULT": "Kulti",
    "BRR": "Barakar",
    "UDL": "Andal",
    "SNT": "Sainthia",
    "NNA": "Naugachia",
    "KGG": "Khagaria",
    "MNE": "Mansi",
    "LKN": "Lakhminia",
    "JMP": "Jamalpur",
    "KIUL": "Kiul",
    "JAJ": "Jhajha",
    "MBI": "Madhubani",
    "JJP": "Jhanjharpur",
    "JYG": "Jaynagar",
    "RXL": "Raxaul",
    "BGU": "Bairgania",
    "CAA": "Chakia",
    "STD": "Sitabdiara",
    "GAP": "Gopalganj",
    "CPR": "Chapra",
    "SEE": "Sonepur",
    "HJP": "Hajipur",
    "DNR": "Danapur",
    "FUT": "Fatuha",
    "BKP": "Bakhtiyarpur",
    "BARH": "Barh",
    "MKA": "Mokama",
    "SSM": "Sasaram",
    "DOS": "Dehri On Sone",
    "KQR": "Koderma",
    "HZBN": "Hazaribagh Town",
    "BRKA": "Barkakana",
    "PTRU": "Patratu",
    "LTHR": "Latehar",
    "BRWD": "Barwadih",
    "DTO": "Daltonganj",
    "GHD": "Garhwa",
    "RNQ": "Renukoot",
    "CPU": "Chopan",
    "OBR": "Obra",
    "SBDR": "Sonbhadra",
    "RBGJ": "Robertsganj",
    "MZP": "Mirzapur",
    "CAR": "Chunar",
    "BOY": "Bhadohi",
    "JNU": "Jaunpur",
    "SHG": "Shahganj",
    "AMH": "Azamgarh",
    "CBE": "Coimbatore",
    "MDU": "Madurai",
    "TPJ": "Tiruchirappalli",
    "SA": "Salem",
    "ED": "Erode",
    "TUP": "Tiruppur",
    "DG": "Dindigul",
    "KRR": "Karur",
    "TEN": "Tirunelveli",
    "NCJ": "Nagercoil",
    "CAPE": "Kanyakumari",
    "TN": "Tuticorin",
    "VPT": "Virudhunagar",
    "SVKS": "Sivakasi",
    "RMM": "Rameswaram",
    "RMD": "Ramanathapuram",
    "SVGA": "Sivaganga",
    "PDKT": "Pudukkottai",
    "TJ": "Thanjavur",
    "KMU": "Kumbakonam",
    "MV": "Mayiladuthurai",
    "VM": "Villupuram",
    "VRI": "Virudhachalam",
    "TBM": "Tambaram",
    "KPD": "Katpadi",
    "TNM": "Tiruvannamalai",
    "DHJ": "Dharmapuri",
    "HSRA": "Hosur",
    "TCN": "Tiruchendur",
    "CVP": "Kovilpatti",
    "POY": "Pollachi",
    "PLNI": "Palani",
    "AJJ": "Arakkonam",
    "CGL": "Chengalpattu",
    "BNC": "Bangalore",
    "MAJN": "Mangaluru",
    "GIM": "Goa"
}

# ------------------------
# WEATHER HELPER
# ------------------------

def get_weather_for_city(city: str):
    """Get current weather directly by city name from OpenWeatherMap."""
    if not OPENWEATHER_API_KEY:
        return {
            "city": city,
            "summary": "API key not set",
            "temperature": "N/A",
        }

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",  # °C
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()

        if resp.status_code != 200:
            message = data.get("message", f"HTTP {resp.status_code}")
            return {
                "city": city,
                "summary": f"API error: {message}",
                "temperature": "N/A",
            }

        main_block = data.get("main", {})
        weather_list = data.get("weather", [])

        temp = main_block.get("temp")
        cond = (
            weather_list[0].get("description", "Unknown").title()
            if weather_list else "Unknown"
        )

        temp_str = f"{temp}°C" if temp is not None else "N/A"

        return {
            "city": city,
            "summary": cond,
            "temperature": temp_str,
        }

    except Exception as e:
        print("ERROR in get_weather_for_city:", e)
        return {
            "city": city,
            "summary": "Error calling weather API",
            "temperature": "N/A",
        }

# ------------------------
# TRAIN HELPER – IRCTC LIVE (RapidAPI)
# ------------------------

def get_train_status(train_number: str, departure_date: str):
    """
    Calls RapidAPI IRCTC live train status.

    departure_date format: YYYYMMDD (example: 20251130)
    """

    params = {
        "departure_date": departure_date,  # YYYYMMDD
        "isH5": "true",
        "client": "web",
        "deviceIdentifier": "Mozilla/5.0 (Rail360 Bot)",
        "train_number": train_number,
    }

    headers = {
        "x-rapidapi-key": RAPID_RAIL_KEY,
        "x-rapidapi-host": RAPID_RAIL_HOST,
    }

    try:
        resp = requests.get(IRCTC_URL, headers=headers, params=params, timeout=15)
        data = resp.json()

        if resp.status_code != 200:
            err = data.get("error") or data.get("message") or "No details"
            if "Wrong start date" in str(err):
                nice_msg = (
                    "Wrong start date. Use the date when the train started "
                    "from its source station, in YYYYMMDD format."
                )
            else:
                nice_msg = f"IRCTC API error: {err}"

            return {
                "has_issue": True,
                "message": f"IRCTC API HTTP {resp.status_code}: {nice_msg}",
                "raw": data,
            }

        # For this IRCTC API, live data is in "body"
        body = data.get("body", {})

        train_name = (
            data.get("train_name")
            or body.get("train_name")
            or f"Train {train_number}"
        )

        last_update = (
            body.get("server_timestamp")
            or "N/A"
        )

        current_location = (
            body.get("current_station")
            or "Location not available"
        )

        status_msg = body.get("train_status_message", "")
        terminated = body.get("terminated", False)

        # No explicit delay in this response → keep 0 or compute later
        delay_min = 0

        return {
            "has_issue": False,
            "train_no": train_number,
            "train_name": train_name,
            "last_update": last_update,
            "delay_min": delay_min,
            "segment": current_location,
            "status_msg": status_msg,
            "terminated": terminated,
            "raw": data,
        }

    except Exception as e:
        print("ERROR in get_train_status:", e)
        return {
            "has_issue": True,
            "message": f"Error calling IRCTC API: {e}",
            "raw": {},
        }

# ------------------------
# ENDPOINTS
# ------------------------

@app.get("/api/weather")
def weather(city: str):
    """Just weather: /api/weather?city=Chennai"""
    info = get_weather_for_city(city)
    text = f"🌦 Weather in {info['city']}: {info['summary']} ({info['temperature']})"
    return {"text": text, "raw": info}


@app.get("/api/rail-360")
def rail_360(train_no: str, station_code: str, departure_date: str | None = None):
    """
    Real-time train + weather.

    Example:
    /api/rail-360?train_no=12051&station_code=MAS&departure_date=20251130
    """

    # If no departure_date provided, default to today's date (YYYYMMDD)
    if not departure_date:
        departure_date = datetime.now().strftime("%Y%m%d")

    # 1) Live train (IRCTC)
    live = get_train_status(train_no, departure_date)

    # 2) Weather at station's city
    city = STATION_TO_CITY.get(station_code.upper(), station_code)
    weather = get_weather_for_city(city)

    lines = []
    lines.append("🚆 Rail 360 – Live Status")

    if live["has_issue"]:
        lines.append(f"Train: {train_no}")
        lines.append(f"⚠️ {live['message']}")
    else:
        lines.append(f"Train: {live['train_no']} – {live['train_name']}")
        lines.append(f"Location: {live['segment']}")
        lines.append(f"Last Update: {live['last_update']}")
        lines.append(f"Delay (approx): {live['delay_min']} min")

        if live.get("status_msg"):
            lines.append(f"Status: {live['status_msg']}")
        if live.get("terminated"):
            lines.append("✅ Train has reached its destination.")

    lines.append("")
    lines.append(f"At station: {station_code}")
    lines.append("(ETA parsing from IRCTC raw JSON can be added later.)")

    lines.append("")
    lines.append(f"🌦 Weather at {city}: {weather['summary']} ({weather['temperature']})")

    return {
        "text": "\n".join(lines),
        "train": live,
        "weather": weather,
    }


@app.get("/")
def root():
    return {
        "message": "Rail 360 backend running",
        "examples": [
            "/api/weather?city=Chennai",
            "/api/rail-360?train_no=12051&station_code=MAS&departure_date=20251130",
        ],
    }
