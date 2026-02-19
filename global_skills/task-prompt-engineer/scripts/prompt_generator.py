"""
Core module for generating task prompts
"""
import re
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

@dataclass
class SubtaskInfo:
    id: str
    title: str
    description: str
    skills: list[str]
    commands: list[str]
    dependencies: list[str]
    checkboxes: list[str]

class TaskPromptEngineer:
    """
    Parse TASK.md and generate execution prompts for subtasks or sections
    """
    
    def __init__(self, task_file: str = "TASK.md"):
        self.task_file = Path(task_file)
        self.content = self._read_task_file()
    
    def _read_task_file(self) -> str:
        """Read TASK.md content"""
        if self.task_file.exists():
            return self.task_file.read_text()
        raise FileNotFoundError(f"TASK.md not found at {self.task_file}")
    
    def extract_subtask(self, subtask_id: str) -> Optional[SubtaskInfo]:
        """
        Extract a specific subtask by ID (e.g., "0.2.1")
        """
        # Pattern to match subtask sections
        pattern = rf"#### {re.escape(subtask_id)}\s+(.+?)(?=\n####|\n###|\Z)"
        match = re.search(pattern, self.content, re.DOTALL)
        
        if not match:
            return None
        
        section = match.group(0)
        title = match.group(1).strip()
        
        # Extract skills
        skills = re.findall(r'`@global_skills/([^/]+)/`', section)
        
        # Extract commands (code blocks)
        commands = re.findall(r'```(?:bash|json|yaml)?\n(.*?)```', section, re.DOTALL)
        
        # Extract checkboxes
        checkboxes = re.findall(r'- \[ \] (.+)', section)
        
        # Extract dependencies (look for "Dependencias:" or "Dependencias")
        deps_match = re.search(r'\*\*Dependencias:\*\*\s*(.+?)(?:\n\n|\n\*\*)', section)
        dependencies = []
        if deps_match:
            dependencies = [d.strip() for d in deps_match.group(1).split(',')]
        
        return SubtaskInfo(
            id=subtask_id,
            title=title,
            description=section,
            skills=skills,
            commands=commands,
            dependencies=dependencies,
            checkboxes=checkboxes
        )
    
    def extract_section(self, section_id: str) -> Optional[SubtaskInfo]:
        """
        Extract a section by ID (e.g., "0.1", "0.2", "1.1")
        Sections are ### level, subtasks are #### level
        """
        pattern = rf"### {re.escape(section_id)}\s+(.+?)(?=\n### |\n## |\Z)"
        match = re.search(pattern, self.content, re.DOTALL)
        
        if not match:
            return None
        
        section = match.group(0)
        title = match.group(1).strip().split('\n')[0]
        
        skills = re.findall(r'`@global_skills/([^/]+)/`', section)
        
        checkboxes = re.findall(r'- \[ \] (.+)', section)
        
        return SubtaskInfo(
            id=section_id,
            title=title,
            description=section,
            skills=skills,
            commands=[],
            dependencies=[],
            checkboxes=checkboxes
        )
    
    def _generate_git_flow_section(self, task_id: str) -> str:
        """
        Generate Git Flow section for the prompt
        """
        parts = task_id.split('.')
        section = '.'.join(parts[:2]) if len(parts) >= 2 else task_id
        section_name = {
            '0.1': 'git-repo',
            '0.2': 'config-files',
            '0.3': 'directories',
            '0.4': 'cicd',
            '0.5': 'supabase',
            '1.1': 'nestjs-backend',
            '1.2': 'agent-1-collector',
        }.get(section, f'section-{section}')
        
        return f"""
## 🔄 Flujo Git Obligatorio

### Al iniciar esta subtask:
```bash
# Verificar rama actual
git branch --show-current

# Si no estás en la rama feature de esta sección:
git checkout develop
git pull origin develop
git checkout -b feature/dato-{section}-{section_name}

# Si ya existe la rama feature:
git checkout feature/dato-{section}-{section_name}
```

### Al finalizar esta subtask (si pasó validaciones):
```bash
git add .
git commit -m "feat({section}): completar subtask {task_id}"
```

### Si algo falla:
```bash
# Crear rama fix
git checkout -b fix/dato-{task_id}-descripcion

# ... solucionar problema ...

git add . && git commit -m "fix: solucionar problema"
git checkout feature/dato-{section}-{section_name}
git merge fix/dato-{task_id}-descripcion
git branch -d fix/dato-{task_id}-descripcion
```

> ⚠️ **NUNCA commitear código que no pase los hooks de Husky**
"""
    
    def generate_prompt(self, task_id: str) -> str:
        """
        Generate an execution prompt for a subtask or section
        """
        is_section = len(task_id.split('.')) == 2
        
        if is_section:
            info = self.extract_section(task_id)
            task_type = "Sección"
        else:
            info = self.extract_subtask(task_id)
            task_type = "Subtask"
        
        if not info:
            return f"ERROR: {task_type} {task_id} not found"
        
        phase = f"FASE {task_id.split('.')[0]}"
        
        skills_section = '\n'.join([f"- `@global_skills/{s}/`" for s in info.skills])
        
        commands_section = '\n'.join([f"```bash\n{c}\n```" for c in info.commands])
        
        criteria_section = '\n'.join([f"- [ ] {cb}" for cb in info.checkboxes])
        
        deps_section = '\n'.join([f"- {d}" for d in info.dependencies]) if info.dependencies else "Ninguna"
        
        git_flow_section = self._generate_git_flow_section(task_id)
        
        prompt = f"""## Contexto
 - Proyecto: DATO (fact-checking político argentino)
 - Fase: {phase}
 - {task_type}: {info.id} - {info.title}
 
 ## Objetivo
 {info.title}
 
 ## Skills a usar
 {skills_section if skills_section else "Sin skills específicas"}
 
 ## Comandos
 {commands_section if commands_section else "Sin comandos específicos"}
 
 ## Criterios de Aceptación
 {criteria_section if criteria_section else "Ver descripción completa"}
 
 ## Dependencias
 {deps_section}
 
 {git_flow_section}
 
 ## Contenido Original de TASK.md
 ```
 {info.description}
 ```
 
 ---
 *Prompt generado por task-prompt-engineer skill*
 """
        return prompt
    
    def generate_all_phase_prompts(self, phase: str = "0") -> dict[str, str]:
        """
        Generate prompts for all subtasks in a phase
        """
        prompts = {}
        
        # Find all subtasks for the phase
        pattern = rf"#### ({re.escape(phase)}\.\d+(?:\.\d+)?)"
        matches = re.findall(pattern, self.content)
        
        for subtask_id in matches:
            prompts[subtask_id] = self.generate_prompt(subtask_id)
        
        return prompts


def main():
    """CLI interface"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python prompt_generator.py <task_id>")
        print("Examples:")
        print("  python prompt_generator.py 0.2.1  # Subtask level")
        print("  python prompt_generator.py 0.1    # Section level")
        sys.exit(1)
    
    task_id = sys.argv[1]
    engineer = TaskPromptEngineer("TASK.md")
    prompt = engineer.generate_prompt(task_id)
    print(prompt)


if __name__ == "__main__":
    main()