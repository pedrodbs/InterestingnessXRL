__author__ = 'Pedro Sequeira'
__email__ = 'pedrodbs@gmail.com'

from abc import abstractmethod, ABC
from os import makedirs
from os.path import exists
from shutil import rmtree
from interestingness_xrl.learning.agents import QValueBasedAgent
import jsonpickle


class AnalysisBase(ABC):
    """
    Represents the base class for analysis objects. Analyses extract useful information from the agent's relationship
    with its environment as dictated by the statistical information collected by the agent.
    """

    def __init__(self, helper, agent):
        """
        Creates a new analysis.
        :param ScenarioHelper helper: the environment helper containing all necessary config and methods.
        :param QValueBasedAgent agent: the agent to be analyzed.
        """
        self.helper = helper
        self.config = helper.config
        self.agent = agent

    @abstractmethod
    def analyze(self):
        """
        Analyzes the agent's history of interaction with its environment according to some criteria and collects
        interesting aspects of that interaction.
        :return:
        """
        pass

    @abstractmethod
    def difference_to(self, other):
        """
        Gets the difference between this analysis and another given analysis, i.e., the elements that are new and
        therefore missing in the other analysis. This can be used to highlight what is new in this analysis compared to
        one that was performed at a prior stage of the agent's behavior / learning.
        :param AnalysisBase other: the other analysis to get the difference to.
        :return AnalysisBase: an analysis resulting from the difference between this and the given analysis.
        """
        pass

    def save_report(self, file_path, write_console=True):
        """
        Saves this analysis's report to a text file and optionally to the console.
        :param str file_path: the path to the file in which to save the report.
        :param bool write_console: whether to write the report to the console.
        :return:
        """
        with open(file_path, 'w') as file:
            self._save_report(file, write_console)

    @abstractmethod
    def _save_report(self, file, write_console):
        """
        Saves this analysis's report to a text file and optionally to the console.
        :param IO file: the file in which to save the report.
        :param bool write_console: whether to write the report to the console.
        :return:
        """
        pass

    def save_visual_report(self, path, clean=True):
        """
        Saves this analysis's visual report, saving relevant images where applicable.
        :param str path: the directory in which to save the images.
        :param bool clean: whether to clear the output directory.
        :return:
        """
        if not exists(path):
            makedirs(path)
        elif clean:
            rmtree(path)
            makedirs(path)

        self._save_visual_report(path)

    @abstractmethod
    def _save_visual_report(self, path):
        """
        Saves this analysis's visual report, saving relevant images where applicable.
        :param str path: the path to the directory in which to save the images.
        :return:
        """
        pass

    @abstractmethod
    def get_sample_interesting_aspects(self, s, a, r, ns):
        """
        Gets the names of the interesting elements generated by this analysis in which the given sample is present, if any.
        :param int s: the initial state.
        :param int a: the action.
        :param float r: the reward received.
        :param int ns: the next state.
        :rtype: list
        :return: a list containing the names of the interesting elements generated by this analysis in which the given
        sample is present. If it's not present in any element, an empty list is returned.
        """
        pass

    @abstractmethod
    def get_interestingness_names(self):
        """
        Gets the names of the possible interesting elements generated by this analysis.
        :rtype: list
        :return: a list containing the names of the possible interesting elements generated by this analysis.
        """
        pass

    @abstractmethod
    def get_stats(self):
        """
        Gets a dictionary containing statistics summarizing this analysis.
        :rtype: dict
        :return: a dictionary containing statistics summarizing this analysis.
        """
        pass

    def save_json(self, json_file_path):
        """
        Saves a text file representing this analysis in a JSON format.
        :param str json_file_path: the path to the JSON file in which to save this analysis.
        :return:
        """
        # ignores agent and env_config when saving to json
        agent = self.agent
        helper = self.helper
        self.agent = self.helper = self.config = None

        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
        with open(json_file_path, 'w') as json_file:
            json_str = jsonpickle.encode(self)
            json_file.write(json_str)

        self.agent = agent
        self.helper = helper
        self.config = helper.config

    @staticmethod
    def load_json(json_file_path):
        """
        Loads an analysis object from the given JSON formatted file.
        :param str json_file_path: the path to the JSON file from which to load an analysis.
        :return AnalysisBase: the analysis object stored in the given JSON file.
        """
        with open(json_file_path) as json_file:
            analysis = jsonpickle.decode(json_file.read())
            analysis._after_loaded_json()
            return analysis

    @abstractmethod
    def _after_loaded_json(self):
        """
        This function is called after the object has been loaded through json. Allows corrections to field objects.
        :return:
        """
        pass
