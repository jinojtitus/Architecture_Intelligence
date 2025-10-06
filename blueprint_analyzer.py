import os
import json
import yaml
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import re
import requests
from urllib.parse import urlparse
from utils import TechnologyDetector, DataFlowAnalyzer, ArchitectureGenerator, PatternManager

class BlueprintAnalyzer:
    """Comprehensive blueprint and Git repository analyzer"""
    
    def __init__(self):
        self.technology_detector = TechnologyDetector()
        self.pattern_manager = PatternManager()
        self.architecture_generator = ArchitectureGenerator()
        self.data_flow_analyzer = DataFlowAnalyzer()
        
        # Approved technology categories
        self.approved_technologies = {
            "Frontend": ["React", "Vue.js", "Angular", "Next.js", "Nuxt.js", "Svelte"],
            "Backend": ["Node.js", "Python", "Java", "C#", "Go", "Rust", "Express", "FastAPI", "Spring Boot"],
            "Database": ["PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch", "Cassandra"],
            "DevOps": ["Docker", "Kubernetes", "Jenkins", "GitLab CI", "GitHub Actions", "Terraform"],
            "Cloud": ["AWS", "Azure", "GCP", "Heroku", "DigitalOcean"],
            "Security": ["OAuth", "JWT", "HTTPS", "SSL", "TLS", "Auth0", "Keycloak"],
            "Testing": ["Jest", "Cypress", "Selenium", "Pytest", "JUnit", "Mocha"]
        }
        
        # Core technologies (must-have)
        self.core_technologies = {
            "Frontend": ["React", "Vue.js", "Angular"],
            "Backend": ["Node.js", "Python", "Java"],
            "Database": ["PostgreSQL", "MySQL", "MongoDB"],
            "DevOps": ["Docker"],
            "Cloud": ["AWS", "Azure", "GCP"],
            "Security": ["HTTPS", "JWT", "OAuth"]
        }
        
        # Non-approved technologies (deprecated or risky)
        self.non_approved_technologies = {
            "jQuery", "Bootstrap 3", "AngularJS", "Backbone.js", "Lodash", "Moment.js",
            "PHP 5", "MySQL 5.6", "MongoDB 3.6", "Node.js 12", "Python 2.7"
        }

    def analyze_blueprint(self, blueprint_path: str) -> Dict[str, Any]:
        """Analyze a blueprint file or directory"""
        if os.path.isfile(blueprint_path):
            return self._analyze_file(blueprint_path)
        elif os.path.isdir(blueprint_path):
            return self._analyze_directory(blueprint_path)
        else:
            raise ValueError(f"Invalid path: {blueprint_path}")

    def analyze_git_repo(self, repo_url: str, branch: str = "main") -> Dict[str, Any]:
        """Analyze a Git repository"""
        temp_dir = tempfile.mkdtemp()
        try:
            # Clone the repository
            clone_cmd = ["git", "clone", "--depth", "1", "--branch", branch, repo_url, temp_dir]
            result = subprocess.run(clone_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"Failed to clone repository: {result.stderr}")
            
            return self._analyze_directory(temp_dir)
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def _analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        file_type = Path(file_path).suffix[1:]
        technologies = self.technology_detector.detect_technologies(content, file_type)
        
        return {
            "type": "file",
            "path": file_path,
            "technologies": technologies,
            "analysis": self._analyze_technologies(technologies),
            "data_flow": self._extract_data_flow(content),
            "security_analysis": self._analyze_security(content),
            "integration_points": self._extract_integration_points(content)
        }

    def _analyze_directory(self, dir_path: str) -> Dict[str, Any]:
        """Analyze a directory structure"""
        all_technologies = []
        data_flows = []
        security_issues = []
        integration_points = []
        
        # Scan all relevant files
        for root, dirs, files in os.walk(dir_path):
            # Skip common directories
            dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '__pycache__', '.venv', 'venv'}]
            
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = Path(file).suffix[1:].lower()
                
                # Only analyze relevant files
                if file_ext in {'json', 'js', 'ts', 'py', 'java', 'go', 'rs', 'yaml', 'yml', 'toml', 'xml', 'md'}:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Detect technologies
                        file_technologies = self.technology_detector.detect_technologies(content, file_ext)
                        all_technologies.extend(file_technologies)
                        
                        # Extract data flows
                        flows = self._extract_data_flow(content)
                        data_flows.extend(flows)
                        
                        # Security analysis
                        security = self._analyze_security(content)
                        security_issues.extend(security)
                        
                        # Integration points
                        integrations = self._extract_integration_points(content)
                        integration_points.extend(integrations)
                        
                    except Exception as e:
                        print(f"Error analyzing {file_path}: {e}")
                        continue
        
        # Remove duplicates
        unique_technologies = self._deduplicate_technologies(all_technologies)
        
        return {
            "type": "directory",
            "path": dir_path,
            "technologies": unique_technologies,
            "analysis": self._analyze_technologies(unique_technologies),
            "data_flow": data_flows,
            "security_analysis": security_issues,
            "integration_points": integration_points,
            "architecture": self._generate_architecture_analysis(unique_technologies, data_flows)
        }

    def _analyze_technologies(self, technologies: List[Dict]) -> Dict[str, Any]:
        """Analyze technology compliance and categorization"""
        approved = []
        core = []
        non_approved = []
        unknown = []
        
        for tech in technologies:
            tech_name = tech['name']
            category = tech['category']
            
            # Check if approved
            if category in self.approved_technologies and tech_name in self.approved_technologies[category]:
                approved.append(tech)
                # Check if core
                if category in self.core_technologies and tech_name in self.core_technologies[category]:
                    core.append(tech)
            elif tech_name in self.non_approved_technologies:
                non_approved.append(tech)
            else:
                unknown.append(tech)
        
        # Calculate compliance score
        total_techs = len(technologies)
        approved_count = len(approved)
        core_count = len(core)
        non_approved_count = len(non_approved)
        
        compliance_score = 0
        if total_techs > 0:
            compliance_score = int((approved_count / total_techs) * 100)
            # Penalty for non-approved
            compliance_score -= non_approved_count * 10
            compliance_score = max(0, compliance_score)
        
        return {
            "approved": approved,
            "core": core,
            "non_approved": non_approved,
            "unknown": unknown,
            "compliance_score": compliance_score,
            "total_technologies": total_techs,
            "approved_count": approved_count,
            "core_count": core_count,
            "non_approved_count": non_approved_count,
            "recommendations": self._generate_recommendations(approved, core, non_approved, unknown)
        }

    def _extract_data_flow(self, content: str) -> List[Dict]:
        """Extract data flow patterns from code"""
        flows = []
        
        # API calls
        api_patterns = [
            r'fetch\s*\(\s*["\']([^"\']+)["\']',
            r'axios\.[a-z]+\s*\(\s*["\']([^"\']+)["\']',
            r'\.get\s*\(\s*["\']([^"\']+)["\']',
            r'\.post\s*\(\s*["\']([^"\']+)["\']',
            r'\.put\s*\(\s*["\']([^"\']+)["\']',
            r'\.delete\s*\(\s*["\']([^"\']+)["\']'
        ]
        
        for pattern in api_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                flows.append({
                    "type": "API Call",
                    "endpoint": match,
                    "security_level": "Medium",
                    "description": f"API call to {match}"
                })
        
        # Database queries
        db_patterns = [
            r'SELECT\s+.*?\s+FROM\s+(\w+)',
            r'INSERT\s+INTO\s+(\w+)',
            r'UPDATE\s+(\w+)\s+SET',
            r'DELETE\s+FROM\s+(\w+)',
            r'\.find\s*\(\s*\{([^}]+)\}',
            r'\.findOne\s*\(\s*\{([^}]+)\}'
        ]
        
        for pattern in db_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                flows.append({
                    "type": "Database Query",
                    "table": match,
                    "security_level": "High",
                    "description": f"Database operation on {match}"
                })
        
        return flows

    def _analyze_security(self, content: str) -> List[Dict]:
        """Analyze security aspects of the code"""
        security_issues = []
        
        # Check for hardcoded secrets
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']'
        ]
        
        for pattern in secret_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                security_issues.append({
                    "type": "Hardcoded Secret",
                    "severity": "High",
                    "description": f"Potential hardcoded secret found: {match[:50]}...",
                    "recommendation": "Use environment variables or secure secret management"
                })
        
        # Check for SQL injection vulnerabilities
        sql_patterns = [
            r'query\s*\(\s*["\'][^"\']*\+[^"\']*["\']',
            r'execute\s*\(\s*["\'][^"\']*\+[^"\']*["\']'
        ]
        
        for pattern in sql_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                security_issues.append({
                    "type": "SQL Injection Risk",
                    "severity": "High",
                    "description": f"Potential SQL injection vulnerability: {match[:50]}...",
                    "recommendation": "Use parameterized queries or prepared statements"
                })
        
        # Check for HTTPS usage
        if 'http://' in content and 'https://' not in content:
            security_issues.append({
                "type": "Insecure HTTP",
                "severity": "Medium",
                "description": "HTTP protocol detected without HTTPS",
                "recommendation": "Use HTTPS for all external communications"
            })
        
        return security_issues

    def _extract_integration_points(self, content: str) -> List[Dict]:
        """Extract integration points from code"""
        integrations = []
        
        # External API integrations
        api_patterns = [
            r'https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            r'api\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        ]
        
        for pattern in api_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                integrations.append({
                    "type": "External API",
                    "endpoint": match,
                    "description": f"Integration with external API: {match}",
                    "security_level": "Medium"
                })
        
        # Database connections
        db_patterns = [
            r'mongodb://[^\s\'"]+',
            r'postgresql://[^\s\'"]+',
            r'mysql://[^\s\'"]+',
            r'redis://[^\s\'"]+'
        ]
        
        for pattern in db_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                integrations.append({
                    "type": "Database Connection",
                    "endpoint": match,
                    "description": f"Database connection: {match}",
                    "security_level": "High"
                })
        
        return integrations

    def _generate_architecture_analysis(self, technologies: List[Dict], data_flows: List[Dict]) -> Dict[str, Any]:
        """Generate architecture analysis"""
        # Determine architecture type
        arch_type = "Unknown"
        if any(tech['name'] in ['Docker', 'Kubernetes'] for tech in technologies):
            arch_type = "Microservices"
        elif any(tech['name'] in ['Express', 'Django', 'Flask'] for tech in technologies):
            arch_type = "Monolithic"
        elif any(tech['name'] in ['AWS Lambda', 'Azure Functions', 'Google Cloud Functions'] for tech in technologies):
            arch_type = "Serverless"
        
        # Generate layers
        layers = self._generate_architecture_layers(technologies)
        
        # Generate integration diagram
        integration_diagram = self._generate_integration_diagram(technologies, data_flows)
        
        # Generate security diagram
        security_diagram = self._generate_security_diagram(technologies, data_flows)
        
        return {
            "type": arch_type,
            "layers": layers,
            "integration_diagram": integration_diagram,
            "security_diagram": security_diagram,
            "complexity_score": self._calculate_complexity_score(technologies, data_flows)
        }

    def _generate_architecture_layers(self, technologies: List[Dict]) -> List[Dict]:
        """Generate architecture layers based on technologies"""
        layers = []
        
        # Frontend layer
        frontend_techs = [tech for tech in technologies if tech['category'] == 'Frontend']
        if frontend_techs:
            layers.append({
                "name": "Presentation Layer",
                "technologies": [tech['name'] for tech in frontend_techs],
                "description": "User interface and client-side logic"
            })
        
        # API layer
        api_techs = [tech for tech in technologies if tech['category'] == 'Backend']
        if api_techs:
            layers.append({
                "name": "API Layer",
                "technologies": [tech['name'] for tech in api_techs],
                "description": "API endpoints and business logic"
            })
        
        # Data layer
        data_techs = [tech for tech in technologies if tech['category'] == 'Database']
        if data_techs:
            layers.append({
                "name": "Data Layer",
                "technologies": [tech['name'] for tech in data_techs],
                "description": "Data storage and persistence"
            })
        
        return layers

    def _generate_integration_diagram(self, technologies: List[Dict], data_flows: List[Dict]) -> Dict[str, Any]:
        """Generate integration diagram data"""
        nodes = []
        edges = []
        
        # Add technology nodes
        for tech in technologies:
            nodes.append({
                "id": tech['name'],
                "label": tech['name'],
                "category": tech['category'],
                "confidence": tech['confidence']
            })
        
        # Add data flow edges
        for flow in data_flows:
            if 'endpoint' in flow:
                edges.append({
                    "source": "Application",
                    "target": flow['endpoint'],
                    "type": flow['type'],
                    "security_level": flow['security_level']
                })
        
        return {
            "nodes": nodes,
            "edges": edges,
            "title": "Integration Architecture"
        }

    def _generate_security_diagram(self, technologies: List[Dict], data_flows: List[Dict]) -> Dict[str, Any]:
        """Generate security diagram data"""
        security_components = []
        threats = []
        
        # Identify security components
        for tech in technologies:
            if tech['category'] == 'Security':
                security_components.append({
                    "name": tech['name'],
                    "type": "Security Component",
                    "status": "Active"
                })
        
        # Identify potential threats
        for flow in data_flows:
            if flow['security_level'] == 'Low':
                threats.append({
                    "type": "Low Security Data Flow",
                    "description": f"Data flow with low security: {flow.get('endpoint', 'Unknown')}",
                    "severity": "Medium"
                })
        
        return {
            "components": security_components,
            "threats": threats,
            "title": "Security Architecture"
        }

    def _calculate_complexity_score(self, technologies: List[Dict], data_flows: List[Dict]) -> int:
        """Calculate architecture complexity score"""
        score = 0
        
        # Technology complexity
        score += len(technologies) * 2
        
        # Data flow complexity
        score += len(data_flows) * 3
        
        # Category diversity
        categories = set(tech['category'] for tech in technologies)
        score += len(categories) * 5
        
        return min(score, 100)

    def _generate_recommendations(self, approved: List, core: List, non_approved: List, unknown: List) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if non_approved:
            recommendations.append(f"Replace {len(non_approved)} non-approved technologies with approved alternatives")
        
        if unknown:
            recommendations.append(f"Review {len(unknown)} unknown technologies for approval")
        
        missing_core = []
        for category, core_techs in self.core_technologies.items():
            has_core = any(tech['name'] in core_techs for tech in approved)
            if not has_core:
                missing_core.append(category)
        
        if missing_core:
            recommendations.append(f"Consider adding core technologies for: {', '.join(missing_core)}")
        
        return recommendations

    def _deduplicate_technologies(self, technologies: List[Dict]) -> List[Dict]:
        """Remove duplicate technologies"""
        seen = set()
        unique = []
        
        for tech in technologies:
            key = (tech['name'], tech['version'])
            if key not in seen:
                seen.add(key)
                unique.append(tech)
        
        return unique

    def generate_report(self, analysis: Dict[str, Any]) -> str:
        """Generate a comprehensive analysis report"""
        report = []
        report.append("# Architecture Intelligence Analysis Report")
        report.append("=" * 50)
        report.append("")
        
        # Technology Analysis
        tech_analysis = analysis['analysis']
        report.append("## Technology Analysis")
        report.append(f"**Total Technologies:** {tech_analysis['total_technologies']}")
        report.append(f"**Approved:** {tech_analysis['approved_count']}")
        report.append(f"**Core:** {tech_analysis['core_count']}")
        report.append(f"**Non-Approved:** {tech_analysis['non_approved_count']}")
        report.append(f"**Compliance Score:** {tech_analysis['compliance_score']}%")
        report.append("")
        
        # Recommendations
        if tech_analysis['recommendations']:
            report.append("## Recommendations")
            for rec in tech_analysis['recommendations']:
                report.append(f"- {rec}")
            report.append("")
        
        # Security Analysis
        if analysis['security_analysis']:
            report.append("## Security Analysis")
            for issue in analysis['security_analysis']:
                report.append(f"**{issue['type']}** ({issue['severity']})")
                report.append(f"- {issue['description']}")
                report.append(f"- Recommendation: {issue['recommendation']}")
                report.append("")
        
        return "\n".join(report)
