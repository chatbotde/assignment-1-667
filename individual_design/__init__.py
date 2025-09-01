#!/usr/bin/env python3
"""
Individual Design Package
Modular helicopter design system
"""

from .helicopter_designer import CompoundHelicopterDesigner
from .design_requirements import DesignRequirements
from .rotor_designer import RotorDesigner
from .aircraft_sizer import AircraftSizer
from .performance_analyzer import PerformanceAnalyzer
from .plot_generator import PlotGenerator
from .report_generator import ReportGenerator

__all__ = [
    'CompoundHelicopterDesigner',
    'DesignRequirements',
    'RotorDesigner', 
    'AircraftSizer',
    'PerformanceAnalyzer',
    'PlotGenerator',
    'ReportGenerator'
]