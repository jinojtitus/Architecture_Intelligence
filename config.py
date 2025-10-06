# Configuration settings for Architecture Intelligence

# Application settings
APP_NAME = "Architecture Intelligence"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Governance-first blueprint generation based on approved patterns"

# Theme settings
THEME_CONFIG = {
    "primary_color": "#667eea",
    "secondary_color": "#764ba2",
    "background_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "glass_opacity": 0.1,
    "border_radius": 20,
    "animation_duration": 0.3
}

# Technology detection settings
TECH_DETECTION = {
    "confidence_threshold": 70,
    "supported_formats": [".json", ".txt", ".yaml", ".yml", ".xml"],
    "categories": ["Frontend", "Backend", "Database", "DevOps", "Cloud", "Security", "Testing"],
    "version_detection": True,
    "auto_update": False
}

# Architecture patterns
PATTERNS = {
    "microservices": {
        "name": "Microservices Pattern",
        "description": "Decompose applications into small, independent services",
        "compliance_score": 95,
        "usage_level": "High",
        "category": "Architecture"
    },
    "cqrs": {
        "name": "CQRS Pattern", 
        "description": "Separate read and write operations for better scalability",
        "compliance_score": 88,
        "usage_level": "Medium",
        "category": "Data"
    },
    "event_sourcing": {
        "name": "Event Sourcing",
        "description": "Store events as the source of truth for state changes",
        "compliance_score": 92,
        "usage_level": "Medium",
        "category": "Data"
    },
    "circuit_breaker": {
        "name": "Circuit Breaker",
        "description": "Prevent cascading failures in distributed systems",
        "compliance_score": 90,
        "usage_level": "High",
        "category": "Resilience"
    },
    "api_gateway": {
        "name": "API Gateway",
        "description": "Single entry point for client requests to microservices",
        "compliance_score": 94,
        "usage_level": "High",
        "category": "Integration"
    }
}

# Security settings
SECURITY = {
    "threat_detection": True,
    "scan_frequency_hours": 6,
    "security_levels": ["High", "Medium", "Low"],
    "compliance_threshold": 80
}

# Data flow settings
DATA_FLOW = {
    "supported_types": ["API Calls", "Database Queries", "User Interactions", "System Events"],
    "time_ranges": ["Last Hour", "Last Day", "Last Week", "Last Month"],
    "security_overlay": True,
    "frequency_analysis": True
}

# Architecture visualization
ARCHITECTURE = {
    "view_modes": ["Layers", "Components", "Dependencies", "Security"],
    "architecture_types": ["Microservices", "Monolithic", "Serverless", "Hybrid"],
    "layers": [
        {"name": "Presentation Layer", "color": "#4CAF50"},
        {"name": "API Layer", "color": "#2196F3"},
        {"name": "Business Logic", "color": "#FF9800"},
        {"name": "Data Access", "color": "#9C27B0"},
        {"name": "Data Layer", "color": "#F44336"}
    ]
}

