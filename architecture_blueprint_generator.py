import json
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import streamlit as st

class ArchitectureBlueprintGenerator:
    """Generate comprehensive architecture blueprints from system specifications"""
    
    def __init__(self):
        self.approved_technologies = {
            "Frontend": ["React", "Vue.js", "Angular", "Next.js"],
            "Backend": ["Node.js", "Python", "Java", "C#", "Go"],
            "Database": ["PostgreSQL", "MySQL", "MongoDB", "Snowflake", "Redis"],
            "Cloud": ["AWS", "Azure", "GCP"],
            "DevOps": ["Docker", "Kubernetes", "Jenkins", "GitLab CI"],
            "Security": ["OAuth", "JWT", "HTTPS", "SSL", "TLS", "PrivateLink"],
            "AI/ML": ["SageMaker", "TensorFlow", "PyTorch", "MCP"],
            "Integration": ["Apigee", "Kong", "AWS API Gateway", "Google APIs"]
        }
        
        self.core_technologies = {
            "Frontend": ["React"],
            "Backend": ["Python", "Node.js"],
            "Database": ["Snowflake", "PostgreSQL"],
            "Cloud": ["AWS"],
            "Security": ["PrivateLink", "OAuth"],
            "AI/ML": ["SageMaker", "MCP"],
            "Integration": ["Apigee", "Google APIs"]
        }
        
        self.non_approved_technologies = {
            "jQuery", "Bootstrap 3", "AngularJS", "Backbone.js", "Lodash",
            "PHP 5", "MySQL 5.6", "MongoDB 3.6", "Node.js 12", "Python 2.7"
        }

    def analyze_blueprint(self, blueprint_data: Dict) -> Dict[str, Any]:
        """Analyze blueprint and generate comprehensive architecture documentation"""
        
        # Technology analysis
        tech_analysis = self._analyze_technologies(blueprint_data["technologies"])
        
        # Generate diagrams
        conceptual_diagram = self._generate_conceptual_diagram(blueprint_data)
        logical_diagram = self._generate_logical_diagram(blueprint_data)
        data_flow_diagram = self._generate_data_flow_diagram(blueprint_data)
        integration_diagram = self._generate_integration_diagram(blueprint_data)
        security_diagram = self._generate_security_diagram(blueprint_data)
        
        return {
            "system_name": blueprint_data["system_name"],
            "description": blueprint_data["description"],
            "technology_analysis": tech_analysis,
            "conceptual_architecture": conceptual_diagram,
            "logical_architecture": logical_diagram,
            "data_flow_architecture": data_flow_diagram,
            "integration_architecture": integration_diagram,
            "security_architecture": security_diagram,
            "ai_agent_policies": blueprint_data["ai_agent_policies"],
            "compliance_score": tech_analysis["compliance_score"],
            "recommendations": tech_analysis["recommendations"]
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
        
        # Generate recommendations
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
            "recommendations": recommendations
        }

    def _generate_conceptual_diagram(self, blueprint_data: Dict) -> Dict[str, Any]:
        """Generate conceptual architecture diagram"""
        
        # Create nodes for major components
        nodes = [
            {"id": "payment_instruction", "label": "Payment Instruction", "type": "input", "x": 0, "y": 0},
            {"id": "intent_agent", "label": "Intent Agent", "type": "ai", "x": 2, "y": 0},
            {"id": "retriever_agent", "label": "Retriever Agent", "type": "ai", "x": 4, "y": 0},
            {"id": "snowflake", "label": "Snowflake\n(AWS)", "type": "data", "x": 6, "y": 0},
            {"id": "anomaly_detection", "label": "Anomaly Detection\n(SageMaker)", "type": "ml", "x": 4, "y": 2},
            {"id": "escalation", "label": "Escalation\n(React App)", "type": "ui", "x": 2, "y": 2},
            {"id": "google_apis", "label": "Google APIs", "type": "external", "x": 0, "y": 2},
            {"id": "approval", "label": "Approval\nWorkflow", "type": "process", "x": 2, "y": 4},
            {"id": "payment_api", "label": "Payment API\n(Apigee)", "type": "api", "x": 4, "y": 4},
            {"id": "apigee", "label": "Apigee\nGateway", "type": "gateway", "x": 6, "y": 4}
        ]
        
        # Create edges
        edges = [
            {"source": "payment_instruction", "target": "intent_agent", "type": "payment_request"},
            {"source": "intent_agent", "target": "retriever_agent", "type": "data_request"},
            {"source": "retriever_agent", "target": "snowflake", "type": "sql_query"},
            {"source": "retriever_agent", "target": "anomaly_detection", "type": "transaction_data"},
            {"source": "anomaly_detection", "target": "escalation", "type": "alert"},
            {"source": "escalation", "target": "google_apis", "type": "research_query"},
            {"source": "escalation", "target": "approval", "type": "escalation"},
            {"source": "approval", "target": "payment_api", "type": "approval"},
            {"source": "payment_api", "target": "apigee", "type": "api_call"}
        ]
        
        return {
            "nodes": nodes,
            "edges": edges,
            "title": "High-Value Payments System - Conceptual Architecture",
            "description": "High-level view of the payment processing system showing major components and data flow"
        }

    def _generate_logical_diagram(self, blueprint_data: Dict) -> Dict[str, Any]:
        """Generate logical architecture diagram"""
        
        layers = blueprint_data["architecture_layers"]
        
        # Create layer-based diagram
        layer_nodes = []
        y_positions = [0, 1, 2, 3, 4, 5]  # 6 layers
        
        for i, layer in enumerate(layers):
            layer_nodes.append({
                "id": f"layer_{i}",
                "label": layer["name"],
                "type": "layer",
                "y": y_positions[i],
                "components": layer["components"],
                "description": layer["description"]
            })
        
        # Create inter-layer connections
        layer_edges = []
        for i in range(len(layers) - 1):
            layer_edges.append({
                "source": f"layer_{i}",
                "target": f"layer_{i+1}",
                "type": "layer_communication"
            })
        
        return {
            "layers": layer_nodes,
            "edges": layer_edges,
            "title": "High-Value Payments System - Logical Architecture",
            "description": "Layered architecture showing system components organized by functional layers"
        }

    def _generate_data_flow_diagram(self, blueprint_data: Dict) -> Dict[str, Any]:
        """Generate data flow diagram"""
        
        flows = blueprint_data["data_flows"]
        
        # Create flow nodes
        flow_nodes = []
        node_positions = {}
        pos_counter = 0
        
        for flow in flows:
            if flow["source"] not in node_positions:
                flow_nodes.append({
                    "id": flow["source"],
                    "label": flow["source"],
                    "type": "component"
                })
                node_positions[flow["source"]] = pos_counter
                pos_counter += 1
            
            if flow["target"] not in node_positions:
                flow_nodes.append({
                    "id": flow["target"],
                    "label": flow["target"],
                    "type": "component"
                })
                node_positions[flow["target"]] = pos_counter
                pos_counter += 1
        
        return {
            "nodes": flow_nodes,
            "flows": flows,
            "title": "High-Value Payments System - Data Flow Architecture",
            "description": "Detailed data flow showing how information moves through the system"
        }

    def _generate_integration_diagram(self, blueprint_data: Dict) -> Dict[str, Any]:
        """Generate integration architecture diagram"""
        
        integrations = blueprint_data["integration_points"]
        
        # Create integration nodes
        integration_nodes = [
            {"id": "internal_system", "label": "Internal System", "type": "internal"},
            {"id": "external_apis", "label": "External APIs", "type": "external"},
            {"id": "cloud_services", "label": "Cloud Services", "type": "cloud"},
            {"id": "data_sources", "label": "Data Sources", "type": "data"}
        ]
        
        return {
            "nodes": integration_nodes,
            "integrations": integrations,
            "title": "High-Value Payments System - Integration Architecture",
            "description": "Integration points and external system connections"
        }

    def _generate_security_diagram(self, blueprint_data: Dict) -> Dict[str, Any]:
        """Generate security architecture diagram"""
        
        security_requirements = blueprint_data["security_requirements"]
        
        # Create security zones
        security_zones = [
            {"id": "on_premise", "label": "On-Premise", "type": "zone", "security_level": "High"},
            {"id": "private_cloud", "label": "Private Cloud\n(AWS VPC)", "type": "zone", "security_level": "High"},
            {"id": "public_cloud", "label": "Public Cloud\n(AWS)", "type": "zone", "security_level": "Medium"},
            {"id": "external", "label": "External Services", "type": "zone", "security_level": "Low"}
        ]
        
        return {
            "zones": security_zones,
            "requirements": security_requirements,
            "title": "High-Value Payments System - Security Architecture",
            "description": "Security zones and requirements for different system components"
        }

    def generate_comprehensive_report(self, analysis: Dict[str, Any]) -> str:
        """Generate comprehensive architecture report"""
        
        report = []
        report.append(f"# {analysis['system_name']} - Architecture Blueprint")
        report.append("=" * 60)
        report.append("")
        
        # Executive Summary
        report.append("## Executive Summary")
        report.append(f"**System:** {analysis['system_name']}")
        report.append(f"**Description:** {analysis['description']}")
        report.append(f"**Compliance Score:** {analysis['compliance_score']}%")
        report.append("")
        
        # Technology Analysis
        tech_analysis = analysis['technology_analysis']
        report.append("## Technology Analysis")
        report.append(f"**Total Technologies:** {tech_analysis['total_technologies']}")
        report.append(f"**Approved Technologies:** {tech_analysis['approved_count']}")
        report.append(f"**Core Technologies:** {tech_analysis['core_count']}")
        report.append(f"**Non-Approved Technologies:** {tech_analysis['non_approved_count']}")
        report.append("")
        
        # Recommendations
        if tech_analysis['recommendations']:
            report.append("## Recommendations")
            for rec in tech_analysis['recommendations']:
                report.append(f"- {rec}")
            report.append("")
        
        # AI Agent Policies
        report.append("## AI Agent Deployment Policies")
        for agent_name, agent_info in analysis['ai_agent_policies'].items():
            report.append(f"### {agent_info['name']}")
            report.append(f"**Purpose:** {agent_info['purpose']}")
            report.append("")
            report.append("**Policies:**")
            for policy in agent_info['policies']:
                report.append(f"- {policy}")
            report.append("")
            report.append("**Deployment Requirements:**")
            for req in agent_info['deployment_requirements']:
                report.append(f"- {req}")
            report.append("")
        
        return "\n".join(report)

def create_architecture_visualizations(analysis: Dict[str, Any]):
    """Create modern, sleek interactive visualizations for the architecture"""
    
    # Conceptual Architecture with modern design
    conceptual = analysis['conceptual_architecture']
    fig_conceptual = go.Figure()
    
    # Define modern node positions with better flow
    node_positions = {
        "payment_instruction": {"x": 0, "y": 0, "label": "Payment<br>Instruction", "icon": "💳"},
        "intent_agent": {"x": 2.5, "y": 0, "label": "Intent<br>Agent", "icon": "🤖"},
        "retriever_agent": {"x": 5, "y": 0, "label": "Retriever<br>Agent", "icon": "🔍"},
        "snowflake": {"x": 7.5, "y": 0, "label": "Snowflake<br>(AWS)", "icon": "❄️"},
        "anomaly_detection": {"x": 5, "y": 2.5, "label": "Anomaly<br>Detection<br>(SageMaker)", "icon": "🔬"},
        "escalation": {"x": 2.5, "y": 2.5, "label": "Escalation<br>(React App)", "icon": "⚠️"},
        "google_apis": {"x": 0, "y": 2.5, "label": "Google<br>APIs", "icon": "🌐"},
        "approval": {"x": 2.5, "y": 5, "label": "Approval<br>Workflow", "icon": "✅"},
        "payment_api": {"x": 5, "y": 5, "label": "Payment API<br>(Apigee)", "icon": "🔗"},
        "apigee": {"x": 7.5, "y": 5, "label": "Apigee<br>Gateway", "icon": "🚪"}
    }
    
    # Create flow paths for better visual flow
    flow_paths = [
        # Main flow
        {"path": ["payment_instruction", "intent_agent", "retriever_agent", "snowflake"], "type": "primary"},
        # AI processing flow
        {"path": ["retriever_agent", "anomaly_detection"], "type": "ai"},
        # Escalation flow
        {"path": ["anomaly_detection", "escalation", "google_apis"], "type": "escalation"},
        # Approval flow
        {"path": ["escalation", "approval", "payment_api", "apigee"], "type": "approval"}
    ]
    
    # Add flow paths as background
    for flow in flow_paths:
        path_x = [node_positions[node]["x"] for node in flow["path"]]
        path_y = [node_positions[node]["y"] for node in flow["path"]]
        
        fig_conceptual.add_trace(go.Scatter(
            x=path_x, y=path_y,
            mode='lines',
            line=dict(
                width=4,
                color=get_flow_color(flow["type"]),
                shape='spline',
                smoothing=0.3
            ),
            opacity=0.4,
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Add nodes with modern styling
    for node in conceptual['nodes']:
        pos = node_positions.get(node['id'], {"x": node['x'], "y": node['y'], "label": node['label'], "icon": "📦"})
        
        # Create gradient effect
        fig_conceptual.add_trace(go.Scatter(
            x=[pos['x']], y=[pos['y']],
            mode='markers+text',
            text=[f"{pos['icon']}<br>{pos['label']}"],
            textposition="middle center",
            textfont=dict(
                size=13,
                color="white",
                family="'Segoe UI', 'Roboto', sans-serif",
                weight="bold"
            ),
            marker=dict(
                size=100,
                color=get_modern_node_color(node['type']),
                line=dict(width=4, color='white'),
                opacity=0.95,
                symbol='circle'
            ),
            name=get_node_type_label(node['type']),
            hovertemplate=f"<b>{pos['icon']} {node['label']}</b><br>Type: {get_node_type_label(node['type'])}<br>Status: Active<extra></extra>",
            showlegend=True
        ))
    
    # Add modern arrows for better flow indication
    for edge in conceptual['edges']:
        source_pos = node_positions.get(edge['source'], {"x": 0, "y": 0})
        target_pos = node_positions.get(edge['target'], {"x": 0, "y": 0})
        
        # Calculate arrow position (80% along the line)
        arrow_x = source_pos['x'] + 0.8 * (target_pos['x'] - source_pos['x'])
        arrow_y = source_pos['y'] + 0.8 * (target_pos['y'] - source_pos['y'])
        
        # Calculate arrow direction
        dx = target_pos['x'] - source_pos['x']
        dy = target_pos['y'] - source_pos['y']
        length = (dx**2 + dy**2)**0.5
        if length > 0:
            dx_norm = dx / length
            dy_norm = dy / length
            
            fig_conceptual.add_annotation(
                x=arrow_x,
                y=arrow_y,
                ax=arrow_x - 0.2 * dx_norm,
                ay=arrow_y - 0.2 * dy_norm,
                arrowhead=2,
                arrowsize=1.2,
                arrowwidth=2,
                arrowcolor="#2c3e50",
                showarrow=True,
                axref="x",
                ayref="y",
                opacity=0.7
            )
    
    # Add modern annotations
    fig_conceptual.add_annotation(
        x=3.75, y=-0.8,
        text="🔄 AI-Powered Payment Processing Flow",
        showarrow=False,
        font=dict(size=16, color="#2c3e50", family="'Segoe UI', sans-serif"),
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="#2c3e50",
        borderwidth=1,
        borderpad=10
    )
    
    # Update layout with modern styling
    fig_conceptual.update_layout(
        title=dict(
            text=f"🏗️ {conceptual['title']}",
            font=dict(size=24, color="#2c3e50", family="'Segoe UI', sans-serif"),
            x=0.5,
            xanchor='center',
            pad=dict(t=20)
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=12, color="#2c3e50", family="'Segoe UI', sans-serif"),
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="#2c3e50",
            borderwidth=1
        ),
        xaxis=dict(
            showgrid=False, 
            zeroline=False, 
            showticklabels=False,
            range=[-1.5, 9]
        ),
        yaxis=dict(
            showgrid=False, 
            zeroline=False, 
            showticklabels=False,
            range=[-1.5, 6.5]
        ),
        plot_bgcolor='rgba(248, 250, 252, 0.95)',
        paper_bgcolor='rgba(248, 250, 252, 0.95)',
        font=dict(color="#2c3e50", family="'Segoe UI', sans-serif"),
        margin=dict(l=60, r=60, t=100, b=80),
        width=1200,
        height=700
    )
    
    return fig_conceptual

def get_modern_node_color(node_type: str) -> str:
    """Get modern gradient colors for different node types"""
    colors = {
        "input": "#00C851",      # Modern Green - Payment Input
        "ai": "#2196F3",         # Modern Blue - AI Agents
        "data": "#FF9800",       # Modern Orange - Data Storage
        "ml": "#9C27B0",         # Modern Purple - ML Services
        "ui": "#F44336",         # Modern Red - User Interface
        "external": "#607D8B",   # Modern Blue Gray - External Services
        "process": "#795548",    # Modern Brown - Business Process
        "api": "#3F51B5",        # Modern Indigo - API Services
        "gateway": "#E91E63"     # Modern Pink - Gateway Services
    }
    return colors.get(node_type, "#757575")

def get_flow_color(flow_type: str) -> str:
    """Get colors for different flow types"""
    colors = {
        "primary": "#2196F3",    # Blue for main flow
        "ai": "#9C27B0",         # Purple for AI processing
        "escalation": "#FF9800", # Orange for escalation
        "approval": "#4CAF50"    # Green for approval
    }
    return colors.get(flow_type, "#757575")

def get_node_type_label(node_type: str) -> str:
    """Get human-readable labels for node types"""
    labels = {
        "input": "Payment Input",
        "ai": "AI Agent",
        "data": "Data Storage",
        "ml": "ML Service",
        "ui": "User Interface",
        "external": "External Service",
        "process": "Business Process",
        "api": "API Service",
        "gateway": "Gateway Service"
    }
    return labels.get(node_type, "Component")

def get_node_color(node_type: str) -> str:
    """Get color for different node types with better contrast (legacy)"""
    colors = {
        "input": "#2E7D32",      # Dark Green - Payment Input
        "ai": "#1565C0",         # Dark Blue - AI Agents
        "data": "#E65100",       # Dark Orange - Data Storage
        "ml": "#6A1B9A",         # Dark Purple - ML Services
        "ui": "#C62828",         # Dark Red - User Interface
        "external": "#37474F",   # Dark Gray - External Services
        "process": "#5D4037",    # Dark Brown - Business Process
        "api": "#1A237E",        # Dark Indigo - API Services
        "gateway": "#AD1457"     # Dark Pink - Gateway Services
    }
    return colors.get(node_type, "#424242")
