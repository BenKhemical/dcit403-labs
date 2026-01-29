# dcit403-labs

# SPADE Multi-Agent System Labs

This repository contains a series of laboratory exercises for learning **SPADE (Smart Python Agent Development Environment)** and building multi-agent systems. The labs focus on creating agents that perceive and interact with a simulated disaster environment, demonstrating fundamental concepts such as agent setup, perception, and environment modeling.

---

## **Overview of the Repository**

The repository is organized by lab exercises, with each lab containing:

- Python scripts implementing SPADE agents
- Event logs capturing agent percepts
- Documentation explaining objectives, percepts, and agent behaviours

Each lab is committed separately to maintain a clear project history.

---

## **Lab 1: Environment and Agent Platform Setup**

**Objective:**  
To configure a Python agent development environment and deploy a basic SPADE agent.

**Description:**  
In this lab, the GitHub Codespaces environment was used to set up Python 3.11 and install the SPADE library. An XMPP server (`xmpp.jp`) was used to handle agent communication. A simple agent was implemented to print a message every few seconds, demonstrating that the agent platform is functional and correctly connected to the server.

**Files:**  
- `lab1_environment_setup.py` — Python script for the basic agent  
- Optional: Event logs (if the agent writes to a file)

**Key Concepts Learned:**  
- Setting up SPADE in Python  
- Connecting agents to an XMPP server  
- Implementing and running a simple cyclic behaviour

---

## **Lab 2: Perception and Environment Modeling**

**Objective:**  
To implement agent perception of environmental events and record disaster-related information.

**Description:**  
This lab introduced a **simulated disaster environment** using the `DisasterEnvironment` class. The `SensorAgent` was implemented to periodically monitor the environment. It perceives **disaster severity levels** (1–10) and logs each event in a file (`event_log_lab2.txt`). This demonstrates how agents sense and respond to changes in their environment. The cyclic behaviour runs repeatedly, generating new percepts every few seconds.

**Files:**  
- `lab2_sensor_agent.py` — SensorAgent code monitoring the disaster environment  
- `event_log_lab2.txt` — Logs of detected events

**Percepts Used:**  
- **Disaster severity level:** Numeric value representing the intensity of a simulated disaster event  
- **Timestamps (optional):** Time when the agent detected the event  

These percepts allow the agent to understand the environment, monitor changes over time, and maintain a record of all events.

**Key Concepts Learned:**  
- Agent perception and environmental modeling  
- Using cyclic behaviours to sense the environment repeatedly  
- Logging percepts to track agent observations  

---

## **Environment Setup**

To run these labs locally or in Codespaces:

1. **Python:** Ensure Python 3.11 or higher is installed.  
2. **Install SPADE:**  

```bash
pip install spade
