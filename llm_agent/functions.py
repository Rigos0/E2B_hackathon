from abc import ABC, abstractmethod


class BaseFunction(ABC):
    """
    Abstract class for defining a function with schema and execution logic.
    """

    @property
    @abstractmethod
    def function_schema(self):
        """Returns the function schema."""
        pass

    @abstractmethod
    def execute(self, **kwargs):
        """Executes the function logic."""
        pass