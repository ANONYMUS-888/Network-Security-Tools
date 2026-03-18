# 🛡️ Advanced Python Security & Automation Toolkit | Red & Blue Team

Welcome to my cybersecurity portfolio. This repository contains a collection of custom Python-based networking, offensive security, and defensive monitoring tools. 

These scripts were developed in a dedicated Kali Linux home lab to solidify core concepts from industry-standard materials like *Black Hat Python* and *Linux Basics for Hackers*. To maximize efficiency and ensure modern, robust code structures, I actively utilized AI-assisted development (LLMs) during the coding and troubleshooting process.

**The Goal:** To bridge the gap between theoretical knowledge and practical, hands-on Security Operations (SOC) engineering.

---

## 🔵 Blue Team Arsenal: Defense, Monitoring & Incident Response

This section focuses on host-based intrusion detection, log analysis, and automated alerting pipelines—core competencies for any Security Operations Center.

### 1. 🚨 Log Analyzer & Alerting Engine (`log_analyzer.py`)
A comprehensive, 136-line log analysis engine that simulates a lightweight SIEM workflow.
* **Core Function:** Automatically parses system logs, identifies anomalous patterns using Threat Intelligence APIs, and pushes structured, real-time alerts directly to a **Discord Webhook**. 
* **Value:** Demonstrates understanding of API integrations, log parsing, and actionable SOC alerting.

### 2. 🛡️ FIM Warden (`warden.py`)
A custom File Integrity Monitoring (FIM) solution utilizing the Python `watchdog` library.
* **Core Function:** Uses `Observer` and `FileSystemEventHandler` to continuously monitor critical system directories for unauthorized file creation, modification, or deletion.
* **Value:** Emulates enterprise host-based intrusion detection systems (HIDS).

### 3. 🕵️‍♂️ Persistence Hunter (`persistence_hunter.py`)
An endpoint threat-hunting script designed to detect common malware persistence mechanisms.
* **Core Function:** Queries the Windows Registry for suspicious AutoRun/Startup keys and immediately triggers a **Discord Webhook** notification upon detecting anomalies.
* **Value:** Shows a proactive approach to hunting advanced persistent threats (APTs).

### 4. 🍯 Deception Honeypot (`honey_pot.py`)
An early-warning deception technology script.
* **Core Function:** Opens decoy ports to attract unauthorized scanning or connection attempts, silently logging the attacker's IP address and methodology before they can reach production assets.

### 5. 📡 Raw Network Sniffer (`pro_sniffer.py`)
A low-level diagnostic tool for deep packet inspection.
* **Core Function:** Captures and analyzes raw IP headers to detect anomalous network flows and baseline deviations on the local interface.

---

## 🔴 Red Team Arsenal: Offensive Security & Reconnaissance

To defend a network, you must understand how to attack it. These tools automate the first phases of the adversary kill chain.

### 1. 🏭 ICS/SCADA Modbus Scanner (`industrial_protocol_security_scanner.py`)
A specialized reconnaissance tool targeting Critical Infrastructure.
* **Core Function:** Probes target IP ranges for exposed Modbus protocols (Port 502), highlighting the critical need for network segmentation in industrial environments.

### 2. ⚡ Multithreaded Port Scanner (`pro_port_scanner.py`)
A high-speed reconnaissance tool built for efficiency.
* **Core Function:** Utilizes `concurrent.futures.ThreadPoolExecutor` to rapidly identify open network ports and potential entry points, drastically reducing scan times compared to linear scripts.

### 3. 🔄 Network TCP Proxy (`proxy.py`)
A traffic manipulation utility built for Man-in-the-Middle (MitM) simulations.
* **Core Function:** Sits between a client and a server to intercept, modify, and hex-dump network traffic in real-time, allowing for the analysis of clear-text protocols.

### 4. 🐚 Custom Netcat Clone (`netcat.py`)
A Python-based implementation of the classic "Swiss Army Knife" of networking.
* **Core Function:** Supports command execution, file transfers, and establishing reverse/bind shells for penetration testing and payload delivery scenarios.

### 5. 🔌 Pro Raw TCP Client (`pro_tcp_client.py`)
A highly flexible, argparse-supported network client.
* **Core Function:** Built for targeted banner grabbing, service interaction, and sending custom payloads to specific open ports during vulnerability assessments.

---

## ⚙️ Environment & Execution

All scripts have been actively tested and debugged in a **Kali Linux** environment. 
* **Dependencies:** Refer to the individual script headers for specific library requirements (e.g., `pymodbus`, `watchdog`, `requests`).
* **Visual Proof:** Screenshots of successful script executions (including handled exceptions) are included alongside the source code in this repository.

> **⚠️ Disclaimer:** All tools within this repository were created for educational purposes and authorized home-lab testing only. I strictly adhere to ethical hacking guidelines. Never execute these tools against systems or networks without explicit, written permission.
