"""Text Extractor Plugin"""

from ..base import Plugin
from datetime import datetime


class TextExtractorPlugin(Plugin):
    """
    Plugin that extracts and monitors text displayed in VM apps
    """

    def __init__(self):
        super().__init__("TextExtractor")
        self.text_count = 0

    def on_load(self, vm) -> None:
        """Register event handler for text display"""
        vm.register_event_handler('text_display', self._handle_text_display)
        print(f"[{self.name}] Monitoring text display events")

    def on_unload(self, vm) -> None:
        """Cleanup when unloaded"""
        print(f"[{self.name}] Unloaded")

    def on_execution_start(self, vm) -> None:
        """Reset counters at start"""
        self.text_count = 0

    def on_execution_end(self, vm) -> None:
        """Report summary at end"""
        print(f"\n[{self.name}] Summary: Captured {self.text_count} text item(s)")

    def _handle_text_display(self, text_data):
        """
        Handle text display event

        Args:
            text_data: Text content being displayed
        """
        self.text_count += 1
        data = {
            'type': 'text',
            'content': str(text_data),
            'timestamp': datetime.now().isoformat(),
            'length': len(str(text_data))
        }
        self.collect_data(data)
        print(f"[{self.name}] Captured text: '{text_data}' ({len(str(text_data))} chars)")

    def get_all_text(self) -> list:
        """
        Get all captured text content

        Returns:
            List of text strings
        """
        return [item['content'] for item in self.data_collected]

    def search_text(self, keyword: str) -> list:
        """
        Search for keyword in captured text

        Args:
            keyword: Keyword to search for

        Returns:
            List of matching text items
        """
        return [
            item for item in self.data_collected
            if keyword.lower() in item['content'].lower()
        ]
