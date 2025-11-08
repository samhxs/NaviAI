"""Plugin Manager"""

from typing import List, Optional
from .base import Plugin


class PluginManager:
    """Manages plugins for the VM"""

    def __init__(self):
        """Initialize plugin manager"""
        self.plugins: List[Plugin] = []

    def register(self, plugin: Plugin) -> None:
        """
        Register a plugin

        Args:
            plugin: Plugin instance to register
        """
        if plugin not in self.plugins:
            self.plugins.append(plugin)
            print(f"[PluginManager] Registered plugin: {plugin.name}")

    def unregister(self, plugin: Plugin) -> None:
        """
        Unregister a plugin

        Args:
            plugin: Plugin instance to unregister
        """
        if plugin in self.plugins:
            self.plugins.remove(plugin)
            print(f"[PluginManager] Unregistered plugin: {plugin.name}")

    def get_plugin(self, name: str) -> Optional[Plugin]:
        """
        Get a plugin by name

        Args:
            name: Plugin name

        Returns:
            Plugin instance or None if not found
        """
        for plugin in self.plugins:
            if plugin.name == name:
                return plugin
        return None

    def list_plugins(self) -> List[str]:
        """
        List all registered plugin names

        Returns:
            List of plugin names
        """
        return [p.name for p in self.plugins]

    def get_all_reports(self) -> dict:
        """
        Get reports from all plugins

        Returns:
            Dictionary mapping plugin names to their reports
        """
        return {p.name: p.get_report() for p in self.plugins}

    def clear_all_data(self) -> None:
        """Clear collected data from all plugins"""
        for plugin in self.plugins:
            plugin.clear_data()
