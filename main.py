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
# STATION → CITY MAP (for weather & pretty names)
# ------------------------

STATION_TO_CITY = {
    "NDLS": "New Delhi",
    "HWH": "Howrah Junction",
    "BCT": "Mumbai Central",
    "CSMT": "Mumbai",
    "SBC": "Bengaluru City",
    "HYB": "Hyderabad Deccan",
    "SC": "Secunderabad",
    "SDAH": "Sealdah",
    "ADI": "Ahmedabad Junction",
    "PUNE": "Pune Junction",
    "PNBE": "Patna Junction",
    "CNB": "Kanpur Central",
    "PRYJ": "Prayagraj Junction",
    "JP": "Jaipur Junction",
    "LKO": "Lucknow Charbagh",
    "GKP": "Gorakhpur Junction",
    "BSB": "Varanasi Junction",
    "GHY": "Guwahati",
    "CDG": "Chandigarh",
    "BPL": "Bhopal Junction",
    "GWL": "Gwalior",
    "JBP": "Jabalpur",
    "CBE": "Coimbatore Junction",
    "TVC": "Thiruvananthapuram Central",
    "ERS": "Ernakulam Junction",
    "TMV": "Tindivanam",
    "MDU": "Madurai Junction",
    "TPJ": "Tiruchirappalli",
    "VSKP": "Visakhapatnam",
    "BZA": "Vijayawada",
    "BBS": "Bhubaneswar",
    "CTC": "Cuttack",
    "R": "Raipur Junction",
    "BSP": "Bilaspur",
    "NGP": "Nagpur",
    "ASR": "Amritsar Junction",
    "LDH": "Ludhiana Junction",
    "JUC": "Jalandhar City",
    "JAT": "Jammu Tawi",
    "UDZ": "Udaipur City",
    "AII": "Ajmer Junction",
    "JU": "Jodhpur Junction",
    "KOTA": "Kota Junction",
    "ST": "Surat",
    "BRC": "Vadodara",
    "RJT": "Rajkot",
    "BVC": "Bhavnagar Terminus",
    "MAO": "Madgaon",
    "MAJN": "Mangaluru Junction",
    "UBL": "Hubballi Junction",
    "MYS": "Mysuru Junction",
    "SA": "Salem Junction",
    "ED": "Erode Junction",
    "NLR": "Nellore",
    "TPTY": "Tirupati",
    "GNT": "Guntur",
    "WL": "Warangal",
    "KZJ": "Kazipet",
    "REWA": "Rewa",
    "ET": "Itarsi Junction",
    "RTM": "Ratlam Junction",
    "JHS": "Jhansi Junction",
    "AGC": "Agra Cantt",
    "MTJ": "Mathura Junction",
    "ALJN": "Aligarh Junction",
    "MTC": "Meerut City",
    "FD": "Faizabad",
    "AY": "Ayodhya Dham",
    "BE": "Bareilly Junction",
    "MB": "Moradabad",
    "DDN": "Dehradun",
    "HW": "Haridwar",
    "KGM": "Kathgodam",
    "RKSH": "Rishikesh",
    "TATA": "Tatanagar",
    "ASN": "Asansol Junction",
    "DHN": "Dhanbad Junction",
    "RNC": "Ranchi",
    "HTE": "Hatia",
    "GAYA": "Gaya Junction",
    "BGP": "Bhagalpur",
    "MFP": "Muzaffarpur",
    "DBG": "Darbhanga",
    "SV": "Siwan",
    "SPJ": "Samastipur",
    "BJU": "Barauni Junction",
    "BXR": "Buxar",
    "ARA": "Arrah",
    "DURG": "Durg Junction",
    "UMB": "Ambala Cantt",
    "ROK": "Rohtak",
    "HSR": "Hisar",
    "RE": "Rewari",
    "DEE": "Delhi Sarai Rohilla",
    "ANVT": "Anand Vihar Terminal",
    "BDTS": "Bandra Terminus",
    "LTT": "Lokmanya Tilak Terminus",
    "DR": "Dadar",
    "CCG": "Churchgate",
    "VSH": "Vashi",
    "PNVL": "Panvel",
    "VR": "Virar",
    "BSR": "Vasai Road",
    "NK": "Nashik Road",
    "BSL": "Bhusaval",
    "JL": "Jalgaon",
    "AK": "Akola",
    "KIK": "Karaikal",
    "AMI": "Amravati",
    "WR": "Wardha",
    "CD": "Chandrapur",
    "BPQ": "Ballarshah",
    "G": "Gondia",
    "DGR": "Durgapur",
    "MLDT": "Malda Town",
    "NJP": "New Jalpaiguri",
    "SGUJ": "Siliguri Junction",
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
    "JJKR": "Jajpur Keonjhar Road",
    "DNKL": "Dhenkanal",
    "VZM": "Vizianagaram",
    "CHE": "Srikakulam Road",
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
    "LTRR": "Latur Road",
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
    "SWV": "Sawantwadi Road",
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
    "PGT": "Palakkad Junction",
    "CAN": "Kannur",
    "CLT": "Kozhikode",
    "KGQ": "Kasaragod",
    "QLN": "Kollam Junction",
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
    "TJ": "Thanjavur Junction",
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
    "BNC": "Bangalore Cantonment",
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
    "BDCR": "Bhadrachalam Road",
    "KMT": "Khammam",
    "STPT": "Suryapet",
    "MRGA": "Miryalaguda",
    "GLP": "Gollaprolu",
    "MRK": "Markapur Road",
    "DKD": "Donakonda",
    "NRT": "Narasaraopet",
    "PGRL": "Piduguralla",
    "BVRM": "Bhimavaram Junction",
    "TNKU": "Tanuku",
    "NS": "Narsapur",
    "MTM": "Machilipatnam",
    "GDV": "Gudivada",
    "AVD": "Avadi",
    "PER": "Perambur",
    "SPE": "Sullurupeta",
    "NLS": "Nellore South",
    "RU": "Renigunta Junction",
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
    "SBHR": "Subrahmanya Road",
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
    "UJN": "Ujjain Junction",
    "DWX": "Dewas",
    "SFY": "Shajapur",
    "MKC": "Maksi",
    "BIX": "Bhind",
    "MRA": "Morena",
    "ETAH": "Etah",
    "HRS": "Hathras Junction",
    "TDL": "Tundla Junction",
    "KSJ": "Kasganj",
    "AWR": "Alwar",
    "BTE": "Bharatpur",
    "SWM": "Sawai Madhopur",
    "TNK": "Tonk",
    "BUDI": "Bundi",
    "BAZ": "Baran",
    "JLWC": "Jhalawar Road",
    "BHL": "Bhilwara",
    "COR": "Chittorgarh",
    "GGC": "Gangapur City",
    "BXN": "Bayana",
    "DO": "Dausa",
    "NGO": "Nagaur",
    "SIKR": "Sikar Junction",
    "JJN": "Jhunjhunu",
    "BNW": "Bhiwani",
    "PWL": "Palwal",
    "HDL": "Hodal",
    "MRT": "Mathura Cantt",
    "HTJ": "Hathras Road",
    "BLNR": "Gwalior Birlanagar",
    "DAA": "Datia",
    "DBA": "Dabra",
    "SOH": "Sirohi Road",
    "ABR": "Abu Road",
    "FA": "Falna",
    "PMY": "Pali Marwar",
    "RANI": "Rani",
    "MJ": "Marwar Junction",
    "LUNI": "Luni Junction",
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
    "BRGA": "Bargarh Road",
    "JSGR": "Jharsuguda Road",
    "SDGH": "Sundargarh",
    "CMU": "Champua",
    "BPO": "Baripada",
    "BGY": "Bangriposi",
    "JER": "Jaleswar",
    "KGP": "Kharagpur Junction",
    "SRC": "Santragachi",
    "SHM": "Shalimar",
    "BDC": "Bandel Junction",
    "BWN": "Barddhaman Junction",
    "TAK": "Tarakeswar",
    "DKAE": "Dankuni",
    "BP": "Barrackpore",
    "NH": "Naihati",
    "KYI": "Kalyani",
    "KNJ": "Krishnanagar City",
    "RHA": "Ranaghat Junction",
    "BNJ": "Bangaon Junction",
    "HB": "Habra",
    "BSHT": "Basirhat",
    "SHE": "Seoraphuli",
    "SRP": "Serampore",
    "UPA": "Uttarpara",
    "BLY": "Bally",
    "BRMH": "Belur Math",
    "DDJ": "Dum Dum Junction",
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
    "JRLE": "Jangipur Road",
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
    "JSME": "Jasidih Junction",
    "MDP": "Madhupur",
    "GRD": "Giridih",
    "DUMK": "Dumka",
    "JMT": "Jamtara",
    "VDSR": "Vidyasagar",
    "CRJ": "Chittaranjan",
    "ULT": "Kulti",
    "BRR": "Barakar",
    "UDL": "Andal Junction",
    "SNT": "Sainthia",
    "NNA": "Naugachia",
    "KGG": "Khagaria",
    "MNE": "Mansi",
    "LKN": "Lakhminia",
    "JMP": "Jamalpur Junction",
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
    "SEE": "Sonepur Junction",
    "HJP": "Hajipur Junction",
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
    "GHD": "Garhwa Road",
    "RNQ": "Renukoot",
    "CPU": "Chopan",
    "OBR": "Obra",
    "SBDR": "Sonbhadra",
    "RBGJ": "Robertsganj",
    "MZP": "Mirzapur",
    "CAR": "Chunar",
    "BOY": "Bhadohi",
    "JNU": "Jaunpur Junction",
    "SHG": "Shahganj",
    "AMH": "Azamgarh",
    "MS": "Chennai",
    "SA": "Salem"

}

# We also use this as "full pretty name" map
STATION_FULL_NAME = STATION_TO_CITY

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

        body = data.get("body", {})

        train_name = (
            data.get("train_name")
            or body.get("train_name")
            or f"Train {train_number}"
        )

        last_update = body.get("server_timestamp") or "N/A"
        current_location = body.get("current_station") or "Location not available"
        status_msg = body.get("train_status_message", "")
        terminated = body.get("terminated", False)

        delay_min = 0  # not directly provided

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

@app.get("/api/rail-360-two-weather")
def rail_360_two_weather(train_no: str, departure_date: str | None = None):
    """
    Train live status + weather at current station AND destination station.

    Example:
    /api/rail-360-two-weather?train_no=12051&departure_date=20251130
    """

    # Default departure_date = today if not given
    if not departure_date:
        departure_date = datetime.now().strftime("%Y%m%d")

    # 1) Live train info
    live = get_train_status(train_no, departure_date)

    # Prepare defaults in case IRCTC data is missing
    current_code = None
    dest_code = None

    body = live.get("raw", {}).get("body", {}) if not live.get("has_issue") else {}
    stations = body.get("stations", [])

    # current station code
    if not live.get("has_issue"):
        current_code = body.get("current_station")
        # IRCTC sometimes gives full code in live['segment'] as well
        if not current_code:
            current_code = live.get("segment")

    # destination station = last station in the list
    if stations:
        dest_code = stations[-1].get("stationCode")

    # Map codes → city names
    current_city = (
        STATION_TO_CITY.get(current_code, current_code)
        if current_code else "Unknown"
    )
    dest_city = (
        STATION_TO_CITY.get(dest_code, dest_code)
        if dest_code else "Unknown"
    )

    # 2) Weather for both
    current_weather = get_weather_for_city(current_city) if current_city != "Unknown" else {
        "city": current_city,
        "summary": "N/A",
        "temperature": "N/A",
    }
    dest_weather = get_weather_for_city(dest_city) if dest_city != "Unknown" else {
        "city": dest_city,
        "summary": "N/A",
        "temperature": "N/A",
    }

    # 3) Build text reply
    lines = []
    lines.append("🚆 Rail 360 – Live Status + Dual Weather")

    if live["has_issue"]:
        lines.append(f"Train: {train_no}")
        lines.append(f"⚠️ {live['message']}")
    else:
        lines.append(f"Train: {live['train_no']} – {live['train_name']}")
        lines.append(f"Last Update: {live['last_update']}")
        if live.get("status_msg"):
            lines.append(f"Status: {live['status_msg']}")
        if live.get("terminated"):
            lines.append("✅ Train has reached its destination.")

    lines.append("")

    # current station weather
    lines.append(f"📍 Current station: {current_city} ({current_code or 'N/A'})")
    lines.append(
        f"   🌦 {current_weather['summary']} ({current_weather['temperature']})"
    )

    lines.append("")

    # destination station weather
    lines.append(f"🏁 Destination: {dest_city} ({dest_code or 'N/A'})")
    lines.append(
        f"   🌦 {dest_weather['summary']} ({dest_weather['temperature']})"
    )

    return {
        "text": "\n".join(lines),
        "train": live,
        "current_weather": current_weather,
        "destination_weather": dest_weather,
    }



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

    lines = []
    lines.append("🚆 Rail 360 – Live Status")

    # Prepare weather variables
    origin_code = dest_code = None
    origin_city = dest_city = current_city = None
    origin_weather = dest_weather = current_weather = None

    if live["has_issue"]:
        # On error, just show message + weather at requested station_code
        lines.append(f"Train: {train_no}")
        lines.append(f"⚠️ {live['message']}")

        city = STATION_TO_CITY.get(station_code.upper(), station_code)
        weather = get_weather_for_city(city)
        lines.append("")
        lines.append(f"At station: {station_code}")
        lines.append("")
        lines.append(f"🌦 Weather at {city}: {weather['summary']} ({weather['temperature']})")

        return {
            "text": "\n".join(lines),
            "train": live,
            "weather": {
                "origin": None,
                "current": weather,
                "destination": None,
            },
        }

    # ------------ SUCCESS CASE ------------

    # Train info
    lines.append(f"Train: {live['train_no']} – {live['train_name']}")

    # Full station name for current segment
    station_full = STATION_FULL_NAME.get(live['segment'], live['segment'])
    lines.append(f"Location: {station_full} ({live['segment']})")
    lines.append(f"Last Update: {live['last_update']}")
    lines.append(f"Delay (approx): {live['delay_min']} min")

    if live.get("status_msg"):
        lines.append(f"Status: {live['status_msg']}")
    if live.get("terminated"):
        lines.append("✅ Train has reached its destination.")

    # 2) Weather: origin, current, destination (Chennai → Madurai style)
    body = live.get("raw", {}).get("body", {})
    stations = body.get("stations") or []

    if stations:
        origin_code = stations[0].get("stationCode")
        dest_code = stations[-1].get("stationCode")

        if origin_code:
            origin_city = STATION_TO_CITY.get(origin_code, origin_code)
            origin_weather = get_weather_for_city(origin_city)

        if dest_code:
            dest_city = STATION_TO_CITY.get(dest_code, dest_code)
            dest_weather = get_weather_for_city(dest_city)

    seg_code = live.get("segment")
    if seg_code:
        current_city = STATION_TO_CITY.get(seg_code, seg_code)
        current_weather = get_weather_for_city(current_city)

    lines.append("")
    lines.append(f"Route station param: {station_code}")

    lines.append("")
    # Origin weather
    if origin_city and origin_weather:
        lines.append(
            f"🌦 Origin ({origin_code} – {origin_city}): "
            f"{origin_weather['summary']} ({origin_weather['temperature']})"
        )
    # Current weather
    if current_city and current_weather:
        lines.append(
            f"🌦 Current ({seg_code} – {current_city}): "
            f"{current_weather['summary']} ({current_weather['temperature']})"
        )
    # Destination weather
    if dest_city and dest_weather:
        lines.append(
            f"🌦 Destination ({dest_code} – {dest_city}): "
            f"{dest_weather['summary']} ({dest_weather['temperature']})"
        )

    return {
        "text": "\n".join(lines),
        "train": live,
        "weather": {
            "origin": origin_weather,
            "current": current_weather,
            "destination": dest_weather,
        },
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









