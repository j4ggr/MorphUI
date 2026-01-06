from morphui.app import MorphApp
from morphui.uix.visualization import MorphChart
import matplotlib.pyplot as plt
import numpy as np

class ChartApp(MorphApp):
    def build(self):
        self.theme_manager.theme_mode = 'Dark'
        
        # Create chart widget
        chart = MorphChart()
        
        # Create matplotlib figure
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x, y, linewidth=2)
        ax.set_title('Sine Wave')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.grid(True, alpha=0.3)
        
        # Set the figure
        chart.figure = fig
        
        return chart

if __name__ == '__main__':
    ChartApp().run()