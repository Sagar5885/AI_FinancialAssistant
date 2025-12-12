#!/usr/bin/env python
"""
Project validation script - Verifies all components are properly set up
"""
import os
import sys
from pathlib import Path
import importlib.util

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


class ProjectValidator:
    """Validates project structure and dependencies"""

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.successes = []
        self.root_path = Path(__file__).parent

    def print_header(self, text):
        """Print section header"""
        print(f"\n{BLUE}{'='*60}")
        print(f"{text}")
        print(f"{'='*60}{RESET}\n")

    def print_success(self, text):
        """Print success message"""
        print(f"{GREEN}✓ {text}{RESET}")
        self.successes.append(text)

    def print_error(self, text):
        """Print error message"""
        print(f"{RED}✗ {text}{RESET}")
        self.errors.append(text)

    def print_warning(self, text):
        """Print warning message"""
        print(f"{YELLOW}⚠ {text}{RESET}")
        self.warnings.append(text)

    def check_directory_structure(self):
        """Verify project directory structure"""
        self.print_header("Checking Directory Structure")

        required_dirs = [
            'src',
            'src/agents',
            'src/core',
            'src/data',
            'src/rag',
            'src/workflow',
            'src/web_app',
            'src/utils',
            'tests',
            'config',
            'docs'
        ]

        for dir_name in required_dirs:
            dir_path = self.root_path / dir_name
            if dir_path.exists():
                self.print_success(f"Directory exists: {dir_name}/")
            else:
                self.print_error(f"Missing directory: {dir_name}/")

    def check_required_files(self):
        """Verify required files exist"""
        self.print_header("Checking Required Files")

        required_files = {
            'requirements.txt': 'Python dependencies',
            'main.py': 'Main entry point',
            'README.md': 'Documentation',
            'QUICK_START.md': 'Quick start guide',
            'Dockerfile': 'Docker configuration',
            'docker-compose.yml': 'Docker compose',
            '.env.example': 'Environment template',
            'config/config.yaml': 'Configuration file',
            'docs/ARCHITECTURE.md': 'Architecture docs',
            'tests/test_suite.py': 'Test suite'
        }

        for file_name, description in required_files.items():
            file_path = self.root_path / file_name
            if file_path.exists():
                self.print_success(f"{file_name} ({description})")
            else:
                self.print_error(f"Missing {file_name} ({description})")

    def check_python_files(self):
        """Verify all Python source files"""
        self.print_header("Checking Python Source Files")

        required_modules = {
            'src/__init__.py': 'Main package init',
            'src/agents/__init__.py': 'Agents package',
            'src/agents/base_agent.py': 'Base agent',
            'src/agents/finance_qa_agent.py': 'Finance QA agent',
            'src/agents/portfolio_analysis_agent.py': 'Portfolio agent',
            'src/agents/market_analysis_agent.py': 'Market agent',
            'src/agents/goal_planning_agent.py': 'Goal planning agent',
            'src/agents/news_synthesizer_agent.py': 'News agent',
            'src/agents/tax_education_agent.py': 'Tax agent',
            'src/core/__init__.py': 'Core package',
            'src/core/llm_client.py': 'LLM client',
            'src/rag/__init__.py': 'RAG package',
            'src/rag/rag_system.py': 'RAG system',
            'src/workflow/__init__.py': 'Workflow package',
            'src/workflow/langgraph_workflow.py': 'Workflow orchestration',
            'src/web_app/__init__.py': 'Web app package',
            'src/web_app/streamlit_app.py': 'Streamlit interface',
            'src/utils/__init__.py': 'Utils package',
            'src/utils/market_data.py': 'Market data provider',
            'src/data/__init__.py': 'Data package',
            'src/data/knowledge_base_builder.py': 'Knowledge base',
        }

        for file_name, description in required_modules.items():
            file_path = self.root_path / file_name
            if file_path.exists():
                self.print_success(f"{file_name} ({description})")
            else:
                self.print_error(f"Missing {file_name} ({description})")

    def check_dependencies(self):
        """Check Python dependencies"""
        self.print_header("Checking Dependencies")

        required_packages = [
            'langchain',
            'google.generativeai',
            'streamlit',
            'pydantic',
            'pyyaml',
        ]

        optional_packages = [
            'sentence_transformers',
            'faiss',
            'yfinance',
            'pytest',
        ]

        print("Required packages:")
        for package in required_packages:
            if self._check_package(package):
                self.print_success(f"Package available: {package}")
            else:
                self.print_error(f"Missing package: {package}")

        print("\nOptional packages (nice to have):")
        for package in optional_packages:
            if self._check_package(package):
                self.print_success(f"Package available: {package}")
            else:
                self.print_warning(f"Missing optional: {package}")

    def _check_package(self, package_name):
        """Check if package is available"""
        try:
            # Handle nested imports
            parts = package_name.split('.')
            module_name = parts[0]
            spec = importlib.util.find_spec(module_name)
            return spec is not None
        except (ImportError, ModuleNotFoundError, ValueError):
            return False

    def check_environment(self):
        """Check environment setup"""
        self.print_header("Checking Environment")

        # Check Python version
        python_version = sys.version_info
        if python_version.major == 3 and python_version.minor >= 9:
            self.print_success(f"Python version: {python_version.major}.{python_version.minor}")
        else:
            self.print_error(f"Python 3.9+ required, found: {python_version.major}.{python_version.minor}")

        # Check API keys
        api_keys = {
            'GOOGLE_API_KEY': 'Google Gemini',
            'OPENAI_API_KEY': 'OpenAI (optional)',
            'ALPHA_VANTAGE_API_KEY': 'Alpha Vantage (optional)',
        }

        print("\nAPI Keys:")
        for key, description in api_keys.items():
            if os.getenv(key):
                self.print_success(f"{description} key configured")
            else:
                self.print_warning(f"{description} key not set (use .env file)")

    def check_knowledge_base(self):
        """Check knowledge base"""
        self.print_header("Checking Knowledge Base")

        kb_path = self.root_path / 'src' / 'data' / 'knowledge_base'
        if kb_path.exists():
            json_files = list(kb_path.glob('*.json'))
            if json_files:
                self.print_success(f"Knowledge base initialized with {len(json_files)} categories")
            else:
                self.print_warning("Knowledge base directory exists but no articles found")
                self.print_warning("Run: python main.py --mode setup")
        else:
            self.print_warning("Knowledge base not initialized")
            self.print_warning("Run: python main.py --mode setup")

    def check_config(self):
        """Check configuration"""
        self.print_header("Checking Configuration")

        config_file = self.root_path / 'config' / 'config.yaml'
        if config_file.exists():
            self.print_success("Configuration file exists")
            
            # Try to parse YAML
            try:
                import yaml
                with open(config_file) as f:
                    config = yaml.safe_load(f)
                    self.print_success("Configuration is valid YAML")
                    
                    # Check key sections
                    required_sections = ['app', 'llm', 'agents']
                    for section in required_sections:
                        if section in config:
                            self.print_success(f"Config section found: {section}")
                        else:
                            self.print_warning(f"Config section missing: {section}")
            except Exception as e:
                self.print_error(f"Error parsing config: {e}")
        else:
            self.print_error("Configuration file not found")

    def generate_report(self):
        """Generate validation report"""
        self.print_header("Validation Report")

        print(f"{GREEN}Successes: {len(self.successes)}{RESET}")
        print(f"{YELLOW}Warnings: {len(self.warnings)}{RESET}")
        print(f"{RED}Errors: {len(self.errors)}{RESET}\n")

        if self.errors:
            print(f"{RED}Critical Issues:{RESET}")
            for error in self.errors:
                print(f"  • {error}")

        if self.warnings:
            print(f"\n{YELLOW}Warnings:{RESET}")
            for warning in self.warnings[:5]:  # Show first 5
                print(f"  • {warning}")

        # Summary
        print(f"\n{BLUE}{'='*60}")
        if not self.errors:
            print(f"{GREEN}✓ Project validation PASSED{RESET}")
            print(f"Ready to run: python main.py --mode web")
        else:
            print(f"{RED}✗ Project validation FAILED{RESET}")
            print(f"Please fix the above errors and run validation again")
        print(f"{BLUE}{'='*60}{RESET}\n")

        return len(self.errors) == 0

    def run_all_checks(self):
        """Run all validation checks"""
        print(f"{BLUE}AI Finance Assistant - Project Validation{RESET}")

        self.check_directory_structure()
        self.check_required_files()
        self.check_python_files()
        self.check_dependencies()
        self.check_environment()
        self.check_knowledge_base()
        self.check_config()
        self.generate_report()

        return len(self.errors) == 0


def main():
    """Main validation function"""
    validator = ProjectValidator()
    success = validator.run_all_checks()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
