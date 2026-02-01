#!/usr/bin/env python3
import os
import time
import shutil
import subprocess
from datetime import datetime, timedelta

import requests
from dateutil import tz

# =========================
# CONFIG
# =========================
CITY = "Balikpapan"
COUNTRY = "Indonesia"

METHOD = 11
SCHOOL = 0

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AZAN_FILE = os.path.join(BASE_DIR, "sounds", "azan.mp3")


REFRESH_MINUTES = 30
NEAR_MINUTES = 15   # waktu dekat (menit) → warna biru terang

LOCAL_TZ = tz.tzlocal()

PRAYER_KEYS = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]

PRAYER_MAP_ID = {
    "Fajr": "Subuh",
    "Dhuhr": "Dzuhur",
    "Asr": "Ashar",
    "Maghrib": "Maghrib",
    "Isha": "Isya",
}

# =========================
# WARNA TERMINAL (ANSI)
# =========================
RESET = "\033[0m"
GREEN = "\033[32m"
BLUE = "\033[34m"
CYAN = "\033[36m"
BOLD = "\033[1m"


def notify(title: str, message: str) -> None:
    if shutil.which("notify-send"):
        subprocess.run(["notify-send", title, message], check=False)


def play_azan() -> None:
    if not os.path.exists(AZAN_FILE):
        notify("Jadwal Sholat", f"File azan tidak ditemukan: {AZAN_FILE}")
        return

    ffplay = shutil.which("ffplay")
    if not ffplay:
        notify("Jadwal Sholat", "ffplay tidak ditemukan. Install ffmpeg dulu.")
        return

    subprocess.Popen(
        [ffplay, "-nodisp", "-autoexit", "-loglevel", "quiet", AZAN_FILE],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def fetch_timings() -> dict:
    url = "https://api.aladhan.com/v1/timingsByCity"
    params = {"city": CITY, "country": COUNTRY, "method": METHOD, "school": SCHOOL}
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    if data.get("code") != 200:
        raise RuntimeError(f"API error: {data}")
    return data["data"]["timings"]


def parse_time_today(hhmm: str) -> datetime:
    hhmm = hhmm.split()[0].strip()
    now = datetime.now(LOCAL_TZ)
    h, m = hhmm.split(":")
    return now.replace(hour=int(h), minute=int(m), second=0, microsecond=0)


def next_prayer_key(timings: dict) -> tuple[str, datetime]:
    now = datetime.now(LOCAL_TZ)
    for k in PRAYER_KEYS:
        t = parse_time_today(timings[k])
        if t > now:
            return k, t

    fajr_tomorrow = parse_time_today(timings["Fajr"]) + timedelta(days=1)
    return "Fajr", fajr_tomorrow


def format_td(delta: timedelta) -> str:
    total = int(delta.total_seconds())
    if total < 0:
        total = 0
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def clear():
    os.system("clear")


def main():
    timings = None
    last_refresh = None
    fired = set()

    while True:
        try:
            now = datetime.now(LOCAL_TZ)

            if timings is None or last_refresh is None or (now - last_refresh) > timedelta(minutes=REFRESH_MINUTES):
                timings = fetch_timings()
                last_refresh = now
                fired.clear()

            next_key, next_time = next_prayer_key(timings)

            # trigger azan
            for k in PRAYER_KEYS:
                pt = parse_time_today(timings[k])
 
                # ==================================================
                # PENGINGAT 15 MENIT
                # ==================================================
                target_pengingat = pt - timedelta(minutes=15)

                # Jika waktu sekarang masuk dalam jendela 2 detik dari target
                if target_pengingat <= now < (target_pengingat + timedelta(seconds=2)):
                    key_pengingat = (now.date().isoformat(), k, "15m_remind")
                    if key_pengingat not in fired:
                        fired.add(key_pengingat)
                        # Memanggil fungsi notify bawaan script (memakai notify-send)
                        notify("Persiapan Sholat", f"15 menit lagi waktu {PRAYER_MAP_ID[k]}")
                # ==================================================

                # Ini adalah trigger azan asli
                if pt <= now < (pt + timedelta(minutes=1)):
                    key = (now.date().isoformat(), k)
                    if key not in fired:
                        fired.add(key)
                        notify("Waktu Sholat", f"Masuk waktu {PRAYER_MAP_ID[k]} ({pt:%H:%M})")
                        play_azan()

            clear()
            print(BOLD + "Jadwal Sholat " + RESET)
            print(f"Kota: {CITY}, {COUNTRY} | TZ: {now.tzname()}")
#            print(f"Terakhir update: {last_refresh:%H:%M:%S}")
            print("-" * 44)

            for k in PRAYER_KEYS:
                nama = PRAYER_MAP_ID[k]
                t = parse_time_today(timings[k])
                delta = t - now

                # Tentukan warna
                if t < now:
                    color = GREEN
                elif k == next_key:
                    if delta <= timedelta(minutes=NEAR_MINUTES):
                        color = CYAN + BOLD
                    else:
                        color = BLUE + BOLD
                else:
                    color = ""

                print(f"{color}{nama:8s}: {t:%H:%M}{RESET}")

            print("-" * 44)
            print(f"Berikutnya: {BOLD}{PRAYER_MAP_ID[next_key]}{RESET} @ {next_time:%H:%M}")
            print(f"Countdown : {format_td(next_time - now)}")
            print("\nCtrl+C untuk keluar.")
            time.sleep(1)

        except KeyboardInterrupt:
            print("\nKeluar.")
            break
        except Exception as e:
            notify("Jadwal Sholat", f"Error: {e}")
            print(f"Error: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()
