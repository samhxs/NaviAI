"""Memory Management for VM"""

from typing import Any, Dict


class Memory:
    """Simple memory manager for the VM"""

    def __init__(self, size: int = 1024):
        """
        Initialize memory

        Args:
            size: Memory size in bytes
        """
        self.size = size
        self.data: Dict[int, Any] = {}
        self.stack: list = []
        self.registers: Dict[str, Any] = {
            'pc': 0,  # Program counter
            'sp': 0,  # Stack pointer
        }

    def read(self, address: int) -> Any:
        """Read value from memory address"""
        return self.data.get(address, 0)

    def write(self, address: int, value: Any) -> None:
        """Write value to memory address"""
        if address >= self.size:
            raise MemoryError(f"Address {address} out of bounds (max: {self.size})")
        self.data[address] = value

    def push(self, value: Any) -> None:
        """Push value onto stack"""
        self.stack.append(value)
        self.registers['sp'] += 1

    def pop(self) -> Any:
        """Pop value from stack"""
        if not self.stack:
            raise RuntimeError("Stack underflow")
        self.registers['sp'] -= 1
        return self.stack.pop()

    def peek(self) -> Any:
        """Peek at top of stack without popping"""
        if not self.stack:
            raise RuntimeError("Stack is empty")
        return self.stack[-1]

    def get_register(self, name: str) -> Any:
        """Get register value"""
        return self.registers.get(name, 0)

    def set_register(self, name: str, value: Any) -> None:
        """Set register value"""
        self.registers[name] = value

    def reset(self) -> None:
        """Reset memory state"""
        self.data.clear()
        self.stack.clear()
        self.registers = {'pc': 0, 'sp': 0}
