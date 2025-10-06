import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import Dict, List, Any, Optional

class TechnologyDetector:
    """Enhanced technology detection with confidence scoring"""
    
    def __init__(self):
        self.technology_database = self._load_technology_database()
    
    def _load_technology_database(self) -> Dict[str, Dict]:
        """Load comprehensive technology database"""
        return {
            "react": {
                "name": "React",
                "category": "Frontend",
                "description": "A JavaScript library for building user interfaces",
                "versions": ["18.2.0", "17.0.2", "16.14.0"],
                "confidence_factors": ["package.json", "import statements", "jsx syntax"]
            },
            "nodejs": {
                "name": "Node.js",
                "category": "Backend",
                "description": "JavaScript runtime built on Chrome's V8 JavaScript engine",
                "versions": ["18.17.0", "16.20.0", "14.21.0"],
                "confidence_factors": ["package.json", "server.js", "app.js"]
            },
            "postgresql": {
                "name": "PostgreSQL",
                "category": "Database",
                "description": "Open source object-relational database system",
                "versions": ["15.3", "14.8", "13.11"],
                "confidence_factors": ["connection strings", "sql queries", "migrations"]
            },
            "docker": {
                "name": "Docker",
                "category": "DevOps",
                "description": "Containerization platform for developing, shipping, and running applications",
                "versions": ["24.0.0", "23.0.0", "20.10.0"],
                "confidence_factors": ["Dockerfile", "docker-compose.yml", "container configs"]
            },
            "aws": {
                "name": "AWS",
                "category": "Cloud",
                "description": "Amazon Web Services cloud computing platform",
                "versions": ["Latest"],
                "confidence_factors": ["aws config", "sdk imports", "service names"]
            },
            "python": {
                "name": "Python",
                "category": "Backend",
                "description": "High-level programming language with dynamic semantics",
                "versions": ["3.11.0", "3.10.0", "3.9.0"],
                "confidence_factors": ["requirements.txt", "import statements", ".py files"]
            },
            "streamlit": {
                "name": "Streamlit",
                "category": "Frontend",
                "description": "Open-source Python library for creating web applications",
                "versions": ["1.28.0", "1.27.0", "1.26.0"],
                "confidence_factors": ["streamlit import", "st. commands", "app.py"]
            }
        }
    
    def detect_technologies(self, content: str, file_type: str = "auto") -> List[Dict]:
        """Detect technologies from content with confidence scoring"""
        detected = []
        content_lower = content.lower()
        
        for tech_id, tech_info in self.technology_database.items():
            confidence = self._calculate_confidence(content_lower, tech_info, file_type)
            
            if confidence > 0:
                detected.append({
                    "id": tech_id,
                    "name": tech_info["name"],
                    "version": self._detect_version(content, tech_info),
                    "confidence": min(confidence, 100),
                    "category": tech_info["category"],
                    "description": tech_info.get("description", "No description available")
                })
        
        return sorted(detected, key=lambda x: x["confidence"], reverse=True)
    
    def _calculate_confidence(self, content: str, tech_info: Dict, file_type: str) -> int:
        """Calculate confidence score based on content analysis"""
        confidence = 0
        factors = tech_info["confidence_factors"]
        
        for factor in factors:
            if factor in content:
                confidence += 20
        
        # File type bonus
        if file_type == "package.json" and "package.json" in factors:
            confidence += 30
        elif file_type == "requirements.txt" and "requirements.txt" in factors:
            confidence += 30
        elif file_type == "dockerfile" and "Dockerfile" in factors:
            confidence += 30
        
        return min(confidence, 100)
    
    def _detect_version(self, content: str, tech_info: Dict) -> str:
        """Detect version from content"""
        versions = tech_info["versions"]
        
        for version in versions:
            if version in content:
                return version
        
        return versions[0] if versions else "Unknown"

class DataFlowAnalyzer:
    """Analyze and visualize data flow patterns"""
    
    def __init__(self):
        self.flow_patterns = self._load_flow_patterns()
    
    def _load_flow_patterns(self) -> Dict[str, Dict]:
        """Load common data flow patterns"""
        return {
            "api_to_database": {
                "pattern": "API → Database",
                "security_level": "Medium",
                "frequency": "High",
                "description": "Direct API calls to database"
            },
            "api_to_cache": {
                "pattern": "API → Cache → Database",
                "security_level": "Low",
                "frequency": "High",
                "description": "Cached data retrieval pattern"
            },
            "event_driven": {
                "pattern": "Event → Queue → Service",
                "security_level": "High",
                "frequency": "Medium",
                "description": "Asynchronous event processing"
            },
            "microservices": {
                "pattern": "Service → Service → Database",
                "security_level": "High",
                "frequency": "High",
                "description": "Inter-service communication"
            }
        }
    
    def analyze_flow(self, flow_type: str, time_range: str) -> Dict:
        """Analyze data flow patterns"""
        # Simulate analysis based on flow type and time range
        base_patterns = list(self.flow_patterns.values())
        selected_patterns = random.sample(base_patterns, min(3, len(base_patterns)))
        
        return {
            "patterns": selected_patterns,
            "total_flows": random.randint(50, 200),
            "security_issues": random.randint(0, 5),
            "performance_score": random.randint(70, 95),
            "time_range": time_range,
            "flow_type": flow_type
        }

class ArchitectureGenerator:
    """Generate architecture visualizations and patterns"""
    
    def __init__(self):
        self.architecture_templates = self._load_architecture_templates()
    
    def _load_architecture_templates(self) -> Dict[str, Dict]:
        """Load architecture templates"""
        return {
            "microservices": {
                "name": "Microservices Architecture",
                "layers": [
                    {"name": "API Gateway", "components": ["Load Balancer", "Rate Limiter", "Auth"]},
                    {"name": "Services", "components": ["User Service", "Order Service", "Payment Service"]},
                    {"name": "Data Layer", "components": ["User DB", "Order DB", "Payment DB"]}
                ],
                "patterns": ["API Gateway", "Circuit Breaker", "Service Discovery"]
            },
            "monolithic": {
                "name": "Monolithic Architecture",
                "layers": [
                    {"name": "Presentation", "components": ["Web UI", "Mobile App"]},
                    {"name": "Business Logic", "components": ["Controllers", "Services", "Models"]},
                    {"name": "Data Access", "components": ["ORM", "Database"]}
                ],
                "patterns": ["Layered Architecture", "Repository Pattern"]
            },
            "serverless": {
                "name": "Serverless Architecture",
                "layers": [
                    {"name": "Frontend", "components": ["Static Site", "CDN"]},
                    {"name": "Functions", "components": ["Lambda Functions", "API Functions"]},
                    {"name": "Services", "components": ["Database", "Storage", "Queue"]}
                ],
                "patterns": ["Function as a Service", "Event-Driven"]
            }
        }
    
    def generate_architecture(self, arch_type: str, view_mode: str) -> Dict:
        """Generate architecture visualization"""
        template = self.architecture_templates.get(arch_type, self.architecture_templates["microservices"])
        
        return {
            "type": arch_type,
            "view_mode": view_mode,
            "layers": template["layers"],
            "patterns": template["patterns"],
            "components": self._extract_components(template["layers"]),
            "dependencies": self._generate_dependencies(template["layers"])
        }
    
    def _extract_components(self, layers: List[Dict]) -> List[str]:
        """Extract all components from layers"""
        components = []
        for layer in layers:
            components.extend(layer["components"])
        return components
    
    def _generate_dependencies(self, layers: List[Dict]) -> List[Dict]:
        """Generate component dependencies"""
        dependencies = []
        all_components = self._extract_components(layers)
        
        # Generate random dependencies
        for _ in range(min(10, len(all_components))):
            source = random.choice(all_components)
            target = random.choice(all_components)
            if source != target:
                dependencies.append({
                    "source": source,
                    "target": target,
                    "strength": random.randint(1, 10),
                    "type": random.choice(["API Call", "Database Query", "Event"])
                })
        
        return dependencies

class PatternManager:
    """Manage approved patterns and compliance scoring"""
    
    def __init__(self):
        self.patterns = self._load_patterns()
        self.compliance_rules = self._load_compliance_rules()
    
    def _load_patterns(self) -> Dict[str, Dict]:
        """Load approved patterns"""
        return {
            "microservices": {
                "name": "Microservices Pattern",
                "category": "Architecture",
                "description": "Decompose applications into small, independent services",
                "compliance_score": 95,
                "usage_level": "High",
                "last_updated": "2024-01-15",
                "governance_rules": ["Service independence", "API contracts", "Data isolation"]
            },
            "cqrs": {
                "name": "CQRS Pattern",
                "category": "Data",
                "description": "Separate read and write operations for better scalability",
                "compliance_score": 88,
                "usage_level": "Medium",
                "last_updated": "2024-01-10",
                "governance_rules": ["Command separation", "Event sourcing", "Read models"]
            },
            "event_sourcing": {
                "name": "Event Sourcing",
                "category": "Data",
                "description": "Store events as the source of truth for state changes",
                "compliance_score": 92,
                "usage_level": "Medium",
                "last_updated": "2024-01-12",
                "governance_rules": ["Event store", "Replay capability", "Audit trail"]
            },
            "circuit_breaker": {
                "name": "Circuit Breaker",
                "category": "Resilience",
                "description": "Prevent cascading failures in distributed systems",
                "compliance_score": 90,
                "usage_level": "High",
                "last_updated": "2024-01-08",
                "governance_rules": ["Failure detection", "Fallback mechanisms", "Recovery testing"]
            },
            "api_gateway": {
                "name": "API Gateway",
                "category": "Integration",
                "description": "Single entry point for client requests to microservices",
                "compliance_score": 94,
                "usage_level": "High",
                "last_updated": "2024-01-14",
                "governance_rules": ["Request routing", "Authentication", "Rate limiting"]
            }
        }
    
    def _load_compliance_rules(self) -> Dict[str, List[str]]:
        """Load compliance rules for different categories"""
        return {
            "Architecture": ["Service boundaries", "Data consistency", "Scalability"],
            "Data": ["Data integrity", "Privacy compliance", "Backup strategy"],
            "Resilience": ["Fault tolerance", "Recovery procedures", "Monitoring"],
            "Integration": ["API standards", "Security protocols", "Documentation"]
        }
    
    def get_patterns(self, category: str = None, usage: str = None, min_compliance: int = 0) -> List[Dict]:
        """Get filtered patterns"""
        patterns = list(self.patterns.values())
        
        if category and category != "All":
            patterns = [p for p in patterns if p["category"] == category]
        
        if usage and usage != "All":
            patterns = [p for p in patterns if p["usage_level"] == usage]
        
        patterns = [p for p in patterns if p["compliance_score"] >= min_compliance]
        
        return patterns
    
    def calculate_compliance_score(self, architecture: Dict) -> int:
        """Calculate overall compliance score for architecture"""
        # Simulate compliance calculation based on patterns used
        base_score = 80
        pattern_bonus = len(architecture.get("patterns", [])) * 5
        return min(base_score + pattern_bonus, 100)

def generate_sample_data() -> Dict[str, Any]:
    """Generate sample data for demonstration"""
    return {
        "technologies": [
            {"name": "React", "version": "18.2.0", "confidence": 95, "category": "Frontend"},
            {"name": "Node.js", "version": "18.17.0", "confidence": 92, "category": "Backend"},
            {"name": "PostgreSQL", "version": "15.3", "confidence": 88, "category": "Database"},
            {"name": "Docker", "version": "24.0.0", "confidence": 90, "category": "DevOps"},
            {"name": "AWS", "version": "Latest", "confidence": 85, "category": "Cloud"}
        ],
        "metrics": {
            "active_patterns": 12,
            "technologies_detected": 8,
            "compliance_score": 95,
            "architecture_views": 24
        },
        "activity": [
            {"Time": "2 minutes ago", "Action": "New pattern approved", "Status": "Success"},
            {"Time": "15 minutes ago", "Action": "Technology stack analyzed", "Status": "Success"},
            {"Time": "1 hour ago", "Action": "Architecture diagram generated", "Status": "Success"},
            {"Time": "3 hours ago", "Action": "Compliance check completed", "Status": "Warning"}
        ]
    }
