import os
import json

def audit_company(skills_path):
    print(f"--- INICIANDO AUDITORÍA SISTÉMICA: {skills_path} ---")
    skills = [d for d in os.listdir(skills_path) if os.path.isdir(os.path.join(skills_path, d))]
    
    report = {
        "total_skills": len(skills),
        "perfect_score": [],
        "needs_improvement": [],
        "missing_critical_roles": []
    }

    # CRITICAL ROLES CHECKLIST 2026
    critical_roles = ["token-accountant", "ai-solutions-architect", "security-auditor", "latency-optimizer"]
    
    for role in critical_roles:
        if role not in skills:
            report["missing_critical_roles"].append(role)

    for skill in skills:
        path = os.path.join(skills_path, skill)
        has_skill_md = os.path.exists(os.path.join(path, "SKILL.md"))
        has_scripts = os.path.exists(os.path.join(path, "scripts")) and len(os.listdir(os.path.join(path, "scripts"))) > 0
        
        score = 0
        if has_skill_md: score += 5
        if has_scripts: score += 5
        
        if score == 10:
            report["perfect_score"].append(skill)
        else:
            report["needs_improvement"].append({"name": skill, "score": score})

    return report

if __name__ == "__main__":
    SKILLS_DIR = os.path.expanduser("~/.gemini/anti_gravity/global_skills")
    results = audit_company(SKILLS_DIR)
    print(json.dumps(results, indent=2))
