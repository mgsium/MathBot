import csv
import os

class ParodyLoader:
    """A class to handle parody links."""

    __slots__ = ("_links")

    def __init__(self):
        super()
        self.links = []
        self.load_parody_links()

    def load_parody_links(self):
        path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(path, "../../assets/parody_links.csv")
        with open(file_path, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            self.links = [[line[0], line[1]] for line in reader]

    @property
    def links(self):
        return self._links

    @links.setter
    def links(self, links):
        self._links = {}
        for l in links:
            self._links[l[0]] = l[1]

    def get_parody_selection_pattern(self):
        parody_selection_pattern = f"show me parody ([1-{len(self.links.keys())}])"
        return parody_selection_pattern

    def get_link(self, identifier: str) -> str:
        return self._links[identifier]