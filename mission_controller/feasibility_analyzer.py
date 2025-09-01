#!/usr/bin/env python3
"""
Mission Controller Feasibility Analyzer
Analyzes mission feasibility and performance requirements
"""

from typing import Dict, Any, List

class FeasibilityAnalyzer:
    """Analyzes mission feasibility"""
    
    def __init__(self, flight_analyzer, engine):
        self.flight_analyzer = flight_analyzer
        self.engine = engine
    
    def analyze_mission_feasibility(self, mission_config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze if a mission is feasible"""
        segments = mission_config.get("segments", [])
        
        analysis = {
            "feasible": True,
            "issues": [],
            "warnings": [],
            "performance": {}
        }
        
        # Analyze each segment
        for i, segment in enumerate(segments):
            seg_type = segment["type"]
            
            if seg_type in ["hover", "cruise", "loiter"]:
                alt = segment.get("altitude_m", 0)
                vel = segment.get("V_forward_mps", segment.get("V_loiter_mps", 0))
                
                # Get performance at this condition
                perf = self.flight_analyzer.get_flight_parameters(alt, vel)
                
                if perf:
                    analysis["performance"][f"segment_{i}"] = {
                        "thrust_N": perf.thrust_N,
                        "power_kW": perf.power_kW,
                        "efficiency_N_per_kW": perf.efficiency,
                        "tip_mach": perf.tip_mach,
                        "disk_loading_N_per_m2": perf.disk_loading,
                        "rpm": perf.rpm
                    }
                    
                    # Check for issues
                    if perf.tip_mach > 0.85:
                        analysis["warnings"].append(f"Segment {i}: High tip Mach ({perf.tip_mach:.3f})")
                    
                    if perf.power_kW > self.engine.P_sl_kW * 0.9:
                        analysis["issues"].append(f"Segment {i}: Power requirement too high ({perf.power_kW:.1f} kW)")
                        analysis["feasible"] = False
        
        # Overall assessment
        if analysis["issues"]:
            analysis["feasible"] = False
        
        return analysis
    
    def generate_mission_summary(self, mission_config: Dict[str, Any], mission_id: str, status: Dict[str, Any]) -> str:
        """Generate a mission summary"""
        summary = f"""
MISSION SUMMARY
==============
Mission: {mission_config['name']}
ID: {mission_id}
Description: {mission_config['description']}
Status: {status.get('status', 'Unknown')}

SEGMENTS ({len(mission_config['segments'])}):
"""
        
        for i, segment in enumerate(mission_config["segments"]):
            seg_type = segment["type"]
            duration = segment.get("duration_s", 0)
            
            summary += f"  {i+1}. {seg_type.upper()}"
            
            if seg_type == "hover":
                summary += f" at {segment['altitude_m']}m for {duration}s"
            elif seg_type == "cruise":
                summary += f" at {segment['altitude_m']}m, {segment['V_forward_mps']} m/s for {duration}s"
            elif seg_type == "vclimb":
                summary += f" from {segment['start_alt_m']}m at {segment['climb_rate_mps']} m/s for {duration}s"
            elif seg_type == "loiter":
                summary += f" at {segment['altitude_m']}m, {segment['V_loiter_mps']} m/s for {duration}s"
            elif seg_type == "payload":
                summary += f" {segment['kind']} {segment['delta_mass_kg']}kg"
            
            summary += "\n"
        
        # Add feasibility analysis
        feasibility = self.analyze_mission_feasibility(mission_config)
        summary += f"\nFEASIBILITY: {'✓ FEASIBLE' if feasibility['feasible'] else '✗ NOT FEASIBLE'}\n"
        
        if feasibility["issues"]:
            summary += "ISSUES:\n"
            for issue in feasibility["issues"]:
                summary += f"  • {issue}\n"
        
        if feasibility["warnings"]:
            summary += "WARNINGS:\n"
            for warning in feasibility["warnings"]:
                summary += f"  • {warning}\n"
        
        return summary