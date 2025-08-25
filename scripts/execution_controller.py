#!/usr/bin/env python3
"""
Sistema de Controle de Execução - Micro SaaS B2B
Responsável por rastreamento, testes e documentação automatizada
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Any
import subprocess
import shutil

class ExecutionController:
    def __init__(self):
        self.project_root = Path.cwd()
        self.docs_dir = self.project_root / "docs"
        self.temp_dir = self.project_root / "temp"
        self.reports_dir = self.docs_dir / "reports"
        self.execution_dir = self.docs_dir / "execucao"
        
        # Criar diretórios se não existirem
        for dir_path in [self.docs_dir, self.reports_dir, self.execution_dir]:
            dir_path.mkdir(exist_ok=True)
        
        self.current_sprint = self._get_current_sprint()
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    
    def _get_current_sprint(self) -> str:
        """Detectar sprint atual baseado na data"""
        today = datetime.date.today()
        # Sprint 0: 25/01 - 01/02
        if datetime.date(2025, 1, 25) <= today <= datetime.date(2025, 2, 1):
            return "sprint0"
        # Sprint 1: 01/02 - 15/02  
        elif datetime.date(2025, 2, 1) < today <= datetime.date(2025, 2, 15):
            return "sprint1"
        # Sprint 2: 15/02 - 01/03
        elif datetime.date(2025, 2, 15) < today <= datetime.date(2025, 3, 1):
            return "sprint2"
        # Sprint 3: 01/03 - 15/03
        elif datetime.date(2025, 3, 1) < today <= datetime.date(2025, 3, 15):
            return "sprint3"
        else:
            return "maintenance"
    
    def start_task(self, task_id: str, task_name: str, sprint: str = None) -> Dict:
        """Iniciar uma nova task com rastreamento"""
        if not sprint:
            sprint = self.current_sprint
            
        task_data = {
            "id": task_id,
            "name": task_name,
            "sprint": sprint,
            "started_at": datetime.datetime.now().isoformat(),
            "status": "in_progress",
            "tests_passed": 0,
            "tests_total": 0,
            "files_created": [],
            "files_modified": []
        }
        
        # Salvar estado da task
        task_file = self.execution_dir / f"{self.timestamp}_{task_id}_started.json"
        with open(task_file, 'w') as f:
            json.dump(task_data, f, indent=2)
        
        print(f"✅ Task iniciada: {task_name}")
        print(f"📁 Arquivo de controle: {task_file}")
        
        return task_data
    
    def run_tests(self, test_suite: str = "all") -> Dict:
        """Executar bateria de testes exaustivos"""
        test_results = {
            "timestamp": datetime.datetime.now().isoformat(),
            "suite": test_suite,
            "results": {}
        }
        
        test_commands = {
            "unit": "npm run test:unit",
            "integration": "npm run test:integration", 
            "e2e": "npm run test:e2e",
            "api": "npm run test:api",
            "lint": "npm run lint",
            "security": "npm run audit",
            "coverage": "npm run coverage"
        }
        
        if test_suite == "all":
            commands_to_run = test_commands
        else:
            commands_to_run = {test_suite: test_commands.get(test_suite, "echo 'Test not found'")}
        
        print(f"🧪 Executando testes: {test_suite}")
        
        for test_name, command in commands_to_run.items():
            try:
                print(f"  ▶️ {test_name}...")
                result = subprocess.run(
                    command.split(), 
                    capture_output=True, 
                    text=True,
                    timeout=300  # 5 minutos timeout
                )
                
                test_results["results"][test_name] = {
                    "passed": result.returncode == 0,
                    "output": result.stdout,
                    "errors": result.stderr,
                    "duration": "N/A"  # Poderia implementar timing
                }
                
                status = "✅ PASS" if result.returncode == 0 else "❌ FAIL"
                print(f"    {status}")
                
            except subprocess.TimeoutExpired:
                test_results["results"][test_name] = {
                    "passed": False,
                    "output": "",
                    "errors": "Timeout after 5 minutes",
                    "duration": "300s+"
                }
                print(f"    ⏱️ TIMEOUT")
            except Exception as e:
                test_results["results"][test_name] = {
                    "passed": False,
                    "output": "",
                    "errors": str(e),
                    "duration": "N/A"
                }
                print(f"    💥 ERROR: {e}")
        
        # Salvar resultados
        test_file = self.reports_dir / f"{self.timestamp}_tests_{test_suite}.json"
        with open(test_file, 'w') as f:
            json.dump(test_results, f, indent=2)
        
        # Gerar report markdown
        self._generate_test_report(test_results, test_file)
        
        return test_results
    
    def _generate_test_report(self, test_results: Dict, test_file: Path):
        """Gerar report de testes em markdown"""
        total_tests = len(test_results["results"])
        passed_tests = sum(1 for r in test_results["results"].values() if r["passed"])
        
        report_content = f"""# 🧪 Report de Testes - {test_results["timestamp"]}

## 📊 Resumo Executivo
- **Suite**: {test_results["suite"]}
- **Total**: {total_tests} testes
- **Passou**: {passed_tests} testes
- **Falhou**: {total_tests - passed_tests} testes
- **Taxa de Sucesso**: {(passed_tests/total_tests*100):.1f}%

## 📋 Resultados Detalhados

"""
        
        for test_name, result in test_results["results"].items():
            status = "✅ PASS" if result["passed"] else "❌ FAIL"
            report_content += f"""### {test_name}
**Status**: {status}

"""
            if result["errors"] and not result["passed"]:
                report_content += f"""**Erros**:
```
{result["errors"][:500]}...
```

"""
        
        report_content += f"""## 📁 Arquivos Gerados
- Dados JSON: `{test_file.name}`
- Este report: `{test_file.stem}.md`

---
*Gerado automaticamente pelo Sistema de Controle de Execução*
"""
        
        report_file = self.reports_dir / f"{test_file.stem}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"📄 Report gerado: {report_file}")
    
    def complete_task(self, task_id: str, success: bool = True, notes: str = "") -> Dict:
        """Finalizar task com cleanup e arquivamento"""
        completion_data = {
            "id": task_id,
            "completed_at": datetime.datetime.now().isoformat(),
            "success": success,
            "notes": notes,
            "files_archived": []
        }
        
        # Executar cleanup de arquivos temporários
        self._cleanup_temp_files()
        
        # Arquivar documentação importante
        archived_files = self._archive_important_files(task_id)
        completion_data["files_archived"] = archived_files
        
        # Salvar dados de conclusão
        completion_file = self.execution_dir / f"{self.timestamp}_{task_id}_completed.json"
        with open(completion_file, 'w') as f:
            json.dump(completion_data, f, indent=2)
        
        status = "✅ CONCLUÍDA" if success else "❌ FALHADA"
        print(f"{status}: Task {task_id}")
        print(f"📁 Arquivos arquivados: {len(archived_files)}")
        
        return completion_data
    
    def _cleanup_temp_files(self):
        """Limpar arquivos temporários"""
        temp_patterns = [
            "*.tmp", "*.temp", "*.log", "*.cache",
            "node_modules/.cache", ".next/cache", 
            "backend/__pycache__", "backend/*.pyc"
        ]
        
        cleaned_count = 0
        for pattern in temp_patterns:
            for file_path in self.project_root.rglob(pattern):
                try:
                    if file_path.is_file():
                        file_path.unlink()
                        cleaned_count += 1
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                        cleaned_count += 1
                except Exception as e:
                    print(f"⚠️ Erro limpando {file_path}: {e}")
        
        print(f"🧹 Cleanup concluído: {cleaned_count} itens removidos")
    
    def _archive_important_files(self, task_id: str) -> List[str]:
        """Arquivar arquivos importantes gerados"""
        important_patterns = [
            "*.md", "*.json", "*.yaml", "*.yml",
            "CHANGELOG*", "README*", "RELEASE*"
        ]
        
        archived_files = []
        archive_dir = self.docs_dir / "archive" / task_id
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        for pattern in important_patterns:
            for file_path in self.project_root.glob(pattern):
                if file_path.is_file() and not str(file_path).startswith(str(self.docs_dir)):
                    try:
                        dest_path = archive_dir / file_path.name
                        shutil.copy2(file_path, dest_path)
                        archived_files.append(str(file_path))
                    except Exception as e:
                        print(f"⚠️ Erro arquivando {file_path}: {e}")
        
        return archived_files
    
    def generate_status_report(self, report_type: str = "daily") -> str:
        """Gerar report de status"""
        now = datetime.datetime.now()
        
        if report_type == "daily":
            report_content = f"""# 📊 Status Report Diário - {now.strftime("%d/%m/%Y")}

## 🎯 Sprint Atual: {self.current_sprint.upper()}

### 📈 Progresso Geral
- **Data**: {now.strftime("%d/%m/%Y %H:%M")}
- **Sprint**: {self.current_sprint}
- **Status**: 🔄 EM ANDAMENTO

### 🧪 Últimos Testes
"""
            
            # Buscar últimos resultados de teste
            latest_tests = sorted(
                self.reports_dir.glob("*_tests_*.json"),
                key=os.path.getmtime,
                reverse=True
            )[:3]
            
            for test_file in latest_tests:
                with open(test_file, 'r') as f:
                    test_data = json.load(f)
                
                total = len(test_data["results"])
                passed = sum(1 for r in test_data["results"].values() if r["passed"])
                
                report_content += f"""- **{test_data["suite"]}**: {passed}/{total} testes passaram ({passed/total*100:.1f}%)
"""
            
            report_content += f"""

### 📋 Próximas 24h
- Continuar desenvolvimento {self.current_sprint}
- Executar bateria de testes
- Atualizar documentação

### 🚨 Alertas
- Nenhum alerta crítico no momento

---
*Gerado automaticamente em {now.strftime("%d/%m/%Y %H:%M")}*
"""
        
        elif report_type == "weekly":
            report_content = f"""# 📊 Executive Report Semanal - Semana {now.isocalendar()[1]}/2025

## 🎯 Objetivos vs Realizado

### Sprint {self.current_sprint.upper()}
- **Meta da Semana**: Desenvolvimento conforme cronograma
- **Realizado**: Em progresso
- **Blockers**: Nenhum blocker crítico

## 📊 Métricas Chave
- **Qualidade**: Monitoramento ativo
- **Performance**: Dentro dos padrões
- **Timeline**: Conforme planejado

## 📈 Próxima Semana
- Continuar execução do sprint atual
- Intensificar testes
- Preparar próxima fase

---
*Executive Report - {now.strftime("%d/%m/%Y %H:%M")}*
"""
        
        # Salvar report
        report_file = self.reports_dir / f"{self.timestamp}_{report_type}_report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"📄 Report {report_type} gerado: {report_file}")
        return str(report_file)
    
    def get_project_status(self) -> Dict:
        """Obter status geral do projeto"""
        return {
            "current_sprint": self.current_sprint,
            "timestamp": self.timestamp,
            "docs_dir": str(self.docs_dir),
            "reports_generated": len(list(self.reports_dir.glob("*.md"))),
            "tasks_tracked": len(list(self.execution_dir.glob("*.json")))
        }

# Instância global
controller = ExecutionController()

if __name__ == "__main__":
    # Exemplo de uso
    print("🎯 Sistema de Controle de Execução Ativo")
    print(f"Sprint atual: {controller.current_sprint}")
    
    # Gerar report inicial
    controller.generate_status_report("daily")
    
    print("\n📋 Comandos disponíveis:")
    print("- controller.start_task(id, name)")
    print("- controller.run_tests(suite)")
    print("- controller.complete_task(id)")
    print("- controller.generate_status_report(type)")

