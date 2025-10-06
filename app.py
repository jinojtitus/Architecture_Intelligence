import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu
import json
from datetime import datetime
import base64
from io import BytesIO
from utils import TechnologyDetector, DataFlowAnalyzer, ArchitectureGenerator, PatternManager, generate_sample_data
from blueprint_analyzer import BlueprintAnalyzer
from architecture_blueprint_generator import ArchitectureBlueprintGenerator, create_architecture_visualizations
import config

# Page configuration
st.set_page_config(
    page_title="Architecture Intelligence",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for iOS theme
def load_css():
    st.markdown("""
    <style>
    /* iOS-inspired theme with improved contrast */
    .main {
        background: linear-gradient(135deg, #f8f9ff 0%, #e8f0ff 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f8f9ff 0%, #e8f0ff 100%);
    }
    
    /* Glass morphism cards with better contrast */
    .glass-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
        color: #2c3e50;
    }
    
    /* Custom sidebar with better contrast */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar text colors */
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: #2c3e50 !important;
    }
    
    .css-1d391kg p {
        color: #5a6c7d !important;
    }
    
    /* Custom buttons */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px 0 rgba(31, 38, 135, 0.37);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(31, 38, 135, 0.5);
    }
    
    /* Custom selectbox with better contrast */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(0, 0, 0, 0.1);
        color: #2c3e50;
    }
    
    /* Custom text input with better contrast */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(0, 0, 0, 0.1);
        color: #2c3e50;
    }
    
    /* Custom metrics with better contrast */
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        border: 1px solid rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: transform 0.3s ease;
        color: #2c3e50;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    /* Custom headers with better contrast */
    h1, h2, h3 {
        color: #2c3e50;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    /* Custom text with better contrast */
    .stMarkdown {
        color: #2c3e50;
    }
    
    /* Animation keyframes */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Custom progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(45deg, #667eea, #764ba2);
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    load_css()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h1 style="color: #2c3e50; margin-bottom: 0;">🏗️</h1>
            <h2 style="color: #2c3e50; margin-top: 0;">Architecture Intelligence</h2>
            <p style="color: #5a6c7d;">Governance-first blueprint generation</p>
        </div>
        """, unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title=None,
            options=["Architecture Blueprint Generator", "Technology Detection", "Data Flow", "Architecture", "Patterns", "Settings"],
            icons=["building-gear", "cpu", "arrow-left-right", "diagram-3", "book", "gear"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "rgba(255, 255, 255, 0.9)"},
                "icon": {"color": "#2c3e50", "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "rgba(0, 0, 0, 0.1)",
                    "color": "#2c3e50",
                },
                "nav-link-selected": {"background-color": "rgba(0, 0, 0, 0.1)"},
            }
        )
    
    # Main content area
    if selected == "Architecture Blueprint Generator":
        show_blueprint_generator()
    elif selected == "Technology Detection":
        show_technology_detection()
    elif selected == "Data Flow":
        show_data_flow()
    elif selected == "Architecture":
        show_architecture()
    elif selected == "Patterns":
        show_patterns()
    elif selected == "Settings":
        show_settings()

# Dashboard function removed - content deleted

def show_blueprint_generator():
    st.markdown("""
    <div class="fade-in-up">
        <h1 style="text-align: center; margin-bottom: 30px;">🏗️ Architecture Blueprint Generator</h1>
        <p style="text-align: center; font-size: 18px; color: #5a6c7d; margin-bottom: 40px;">
            Generate comprehensive architecture blueprints with AI-powered intelligence
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different sections
    tab1, tab2 = st.tabs(["🎯 Blueprint Builder", "🔍 Analysis Tools"])
    
    with tab1:
        show_blueprint_builder()
    
    with tab2:
        show_blueprint_analysis()

def show_blueprint_builder():
    st.markdown("""
    <div class="glass-card">
        <h2>🎯 Blueprint Builder</h2>
        <p style="color: #5a6c7d; margin-bottom: 20px;">Create comprehensive architecture blueprints with guided inputs</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Prompt Library Section
    st.markdown("### 📚 Prompt Library")
    
    # Define prompt categories
    prompt_categories = {
        "Financial Services": [
            "Design a high-value payments processing system with real-time fraud detection",
            "Create a microservices architecture for a digital banking platform",
            "Build a trading system with low-latency requirements and regulatory compliance",
            "Design a credit scoring system with machine learning capabilities"
        ],
        "E-commerce": [
            "Design a scalable e-commerce platform with inventory management",
            "Create a recommendation engine architecture with real-time personalization",
            "Build a multi-tenant marketplace with vendor management",
            "Design a subscription billing system with usage-based pricing"
        ],
        "Healthcare": [
            "Design a HIPAA-compliant patient data management system",
            "Create a telemedicine platform with video conferencing capabilities",
            "Build a medical device integration system with real-time monitoring",
            "Design a clinical trial management system with data analytics"
        ],
        "AI/ML Systems": [
            "Design an AI-powered customer service platform with multiple agents",
            "Create a machine learning pipeline for real-time predictions",
            "Build an intelligent document processing system with NLP capabilities",
            "Design a computer vision system for quality control in manufacturing"
        ],
        "IoT & Real-time": [
            "Design an IoT data collection and processing system",
            "Create a real-time monitoring dashboard for industrial equipment",
            "Build a smart city infrastructure with sensor networks",
            "Design a fleet management system with GPS tracking and analytics"
        ],
        "Enterprise": [
            "Design an enterprise resource planning (ERP) system",
            "Create a customer relationship management (CRM) platform",
            "Build a human resources management system with payroll integration",
            "Design a supply chain management system with vendor collaboration"
        ]
    }
    
    # Create columns for prompt categories
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏦 Business Domains")
        selected_category = st.selectbox(
            "Select a business domain:",
            list(prompt_categories.keys()),
            key="prompt_category"
        )
    
    with col2:
        st.markdown("#### 📝 Available Prompts")
        if selected_category:
            selected_prompt = st.selectbox(
                "Choose a prompt:",
                prompt_categories[selected_category],
                key="selected_prompt",
                help="Select a prompt to automatically populate the application purpose field"
            )
            
            if st.button("📋 Use This Prompt", type="secondary", key="use_prompt_btn"):
                st.session_state.app_purpose = selected_prompt
                st.success("✅ Prompt applied! Check the Application Purpose field below.")
    
    # Custom prompt section
    st.markdown("#### ✏️ Custom Prompt")
    custom_prompt = st.text_area(
        "Or create your own architecture prompt:",
        placeholder="Describe the architecture you want to generate...",
        height=80,
        key="custom_prompt"
    )
    
    if st.button("📝 Use Custom Prompt", type="secondary", key="use_custom_prompt_btn"):
        if custom_prompt:
            st.session_state.app_purpose = custom_prompt
            st.success("✅ Custom prompt applied! Check the Application Purpose field below.")
        else:
            st.warning("Please enter a custom prompt.")
    
    st.divider()
    
    # Application Purpose Section
    st.markdown("### 📋 Application Purpose & Requirements")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        app_purpose = st.text_area(
            "Describe your application purpose and requirements:",
            value=st.session_state.get('app_purpose', ''),
            placeholder="e.g., Build a high-value payments processing system with real-time fraud detection, multi-level approval workflows, and compliance with PCI DSS standards...",
            height=120,
            help="Provide detailed information about what your application does, its key features, and business requirements."
        )
        
        business_domain = st.selectbox(
            "Business Domain:",
            ["Financial Services", "Healthcare", "E-commerce", "Manufacturing", "Education", "Government", "Technology", "Other"]
        )
        
        if business_domain == "Other":
            business_domain = st.text_input("Specify business domain:")
    
    with col2:
        st.markdown("""
        <div style="background: rgba(33, 150, 243, 0.1); padding: 20px; border-radius: 10px; border: 1px solid rgba(33, 150, 243, 0.3);">
            <h4 style="color: #1976D2; margin-top: 0;">💡 Tips for Better Results</h4>
            <ul style="color: #5a6c7d; font-size: 14px; margin: 0; padding-left: 20px;">
                <li>Be specific about functional requirements</li>
                <li>Mention performance expectations</li>
                <li>Include security requirements</li>
                <li>Specify compliance needs</li>
                <li>Describe user interactions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Technology Selection Section
    st.markdown("### 🛠️ Technology Stack Selection")
    
    # Load approved technologies
    try:
        with open('high_value_payments_blueprint.json', 'r') as f:
            blueprint_data = json.load(f)
        
        technologies = blueprint_data.get('technologies', [])
        
        # Group technologies by category
        tech_categories = {}
        for tech in technologies:
            category = tech.get('category', 'Other')
            if category not in tech_categories:
                tech_categories[category] = []
            tech_categories[category].append(tech)
        
        # Create technology selection interface
        selected_technologies = []
        
        for category, techs in tech_categories.items():
            st.markdown(f"#### {category}")
            
            # Create columns for technology selection
            cols = st.columns(3)
            for i, tech in enumerate(techs):
                with cols[i % 3]:
                    if st.checkbox(
                        f"{tech['name']} ({tech['version']})",
                        key=f"tech_{tech['name']}",
                        help=tech.get('description', 'No description available')
                    ):
                        selected_technologies.append(tech)
    
    except Exception as e:
        st.error(f"Error loading technology data: {str(e)}")
        selected_technologies = []
    
    st.divider()
    
    # Pattern Selection Section
    st.markdown("### 🎨 Architectural Patterns")
    
    # Define architectural patterns
    patterns = {
        "Microservices": {
            "description": "Decompose application into small, independent services",
            "use_cases": ["Scalable systems", "Team autonomy", "Technology diversity"],
            "complexity": "High"
        },
        "Event-Driven": {
            "description": "Components communicate through events and messages",
            "use_cases": ["Real-time processing", "Loose coupling", "Scalability"],
            "complexity": "Medium"
        },
        "CQRS": {
            "description": "Command Query Responsibility Segregation pattern",
            "use_cases": ["Complex domains", "Performance optimization", "Scalability"],
            "complexity": "High"
        },
        "API Gateway": {
            "description": "Single entry point for client requests",
            "use_cases": ["Microservices", "Authentication", "Rate limiting"],
            "complexity": "Medium"
        },
        "Event Sourcing": {
            "description": "Store events instead of current state",
            "use_cases": ["Audit trails", "Temporal queries", "Complex business logic"],
            "complexity": "High"
        },
        "Saga": {
            "description": "Manage distributed transactions",
            "use_cases": ["Microservices", "Distributed systems", "Data consistency"],
            "complexity": "High"
        }
    }
    
    # Agentic Patterns
    agentic_patterns = {
        "AI Agent Orchestration": {
            "description": "Multiple AI agents working together to achieve complex goals",
            "use_cases": ["Complex decision making", "Multi-step processes", "Intelligent automation"],
            "complexity": "High"
        },
        "Intent-Based Processing": {
            "description": "AI agents that understand and process user intents",
            "use_cases": ["Natural language interfaces", "Smart routing", "Contextual responses"],
            "complexity": "Medium"
        },
        "Retrieval-Augmented Generation": {
            "description": "AI agents that retrieve relevant information before generating responses",
            "use_cases": ["Knowledge management", "Context-aware responses", "Data-driven decisions"],
            "complexity": "Medium"
        },
        "Multi-Agent Collaboration": {
            "description": "Specialized agents collaborating on complex tasks",
            "use_cases": ["Workflow automation", "Expert systems", "Distributed intelligence"],
            "complexity": "High"
        },
        "Reactive Agents": {
            "description": "Agents that respond to events and changes in real-time",
            "use_cases": ["Real-time monitoring", "Event processing", "Adaptive systems"],
            "complexity": "Medium"
        }
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Traditional Patterns")
        selected_patterns = []
        for pattern_name, pattern_info in patterns.items():
            if st.checkbox(
                f"{pattern_name}",
                key=f"pattern_{pattern_name}",
                help=f"{pattern_info['description']}\n\nUse cases: {', '.join(pattern_info['use_cases'])}\nComplexity: {pattern_info['complexity']}"
            ):
                selected_patterns.append({
                    "name": pattern_name,
                    "type": "Traditional",
                    **pattern_info
                })
    
    with col2:
        st.markdown("#### Agentic Patterns")
        selected_agentic_patterns = []
        for pattern_name, pattern_info in agentic_patterns.items():
            if st.checkbox(
                f"{pattern_name}",
                key=f"agentic_{pattern_name}",
                help=f"{pattern_info['description']}\n\nUse cases: {', '.join(pattern_info['use_cases'])}\nComplexity: {pattern_info['complexity']}"
            ):
                selected_agentic_patterns.append({
                    "name": pattern_name,
                    "type": "Agentic",
                    **pattern_info
                })
    
    st.divider()
    
    # Generate Blueprint Button
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button(
            "🚀 Generate Architecture Blueprint",
            type="primary",
            use_container_width=True,
            help="Generate a comprehensive architecture blueprint based on your inputs"
        ):
            if app_purpose and (selected_technologies or selected_patterns or selected_agentic_patterns):
                # Generate blueprint
                generate_blueprint_from_inputs(
                    app_purpose, 
                    business_domain, 
                    selected_technologies, 
                    selected_patterns + selected_agentic_patterns
                )
            else:
                st.warning("Please provide application purpose and select at least one technology or pattern.")

def generate_blueprint_from_inputs(purpose, domain, technologies, patterns):
    """Generate a blueprint based on user inputs"""
    st.markdown("### 🎯 Generated Architecture Blueprint")
    
    # Create a comprehensive blueprint
    blueprint = {
        "application_purpose": purpose,
        "business_domain": domain,
        "selected_technologies": technologies,
        "selected_patterns": patterns,
        "generated_at": datetime.now().isoformat()
    }
    
    # Display the blueprint
    st.json(blueprint)
    
    # Generate architecture diagrams
    st.markdown("#### 🏗️ Architecture Visualization")
    
    # Create a simple network diagram
    G = nx.DiGraph()
    
    # Add nodes for each technology
    for tech in technologies:
        G.add_node(tech['name'], category=tech['category'])
    
    # Add pattern nodes
    for pattern in patterns:
        G.add_node(pattern['name'], category='Pattern')
    
    # Create layout
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    # Create plotly visualization
    edge_x = []
    edge_y = []
    
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    node_x = []
    node_y = []
    node_text = []
    node_colors = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        
        # Color based on category
        if G.nodes[node].get('category') == 'Frontend':
            node_colors.append('#2196F3')
        elif G.nodes[node].get('category') == 'Backend':
            node_colors.append('#4CAF50')
        elif G.nodes[node].get('category') == 'Database':
            node_colors.append('#9C27B0')
        elif G.nodes[node].get('category') == 'Pattern':
            node_colors.append('#FF9800')
        else:
            node_colors.append('#607D8B')
    
    fig = go.Figure()
    
    # Add edges
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='rgba(100, 100, 100, 0.4)'),
        hoverinfo='none',
        mode='lines',
        showlegend=False
    ))
    
    # Add nodes
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        textposition="middle center",
        textfont=dict(size=12, color='white'),
        marker=dict(
            size=60,
            color=node_colors,
            line=dict(width=2, color='white')
        ),
        showlegend=False
    ))
    
    fig.update_layout(
        title="Generated Architecture Blueprint",
        title_font_size=16,
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20,l=20,r=20,t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        width=800,
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Download button
    blueprint_json = json.dumps(blueprint, indent=2)
    st.download_button(
        label="📥 Download Blueprint as JSON",
        data=blueprint_json,
        file_name=f"architecture_blueprint_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

def show_blueprint_analysis():
    st.markdown("""
    <div class="fade-in-up">
        <h1>Blueprint & Repository Analysis</h1>
        <p style="color: #5a6c7d;">Comprehensive analysis of blueprints and Git repositories with technology compliance, data flow, and security analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Analysis type selection
    analysis_type = st.radio(
        "Select Analysis Type:",
        ["Git Repository URL", "High-Value Payments System Blueprint"],
        horizontal=True
    )
    
    if analysis_type == "Git Repository URL":
        repo_url = st.text_input("Git Repository URL", placeholder="https://github.com/username/repository")
        branch = st.text_input("Branch (optional)", value="main", placeholder="main")
        
        if repo_url and st.button("Analyze Repository", width='stretch'):
            with st.spinner("Cloning and analyzing repository..."):
                try:
                    analyzer = BlueprintAnalyzer()
                    analysis = analyzer.analyze_git_repo(repo_url, branch)
                    display_blueprint_analysis(analysis)
                except Exception as e:
                    st.error(f"Error analyzing repository: {str(e)}")
    
    elif analysis_type == "High-Value Payments System Blueprint":
        st.markdown("""
        <div class="glass-card">
            <h3>High-Value Payments System Blueprint Analysis</h3>
            <p>Comprehensive analysis of the AI-powered high-value payments processing system with anomaly detection and approval workflow.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Generate Comprehensive Blueprint Analysis", width='stretch'):
            with st.spinner("Generating comprehensive architecture blueprint..."):
                try:
                    # Load the blueprint data
                    with open('high_value_payments_blueprint.json', 'r') as f:
                        blueprint_data = json.load(f)
                    
                    # Generate comprehensive analysis
                    generator = ArchitectureBlueprintGenerator()
                    analysis = generator.analyze_blueprint(blueprint_data)
                    
                    # Display the comprehensive analysis
                    display_comprehensive_blueprint_analysis(analysis)
                    
                except Exception as e:
                    st.error(f"Error generating blueprint analysis: {str(e)}")

def display_blueprint_analysis(analysis):
    """Display comprehensive blueprint analysis results"""
    
    # Technology Analysis Section
    st.markdown("""
    <div class="glass-card">
        <h2>Technology Analysis</h2>
    </div>
    """, unsafe_allow_html=True)
    
    tech_analysis = analysis['analysis']
    
    # Compliance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Technologies", tech_analysis['total_technologies'])
    
    with col2:
        st.metric("Approved", tech_analysis['approved_count'], 
                 delta=f"{tech_analysis['approved_count'] - tech_analysis['non_approved_count']}")
    
    with col3:
        st.metric("Core Technologies", tech_analysis['core_count'])
    
    with col4:
        compliance_color = "normal" if tech_analysis['compliance_score'] >= 80 else "off"
        st.metric("Compliance Score", f"{tech_analysis['compliance_score']}%", 
                 delta_color=compliance_color)
    
    # Technology categories
    tab1, tab2, tab3, tab4 = st.tabs(["✅ Approved", "⭐ Core", "❌ Non-Approved", "❓ Unknown"])
    
    with tab1:
        if tech_analysis['approved']:
            for tech in tech_analysis['approved']:
                st.markdown(f"""
                <div style="background: rgba(76, 175, 80, 0.1); border-left: 4px solid #4CAF50; padding: 10px; margin: 5px 0; border-radius: 5px;">
                    <strong>{tech['name']}</strong> v{tech['version']} - {tech['category']} ({tech['confidence']}% confidence)
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No approved technologies found")
    
    with tab2:
        if tech_analysis['core']:
            for tech in tech_analysis['core']:
                st.markdown(f"""
                <div style="background: rgba(33, 150, 243, 0.1); border-left: 4px solid #2196F3; padding: 10px; margin: 5px 0; border-radius: 5px;">
                    <strong>{tech['name']}</strong> v{tech['version']} - {tech['category']} ({tech['confidence']}% confidence)
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No core technologies found")
    
    with tab3:
        if tech_analysis['non_approved']:
            for tech in tech_analysis['non_approved']:
                st.markdown(f"""
                <div style="background: rgba(244, 67, 54, 0.1); border-left: 4px solid #F44336; padding: 10px; margin: 5px 0; border-radius: 5px;">
                    <strong>{tech['name']}</strong> v{tech['version']} - {tech['category']} ({tech['confidence']}% confidence)
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("No non-approved technologies found")
    
    with tab4:
        if tech_analysis['unknown']:
            for tech in tech_analysis['unknown']:
                st.markdown(f"""
                <div style="background: rgba(255, 152, 0, 0.1); border-left: 4px solid #FF9800; padding: 10px; margin: 5px 0; border-radius: 5px;">
                    <strong>{tech['name']}</strong> v{tech['version']} - {tech['category']} ({tech['confidence']}% confidence)
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No unknown technologies found")
    
    # Recommendations
    if tech_analysis['recommendations']:
        st.markdown("""
        <div class="glass-card">
            <h3>Recommendations</h3>
        </div>
        """, unsafe_allow_html=True)
        
        for rec in tech_analysis['recommendations']:
            st.info(f"💡 {rec}")
    
    # Data Flow Analysis
    if analysis.get('data_flow'):
        st.markdown("""
        <div class="glass-card">
            <h2>Data Flow Analysis</h2>
        </div>
        """, unsafe_allow_html=True)
        
        flows_df = pd.DataFrame(analysis['data_flow'])
        if not flows_df.empty:
            st.dataframe(flows_df, width='stretch')
        else:
            st.info("No data flows detected")
    
    # Security Analysis
    if analysis.get('security_analysis'):
        st.markdown("""
        <div class="glass-card">
            <h2>Security Analysis</h2>
        </div>
        """, unsafe_allow_html=True)
        
        for issue in analysis['security_analysis']:
            severity_color = "#F44336" if issue['severity'] == 'High' else "#FF9800" if issue['severity'] == 'Medium' else "#4CAF50"
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.8); border-left: 4px solid {severity_color}; padding: 15px; margin: 10px 0; border-radius: 5px;">
                <h4 style="margin: 0 0 10px 0; color: #2c3e50;">{issue['type']} ({issue['severity']})</h4>
                <p style="margin: 0 0 10px 0; color: #5a6c7d;">{issue['description']}</p>
                <p style="margin: 0; color: #2c3e50;"><strong>Recommendation:</strong> {issue['recommendation']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Architecture Analysis
    if analysis.get('architecture'):
        arch = analysis['architecture']
        st.markdown("""
        <div class="glass-card">
            <h2>Architecture Analysis</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Architecture Type", arch['type'])
            st.metric("Complexity Score", f"{arch['complexity_score']}/100")
        
        with col2:
            if arch.get('layers'):
                st.write("**Architecture Layers:**")
                for layer in arch['layers']:
                    st.write(f"• {layer['name']}: {', '.join(layer['technologies'])}")
    
    # Integration Points
    if analysis.get('integration_points'):
        st.markdown("""
        <div class="glass-card">
            <h2>Integration Points</h2>
        </div>
        """, unsafe_allow_html=True)
        
        integrations_df = pd.DataFrame(analysis['integration_points'])
        if not integrations_df.empty:
            st.dataframe(integrations_df, width='stretch')
        else:
            st.info("No integration points detected")
    
    # Generate Report
    if st.button("Generate Full Report", width='stretch'):
        analyzer = BlueprintAnalyzer()
        report = analyzer.generate_report(analysis)
        
        st.download_button(
            label="Download Analysis Report",
            data=report,
            file_name="architecture_analysis_report.md",
            mime="text/markdown"
        )

def display_comprehensive_blueprint_analysis(analysis):
    """Display comprehensive blueprint analysis with all architecture diagrams"""
    
    # System Overview
    st.markdown(f"""
    <div class="glass-card">
        <h2>{analysis['system_name']}</h2>
        <p style="color: #5a6c7d; font-size: 18px;">{analysis['description']}</p>
        <div style="display: flex; gap: 20px; margin-top: 20px;">
            <div style="text-align: center;">
                <div style="font-size: 24px; font-weight: bold; color: #4CAF50;">{analysis['compliance_score']}%</div>
                <div style="color: #5a6c7d;">Compliance Score</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 24px; font-weight: bold; color: #2196F3;">{analysis['technology_analysis']['total_technologies']}</div>
                <div style="color: #5a6c7d;">Technologies</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 24px; font-weight: bold; color: #FF9800;">{analysis['technology_analysis']['core_count']}</div>
                <div style="color: #5a6c7d;">Core Technologies</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Technology Analysis
    tech_analysis = analysis['technology_analysis']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Approved", tech_analysis['approved_count'], 
                 delta=f"{tech_analysis['approved_count'] - tech_analysis['non_approved_count']}")
    
    with col2:
        st.metric("Core", tech_analysis['core_count'])
    
    with col3:
        st.metric("Non-Approved", tech_analysis['non_approved_count'], 
                 delta=f"-{tech_analysis['non_approved_count']}" if tech_analysis['non_approved_count'] > 0 else None)
    
    with col4:
        st.metric("Unknown", len(tech_analysis['unknown']))
    
    # Architecture Diagrams Section
    st.markdown("""
    <div class="glass-card">
        <h2>Architecture Diagrams</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different diagrams
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏗️ Conceptual", "📋 Logical", "🔄 Data Flow", "🔗 Integration", "🛡️ Security"
    ])
    
    with tab1:
        st.markdown("### Conceptual Architecture")
        st.markdown("High-level view of the payment processing system showing major components and data flow.")
        
        # Generate conceptual diagram
        fig_conceptual = create_architecture_visualizations(analysis)
        st.plotly_chart(fig_conceptual, width='stretch')
        
        st.markdown("""
        **Key Components:**
        - **Payment Instruction**: Initial payment request input
        - **Intent Agent**: AI agent for processing payment instructions
        - **Retriever Agent**: AI agent for data retrieval from Snowflake
        - **Anomaly Detection**: ML model hosted on SageMaker
        - **Escalation Interface**: React app for manual review
        - **Approval Workflow**: Automated approval process
        - **Payment API**: Final transaction execution via Apigee
        """)
    
    with tab2:
        st.markdown("### Logical Architecture")
        st.markdown("Layered architecture showing system components organized by functional layers.")
        
        # Display logical architecture layers
        for i, layer in enumerate(analysis['logical_architecture']['layers']):
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.8); border-left: 4px solid #2196F3; padding: 15px; margin: 10px 0; border-radius: 5px;">
                <h4 style="margin: 0 0 10px 0; color: #2c3e50;">{layer['label']}</h4>
                <p style="margin: 0 0 10px 0; color: #5a6c7d;">{layer['description']}</p>
                <div style="display: flex; flex-wrap: wrap; gap: 5px;">
            """, unsafe_allow_html=True)
            
            for component in layer['components']:
                st.markdown(f"""
                <span style="background: #2196F3; color: white; padding: 3px 8px; border-radius: 10px; font-size: 12px;">
                    {component}
                </span>
                """, unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### Data Flow Architecture")
        st.markdown("Detailed data flow showing how information moves through the system.")
        
        # Display data flows
        flows_df = pd.DataFrame(analysis['data_flow_architecture']['flows'])
        if not flows_df.empty:
            st.dataframe(flows_df, width='stretch')
        
        st.markdown("""
        **Data Flow Summary:**
        - Payment instructions flow through AI agents for processing
        - Customer data is retrieved from Snowflake via secure PrivateLink
        - Anomaly detection processes transaction data in real-time
        - Escalated cases trigger research workflows using external APIs
        - Approved transactions are executed through secure payment APIs
        """)
    
    with tab4:
        st.markdown("### Integration Architecture")
        st.markdown("Integration points and external system connections.")
        
        # Display integration points
        integrations_df = pd.DataFrame(analysis['integration_architecture']['integrations'])
        if not integrations_df.empty:
            st.dataframe(integrations_df, width='stretch')
        
        st.markdown("""
        **Integration Points:**
        - **Payment Networks**: External payment processing systems
        - **Google APIs**: External data sources for research
        - **Snowflake**: Customer transaction data warehouse
        - **SageMaker**: ML model hosting and inference
        - **Apigee**: API management and security gateway
        """)
    
    with tab5:
        st.markdown("### Security Architecture")
        st.markdown("Security zones and requirements for different system components.")
        
        # Display security requirements
        for req in analysis['security_architecture']['requirements']:
            severity_color = "#F44336" if req['security_level'] == 'High' else "#FF9800" if req['security_level'] == 'Medium' else "#4CAF50"
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.8); border-left: 4px solid {severity_color}; padding: 15px; margin: 10px 0; border-radius: 5px;">
                <h4 style="margin: 0 0 10px 0; color: #2c3e50;">{req['component']} ({req['security_level']} Security)</h4>
                <ul style="margin: 0; color: #5a6c7d;">
            """, unsafe_allow_html=True)
            
            for requirement in req['requirements']:
                st.markdown(f"<li>{requirement}</li>", unsafe_allow_html=True)
            
            st.markdown("</ul></div>", unsafe_allow_html=True)
    
    # AI Agent Policies Section
    st.markdown("""
    <div class="glass-card">
        <h2>AI Agent Deployment Policies</h2>
    </div>
    """, unsafe_allow_html=True)
    
    for agent_name, agent_info in analysis['ai_agent_policies'].items():
        with st.expander(f"🤖 {agent_info['name']}", expanded=True):
            st.markdown(f"**Purpose:** {agent_info['purpose']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Policies:**")
                for policy in agent_info['policies']:
                    st.markdown(f"• {policy}")
            
            with col2:
                st.markdown("**Deployment Requirements:**")
                for req in agent_info['deployment_requirements']:
                    st.markdown(f"• {req}")
    
    # Recommendations
    if analysis['recommendations']:
        st.markdown("""
        <div class="glass-card">
            <h3>Recommendations</h3>
        </div>
        """, unsafe_allow_html=True)
        
        for rec in analysis['recommendations']:
            st.info(f"💡 {rec}")
    
    # Generate Report
    if st.button("Generate Comprehensive Architecture Report", width='stretch'):
        generator = ArchitectureBlueprintGenerator()
        report = generator.generate_comprehensive_report(analysis)
        
        st.download_button(
            label="Download Architecture Blueprint Report",
            data=report,
            file_name="high_value_payments_architecture_blueprint.md",
            mime="text/markdown"
        )

def show_technology_detection():
    st.markdown("""
    <div class="fade-in-up">
        <h1>Technology Detection & Analysis</h1>
        <p style="color: #5a6c7d;">High-Value Payments System Technology Stack Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load High-Value Payments System blueprint
    try:
        with open('high_value_payments_blueprint.json', 'r') as f:
            blueprint_data = json.load(f)
        
        generator = ArchitectureBlueprintGenerator()
        analysis = generator.analyze_blueprint(blueprint_data)
        tech_analysis = analysis['technology_analysis']
        
        # System Overview
        st.markdown(f"""
        <div class="glass-card">
            <h2>High-Value Payments System Technology Analysis</h2>
            <p style="color: #5a6c7d; font-size: 18px;">Comprehensive technology stack analysis with compliance scoring</p>
            <div style="display: flex; gap: 20px; margin-top: 20px;">
                <div style="text-align: center;">
                    <div style="font-size: 24px; font-weight: bold; color: #4CAF50;">{tech_analysis['compliance_score']}%</div>
                    <div style="color: #5a6c7d;">Compliance Score</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 24px; font-weight: bold; color: #2196F3;">{tech_analysis['total_technologies']}</div>
                    <div style="color: #5a6c7d;">Total Technologies</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 24px; font-weight: bold; color: #FF9800;">{tech_analysis['core_count']}</div>
                    <div style="color: #5a6c7d;">Core Technologies</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Technology categories
        tab1, tab2, tab3, tab4 = st.tabs(["✅ Approved", "⭐ Core", "❌ Non-Approved", "❓ Unknown"])
        
        with tab1:
            st.markdown("### Approved Technologies")
            if tech_analysis['approved']:
                for tech in tech_analysis['approved']:
                    confidence_color = "#4CAF50" if tech['confidence'] >= 90 else "#FF9800" if tech['confidence'] >= 70 else "#F44336"
                    st.markdown(f"""
                    <div style="background: rgba(76, 175, 80, 0.1); border-left: 4px solid #4CAF50; padding: 15px; margin: 10px 0; border-radius: 10px; border: 1px solid rgba(0, 0, 0, 0.1);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h4 style="margin: 0; color: #2c3e50;">{tech['name']} v{tech['version']}</h4>
                                <p style="margin: 5px 0; color: #5a6c7d;">{tech['description']}</p>
                                <span style="background: #4CAF50; color: white; padding: 4px 8px; border-radius: 10px; font-size: 12px;">{tech['category']}</span>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 24px; font-weight: bold; color: {confidence_color};">{tech['confidence']}%</div>
                                <div style="font-size: 12px; color: #5a6c7d;">Confidence</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No approved technologies found")
        
        with tab2:
            st.markdown("### Core Technologies")
            if tech_analysis['core']:
                for tech in tech_analysis['core']:
                    st.markdown(f"""
                    <div style="background: rgba(33, 150, 243, 0.1); border-left: 4px solid #2196F3; padding: 15px; margin: 10px 0; border-radius: 10px; border: 1px solid rgba(0, 0, 0, 0.1);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h4 style="margin: 0; color: #2c3e50;">{tech['name']} v{tech['version']}</h4>
                                <p style="margin: 5px 0; color: #5a6c7d;">{tech['description']}</p>
                                <span style="background: #2196F3; color: white; padding: 4px 8px; border-radius: 10px; font-size: 12px;">{tech['category']}</span>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 24px; font-weight: bold; color: #2196F3;">{tech['confidence']}%</div>
                                <div style="font-size: 12px; color: #5a6c7d;">Confidence</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No core technologies found")
        
        with tab3:
            st.markdown("### Non-Approved Technologies")
            if tech_analysis['non_approved']:
                for tech in tech_analysis['non_approved']:
                    st.markdown(f"""
                    <div style="background: rgba(244, 67, 54, 0.1); border-left: 4px solid #F44336; padding: 15px; margin: 10px 0; border-radius: 10px; border: 1px solid rgba(0, 0, 0, 0.1);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h4 style="margin: 0; color: #2c3e50;">{tech['name']} v{tech['version']}</h4>
                                <p style="margin: 5px 0; color: #5a6c7d;">{tech['description']}</p>
                                <span style="background: #F44336; color: white; padding: 4px 8px; border-radius: 10px; font-size: 12px;">{tech['category']}</span>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 24px; font-weight: bold; color: #F44336;">{tech['confidence']}%</div>
                                <div style="font-size: 12px; color: #5a6c7d;">Confidence</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("No non-approved technologies found")
        
        with tab4:
            st.markdown("### Unknown Technologies")
            if tech_analysis['unknown']:
                for tech in tech_analysis['unknown']:
                    st.markdown(f"""
                    <div style="background: rgba(255, 152, 0, 0.1); border-left: 4px solid #FF9800; padding: 15px; margin: 10px 0; border-radius: 10px; border: 1px solid rgba(0, 0, 0, 0.1);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h4 style="margin: 0; color: #2c3e50;">{tech['name']} v{tech['version']}</h4>
                                <p style="margin: 5px 0; color: #5a6c7d;">{tech['description']}</p>
                                <span style="background: #FF9800; color: white; padding: 4px 8px; border-radius: 10px; font-size: 12px;">{tech['category']}</span>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 24px; font-weight: bold; color: #FF9800;">{tech['confidence']}%</div>
                                <div style="font-size: 12px; color: #5a6c7d;">Confidence</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No unknown technologies found")
        
        # Recommendations
        if tech_analysis['recommendations']:
            st.markdown("""
            <div class="glass-card">
                <h3>Technology Recommendations</h3>
            </div>
            """, unsafe_allow_html=True)
            
            for rec in tech_analysis['recommendations']:
                st.info(f"💡 {rec}")
    
    except Exception as e:
        st.error(f"Error loading blueprint data: {str(e)}")
        st.info("Please ensure the high_value_payments_blueprint.json file exists in the project directory.")

def show_data_flow():
    st.markdown("""
    <div class="fade-in-up">
        <h1>Data Flow Visualization</h1>
        <p style="color: #5a6c7d;">High-Value Payments System Data Flow Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load High-Value Payments System blueprint
    try:
        with open('high_value_payments_blueprint.json', 'r') as f:
            blueprint_data = json.load(f)
        
        generator = ArchitectureBlueprintGenerator()
        analysis = generator.analyze_blueprint(blueprint_data)
        data_flows = analysis['data_flow_architecture']['flows']
        
        # System Overview
        st.markdown(f"""
        <div class="glass-card">
            <h2>High-Value Payments System Data Flow</h2>
            <p style="color: #5a6c7d; font-size: 18px;">Real-time data flow analysis with security and frequency analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Data flow controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            flow_type = st.selectbox("Flow Type", ["All", "Payment Request", "Data Request", "SQL Query", "ML Inference", "Alert", "Research Query", "Transaction Execution"])
        
        with col2:
            security_level = st.selectbox("Security Level", ["All", "High", "Medium", "Low"])
        
        with col3:
            time_range = st.selectbox("Time Range", ["Real-time", "Last Hour", "Last Day", "Last Week"])
        
        # Filter flows based on selections
        filtered_flows = data_flows
        if flow_type != "All":
            filtered_flows = [flow for flow in filtered_flows if flow_type.lower() in flow['type'].lower()]
        if security_level != "All":
            filtered_flows = [flow for flow in filtered_flows if flow['security_level'] == security_level]
        
        # Create network graph for data flows
        G = nx.DiGraph()
        
        # Add nodes and edges from data flows
        for flow in filtered_flows:
            source = flow['source']
            target = flow['target']
            flow_type = flow['type']
            security = flow['security_level']
            
            # Add nodes
            G.add_node(source, label=source, type="component")
            G.add_node(target, label=target, type="component")
            
            # Add edge with flow information
            G.add_edge(source, target, 
                      type=flow_type, 
                      security=security,
                      description=flow['description'])
        
        # Create hierarchical layout for better flow visualization
        # Define the flow order from Payment Instruction to Payment Execution
        flow_order = [
            "Payment Instruction",
            "Intent Agent", 
            "Retriever Agent",
            "Snowflake",
            "Anomaly Detection",
            "SageMaker API",
            "Escalation Workflow",
            "React App",
            "Google APIs",
            "Approval Workflow",
            "Payment API"
        ]
        
        # Create hierarchical positions
        pos = {}
        layer_height = 2.0
        nodes_per_layer = 3
        
        for i, node in enumerate(flow_order):
            if node in G.nodes():
                layer = i // nodes_per_layer
                position_in_layer = i % nodes_per_layer
                x = position_in_layer * 2.0 - (nodes_per_layer - 1)
                y = -layer * layer_height
                pos[node] = (x, y)
        
        # Position remaining nodes
        remaining_nodes = [node for node in G.nodes() if node not in flow_order]
        for i, node in enumerate(remaining_nodes):
            layer = len(flow_order) // nodes_per_layer + 1
            position_in_layer = i % nodes_per_layer
            x = position_in_layer * 2.0 - (nodes_per_layer - 1)
            y = -layer * layer_height
            pos[node] = (x, y)
        
        edge_x = []
        edge_y = []
        edge_info = []
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            
            edge_data = G.edges[edge]
            # Lighter, more intuitive colors based on security level
            security_color = "rgba(76, 175, 80, 0.6)" if edge_data['security'] == 'High' else "rgba(255, 152, 0, 0.6)" if edge_data['security'] == 'Medium' else "rgba(244, 67, 54, 0.6)"
            edge_info.append(f"From: {edge[0]}<br>To: {edge[1]}<br>Type: {edge_data['type']}<br>Security: {edge_data['security']}<br>Description: {edge_data['description']}")
        
        node_x = []
        node_y = []
        node_text = []
        node_colors = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
            # Color nodes based on type
            if "Agent" in node or "AI" in node:
                node_colors.append("#2196F3")  # Blue for AI agents
            elif "API" in node or "Gateway" in node:
                node_colors.append("#4CAF50")  # Green for APIs
            elif "Database" in node or "Snowflake" in node:
                node_colors.append("#9C27B0")  # Purple for databases
            elif "SageMaker" in node or "ML" in node:
                node_colors.append("#FF9800")  # Orange for ML
            else:
                node_colors.append("#607D8B")  # Gray for others
        
        # Create the plot
        fig = go.Figure()
        
        # Add edges with lighter, more intuitive styling
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='rgba(100, 100, 100, 0.4)'),
            hoverinfo='text',
            hovertext=edge_info,
            mode='lines',
            name='Data Flows',
            showlegend=False
        ))
        
        # Add arrow annotations for better flow direction indication
        for i in range(0, len(edge_x), 3):
            if i + 2 < len(edge_x):
                x0, x1 = edge_x[i], edge_x[i+1]
                y0, y1 = edge_y[i], edge_y[i+1]
                
                # Calculate arrow position (80% along the line)
                arrow_x = x0 + 0.8 * (x1 - x0)
                arrow_y = y0 + 0.8 * (y1 - y0)
                
                # Calculate arrow direction
                dx = x1 - x0
                dy = y1 - y0
                length = (dx**2 + dy**2)**0.5
                if length > 0:
                    dx_norm = dx / length
                    dy_norm = dy / length
                    
                    # Add arrow annotation
                    fig.add_annotation(
                        x=arrow_x,
                        y=arrow_y,
                        ax=arrow_x - 0.1 * dx_norm,
                        ay=arrow_y - 0.1 * dy_norm,
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="rgba(100, 100, 100, 0.6)",
                        showarrow=True,
                        axref="x",
                        ayref="y"
                    )
        
        # Add nodes with improved styling
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition="middle center",
            textfont=dict(size=12, color='white', family='Arial Black'),
            marker=dict(
                size=80,
                color=node_colors,
                line=dict(width=2, color='rgba(255, 255, 255, 0.8)'),
                opacity=0.9
            ),
            name='Components',
            showlegend=False
        ))
        
        fig.update_layout(
            title="High-Value Payments System Data Flow - Payment Instruction → Payment Execution",
            title_font_size=18,
            title_font_color="#2c3e50",
            showlegend=False,
            hovermode='closest',
            margin=dict(b=40,l=20,r=20,t=60),
            annotations=[
                dict(
                    text="🔄 Data flows from Payment Instruction to Payment Execution",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.5, y=-0.05,
                    xanchor="center", yanchor="top",
                    font=dict(color="#5a6c7d", size=14, family="Arial")
                ),
                dict(
                    text="💡 Hover over components and flows for detailed information",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.5, y=-0.1,
                    xanchor="center", yanchor="top",
                    font=dict(color="#9E9E9E", size=12, family="Arial")
                )
            ],
            xaxis=dict(
                showgrid=False, 
                zeroline=False, 
                showticklabels=False,
                range=[-4, 4]
            ),
            yaxis=dict(
                showgrid=False, 
                zeroline=False, 
                showticklabels=False,
                range=[-8, 2]
            ),
            plot_bgcolor='rgba(255,255,255,0.8)',
            paper_bgcolor='rgba(255,255,255,0.8)',
            font=dict(color="#2c3e50"),
            width=900,
            height=600
        )
        
        st.plotly_chart(fig, width='stretch')
        
        # Flow Legend
        st.markdown("""
        <div class="glass-card" style="margin-top: 20px;">
            <h4 style="color: #2c3e50; margin-bottom: 15px;">Flow Legend</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px;">
                <div style="text-align: center; padding: 10px; background: rgba(76, 175, 80, 0.1); border-radius: 8px; border: 1px solid rgba(76, 175, 80, 0.3);">
                    <div style="width: 20px; height: 3px; background: rgba(76, 175, 80, 0.6); margin: 0 auto 8px;"></div>
                    <strong style="color: #2E7D32;">High Security</strong><br>
                    <small style="color: #5a6c7d;">Payment & ML flows</small>
                </div>
                <div style="text-align: center; padding: 10px; background: rgba(255, 152, 0, 0.1); border-radius: 8px; border: 1px solid rgba(255, 152, 0, 0.3);">
                    <div style="width: 20px; height: 3px; background: rgba(255, 152, 0, 0.6); margin: 0 auto 8px;"></div>
                    <strong style="color: #F57C00;">Medium Security</strong><br>
                    <small style="color: #5a6c7d;">Research & alerts</small>
                </div>
                <div style="text-align: center; padding: 10px; background: rgba(244, 67, 54, 0.1); border-radius: 8px; border: 1px solid rgba(244, 67, 54, 0.3);">
                    <div style="width: 20px; height: 3px; background: rgba(244, 67, 54, 0.6); margin: 0 auto 8px;"></div>
                    <strong style="color: #D32F2F;">Low Security</strong><br>
                    <small style="color: #5a6c7d;">Review needed</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Data flow details table
        st.markdown("""
        <div class="glass-card">
            <h3>Data Flow Details</h3>
        </div>
        """, unsafe_allow_html=True)
        
        flows_df = pd.DataFrame(filtered_flows)
        if not flows_df.empty:
            st.dataframe(flows_df, width='stretch')
        else:
            st.info("No data flows match the selected criteria")
        
        # Security analysis
        st.markdown("""
        <div class="glass-card">
            <h3>Security Analysis</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Count flows by security level
        security_counts = {}
        for flow in data_flows:
            level = flow['security_level']
            security_counts[level] = security_counts.get(level, 0) + 1
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("High Security Flows", security_counts.get('High', 0), delta="Secure")
        
        with col2:
            st.metric("Medium Security Flows", security_counts.get('Medium', 0), delta="Moderate")
        
        with col3:
            st.metric("Low Security Flows", security_counts.get('Low', 0), delta="Review Needed")
        
        # Security recommendations
        st.markdown("""
        <div class="glass-card">
            <h4>Security Recommendations</h4>
            <ul style="color: #5a6c7d;">
                <li>All payment-related data flows use High security level</li>
                <li>Customer data retrieval via PrivateLink ensures network isolation</li>
                <li>ML inference calls are secured with authentication</li>
                <li>External API calls require proper rate limiting and monitoring</li>
                <li>Transaction execution flows have end-to-end encryption</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Error loading blueprint data: {str(e)}")
        st.info("Please ensure the high_value_payments_blueprint.json file exists in the project directory.")

def show_architecture():
    st.markdown("""
    <div class="fade-in-up">
        <h1>Architecture Visualization</h1>
        <p style="color: #5a6c7d;">High-Value Payments System Conceptual and Logical Architecture</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load High-Value Payments System blueprint
    try:
        with open('high_value_payments_blueprint.json', 'r') as f:
            blueprint_data = json.load(f)
        
        generator = ArchitectureBlueprintGenerator()
        analysis = generator.analyze_blueprint(blueprint_data)
        
        # Architecture view controls
        col1, col2 = st.columns(2)
        
        with col1:
            view_mode = st.selectbox("View Mode", ["Conceptual", "Logical", "Integration", "Security"])
        
        with col2:
            architecture_type = st.selectbox("Architecture Type", ["High-Value Payments", "AI-Powered", "Microservices", "Hybrid Cloud"])
        
        # Create tabs for different architecture views
        tab1, tab2, tab3, tab4 = st.tabs(["🏗️ Conceptual", "📋 Logical", "🔗 Integration", "🛡️ Security"])
        
        with tab1:
            st.markdown("### Conceptual Architecture")
            st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.8); border-radius: 15px; padding: 20px; margin: 10px 0; border: 1px solid rgba(0, 0, 0, 0.1);">
                <h4 style="color: #2c3e50; margin-bottom: 15px;">High-Value Payments System Overview</h4>
                <p style="color: #5a6c7d; font-size: 16px; line-height: 1.6;">
                    This diagram shows the complete flow of a high-value payment through our AI-powered system. 
                    The process begins with a payment instruction and flows through various AI agents, data sources, 
                    and approval workflows to ensure secure and compliant transaction processing.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Generate conceptual diagram
            fig_conceptual = create_architecture_visualizations(analysis)
            st.plotly_chart(fig_conceptual, width='stretch')
            
            # Enhanced component descriptions with detailed paragraphs
            st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.8); border-radius: 15px; padding: 20px; margin: 20px 0; border: 1px solid rgba(0, 0, 0, 0.1);">
                <h4 style="color: #2c3e50; margin-bottom: 20px;">System Components</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div>
                        <h5 style="color: #2E7D32; margin-bottom: 10px;">🟢 Payment Input</h5>
                        <p style="color: #5a6c7d; margin-bottom: 15px; line-height: 1.6;"><strong>Payment Instruction:</strong> The Payment Instruction serves as the initial input for a payment transaction, detailing essential information such as the payer and payee details, transaction amount, currency, and payment method. This instruction is crucial for initiating the payment process and ensuring all necessary data is accurately captured. It acts as the foundation for the entire payment process, ensuring that all subsequent steps are based on accurate and complete data.</p>
                        
                        <h5 style="color: #1565C0; margin-bottom: 10px;">🔵 AI Agents</h5>
                        <p style="color: #5a6c7d; margin-bottom: 10px; line-height: 1.6;"><strong>Intent Agent:</strong> The Intent Agent is an AI-driven component designed to interpret and understand the user's payment requests. It analyzes natural language inputs to discern the user's intent, ensuring that the payment instructions are accurately formulated and aligned with the user's expectations. This agent plays a pivotal role in enhancing user experience by facilitating seamless and intuitive payment interactions through natural language processing and contextual analysis.</p>
                        <p style="color: #5a6c7d; margin-bottom: 15px; line-height: 1.6;"><strong>Retriever Agent:</strong> The Retriever Agent is responsible for accessing and retrieving relevant data stored in Snowflake, a cloud-based data warehousing service. It ensures that the payment system has access to up-to-date and accurate information, such as account balances, transaction histories, and user profiles, which are essential for processing payments and conducting risk assessments. By leveraging Snowflake's scalable architecture, it ensures timely and efficient data access.</p>
                        
                        <h5 style="color: #E65100; margin-bottom: 10px;">🟠 Data Storage</h5>
                        <p style="color: #5a6c7d; margin-bottom: 15px; line-height: 1.6;"><strong>Snowflake (AWS):</strong> Snowflake serves as the centralized data warehouse for customer transaction history and analytics, providing a secure and scalable platform for storing and retrieving financial data. It offers advanced features including encryption at rest, column-level security, network isolation through PrivateLink, and comprehensive audit logging. The platform is optimized for analytical queries and real-time data access, ensuring that the payment system can quickly retrieve necessary information for transaction processing and risk assessment.</p>
                    </div>
                    <div>
                        <h5 style="color: #6A1B9A; margin-bottom: 10px;">🟣 ML Services</h5>
                        <p style="color: #5a6c7d; margin-bottom: 15px; line-height: 1.6;"><strong>Anomaly Detection (SageMaker):</strong> The Anomaly Detection system utilizes AWS SageMaker's machine learning capabilities to monitor and analyze transaction patterns in real-time, identifying deviations that may indicate fraudulent activity. By employing advanced ML algorithms such as Isolation Forest, One-Class SVM, and Autoencoders, it can detect unusual patterns in transaction amounts, frequencies, geolocations, and behavioral patterns. The system continuously learns from historical data, enhancing its ability to detect and prevent unauthorized transactions while providing explainable AI insights for compliance and audit purposes.</p>
                        
                        <h5 style="color: #C62828; margin-bottom: 10px;">🔴 User Interface</h5>
                        <p style="color: #5a6c7d; margin-bottom: 10px; line-height: 1.6;"><strong>Escalation (React App):</strong> The Escalation Interface is a user-friendly React application designed to handle cases that require manual intervention and review. When the Anomaly Detection Agent identifies suspicious transactions or when the system encounters complex cases that cannot be automatically processed, they are routed to this interface for human review. The application provides comprehensive transaction details, research tools, and approval workflows, enabling analysts, compliance officers, and risk managers to make informed decisions efficiently while maintaining a complete audit trail.</p>
                        <p style="color: #5a6c7d; margin-bottom: 15px; line-height: 1.6;"><strong>Google APIs:</strong> Google APIs serve as external data sources for research and validation during the escalation process, providing access to services such as Google Search API, Maps API, News API, and Translate API. These APIs enable comprehensive entity verification, news research, location validation, and language translation capabilities, supporting the manual review process with rich contextual information while implementing proper rate limiting and cost management controls.</p>
                        
                        <h5 style="color: #1A237E; margin-bottom: 10px;">🔵 API Services</h5>
                        <p style="color: #5a6c7d; margin-bottom: 10px; line-height: 1.6;"><strong>Approval Workflow:</strong> The Approval Workflow automates the process of reviewing and approving payment transactions by incorporating predefined rules, compliance checks, and risk assessments. It defines a series of steps and criteria that transactions must meet to be approved, including amount thresholds, customer limits, compliance verification, and risk scoring. This automation streamlines operations, reduces processing times, ensures consistency in decision-making, and can be configured to accommodate various approval hierarchies and organizational policies.</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px; line-height: 1.6;"><strong>Payment API (Apigee):</strong> The Payment API serves as the final conduit for executing approved payment transactions, utilizing Apigee as the API management platform to handle secure communication with financial institutions and payment processors. It manages the complete payment lifecycle including payment processing, settlement, confirmation, and error handling, while integrating with payment networks, banks, clearing houses, and settlement systems. The API ensures that transactions are completed accurately and efficiently while maintaining comprehensive audit trails and compliance with financial regulations.</p>
                        <p style="color: #5a6c7d; margin-bottom: 15px; line-height: 1.6;"><strong>Apigee Gateway:</strong> Apigee Gateway provides centralized API management and security for all payment services, offering robust features including authentication, authorization, rate limiting, monitoring, and analytics. It implements advanced security measures such as OAuth 2.0, JWT tokens, API key management, and threat protection, while providing comprehensive usage analytics, performance metrics, and audit logs. This gateway ensures that all API communications are secure, monitored, and compliant with industry standards and regulatory requirements.</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Process flow explanation
            st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.8); border-radius: 15px; padding: 20px; margin: 20px 0; border: 1px solid rgba(0, 0, 0, 0.1);">
                <h4 style="color: #2c3e50; margin-bottom: 20px;">Process Flow</h4>
                <div style="display: flex; flex-direction: column; gap: 15px;">
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <div style="background: #2E7D32; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">1</div>
                        <p style="color: #5a6c7d; margin: 0;"><strong>Payment Instruction</strong> is received and processed by the <strong>Intent Agent</strong></p>
                    </div>
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <div style="background: #1565C0; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">2</div>
                        <p style="color: #5a6c7d; margin: 0;"><strong>Retriever Agent</strong> fetches customer data from <strong>Snowflake</strong> via secure PrivateLink</p>
                    </div>
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <div style="background: #6A1B9A; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">3</div>
                        <p style="color: #5a6c7d; margin: 0;"><strong>Anomaly Detection</strong> analyzes transaction data using ML models on <strong>SageMaker</strong></p>
                    </div>
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <div style="background: #C62828; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">4</div>
                        <p style="color: #5a6c7d; margin: 0;">If suspicious, transaction is escalated to <strong>React App</strong> for manual review</p>
                    </div>
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <div style="background: #1A237E; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">5</div>
                        <p style="color: #5a6c7d; margin: 0;">Approved transactions are executed via <strong>Payment API</strong> through <strong>Apigee Gateway</strong></p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Detailed Component Documentation
            st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.8); border-radius: 15px; padding: 20px; margin: 20px 0; border: 1px solid rgba(0, 0, 0, 0.1);">
                <h4 style="color: #2c3e50; margin-bottom: 25px;">Detailed Component Documentation</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Component 1: Payment Instruction
            st.markdown("""
            <div style="background: rgba(46, 125, 50, 0.1); border-left: 4px solid #2E7D32; border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h5 style="color: #2E7D32; margin-bottom: 15px;">🟢 Payment Instruction</h5>
                <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 20px;">
                    <div>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Type:</strong> Input Component</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Technology:</strong> REST API, JSON</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Security Level:</strong> High</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Data Format:</strong> Structured JSON</p>
                    </div>
                    <div>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Purpose:</strong> Initial payment request input from users, systems, or external applications</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Key Data:</strong> Amount, currency, recipient details, sender information, payment type</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Validation:</strong> Format validation, required field checks, data type verification</p>
                        <p style="color: #5a6c7d; margin-bottom: 0;"><strong>Output:</strong> Validated payment instruction passed to Intent Agent</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Component 2: Intent Agent
            st.markdown("""
            <div style="background: rgba(21, 101, 192, 0.1); border-left: 4px solid #1565C0; border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h5 style="color: #1565C0; margin-bottom: 15px;">🔵 Intent Agent (AI)</h5>
                <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 20px;">
                    <div>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Type:</strong> AI Agent</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Technology:</strong> Python, MCP Protocol</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Security Level:</strong> High</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Deployment:</strong> Containerized</p>
                    </div>
                    <div>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Purpose:</strong> Process and understand payment instructions using natural language processing</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Key Functions:</strong> Intent classification, entity extraction, payment validation, risk assessment</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>AI Capabilities:</strong> NLP models, pattern recognition, decision trees, confidence scoring</p>
                        <p style="color: #5a6c7d; margin-bottom: 0;"><strong>Output:</strong> Structured payment data and processing instructions for Retriever Agent</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Component 3: Retriever Agent
            st.markdown("""
            <div style="background: rgba(21, 101, 192, 0.1); border-left: 4px solid #1565C0; border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h5 style="color: #1565C0; margin-bottom: 15px;">🔵 Retriever Agent (AI)</h5>
                <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 20px;">
                    <div>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Type:</strong> AI Agent</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Technology:</strong> Python, SQL, MCP Protocol</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Security Level:</strong> High</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Deployment:</strong> Containerized</p>
                    </div>
                    <div>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Purpose:</strong> Retrieve customer transaction history and relevant data from Snowflake</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Key Functions:</strong> Query optimization, data retrieval, privacy compliance, caching</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Data Sources:</strong> Customer profiles, transaction history, risk scores, compliance data</p>
                        <p style="color: #5a6c7d; margin-bottom: 0;"><strong>Output:</strong> Customer data and transaction context for anomaly detection</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Component 4: Snowflake
            st.markdown("""
            <div style="background: rgba(230, 81, 0, 0.1); border-left: 4px solid #E65100; border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h5 style="color: #E65100; margin-bottom: 15px;">🟠 Snowflake (AWS)</h5>
                <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 20px;">
                    <div>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Type:</strong> Data Warehouse</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Technology:</strong> Snowflake, AWS</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Security Level:</strong> High</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Connectivity:</strong> PrivateLink</p>
                    </div>
                    <div>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Purpose:</strong> Centralized data warehouse for customer transaction history and analytics</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Key Data:</strong> Customer profiles, transaction history, risk assessments, compliance records</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Security Features:</strong> Encryption at rest, column-level security, network isolation, audit logging</p>
                        <p style="color: #5a6c7d; margin-bottom: 0;"><strong>Performance:</strong> Optimized for analytical queries, real-time data access, scalable compute</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Component 5: Anomaly Detection
            st.markdown("""
            <div style="background: rgba(106, 27, 154, 0.1); border-left: 4px solid #6A1B9A; border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h5 style="color: #6A1B9A; margin-bottom: 15px;">🟣 Anomaly Detection (SageMaker)</h5>
                <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 20px;">
                    <div>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Type:</strong> ML Service</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Technology:</strong> AWS SageMaker, ML Models</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Security Level:</strong> High</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Deployment:</strong> Managed Service</p>
                    </div>
                    <div>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Purpose:</strong> Real-time analysis of transaction data to detect suspicious patterns and anomalies</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>ML Models:</strong> Isolation Forest, One-Class SVM, Autoencoders, Ensemble methods</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Key Features:</strong> Real-time inference, model versioning, A/B testing, explainable AI</p>
                        <p style="color: #5a6c7d; margin-bottom: 0;"><strong>Output:</strong> Anomaly scores, risk levels, and escalation recommendations</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Component 6: Escalation Interface
            st.markdown("""
            <div style="background: rgba(198, 40, 40, 0.1); border-left: 4px solid #C62828; border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h5 style="color: #C62828; margin-bottom: 15px;">🔴 Escalation Interface (React App)</h5>
                <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 20px;">
                    <div>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Type:</strong> User Interface</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Technology:</strong> React 18, JavaScript</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Security Level:</strong> Medium</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Deployment:</strong> Web Application</p>
                    </div>
                    <div>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Purpose:</strong> Web interface for manual review and research of escalated transactions</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Key Features:</strong> Transaction details, research tools, approval workflow, audit trail</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>User Roles:</strong> Analysts, approvers, compliance officers, risk managers</p>
                        <p style="color: #5a6c7d; margin-bottom: 0;"><strong>Integration:</strong> Google APIs for external research, approval workflow for decision tracking</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Component 7: Google APIs
            st.markdown("""
            <div style="background: rgba(55, 71, 79, 0.1); border-left: 4px solid #37474F; border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h5 style="color: #37474F; margin-bottom: 15px;">⚫ Google APIs (External)</h5>
                <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 20px;">
                    <div>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Type:</strong> External Service</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Technology:</strong> REST APIs, OAuth 2.0</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Security Level:</strong> Medium</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Connectivity:</strong> HTTPS</p>
                    </div>
                    <div>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Purpose:</strong> External data sources for research and validation during escalation</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Key Services:</strong> Google Search API, Maps API, News API, Translate API</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Use Cases:</strong> Entity verification, news research, location validation, language translation</p>
                        <p style="color: #5a6c7d; margin-bottom: 0;"><strong>Rate Limiting:</strong> API quotas, request throttling, cost management</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Component 8: Approval Workflow
            st.markdown("""
            <div style="background: rgba(26, 35, 126, 0.1); border-left: 4px solid #1A237E; border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h5 style="color: #1A237E; margin-bottom: 15px;">🔵 Approval Workflow (API)</h5>
                <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 20px;">
                    <div>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Type:</strong> Business Process</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Technology:</strong> Node.js, Workflow Engine</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Security Level:</strong> High</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Deployment:</strong> Microservice</p>
                    </div>
                    <div>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Purpose:</strong> Automated approval process for transactions based on business rules and policies</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Key Functions:</strong> Rule evaluation, approval routing, notification management, audit logging</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Business Rules:</strong> Amount thresholds, customer limits, compliance checks, risk scoring</p>
                        <p style="color: #5a6c7d; margin-bottom: 0;"><strong>Output:</strong> Approval decisions and transaction execution instructions</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Component 9: Payment API
            st.markdown("""
            <div style="background: rgba(26, 35, 126, 0.1); border-left: 4px solid #1A237E; border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h5 style="color: #1A237E; margin-bottom: 15px;">🔵 Payment API (Apigee)</h5>
                <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 20px;">
                    <div>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Type:</strong> API Service</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Technology:</strong> REST API, Apigee</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Security Level:</strong> High</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Deployment:</strong> Managed Service</p>
                    </div>
                    <div>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Purpose:</strong> Final transaction execution service for approved payments</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Key Functions:</strong> Payment processing, settlement, confirmation, error handling</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Integration:</strong> Payment networks, banks, clearing houses, settlement systems</p>
                        <p style="color: #5a6c7d; margin-bottom: 0;"><strong>Output:</strong> Transaction confirmations, status updates, settlement notifications</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Component 10: Apigee Gateway
            st.markdown("""
            <div style="background: rgba(173, 20, 87, 0.1); border-left: 4px solid #AD1457; border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h5 style="color: #AD1457; margin-bottom: 15px;">🟣 Apigee Gateway</h5>
                <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 20px;">
                    <div>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Type:</strong> API Gateway</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Technology:</strong> Apigee, API Management</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Security Level:</strong> High</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Deployment:</strong> Managed Service</p>
                    </div>
                    <div>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Purpose:</strong> Centralized API management and security gateway for all payment services</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Key Functions:</strong> Authentication, authorization, rate limiting, monitoring, analytics</p>
                        <p style="color: #5a6c7d; margin-bottom: 10px;"><strong>Security Features:</strong> OAuth 2.0, JWT tokens, API key management, threat protection</p>
                        <p style="color: #5a6c7d; margin-bottom: 0;"><strong>Output:</strong> Secured API access, usage analytics, performance metrics, audit logs</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown("### Logical Architecture")
            st.markdown("Layered architecture showing system components organized by functional layers.")
            
            # Display logical architecture layers
            layers = analysis['logical_architecture']['layers']
            layer_colors = ["#4CAF50", "#2196F3", "#FF9800", "#9C27B0", "#F44336", "#607D8B"]
            
            for i, layer in enumerate(layers):
                color = layer_colors[i % len(layer_colors)]
                st.markdown(f"""
                <div style="background: {color}15; border-left: 4px solid {color}; border-radius: 10px; padding: 20px; margin: 10px 0; border: 1px solid rgba(0, 0, 0, 0.1);">
                    <h4 style="margin: 0 0 10px 0; color: #2c3e50;">{layer['label']}</h4>
                    <p style="margin: 0 0 15px 0; color: #5a6c7d;">{layer['description']}</p>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                """, unsafe_allow_html=True)
                
                for component in layer['components']:
                    st.markdown(f"""
                    <span style="background: {color}; color: white; padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: 500;">
                        {component}
                    </span>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
        
        with tab3:
            st.markdown("### Integration Architecture")
            st.markdown("Integration points and external system connections.")
            
            # Display integration points
            integrations = analysis['integration_architecture']['integrations']
            for integration in integrations:
                security_color = "#4CAF50" if integration['security_level'] == 'High' else "#FF9800" if integration['security_level'] == 'Medium' else "#F44336"
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.8); border-left: 4px solid {security_color}; padding: 15px; margin: 10px 0; border-radius: 10px; border: 1px solid rgba(0, 0, 0, 0.1);">
                    <h4 style="margin: 0 0 10px 0; color: #2c3e50;">{integration['name']}</h4>
                    <p style="margin: 0 0 10px 0; color: #5a6c7d;"><strong>Type:</strong> {integration['type']}</p>
                    <p style="margin: 0 0 10px 0; color: #5a6c7d;"><strong>Endpoint:</strong> {integration['endpoint']}</p>
                    <p style="margin: 0 0 10px 0; color: #5a6c7d;"><strong>Security Level:</strong> {integration['security_level']}</p>
                    <p style="margin: 0; color: #5a6c7d;"><strong>Description:</strong> {integration['description']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with tab4:
            st.markdown("### Security Architecture")
            st.markdown("Security zones and requirements for different system components.")
            
            # Display security requirements
            security_reqs = analysis['security_architecture']['requirements']
            for req in security_reqs:
                severity_color = "#F44336" if req['security_level'] == 'High' else "#FF9800" if req['security_level'] == 'Medium' else "#4CAF50"
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.8); border-left: 4px solid {severity_color}; padding: 15px; margin: 10px 0; border-radius: 10px; border: 1px solid rgba(0, 0, 0, 0.1);">
                    <h4 style="margin: 0 0 10px 0; color: #2c3e50;">{req['component']} ({req['security_level']} Security)</h4>
                    <ul style="margin: 0; color: #5a6c7d;">
                """, unsafe_allow_html=True)
                
                for requirement in req['requirements']:
                    st.markdown(f"<li>{requirement}</li>", unsafe_allow_html=True)
                
                st.markdown("</ul></div>", unsafe_allow_html=True)
        
        # Component dependency analysis
        st.markdown("""
        <div class="glass-card">
            <h3>Component Dependencies Analysis</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Create a dependency matrix for the payment system components
        components = [
            "Payment Instruction", "Intent Agent", "Retriever Agent", "Snowflake", 
            "Anomaly Detection", "Escalation Interface", "Google APIs", 
            "Approval Workflow", "Payment API", "Apigee Gateway"
        ]
        
        # Create a realistic dependency matrix
        dependency_matrix = np.zeros((len(components), len(components)))
        
        # Define dependencies based on the payment flow
        dependencies = [
            (0, 1), (1, 2), (2, 3), (2, 4), (4, 5), (5, 6), (5, 7), (7, 8), (8, 9)
        ]
        
        for dep in dependencies:
            dependency_matrix[dep[0]][dep[1]] = 1
        
        # Make it symmetric for visualization
        dependency_matrix = np.maximum(dependency_matrix, dependency_matrix.T)
        np.fill_diagonal(dependency_matrix, 0)
        
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(dependency_matrix, 
                    xticklabels=components, 
                    yticklabels=components,
                    cmap='Blues',
                    cbar_kws={'label': 'Dependency Strength'},
                    ax=ax)
        
        ax.set_title('High-Value Payments System Component Dependencies', color='#2c3e50', fontsize=16, pad=20)
        ax.set_xlabel('Dependencies', color='#2c3e50', fontsize=12)
        ax.set_ylabel('Components', color='#2c3e50', fontsize=12)
        
        # Style the plot
        ax.tick_params(colors='#2c3e50')
        ax.set_facecolor('white')
        fig.patch.set_facecolor('white')
        
        # Rotate labels for better readability
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        
        st.pyplot(fig)
    
    except Exception as e:
        st.error(f"Error loading blueprint data: {str(e)}")
        st.info("Please ensure the high_value_payments_blueprint.json file exists in the project directory.")

def show_patterns():
    st.markdown("""
    <div class="fade-in-up">
        <h1>Approved Patterns & Standards</h1>
        <p style="color: #5a6c7d;">High-Value Payments System Pattern Compliance and Governance</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load High-Value Payments System blueprint
    try:
        with open('high_value_payments_blueprint.json', 'r') as f:
            blueprint_data = json.load(f)
        
        generator = ArchitectureBlueprintGenerator()
        analysis = generator.analyze_blueprint(blueprint_data)
        tech_analysis = analysis['technology_analysis']
        
        # System Overview
        st.markdown(f"""
        <div class="glass-card">
            <h2>High-Value Payments System Pattern Compliance</h2>
            <p style="color: #5a6c7d; font-size: 18px;">Technology compliance analysis against approved patterns and standards</p>
            <div style="display: flex; gap: 20px; margin-top: 20px;">
                <div style="text-align: center;">
                    <div style="font-size: 24px; font-weight: bold; color: #4CAF50;">{tech_analysis['compliance_score']}%</div>
                    <div style="color: #5a6c7d;">Overall Compliance</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 24px; font-weight: bold; color: #2196F3;">{tech_analysis['approved_count']}</div>
                    <div style="color: #5a6c7d;">Approved Technologies</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 24px; font-weight: bold; color: #FF9800;">{tech_analysis['core_count']}</div>
                    <div style="color: #5a6c7d;">Core Technologies</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Pattern categories specific to High-Value Payments
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🏗️ Architecture Patterns", "🔒 Security Patterns", "🔄 Data Patterns", 
            "🤖 AI/ML Patterns", "🔗 Integration Patterns"
        ])
        
        with tab1:
            st.markdown("### Architecture Patterns")
            
            architecture_patterns = [
                {
                    "name": "Microservices Architecture",
                    "description": "Decompose payment system into independent services for scalability and maintainability",
                    "compliance_score": 95,
                    "usage_level": "High",
                    "category": "Architecture",
                    "technologies": ["React", "Node.js", "Python", "Docker", "Kubernetes"],
                    "last_updated": "2024-01-15"
                },
                {
                    "name": "API Gateway Pattern",
                    "description": "Centralized API management for payment processing and external integrations",
                    "compliance_score": 90,
                    "usage_level": "High",
                    "category": "Architecture",
                    "technologies": ["Apigee", "AWS API Gateway"],
                    "last_updated": "2024-01-10"
                },
                {
                    "name": "Event-Driven Architecture",
                    "description": "Asynchronous processing for payment events and notifications",
                    "compliance_score": 85,
                    "usage_level": "Medium",
                    "category": "Architecture",
                    "technologies": ["Message Queues", "Event Streaming"],
                    "last_updated": "2024-01-05"
                }
            ]
            
            for pattern in architecture_patterns:
                compliance_color = "#4CAF50" if pattern['compliance_score'] >= 90 else "#FF9800" if pattern['compliance_score'] >= 70 else "#F44336"
                usage_color = "#4CAF50" if pattern['usage_level'] == "High" else "#FF9800" if pattern['usage_level'] == "Medium" else "#F44336"
                
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.8); border-radius: 15px; padding: 20px; margin: 10px 0; border-left: 4px solid {compliance_color}; border: 1px solid rgba(0, 0, 0, 0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div style="flex: 1;">
                            <h4 style="margin: 0 0 10px 0; color: #2c3e50;">{pattern['name']}</h4>
                            <p style="margin: 0 0 10px 0; color: #5a6c7d;">{pattern['description']}</p>
                            <div style="display: flex; gap: 15px; align-items: center; margin: 10px 0;">
                                <span style="background: {compliance_color}; color: white; padding: 4px 8px; border-radius: 10px; font-size: 12px;">{pattern['category']}</span>
                                <span style="background: {usage_color}; color: white; padding: 4px 8px; border-radius: 10px; font-size: 12px;">{pattern['usage_level']} Usage</span>
                                <span style="color: #5a6c7d; font-size: 12px;">Updated: {pattern['last_updated']}</span>
                            </div>
                            <div style="display: flex; flex-wrap: wrap; gap: 5px;">
                """, unsafe_allow_html=True)
                
                for tech in pattern['technologies']:
                    st.markdown(f"""
                    <span style="background: #2196F3; color: white; padding: 3px 8px; border-radius: 10px; font-size: 11px;">
                        {tech}
                    </span>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="text-align: right; margin-left: 20px;">
                    <div style="font-size: 24px; font-weight: bold; color: {compliance_color};">{pattern['compliance_score']}%</div>
                    <div style="font-size: 12px; color: #5a6c7d;">Compliance</div>
                </div>
                <div style="background: rgba(0, 0, 0, 0.2); border-radius: 10px; height: 6px; margin-top: 15px;">
                    <div style="background: {compliance_color}; height: 100%; width: {pattern['compliance_score']}%; border-radius: 10px; transition: width 0.3s ease;"></div>
                </div>
                </div>
                """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown("### Security Patterns")
            
            security_patterns = [
                {
                    "name": "Zero Trust Architecture",
                    "description": "Never trust, always verify approach for payment system security",
                    "compliance_score": 92,
                    "usage_level": "High",
                    "category": "Security",
                    "technologies": ["OAuth 2.0", "JWT", "PrivateLink", "HTTPS"],
                    "last_updated": "2024-01-12"
                },
                {
                    "name": "Encryption at Rest and in Transit",
                    "description": "Comprehensive data protection for sensitive payment information",
                    "compliance_score": 88,
                    "usage_level": "High",
                    "category": "Security",
                    "technologies": ["TLS", "AES-256", "Snowflake Encryption"],
                    "last_updated": "2024-01-08"
                },
                {
                    "name": "API Security Gateway",
                    "description": "Centralized security controls for all payment APIs",
                    "compliance_score": 95,
                    "usage_level": "High",
                    "category": "Security",
                    "technologies": ["Apigee", "Rate Limiting", "Authentication"],
                    "last_updated": "2024-01-14"
                }
            ]
            
            for pattern in security_patterns:
                compliance_color = "#4CAF50" if pattern['compliance_score'] >= 90 else "#FF9800" if pattern['compliance_score'] >= 70 else "#F44336"
                usage_color = "#4CAF50" if pattern['usage_level'] == "High" else "#FF9800" if pattern['usage_level'] == "Medium" else "#F44336"
                
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.8); border-radius: 15px; padding: 20px; margin: 10px 0; border-left: 4px solid {compliance_color}; border: 1px solid rgba(0, 0, 0, 0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div style="flex: 1;">
                            <h4 style="margin: 0 0 10px 0; color: #2c3e50;">{pattern['name']}</h4>
                            <p style="margin: 0 0 10px 0; color: #5a6c7d;">{pattern['description']}</p>
                            <div style="display: flex; gap: 15px; align-items: center; margin: 10px 0;">
                                <span style="background: {compliance_color}; color: white; padding: 4px 8px; border-radius: 10px; font-size: 12px;">{pattern['category']}</span>
                                <span style="background: {usage_color}; color: white; padding: 4px 8px; border-radius: 10px; font-size: 12px;">{pattern['usage_level']} Usage</span>
                                <span style="color: #5a6c7d; font-size: 12px;">Updated: {pattern['last_updated']}</span>
                            </div>
                            <div style="display: flex; flex-wrap: wrap; gap: 5px;">
                """, unsafe_allow_html=True)
                
                for tech in pattern['technologies']:
                    st.markdown(f"""
                    <span style="background: #F44336; color: white; padding: 3px 8px; border-radius: 10px; font-size: 11px;">
                        {tech}
                    </span>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="text-align: right; margin-left: 20px;">
                    <div style="font-size: 24px; font-weight: bold; color: {compliance_color};">{pattern['compliance_score']}%</div>
                    <div style="font-size: 12px; color: #5a6c7d;">Compliance</div>
                </div>
                <div style="background: rgba(0, 0, 0, 0.2); border-radius: 10px; height: 6px; margin-top: 15px;">
                    <div style="background: {compliance_color}; height: 100%; width: {pattern['compliance_score']}%; border-radius: 10px; transition: width 0.3s ease;"></div>
                </div>
                </div>
                """, unsafe_allow_html=True)
        
        with tab3:
            st.markdown("### Data Patterns")
            
            data_patterns = [
                {
                    "name": "Data Lake Architecture",
                    "description": "Centralized data storage for customer transaction history and analytics",
                    "compliance_score": 90,
                    "usage_level": "High",
                    "category": "Data",
                    "technologies": ["Snowflake", "AWS S3", "Data Pipelines"],
                    "last_updated": "2024-01-11"
                },
                {
                    "name": "Real-time Data Processing",
                    "description": "Stream processing for immediate payment validation and anomaly detection",
                    "compliance_score": 85,
                    "usage_level": "High",
                    "category": "Data",
                    "technologies": ["Kafka", "Stream Processing", "Real-time Analytics"],
                    "last_updated": "2024-01-09"
                }
            ]
            
            for pattern in data_patterns:
                compliance_color = "#4CAF50" if pattern['compliance_score'] >= 90 else "#FF9800" if pattern['compliance_score'] >= 70 else "#F44336"
                usage_color = "#4CAF50" if pattern['usage_level'] == "High" else "#FF9800" if pattern['usage_level'] == "Medium" else "#F44336"
                
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.8); border-radius: 15px; padding: 20px; margin: 10px 0; border-left: 4px solid {compliance_color}; border: 1px solid rgba(0, 0, 0, 0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div style="flex: 1;">
                            <h4 style="margin: 0 0 10px 0; color: #2c3e50;">{pattern['name']}</h4>
                            <p style="margin: 0 0 10px 0; color: #5a6c7d;">{pattern['description']}</p>
                            <div style="display: flex; gap: 15px; align-items: center; margin: 10px 0;">
                                <span style="background: {compliance_color}; color: white; padding: 4px 8px; border-radius: 10px; font-size: 12px;">{pattern['category']}</span>
                                <span style="background: {usage_color}; color: white; padding: 4px 8px; border-radius: 10px; font-size: 12px;">{pattern['usage_level']} Usage</span>
                                <span style="color: #5a6c7d; font-size: 12px;">Updated: {pattern['last_updated']}</span>
                            </div>
                            <div style="display: flex; flex-wrap: wrap; gap: 5px;">
                """, unsafe_allow_html=True)
                
                for tech in pattern['technologies']:
                    st.markdown(f"""
                    <span style="background: #9C27B0; color: white; padding: 3px 8px; border-radius: 10px; font-size: 11px;">
                        {tech}
                    </span>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="text-align: right; margin-left: 20px;">
                    <div style="font-size: 24px; font-weight: bold; color: {compliance_color};">{pattern['compliance_score']}%</div>
                    <div style="font-size: 12px; color: #5a6c7d;">Compliance</div>
                </div>
                <div style="background: rgba(0, 0, 0, 0.2); border-radius: 10px; height: 6px; margin-top: 15px;">
                    <div style="background: {compliance_color}; height: 100%; width: {pattern['compliance_score']}%; border-radius: 10px; transition: width 0.3s ease;"></div>
                </div>
                </div>
                """, unsafe_allow_html=True)
        
        with tab4:
            st.markdown("### AI/ML Patterns")
            
            ai_patterns = [
                {
                    "name": "AI Agent Architecture",
                    "description": "Distributed AI agents for payment processing and decision making",
                    "compliance_score": 88,
                    "usage_level": "High",
                    "category": "AI/ML",
                    "technologies": ["MCP Protocol", "Intent Agent", "Retriever Agent"],
                    "last_updated": "2024-01-13"
                },
                {
                    "name": "ML Model Serving",
                    "description": "Production ML model deployment for real-time anomaly detection",
                    "compliance_score": 92,
                    "usage_level": "High",
                    "category": "AI/ML",
                    "technologies": ["SageMaker", "Model Endpoints", "A/B Testing"],
                    "last_updated": "2024-01-07"
                }
            ]
            
            for pattern in ai_patterns:
                compliance_color = "#4CAF50" if pattern['compliance_score'] >= 90 else "#FF9800" if pattern['compliance_score'] >= 70 else "#F44336"
                usage_color = "#4CAF50" if pattern['usage_level'] == "High" else "#FF9800" if pattern['usage_level'] == "Medium" else "#F44336"
                
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.8); border-radius: 15px; padding: 20px; margin: 10px 0; border-left: 4px solid {compliance_color}; border: 1px solid rgba(0, 0, 0, 0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div style="flex: 1;">
                            <h4 style="margin: 0 0 10px 0; color: #2c3e50;">{pattern['name']}</h4>
                            <p style="margin: 0 0 10px 0; color: #5a6c7d;">{pattern['description']}</p>
                            <div style="display: flex; gap: 15px; align-items: center; margin: 10px 0;">
                                <span style="background: {compliance_color}; color: white; padding: 4px 8px; border-radius: 10px; font-size: 12px;">{pattern['category']}</span>
                                <span style="background: {usage_color}; color: white; padding: 4px 8px; border-radius: 10px; font-size: 12px;">{pattern['usage_level']} Usage</span>
                                <span style="color: #5a6c7d; font-size: 12px;">Updated: {pattern['last_updated']}</span>
                            </div>
                            <div style="display: flex; flex-wrap: wrap; gap: 5px;">
                """, unsafe_allow_html=True)
                
                for tech in pattern['technologies']:
                    st.markdown(f"""
                    <span style="background: #FF9800; color: white; padding: 3px 8px; border-radius: 10px; font-size: 11px;">
                        {tech}
                    </span>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="text-align: right; margin-left: 20px;">
                    <div style="font-size: 24px; font-weight: bold; color: {compliance_color};">{pattern['compliance_score']}%</div>
                    <div style="font-size: 12px; color: #5a6c7d;">Compliance</div>
                </div>
                <div style="background: rgba(0, 0, 0, 0.2); border-radius: 10px; height: 6px; margin-top: 15px;">
                    <div style="background: {compliance_color}; height: 100%; width: {pattern['compliance_score']}%; border-radius: 10px; transition: width 0.3s ease;"></div>
                </div>
                </div>
                """, unsafe_allow_html=True)
        
        with tab5:
            st.markdown("### Integration Patterns")
            
            integration_patterns = [
                {
                    "name": "API-First Integration",
                    "description": "RESTful APIs for all external system integrations and data exchange",
                    "compliance_score": 95,
                    "usage_level": "High",
                    "category": "Integration",
                    "technologies": ["Apigee", "REST APIs", "Google APIs"],
                    "last_updated": "2024-01-16"
                },
                {
                    "name": "Private Network Integration",
                    "description": "Secure private connectivity for sensitive data exchange",
                    "compliance_score": 90,
                    "usage_level": "High",
                    "category": "Integration",
                    "technologies": ["AWS PrivateLink", "VPN", "Private Networks"],
                    "last_updated": "2024-01-06"
                }
            ]
            
            for pattern in integration_patterns:
                compliance_color = "#4CAF50" if pattern['compliance_score'] >= 90 else "#FF9800" if pattern['compliance_score'] >= 70 else "#F44336"
                usage_color = "#4CAF50" if pattern['usage_level'] == "High" else "#FF9800" if pattern['usage_level'] == "Medium" else "#F44336"
                
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.8); border-radius: 15px; padding: 20px; margin: 10px 0; border-left: 4px solid {compliance_color}; border: 1px solid rgba(0, 0, 0, 0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div style="flex: 1;">
                            <h4 style="margin: 0 0 10px 0; color: #2c3e50;">{pattern['name']}</h4>
                            <p style="margin: 0 0 10px 0; color: #5a6c7d;">{pattern['description']}</p>
                            <div style="display: flex; gap: 15px; align-items: center; margin: 10px 0;">
                                <span style="background: {compliance_color}; color: white; padding: 4px 8px; border-radius: 10px; font-size: 12px;">{pattern['category']}</span>
                                <span style="background: {usage_color}; color: white; padding: 4px 8px; border-radius: 10px; font-size: 12px;">{pattern['usage_level']} Usage</span>
                                <span style="color: #5a6c7d; font-size: 12px;">Updated: {pattern['last_updated']}</span>
                            </div>
                            <div style="display: flex; flex-wrap: wrap; gap: 5px;">
                """, unsafe_allow_html=True)
                
                for tech in pattern['technologies']:
                    st.markdown(f"""
                    <span style="background: #607D8B; color: white; padding: 3px 8px; border-radius: 10px; font-size: 11px;">
                        {tech}
                    </span>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="text-align: right; margin-left: 20px;">
                    <div style="font-size: 24px; font-weight: bold; color: {compliance_color};">{pattern['compliance_score']}%</div>
                    <div style="font-size: 12px; color: #5a6c7d;">Compliance</div>
                </div>
                <div style="background: rgba(0, 0, 0, 0.2); border-radius: 10px; height: 6px; margin-top: 15px;">
                    <div style="background: {compliance_color}; height: 100%; width: {pattern['compliance_score']}%; border-radius: 10px; transition: width 0.3s ease;"></div>
                </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Pattern compliance summary
        st.markdown("""
        <div class="glass-card">
            <h3>Pattern Compliance Summary</h3>
            <p style="color: #5a6c7d;">High-Value Payments System demonstrates strong compliance with enterprise architecture patterns across all categories.</p>
        </div>
        """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Error loading blueprint data: {str(e)}")
        st.info("Please ensure the high_value_payments_blueprint.json file exists in the project directory.")

def show_settings():
    st.markdown("""
    <div class="fade-in-up">
        <h1>Settings & Configuration</h1>
        <p style="color: #5a6c7d;">Configure your Architecture Intelligence preferences</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Settings sections
    with st.expander("General Settings", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Organization Name", value="Your Organization")
            st.selectbox("Default Architecture Type", ["Microservices", "Monolithic", "Serverless", "Hybrid"])
            st.number_input("Auto-scan Interval (minutes)", min_value=5, max_value=60, value=15)
        
        with col2:
            st.selectbox("Theme", ["iOS Dark", "Material Dark", "Custom"])
            st.checkbox("Enable Notifications", value=True)
            st.checkbox("Auto-save Changes", value=True)
    
    with st.expander("Technology Detection Settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.slider("Confidence Threshold", 0, 100, 70)
            st.checkbox("Enable Version Detection", value=True)
            st.checkbox("Auto-update Dependencies", value=False)
        
        with col2:
            st.multiselect("Excluded Technologies", ["jQuery", "Bootstrap", "Lodash"])
            st.text_input("Custom Detection Rules", placeholder="Enter custom rules...")
    
    with st.expander("Security Settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.selectbox("Security Level", ["High", "Medium", "Low"])
            st.checkbox("Enable Threat Detection", value=True)
            st.checkbox("Require Authentication", value=True)
        
        with col2:
            st.number_input("Scan Frequency (hours)", min_value=1, max_value=24, value=6)
            st.text_input("Security API Key", type="password")
    
    # Save settings button
    if st.button("Save Settings", width='stretch'):
        st.success("Settings saved successfully!")

if __name__ == "__main__":
    main()
