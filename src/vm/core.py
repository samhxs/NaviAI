"""Virtual Machine Core"""

from typing import List, Optional
from .memory import Memory
from .executor import Executor, OpCode


class VirtualMachine:
    """
    Simple stack-based virtual machine that can run apps
    and supports plugin hooks
    """

    def __init__(self, memory_size: int = 1024):
        """
        Initialize the virtual machine

        Args:
            memory_size: Size of VM memory in bytes
        """
        self.memory = Memory(memory_size)
        self.executor = Executor(self.memory)
        self.plugins = []

    def load_plugin(self, plugin) -> None:
        """
        Load a plugin into the VM

        Args:
            plugin: Plugin instance to load
        """
        self.plugins.append(plugin)
        plugin.on_load(self)
        print(f"[VM] Loaded plugin: {plugin.name}")

    def unload_plugin(self, plugin) -> None:
        """
        Unload a plugin from the VM

        Args:
            plugin: Plugin instance to unload
        """
        if plugin in self.plugins:
            plugin.on_unload(self)
            self.plugins.remove(plugin)
            print(f"[VM] Unloaded plugin: {plugin.name}")

    def register_event_handler(self, event: str, handler) -> None:
        """
        Register an event handler (typically called by plugins)

        Args:
            event: Event name
            handler: Handler function
        """
        self.executor.register_event_handler(event, handler)

    def run(self, program: List[tuple]) -> None:
        """
        Run a program (app) on the VM

        Args:
            program: List of (opcode, operand) instruction tuples
        """
        print(f"\n[VM] Starting program execution...")
        print(f"[VM] Loaded {len(self.plugins)} plugin(s)")

        # Notify plugins that execution is starting
        for plugin in self.plugins:
            plugin.on_execution_start(self)

        # Run the program
        try:
            self.executor.run_program(program)
            print(f"[VM] Program execution completed")
        except Exception as e:
            print(f"[VM] Error during execution: {e}")
            raise
        finally:
            # Notify plugins that execution is ending
            for plugin in self.plugins:
                plugin.on_execution_end(self)

    def get_state(self) -> dict:
        """
        Get current VM state

        Returns:
            Dictionary containing VM state information
        """
        return {
            'memory_size': self.memory.size,
            'stack': self.memory.stack.copy(),
            'registers': self.memory.registers.copy(),
            'plugins_loaded': len(self.plugins),
        }

    def reset(self) -> None:
        """Reset VM to initial state"""
        self.memory.reset()
        print("[VM] Reset complete")
