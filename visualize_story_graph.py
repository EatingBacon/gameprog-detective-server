"""Utility to render story"""

import json
from graphviz import Digraph

from config import Config

OUTPUT_FILE = "graphviz_story"


def main():
    """Load story file and render it to pdf with graphviz"""
    with open(Config.STORY_FILE, "r") as story_file:
        story = json.loads(story_file.read())

    story_graph = Digraph("Story")
    story_graph.attr('graph', forcelabels='True')

    # Add start Node
    story_graph.attr('node', shape='doublecircle')
    story_graph.node(story["start_point"], margin="0.4")
    # Add Nodes
    story_graph.attr('node', shape='circle')
    for story_point, values in story["story_points"].items():
        story_graph.node(story_point, margin="0.4")

        for task in values.get("tasks", []):
            story_graph.node(task, shape='box', margin="0.4")
            story_graph.edge(task, story_point, style="dotted")

    # Add edges
    for story_point in story["story_points"].keys():
        for reply, next_point in story["story_points"][story_point]["paths"].items():
            story_graph.edge(story_point, next_point, xlabel=reply)

    try:
        story_graph.render(OUTPUT_FILE, format="pdf", view=True)
    except FileNotFoundError as e:
        # xdg-open is used as default to open output file
        # xdg-open might not be installed which will lead to system interpreting xdg-open as filename
        if (str(e) == "[Errno 2] No such file or directory: 'xdg-open'"):
            story_graph.render(OUTPUT_FILE, format="pdf", view=False)
            print(f"Could not open the output file. Saving it to {OUTPUT_FILE}.pdf")
        else:
            raise e

if __name__ == "__main__":
    main()
