from matplotlib import pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import LineString
from descartes import PolygonPatch

from code_pipeline.tests_generation import RoadTest

# https://stackoverflow.com/questions/34764535/why-cant-matplotlib-plot-in-a-different-thread
class RoadTestVisualizer:
    """
        Visualize and Plot RoadTests
    """


    def __init__(self, map_size):
        self.map_size = map_size
        self.last_submitted_test_figure = None

        # Make sure there's a windows and does not block anything when calling show
        plt.ion()
        plt.show()

    def _setup_figure(self):
        if self.last_submitted_test_figure is not None:
            # Make sure we operate on the right figure
            plt.figure(self.last_submitted_test_figure.number)
            plt.clf()
        else:
            self.last_submitted_test_figure = plt.figure()

        # plt.gcf().set_title("Last Generated Test")
        plt.gca().set_aspect('equal', 'box')
        plt.gca().set(xlim=(-30, self.map_size + 30), ylim=(-30, self.map_size + 30))

    def visualize_road_test(self, the_test: RoadTest):

        self._setup_figure()

        # Plot the map. Trying to re-use an artist in more than one Axes which is supported
        map_patch = patches.Rectangle((0, 0), self.map_size, self.map_size, linewidth=1, edgecolor='black', facecolor='none')
        plt.gca().add_patch(map_patch)
        plt.draw()
        plt.pause(0.001)

        # Road Geometry.
        road_poly = LineString([(t[0], t[1]) for t in the_test.interpolated_points]).buffer(8.0, cap_style=2, join_style=2)
        road_patch = PolygonPatch(road_poly, fc='gray', ec='dimgray')  # ec='#555555', alpha=0.5, zorder=4)
        plt.gca().add_patch(road_patch )
        plt.draw()
        plt.pause(0.001)

        # Interpolated Points
        sx = [t[0] for t in the_test.interpolated_points]
        sy = [t[1] for t in the_test.interpolated_points]
        plt.plot(sx, sy, 'yellow')
        plt.draw()
        plt.pause(0.001)

        # Road Points
        x = [t[0] for t in the_test.road_points]
        y = [t[1] for t in the_test.road_points]
        plt.plot(x, y, 'wo')
        plt.draw()
        plt.pause(0.001)

