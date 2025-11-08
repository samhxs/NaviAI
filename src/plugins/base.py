"""Base Plugin Class"""

from abc import ABC, abstractmethod
from typing import Any


class Plugin(ABC):
    """
    Base class for all VM plugins

    Plugins can hook into VM execution and extract/monitor data
    """

    def __init__(self, name: str):
        """
        Initialize plugin

        Args:
            name: Plugin name
        """
        self.name = name
        self.enabled = True
        self.data_collected = []

    @abstractmethod
    def on_load(self, vm) -> None:
        """
        Called when plugin is loaded into VM

        Args:
            vm: VirtualMachine instance
        """
        pass

    @abstractmethod
    def on_unload(self, vm) -> None:
        """
        Called when plugin is unloaded from VM

        Args:
            vm: VirtualMachine instance
        """
        pass

    def on_execution_start(self, vm) -> None:
        """
        Called when VM starts executing a program

        Args:
            vm: VirtualMachine instance
        """
        pass

    def on_execution_end(self, vm) -> None:
        """
        Called when VM finishes executing a program

        Args:
            vm: VirtualMachine instance
        """
        pass

    def collect_data(self, data: Any) -> None:
        """
        Collect data during VM execution

        Args:
            data: Data to collect
        """
        if self.enabled:
            self.data_collected.append(data)

    def get_collected_data(self) -> list:
        """
        Get all collected data

        Returns:
            List of collected data items
        """
        return self.data_collected.copy()

    def clear_data(self) -> None:
        """Clear all collected data"""
        self.data_collected.clear()

    def enable(self) -> None:
        """Enable the plugin"""
        self.enabled = True

    def disable(self) -> None:
        """Disable the plugin"""
        self.enabled = False

    def get_report(self) -> dict:
        """
        Get a report of plugin activity

        Returns:
            Dictionary containing plugin report
        """
        return {
            'name': self.name,
            'enabled': self.enabled,
            'data_count': len(self.data_collected),
            'data': self.data_collected.copy()
        }
