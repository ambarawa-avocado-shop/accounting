"""Pengaturan koneksi MySQL.
Urutan pembacaan: .streamlit/secrets.toml (bagian [mysql]) -> environment variable (DB_HOST, DB_USER, ...) -> nilai default.

Untuk MySQL yang di-host (Aiven, TiDB, Railway) yang mewajibkan TLS, isi `ssl_ca` dengan isi sertifikat
(PEM, boleh ditempel langsung) atau path file-nya. Bila verifikasi sertifikat perlu dimatikan, isi
`ssl_verify_cert = false`.
"""
import os
import tempfile

GALAT = None                                    # alasan secrets tidak terbaca, ditampilkan bila koneksi gagal

try:
    import streamlit as st
    _s = dict(st.secrets["mysql"])
except Exception as e:
    _s = {}
    GALAT = f"{type(e).__name__}: {e}"


def _ambil(kunci, default=None):
    if kunci in _s:
        return _s[kunci]
    return os.getenv("DB_" + kunci.upper(), default)


def _opsi_ssl():
    ca = _ambil("ssl_ca")
    if not ca:
        return {}
    if "BEGIN CERTIFICATE" in ca:                     # sertifikat ditempel langsung di secrets/hosting
        path = os.path.join(tempfile.gettempdir(), "mysql_ssl_ca.pem")
        with open(path, "w") as f:
            f.write(ca)
        ca = path
    return {"ssl_ca": ca, "ssl_verify_cert": str(_ambil("ssl_verify_cert", True)).lower() not in ("0", "false")}


DB = {
    "host": _ambil("host", "localhost"),
    "port": int(_ambil("port", 3306)),
    "user": _ambil("user", "root"),
    "password": _ambil("password", ""),          # kosong = tanpa password
    "database": _ambil("database", "alpukat estate"),
}

SSL = _opsi_ssl()
