from abc import ABC, abstractmethod

class ToolAdapter(ABC):
    @abstractmethod
    def run(self, **kwargs):
        """Execute the tool. Return dict with {returncode, stdout, stderr, artifacts}"""
        pass

    @abstractmethod
    def parse_output(self, path_or_raw):
        """Parse tool-specific output and return structured summary"""
        pass
