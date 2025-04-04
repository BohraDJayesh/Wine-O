#!/bin/bash

echo "[*] Starting Wine Malware Execution"

if [ -f "$1" ]; then
	echo "[*] Executing: $1"
	wine "$1"
else
	echo "[!] Malware file not found!"
fi

echo "[*] Execution Completed"
