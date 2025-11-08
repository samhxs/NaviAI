"""Instruction Executor for VM"""

from enum import IntEnum
from typing import Any, Dict, Callable, List, Optional


class OpCode(IntEnum):
    """Operation codes for the VM"""
    # Stack operations
    PUSH = 0x01      # Push value onto stack
    POP = 0x02       # Pop value from stack

    # Arithmetic operations
    ADD = 0x10       # Add top two stack values
    SUB = 0x11       # Subtract top two stack values
    MUL = 0x12       # Multiply top two stack values
    DIV = 0x13       # Divide top two stack values

    # Memory operations
    LOAD = 0x20      # Load from memory to stack
    STORE = 0x21     # Store from stack to memory

    # Display operations (for app functionality)
    PRINT_TEXT = 0x30    # Display text (triggers text extraction plugin)
    SHOW_IMAGE = 0x31    # Show image (triggers image capture plugin)
    PLAY_SOUND = 0x32    # Play sound (triggers sound recording plugin)

    # Control flow
    HALT = 0xFF      # Stop execution


class Executor:
    """Executes instructions on the VM"""

    def __init__(self, memory):
        """
        Initialize executor

        Args:
            memory: Memory instance to operate on
        """
        self.memory = memory
        self.running = False
        self.event_handlers: Dict[str, List[Callable]] = {}

    def register_event_handler(self, event: str, handler: Callable) -> None:
        """
        Register an event handler (for plugin hooks)

        Args:
            event: Event name (e.g., 'text_display', 'image_show')
            handler: Callback function
        """
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        self.event_handlers[event].append(handler)

    def trigger_event(self, event: str, data: Any) -> None:
        """
        Trigger an event (notifies all registered plugins)

        Args:
            event: Event name
            data: Event data to pass to handlers
        """
        if event in self.event_handlers:
            for handler in self.event_handlers[event]:
                handler(data)

    def execute_instruction(self, opcode: int, operand: Optional[Any] = None) -> bool:
        """
        Execute a single instruction

        Args:
            opcode: Operation code
            operand: Optional operand for the instruction

        Returns:
            True if execution should continue, False if halted
        """
        if opcode == OpCode.PUSH:
            self.memory.push(operand)

        elif opcode == OpCode.POP:
            self.memory.pop()

        elif opcode == OpCode.ADD:
            b = self.memory.pop()
            a = self.memory.pop()
            self.memory.push(a + b)

        elif opcode == OpCode.SUB:
            b = self.memory.pop()
            a = self.memory.pop()
            self.memory.push(a - b)

        elif opcode == OpCode.MUL:
            b = self.memory.pop()
            a = self.memory.pop()
            self.memory.push(a * b)

        elif opcode == OpCode.DIV:
            b = self.memory.pop()
            a = self.memory.pop()
            if b == 0:
                raise ZeroDivisionError("Division by zero")
            self.memory.push(a / b)

        elif opcode == OpCode.LOAD:
            address = operand
            value = self.memory.read(address)
            self.memory.push(value)

        elif opcode == OpCode.STORE:
            address = operand
            value = self.memory.pop()
            self.memory.write(address, value)

        elif opcode == OpCode.PRINT_TEXT:
            text = self.memory.pop() if operand is None else operand
            print(f"[VM Display] {text}")
            self.trigger_event('text_display', text)

        elif opcode == OpCode.SHOW_IMAGE:
            image_data = self.memory.pop() if operand is None else operand
            print(f"[VM Display] Showing image: {image_data}")
            self.trigger_event('image_show', image_data)

        elif opcode == OpCode.PLAY_SOUND:
            sound_data = self.memory.pop() if operand is None else operand
            print(f"[VM Audio] Playing sound: {sound_data}")
            self.trigger_event('sound_play', sound_data)

        elif opcode == OpCode.HALT:
            return False

        else:
            raise ValueError(f"Unknown opcode: {opcode}")

        return True

    def run_program(self, program: List[tuple]) -> None:
        """
        Run a complete program

        Args:
            program: List of (opcode, operand) tuples
        """
        self.running = True
        pc = 0

        while self.running and pc < len(program):
            instruction = program[pc]

            # Handle both tuple and direct OpCode formats
            if isinstance(instruction, tuple):
                opcode = instruction[0]
                operand = instruction[1] if len(instruction) > 1 else None
            else:
                # Single OpCode without operand
                opcode = instruction
                operand = None

            self.memory.set_register('pc', pc)

            if not self.execute_instruction(opcode, operand):
                self.running = False
                break

            pc += 1

        self.running = False
