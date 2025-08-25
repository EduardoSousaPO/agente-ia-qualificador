#!/usr/bin/env python3
"""
Sistema de Cleanup e Arquivamento Automático
Responsável por limpeza de arquivos temporários e arquivamento de documentação
"""

import os
import shutil
import datetime
from pathlib import Path
from typing import List, Dict
import json

class CleanupArchiver:
    def __init__(self):
        self.project_root = Path.cwd()
        self.docs_dir = self.project_root / "docs"
        self.archive_dir = self.docs_dir / "archive"
        self.temp_patterns = [
            "*.tmp", "*.temp", "*.log", "*.cache", "*.bak",
            "__pycache__", "*.pyc", ".pytest_cache",
            "node_modules/.cache", ".next/cache", ".next/trace",
            "*.swp", "*.swo", "*~", ".DS_Store", "Thumbs.db"
        ]
        
        # Criar diretórios necessários
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    
    def cleanup_temp_files(self) -> Dict:
        """Limpeza completa de arquivos temporários"""
        print("🧹 Iniciando limpeza de arquivos temporários...")
        
        cleanup_stats = {
            "timestamp": self.timestamp,
            "files_removed": 0,
            "dirs_removed": 0,
            "space_freed": 0,
            "patterns_cleaned": []
        }
        
        for pattern in self.temp_patterns:
            pattern_stats = self._clean_pattern(pattern)
            cleanup_stats["files_removed"] += pattern_stats["files"]
            cleanup_stats["dirs_removed"] += pattern_stats["dirs"]
            cleanup_stats["space_freed"] += pattern_stats["space"]
            
            if pattern_stats["files"] > 0 or pattern_stats["dirs"] > 0:
                cleanup_stats["patterns_cleaned"].append({
                    "pattern": pattern,
                    "files": pattern_stats["files"],
                    "dirs": pattern_stats["dirs"],
                    "space": pattern_stats["space"]
                })
        
        # Limpeza específica de diretórios conhecidos
        specific_cleanup = self._clean_specific_dirs()
        cleanup_stats["files_removed"] += specific_cleanup["files"]
        cleanup_stats["dirs_removed"] += specific_cleanup["dirs"]
        cleanup_stats["space_freed"] += specific_cleanup["space"]
        
        # Salvar log de limpeza
        self._save_cleanup_log(cleanup_stats)
        
        print(f"✅ Limpeza concluída:")
        print(f"   📁 Arquivos removidos: {cleanup_stats['files_removed']}")
        print(f"   📂 Diretórios removidos: {cleanup_stats['dirs_removed']}")
        print(f"   💾 Espaço liberado: {self._format_size(cleanup_stats['space_freed'])}")
        
        return cleanup_stats
    
    def _clean_pattern(self, pattern: str) -> Dict:
        """Limpar arquivos por padrão específico"""
        stats = {"files": 0, "dirs": 0, "space": 0}
        
        try:
            for path in self.project_root.rglob(pattern):
                # Pular diretórios importantes
                if any(important in str(path) for important in [".git", "node_modules", ".env"]):
                    continue
                
                try:
                    if path.is_file():
                        stats["space"] += path.stat().st_size
                        path.unlink()
                        stats["files"] += 1
                    elif path.is_dir() and pattern in ["__pycache__", ".pytest_cache"]:
                        stats["space"] += sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
                        shutil.rmtree(path)
                        stats["dirs"] += 1
                except (PermissionError, OSError) as e:
                    print(f"⚠️ Não foi possível remover {path}: {e}")
                    
        except Exception as e:
            print(f"⚠️ Erro limpando padrão {pattern}: {e}")
        
        return stats
    
    def _clean_specific_dirs(self) -> Dict:
        """Limpeza de diretórios específicos conhecidos"""
        stats = {"files": 0, "dirs": 0, "space": 0}
        
        specific_dirs = [
            self.project_root / "backend" / "__pycache__",
            self.project_root / "frontend" / ".next" / "cache",
            self.project_root / "frontend" / "node_modules" / ".cache",
            self.project_root / "temp",
            self.project_root / "tmp"
        ]
        
        for dir_path in specific_dirs:
            if dir_path.exists():
                try:
                    if dir_path.is_dir():
                        stats["space"] += sum(f.stat().st_size for f in dir_path.rglob('*') if f.is_file())
                        shutil.rmtree(dir_path)
                        stats["dirs"] += 1
                except (PermissionError, OSError) as e:
                    print(f"⚠️ Não foi possível remover {dir_path}: {e}")
        
        return stats
    
    def archive_important_files(self, task_id: str = None) -> Dict:
        """Arquivar arquivos importantes com timestamp"""
        if not task_id:
            task_id = f"archive_{self.timestamp}"
        
        print(f"📦 Arquivando arquivos importantes para: {task_id}")
        
        archive_stats = {
            "timestamp": self.timestamp,
            "task_id": task_id,
            "files_archived": 0,
            "total_size": 0,
            "categories": {}
        }
        
        # Criar diretório de arquivo específico
        task_archive_dir = self.archive_dir / task_id
        task_archive_dir.mkdir(exist_ok=True)
        
        # Categorias de arquivos importantes
        important_categories = {
            "documentation": ["*.md", "*.txt", "README*", "CHANGELOG*"],
            "configuration": ["*.json", "*.yaml", "*.yml", "*.toml", "*.ini"],
            "scripts": ["*.py", "*.sh", "*.bat", "*.ps1"],
            "reports": ["*report*", "*status*", "*log*"],
            "releases": ["RELEASE*", "VERSION*", "NOTES*"]
        }
        
        for category, patterns in important_categories.items():
            category_dir = task_archive_dir / category
            category_dir.mkdir(exist_ok=True)
            
            category_stats = {"files": 0, "size": 0}
            
            for pattern in patterns:
                for file_path in self.project_root.glob(pattern):
                    if (file_path.is_file() and 
                        not str(file_path).startswith(str(self.docs_dir)) and
                        file_path.name not in [".env", ".env.local"]):
                        
                        try:
                            dest_path = category_dir / file_path.name
                            shutil.copy2(file_path, dest_path)
                            
                            file_size = file_path.stat().st_size
                            category_stats["files"] += 1
                            category_stats["size"] += file_size
                            
                        except Exception as e:
                            print(f"⚠️ Erro arquivando {file_path}: {e}")
            
            if category_stats["files"] > 0:
                archive_stats["categories"][category] = category_stats
                archive_stats["files_archived"] += category_stats["files"]
                archive_stats["total_size"] += category_stats["size"]
        
        # Criar índice do arquivo
        self._create_archive_index(task_archive_dir, archive_stats)
        
        print(f"✅ Arquivamento concluído:")
        print(f"   📁 Arquivos arquivados: {archive_stats['files_archived']}")
        print(f"   💾 Tamanho total: {self._format_size(archive_stats['total_size'])}")
        print(f"   📂 Localização: {task_archive_dir}")
        
        return archive_stats
    
    def _create_archive_index(self, archive_dir: Path, stats: Dict):
        """Criar índice do arquivo"""
        index_content = f"""# 📦 Índice do Arquivo - {stats['task_id']}

**Data**: {stats['timestamp']}  
**Arquivos**: {stats['files_archived']}  
**Tamanho**: {self._format_size(stats['total_size'])}

## 📋 Categorias

"""
        
        for category, category_stats in stats["categories"].items():
            index_content += f"""### {category.title()}
- **Arquivos**: {category_stats['files']}
- **Tamanho**: {self._format_size(category_stats['size'])}

"""
        
        index_content += f"""## 📁 Estrutura
```
{stats['task_id']}/
"""
        
        for category in stats["categories"].keys():
            index_content += f"├── {category}/\n"
        
        index_content += f"""└── INDEX.md (este arquivo)
```

---
*Gerado automaticamente em {stats['timestamp']}*
"""
        
        index_file = archive_dir / "INDEX.md"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
    
    def _save_cleanup_log(self, stats: Dict):
        """Salvar log detalhado da limpeza"""
        log_file = self.docs_dir / "reports" / f"cleanup_log_{self.timestamp}.json"
        log_file.parent.mkdir(exist_ok=True)
        
        with open(log_file, 'w') as f:
            json.dump(stats, f, indent=2)
        
        # Criar também versão markdown
        md_content = f"""# 🧹 Log de Limpeza - {stats['timestamp']}

## 📊 Estatísticas Gerais
- **Arquivos removidos**: {stats['files_removed']}
- **Diretórios removidos**: {stats['dirs_removed']}
- **Espaço liberado**: {self._format_size(stats['space_freed'])}

## 📋 Padrões Limpos

"""
        
        for pattern_info in stats["patterns_cleaned"]:
            md_content += f"""### {pattern_info['pattern']}
- Arquivos: {pattern_info['files']}
- Diretórios: {pattern_info['dirs']}
- Espaço: {self._format_size(pattern_info['space'])}

"""
        
        md_content += """---
*Log gerado automaticamente pelo Sistema de Cleanup*
"""
        
        md_file = self.docs_dir / "reports" / f"cleanup_log_{self.timestamp}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"📄 Log salvo: {md_file}")
    
    def _format_size(self, size_bytes: int) -> str:
        """Formatar tamanho em bytes para formato legível"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        size = float(size_bytes)
        
        while size >= 1024.0 and i < len(size_names) - 1:
            size /= 1024.0
            i += 1
        
        return f"{size:.1f} {size_names[i]}"
    
    def full_maintenance(self, task_id: str = None) -> Dict:
        """Executar manutenção completa"""
        print("🔧 Iniciando manutenção completa do projeto...")
        
        # 1. Limpeza de arquivos temporários
        cleanup_stats = self.cleanup_temp_files()
        
        # 2. Arquivamento de arquivos importantes
        archive_stats = self.archive_important_files(task_id)
        
        # 3. Estatísticas consolidadas
        maintenance_stats = {
            "timestamp": self.timestamp,
            "task_id": task_id or f"maintenance_{self.timestamp}",
            "cleanup": cleanup_stats,
            "archive": archive_stats,
            "summary": {
                "temp_files_removed": cleanup_stats["files_removed"],
                "space_freed": cleanup_stats["space_freed"],
                "files_archived": archive_stats["files_archived"],
                "archive_size": archive_stats["total_size"]
            }
        }
        
        # Salvar relatório consolidado
        self._save_maintenance_report(maintenance_stats)
        
        print("\n🎉 Manutenção completa finalizada!")
        return maintenance_stats
    
    def _save_maintenance_report(self, stats: Dict):
        """Salvar relatório consolidado de manutenção"""
        report_content = f"""# 🔧 Relatório de Manutenção - {stats['timestamp']}

## 📊 Resumo Executivo
- **Task ID**: {stats['task_id']}
- **Arquivos temporários removidos**: {stats['summary']['temp_files_removed']}
- **Espaço liberado**: {self._format_size(stats['summary']['space_freed'])}
- **Arquivos arquivados**: {stats['summary']['files_archived']}
- **Tamanho do arquivo**: {self._format_size(stats['summary']['archive_size'])}

## 🧹 Limpeza de Arquivos Temporários
- **Arquivos removidos**: {stats['cleanup']['files_removed']}
- **Diretórios removidos**: {stats['cleanup']['dirs_removed']}
- **Espaço total liberado**: {self._format_size(stats['cleanup']['space_freed'])}

### Padrões Limpos
"""
        
        for pattern_info in stats['cleanup']['patterns_cleaned']:
            report_content += f"- `{pattern_info['pattern']}`: {pattern_info['files']} arquivos, {self._format_size(pattern_info['space'])}\n"
        
        report_content += f"""

## 📦 Arquivamento
- **Arquivos arquivados**: {stats['archive']['files_archived']}
- **Tamanho total**: {self._format_size(stats['archive']['total_size'])}
- **Localização**: `docs/archive/{stats['task_id']}/`

### Categorias Arquivadas
"""
        
        for category, category_stats in stats['archive']['categories'].items():
            report_content += f"- **{category.title()}**: {category_stats['files']} arquivos, {self._format_size(category_stats['size'])}\n"
        
        report_content += f"""

## 📁 Estrutura Pós-Manutenção
```
docs/
├── archive/
│   └── {stats['task_id']}/
│       ├── documentation/
│       ├── configuration/
│       ├── scripts/
│       └── INDEX.md
└── reports/
    ├── cleanup_log_{stats['timestamp']}.md
    └── maintenance_report_{stats['timestamp']}.md
```

---
*Relatório gerado automaticamente em {stats['timestamp']}*
"""
        
        report_file = self.docs_dir / "reports" / f"maintenance_report_{stats['timestamp']}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"📄 Relatório de manutenção: {report_file}")

# Instância global
cleaner = CleanupArchiver()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "cleanup":
            cleaner.cleanup_temp_files()
        elif sys.argv[1] == "archive":
            task_id = sys.argv[2] if len(sys.argv) > 2 else None
            cleaner.archive_important_files(task_id)
        elif sys.argv[1] == "full":
            task_id = sys.argv[2] if len(sys.argv) > 2 else None
            cleaner.full_maintenance(task_id)
    else:
        # Executar manutenção completa por padrão
        cleaner.full_maintenance()

