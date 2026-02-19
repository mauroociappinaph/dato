import os
import sys
import json
from datetime import datetime

def generate_docs(project_path, project_name, tech_stack, features):
    """Generates a standard documentation suite for a new project."""
    docs_base = os.path.join(project_path, "docs")
    
    # Structure definition
    structure = {
        "sop": {
            "init.md": f"# SOP: Project Initialization - {project_name}\n\n1. Standard naming applied.\n2. Tech stack: {tech_stack} installed.\n3. Repository synchronized.",
            "workflow.md": "# SOP: Development Workflow\n\n1. Branch from develop.\n2. Visual validation required.\n3. Automatic cleanup."
        },
        "specs": {
            "architecture.md": f"# Architecture Specification: {project_name}\n\n- **Tech Stack:** {tech_stack}\n- **Core Components:** Backend, Frontend, Redis Blackboard.\n- **Orchestration:** LangGraph Director.",
            "features.md": f"# Functional Features: {project_name}\n\n" + "\n".join([f"- {feat}" for feat in features])
        },
        "tasks": {
            "backlog.md": f"# Project Backlog: {project_name}\n\n- [ ] TASK-001: Scaffolding\n- [ ] TASK-002: Infrastructure Setup\n- [ ] TASK-003: Core Feature Implementation"
        }
    }

    # Creation logic
    for folder, files in structure.items():
        folder_path = os.path.join(docs_base, folder)
        os.makedirs(folder_path, exist_ok=True)
        for filename, content in files.items():
            with open(os.path.join(folder_path, filename), "w") as f:
                f.write(content)
                print(f"Generated: {folder}/{filename}")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python generate_project_docs.py <path> <name> <stack> <features_json>")
        sys.exit(1)
    
    path = sys.argv[1]
    name = sys.argv[2]
    stack = sys.argv[3]
    features = json.loads(sys.argv[4])
    
    generate_docs(path, name, stack, features)
