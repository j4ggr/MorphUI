"""
MorphUI Visualization Example

This example demonstrates how to use MorphChart for interactive data visualization
within a MorphUI application. It showcases various chart types and the automatic
setup of interactive features like zooming, panning, and saving.

Requirements:
    pip install morphui[visualization]
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[2].resolve()))

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen

from morphui.app import MorphApp
from morphui.uix.label import MorphLabel
from morphui.uix.button import MorphButton
from morphui.uix.boxlayout import MorphBoxLayout
from morphui.uix.visualization import MorphChart
from morphui.uix.visualization import VISUALIZATION_AVAILABLE


class VisualizationExample(MorphApp):
    """Example application demonstrating MorphUI visualization capabilities."""
    
    def build(self) -> MorphLabel | MorphBoxLayout:
        """Build the main application interface."""
        self.theme_manager.theme_mode = 'Dark'
        self.theme_manager.seed_color = 'Orange'
        if not VISUALIZATION_AVAILABLE:
            return MorphLabel(
                text="Visualization components not available.\nInstall with: pip install morphui[visualization]",
                halign='center',
                valign='center')
        
        # Create screen manager for different chart examples
        self.screen_manager = ScreenManager()
        
        # Add different chart examples
        self.screen_manager.add_widget(self.create_line_chart_screen())
        self.screen_manager.add_widget(self.create_scatter_plot_screen())
        self.screen_manager.add_widget(self.create_bar_chart_screen())
        self.screen_manager.add_widget(self.create_multiple_plots_screen())
        
        # Create main layout with navigation
        main_layout = MorphBoxLayout(
            MorphBoxLayout(
                MorphButton(
                    text="Line Chart",
                    on_release=lambda x: setattr(
                        self.screen_manager, 'current', 'line_chart')),
                MorphButton(
                    text="Scatter Plot", 
                    on_release=lambda x: setattr(
                        self.screen_manager, 'current', 'scatter_plot')),
                MorphButton(
                    text="Bar Chart",
                    on_release=lambda x: setattr(
                        self.screen_manager, 'current', 'bar_chart')),
                MorphButton(
                    text="Multiple Plots",
                    on_release=lambda x: setattr(
                        self.screen_manager, 'current', 'multiple_plots')),
                orientation='horizontal',
                spacing=dp(10),
                size_hint_y=None,
                height=dp(50)),
            self.screen_manager,
            orientation='vertical',
            spacing=dp(10),
            padding=dp(20))
        
        return main_layout
    
    def create_line_chart_screen(self):
        """Create a screen with a line chart example."""
        screen = Screen(name='line_chart')
        
        # Create the chart
        chart = MorphChart()
        
        # Generate sample data
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x)
        y2 = np.cos(x)
        y3 = np.sin(x) * np.cos(x)
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x, y1, label='sin(x)', linewidth=2)
        ax.plot(x, y2, label='cos(x)', linewidth=2)
        ax.plot(x, y3, label='sin(x)*cos(x)', linewidth=2)
        
        ax.set_xlabel('X values')
        ax.set_ylabel('Y values')
        ax.set_title('Interactive Line Chart Example')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Set the figure - this automatically sets up all interactive features!
        chart.figure = fig
        
        layout = MorphBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(30))
        layout.add_widget(MorphLabel(
            text="Line Chart with multiple series. Try the toolbar for zoom, pan, and save!",
            size_hint_y=None,
            height=dp(40),
            halign='center'
        ))
        layout.add_widget(chart)
        
        screen.add_widget(layout)
        return screen
    
    def create_scatter_plot_screen(self):
        """Create a screen with a scatter plot example."""
        screen = Screen(name='scatter_plot')
        
        # Create custom chart class to demonstrate save directory customization
        class CustomChart(MorphChart):
            def get_save_dir(self) -> Path:
                """Custom save directory - could open a dialog here."""
                custom_dir = Path.home() / 'Documents' / 'MorphUI_Charts'
                custom_dir.mkdir(exist_ok=True)
                return custom_dir
        
        chart = CustomChart()
        
        # Generate sample data
        np.random.seed(42)
        n = 200
        x = np.random.randn(n)
        y = np.random.randn(n)
        colors = np.random.rand(n)
        sizes = 1000 * np.random.rand(n)
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = ax.scatter(x, y, c=colors, s=sizes, alpha=0.6, cmap='viridis')
        
        ax.set_xlabel('X values')
        ax.set_ylabel('Y values')
        ax.set_title('Interactive Scatter Plot with Custom Save Directory')
        plt.colorbar(scatter, ax=ax)
        
        # Set the figure
        chart.figure = fig
        
        layout = MorphBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        layout.add_widget(MorphLabel(
            text="Scatter plot with color mapping. This chart saves to Documents/MorphUI_Charts/",
            size_hint_y=None,
            height=dp(40),
            halign='center'
        ))
        layout.add_widget(chart)
        
        screen.add_widget(layout)
        return screen
    
    def create_bar_chart_screen(self):
        """Create a screen with a bar chart example."""
        screen = Screen(name='bar_chart')
        
        chart = MorphChart()
        
        # Sample data
        categories = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E']
        values1 = [23, 45, 56, 78, 32]
        values2 = [34, 25, 67, 45, 56]
        
        x = np.arange(len(categories))
        width = 0.35
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 6))
        bars1 = ax.bar(x - width/2, values1, width, label='Series 1', alpha=0.8)
        bars2 = ax.bar(x + width/2, values2, width, label='Series 2', alpha=0.8)
        
        ax.set_xlabel('Categories')
        ax.set_ylabel('Values')
        ax.set_title('Interactive Bar Chart Example')
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.legend()
        ax.grid(True, axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height}',
                           xy=(bar.get_x() + bar.get_width()/2, height),
                           xytext=(0, 3), textcoords="offset points",
                           ha='center', va='bottom', fontsize=9)
        
        # Set the figure
        chart.figure = fig
        
        layout = MorphBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        layout.add_widget(MorphLabel(
            text="Bar chart with multiple series and annotations. Fully interactive!",
            size_hint_y=None,
            height=dp(40),
            halign='center'
        ))
        layout.add_widget(chart)
        
        screen.add_widget(layout)
        return screen
    
    def create_multiple_plots_screen(self):
        """Create a screen with multiple subplots."""
        screen = Screen(name='multiple_plots')
        
        chart = MorphChart()
        
        # Create matplotlib figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        
        # Subplot 1: Line plot
        x = np.linspace(0, 10, 50)
        ax1.plot(x, np.exp(-x/3) * np.sin(2*x), 'b-', linewidth=2)
        ax1.set_title('Damped Oscillation')
        ax1.grid(True, alpha=0.3)
        
        # Subplot 2: Histogram
        data = np.random.normal(100, 15, 1000)
        ax2.hist(data, bins=30, alpha=0.7, color='green')
        ax2.set_title('Normal Distribution')
        ax2.set_xlabel('Values')
        ax2.set_ylabel('Frequency')
        
        # Subplot 3: Pie chart
        labels = ['A', 'B', 'C', 'D']
        sizes = [30, 25, 20, 25]
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
        ax3.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax3.set_title('Distribution')
        
        # Subplot 4: Heatmap
        data = np.random.rand(10, 10)
        im = ax4.imshow(data, cmap='coolwarm', aspect='auto')
        ax4.set_title('Heatmap')
        plt.colorbar(im, ax=ax4)
        
        plt.tight_layout()
        
        # Set the figure
        chart.figure = fig
        
        layout = MorphBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        layout.add_widget(MorphLabel(
            text="Multiple subplots in one chart. All toolbar features work on the entire figure!",
            size_hint_y=None,
            height=dp(40),
            halign='center'
        ))
        layout.add_widget(chart)
        
        screen.add_widget(layout)
        return screen


if __name__ == '__main__':
    """
    Run the visualization example.
    
    This demonstrates the key features of MorphChart:
    1. Simple usage: just set chart.figure = your_matplotlib_figure
    2. Automatic interactive features (zoom, pan, save, coordinate display)
    3. Custom save directory handling
    4. Works with any matplotlib figure (single plots, subplots, etc.)
    """
    VisualizationExample().run()
