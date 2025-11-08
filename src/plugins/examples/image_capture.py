"""Image Capture Plugin"""

from ..base import Plugin
from datetime import datetime


class ImageCapturePlugin(Plugin):
    """
    Plugin that captures images displayed in VM apps
    """

    def __init__(self):
        super().__init__("ImageCapture")
        self.image_count = 0

    def on_load(self, vm) -> None:
        """Register event handler for image display"""
        vm.register_event_handler('image_show', self._handle_image_show)
        print(f"[{self.name}] Monitoring image display events")

    def on_unload(self, vm) -> None:
        """Cleanup when unloaded"""
        print(f"[{self.name}] Unloaded")

    def on_execution_start(self, vm) -> None:
        """Reset counters at start"""
        self.image_count = 0

    def on_execution_end(self, vm) -> None:
        """Report summary at end"""
        print(f"\n[{self.name}] Summary: Captured {self.image_count} image(s)")

    def _handle_image_show(self, image_data):
        """
        Handle image display event

        Args:
            image_data: Image data (could be path, URL, or binary data)
        """
        self.image_count += 1
        data = {
            'type': 'image',
            'source': str(image_data),
            'timestamp': datetime.now().isoformat(),
            'index': self.image_count
        }
        self.collect_data(data)
        print(f"[{self.name}] Captured image #{self.image_count}: {image_data}")

    def get_all_images(self) -> list:
        """
        Get all captured image sources

        Returns:
            List of image sources
        """
        return [item['source'] for item in self.data_collected]

    def export_metadata(self) -> dict:
        """
        Export image metadata

        Returns:
            Dictionary with image metadata
        """
        return {
            'total_images': self.image_count,
            'images': self.data_collected.copy()
        }
