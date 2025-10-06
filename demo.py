#!/usr/bin/env python3
"""
Architecture Intelligence Demo Script
Demonstrates key features and capabilities
"""

import streamlit as st
import pandas as pd
import numpy as np
from utils import TechnologyDetector, DataFlowAnalyzer, ArchitectureGenerator, PatternManager

def demo_technology_detection():
    """Demo technology detection capabilities"""
    print("🔍 Technology Detection Demo")
    print("=" * 50)
    
    try:
        detector = TechnologyDetector()
        
        # Sample package.json content
        sample_content = """
        {
            "name": "my-app",
            "version": "1.0.0",
            "dependencies": {
                "react": "^18.2.0",
                "node": "^18.17.0",
                "express": "^4.18.0",
                "postgresql": "^15.3.0"
            }
        }
        """
        
        print("Analyzing sample package.json...")
        technologies = detector.detect_technologies(sample_content, "json")
        
        for tech in technologies:
            print(f"✅ {tech['name']} v{tech['version']} - {tech['confidence']}% confidence")
            print(f"   Category: {tech['category']}")
            print(f"   Description: {tech['description']}")
            print()
        
        return technologies
    except Exception as e:
        print(f"❌ Technology detection demo failed: {e}")
        return []

def demo_data_flow_analysis():
    """Demo data flow analysis capabilities"""
    print("🔄 Data Flow Analysis Demo")
    print("=" * 50)
    
    try:
        analyzer = DataFlowAnalyzer()
        
        flow_analysis = analyzer.analyze_flow("API Calls", "Last Day")
        
        print(f"Flow Type: {flow_analysis['flow_type']}")
        print(f"Time Range: {flow_analysis['time_range']}")
        print(f"Total Flows: {flow_analysis['total_flows']}")
        print(f"Security Issues: {flow_analysis['security_issues']}")
        print(f"Performance Score: {flow_analysis['performance_score']}")
        print()
        
        print("Detected Patterns:")
        for pattern in flow_analysis['patterns']:
            print(f"  • {pattern['pattern']} - {pattern['security_level']} security")
            print(f"    {pattern['description']}")
        print()
        
        return flow_analysis
    except Exception as e:
        print(f"❌ Data flow analysis demo failed: {e}")
        return {}

def demo_architecture_generation():
    """Demo architecture generation capabilities"""
    print("🏛️ Architecture Generation Demo")
    print("=" * 50)
    
    generator = ArchitectureGenerator()
    
    # Generate microservices architecture
    architecture = generator.generate_architecture("microservices", "Layers")
    
    print(f"Architecture Type: {architecture['type']}")
    print(f"View Mode: {architecture['view_mode']}")
    print()
    
    print("Architecture Layers:")
    for layer in architecture['layers']:
        print(f"  📋 {layer['name']}")
        for component in layer['components']:
            print(f"    • {component}")
    print()
    
    print("Applied Patterns:")
    for pattern in architecture['patterns']:
        print(f"  • {pattern}")
    print()
    
    print("Component Dependencies:")
    for dep in architecture['dependencies'][:5]:  # Show first 5
        print(f"  • {dep['source']} → {dep['target']} ({dep['type']})")
    print()
    
    return architecture

def demo_pattern_management():
    """Demo pattern management capabilities"""
    print("📋 Pattern Management Demo")
    print("=" * 50)
    
    manager = PatternManager()
    
    # Get all patterns
    patterns = manager.get_patterns()
    
    print(f"Total Patterns: {len(patterns)}")
    print()
    
    print("Pattern Categories:")
    categories = {}
    for pattern in patterns:
        cat = pattern['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    for cat, count in categories.items():
        print(f"  • {cat}: {count} patterns")
    print()
    
    print("High Compliance Patterns (≥90%):")
    high_compliance = [p for p in patterns if p['compliance_score'] >= 90]
    for pattern in high_compliance:
        print(f"  • {pattern['name']} - {pattern['compliance_score']}%")
    print()
    
    # Demo filtering
    print("Filtered Patterns (Architecture category, High usage):")
    filtered = manager.get_patterns(category="Architecture", usage="High")
    for pattern in filtered:
        print(f"  • {pattern['name']} - {pattern['usage_level']} usage")
    print()
    
    return patterns

def demo_compliance_scoring():
    """Demo compliance scoring capabilities"""
    print("📊 Compliance Scoring Demo")
    print("=" * 50)
    
    manager = PatternManager()
    generator = ArchitectureGenerator()
    
    # Generate sample architecture
    architecture = generator.generate_architecture("microservices", "Layers")
    
    # Calculate compliance score
    compliance_score = manager.calculate_compliance_score(architecture)
    
    print(f"Architecture Type: {architecture['type']}")
    print(f"Applied Patterns: {len(architecture['patterns'])}")
    print(f"Compliance Score: {compliance_score}%")
    print()
    
    if compliance_score >= 90:
        print("✅ Excellent compliance - Ready for production")
    elif compliance_score >= 70:
        print("⚠️  Good compliance - Minor improvements needed")
    else:
        print("❌ Low compliance - Significant improvements required")
    print()
    
    return compliance_score

def main():
    """Run all demos"""
    print("🏗️ Architecture Intelligence - Feature Demo")
    print("=" * 60)
    print()
    
    try:
        # Run all demos
        technologies = demo_technology_detection()
        flow_analysis = demo_data_flow_analysis()
        architecture = demo_architecture_generation()
        patterns = demo_pattern_management()
        compliance_score = demo_compliance_scoring()
        
        print("🎉 Demo completed successfully!")
        print("=" * 60)
        print()
        print("Summary:")
        print(f"  • Technologies detected: {len(technologies)}")
        print(f"  • Data flows analyzed: {flow_analysis['total_flows']}")
        print(f"  • Architecture components: {len(architecture['components'])}")
        print(f"  • Available patterns: {len(patterns)}")
        print(f"  • Overall compliance: {compliance_score}%")
        print()
        print("To run the full application:")
        print("  streamlit run app.py")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
