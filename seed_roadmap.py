import requests
import json

BASE_URL = "http://localhost:8000/api/milestones/"

milestones = [
    {
        "title": "Core Engine Completion",
        "description": "Stabilize the primary data structures and neural archive protocols.",
        "target_date": "Q1 2026",
        "status": "completed",
        "tags": ["Backend", "Infrastructure"],
        "icon_name": "CheckCircle2"
    },
    {
        "title": "Inter-System Connectivity",
        "description": "Establish high-velocity data bridges between internal modules.",
        "target_date": "Q2 2026",
        "status": "in-progress",
        "tags": ["Networking", "API"],
        "icon_name": "Zap"
    },
    {
        "title": "Predictive Intelligence Launch",
        "description": "Integrate Bayesian inference models for automated trend analysis.",
        "target_date": "Q3 2026",
        "status": "planned",
        "tags": ["AI", "Data Science"],
        "icon_name": "BrainCircuit"
    },
    {
        "title": "External Node Synchronization",
        "description": "Expand the ecosystem beyond local nodes to external API clusters.",
        "target_date": "Q4 2026",
        "status": "planned",
        "tags": ["Expansion", "External"],
        "icon_name": "Flag"
    }
]

for milestone in milestones:
    response = requests.post(BASE_URL, json=milestone)
    if response.status_code == 200:
        print(f"Created: {milestone['title']}")
    else:
        print(f"Failed: {milestone['title']} - {response.text}")
