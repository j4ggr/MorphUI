"""
MorphUI Visualization Example

Demonstrates how to use MorphPlotWidget and MorphChartCard for data visualization.

Installation:
    pip install morphui[visualization]

Usage:
    python visualization_example.py
"""

import numpy as np
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

# Import MorphUI components
from morphui.uix.label import MorphLabel
from morphui.uix.button import MorphButton
from morphui.theme.manager import theme_manager

# Import visualization components
try:
    from morphui.uix.visualization import MorphPlotWidget, MorphChartCard, VISUALIZATION_AVAILABLE  # noqa: F401
except ImportError:
    print("Visualization components not available. Install with: pip install morphui[visualization]")
    exit(1)

if not VISUALIZATION_AVAILABLE:
    print("Visualization dependencies not installed. Install with: pip install morphui[visualization]")
    exit(1)


class VisualizationExampleApp(App):
    """Example app showcasing MorphUI visualization components"""
    
    def build(self):
        # Create main scroll view
        scroll = ScrollView()
        
        # Main container
        main_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=[dp(20), dp(40)],
            size_hint_y=None
        )
        main_layout.bind(minimum_height=main_layout.setter('height'))
        
        # Title
        title = MorphLabel(
            text="MorphUI Visualization Demo",
            text_style="display",
            size_hint_y=None,
            height=dp(50)
        )
        main_layout.add_widget(title)
        
        # Subtitle
        subtitle = MorphLabel(
            text="Interactive charts and plots with matplotlib integration",
            text_style="headline", 
            size_hint_y=None,
            height=dp(30)
        )
        main_layout.add_widget(subtitle)
        
        # Line chart example
        line_chart = MorphChartCard(
            title="Stock Price Simulation",
            description="Random walk simulation showing price movements over time",
            size_hint_y=None,
            height=dp(400)
        )
        
        # Generate sample data
        days = np.arange(100)
        price_changes = np.random.normal(0, 1, 100)
        prices = 100 + np.cumsum(price_changes)
        
        line_chart.plot_widget.plot(
            days, prices, 
            kind='line',
            xlabel='Days',
            ylabel='Price ($)',
            color='#2196F3',
            linewidth=2
        )
        main_layout.add_widget(line_chart)
        
        # Bar chart example
        bar_chart = MorphChartCard(
            title="Monthly Sales Data",
            description="Revenue breakdown by month for current year",
            size_hint_y=None,
            height=dp(400)
        )
        
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        sales = np.random.randint(50000, 150000, 12)
        
        bar_chart.plot_widget.plot(
            months, sales,
            kind='bar',
            xlabel='Month',
            ylabel='Revenue ($)',
            color='#4CAF50',
            alpha=0.8
        )
        main_layout.add_widget(bar_chart)
        
        # Scatter plot example
        scatter_chart = MorphChartCard(
            title="Performance vs Experience",
            description="Employee performance ratings correlated with years of experience",
            size_hint_y=None,
            height=dp(400)
        )
        
        experience = np.random.uniform(0, 20, 50)
        performance = 60 + experience * 2 + np.random.normal(0, 10, 50)
        performance = np.clip(performance, 0, 100)
        
        scatter_chart.plot_widget.plot(
            experience, performance,
            kind='scatter',
            xlabel='Years of Experience',
            ylabel='Performance Score',
            alpha=0.7,
            s=50,
            color='#FF9800'
        )
        main_layout.add_widget(scatter_chart)
        
        # Histogram example
        hist_chart = MorphChartCard(
            title="Test Score Distribution",
            description="Distribution of test scores across all students",
            size_hint_y=None,
            height=dp(400)
        )
        
        scores = np.random.normal(75, 15, 1000)
        hist_chart.plot_widget.plot(
            30, scores,  # 30 bins
            kind='hist',
            xlabel='Score',
            ylabel='Frequency',
            alpha=0.7,
            color='#9C27B0',
            edgecolor='black'
        )
        main_layout.add_widget(hist_chart)
        
        # Theme toggle button
        theme_btn = MorphButton(
            text="Switch to Dark Theme",
            size_hint_y=None,
            height=dp(48)
        )
        theme_btn.bind(on_press=self.toggle_theme)
        main_layout.add_widget(theme_btn)
        
        scroll.add_widget(main_layout)
        return scroll
    
    def toggle_theme(self, instance):
        """Toggle between light and dark themes"""
        if theme_manager.current_theme == "light":
            theme_manager.current_theme = "dark"
            instance.text = "Switch to Light Theme"
        else:
            theme_manager.current_theme = "light"
            instance.text = "Switch to Dark Theme"


if __name__ == "__main__":
    VisualizationExampleApp().run()