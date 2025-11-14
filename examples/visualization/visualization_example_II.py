import sys
import logging

import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from kivy.lang import Builder

logging.getLogger('matplotlib.font_manager').disabled = True
sys.path.append(str(Path(__file__).parents[1].resolve()))

from morphui.app import MorphApp
from morphui.uix.visualization import MorphChart


KV = """
BoxLayout:
    MorphChart:
        id: chart
"""

class TestPlotApp(MorphApp):
    title = "Test Matplotlib"

    def build(self):
        self.theme_manager.theme_mode = "Dark"
        self.theme_manager.seed_color = "Orange"
        fig, axs = plt.subplots(1, 2, sharey=True, sharex=True)
        t = np.arange(0.0, 1_000, 0.01)
        s1 = np.sin(8 * np.pi * t)
        s2 = np.sin(1 * np.pi * t)
        axs[0].scatter(t, s1)
        axs[0].plot(t, s2)
        axs[1].plot(t, s1)
        axs[1].scatter(t, s2)

        root = Builder.load_string(KV)
        chart = root.ids['chart']
        chart.figure = fig
        return root

if __name__ == '__main__':
    TestPlotApp().run()
