"""Sound Recorder Plugin"""

from ..base import Plugin
from datetime import datetime


class SoundRecorderPlugin(Plugin):
    """
    Plugin that records sound played in VM apps
    """

    def __init__(self):
        super().__init__("SoundRecorder")
        self.sound_count = 0
        self.total_duration = 0

    def on_load(self, vm) -> None:
        """Register event handler for sound playback"""
        vm.register_event_handler('sound_play', self._handle_sound_play)
        print(f"[{self.name}] Monitoring sound playback events")

    def on_unload(self, vm) -> None:
        """Cleanup when unloaded"""
        print(f"[{self.name}] Unloaded")

    def on_execution_start(self, vm) -> None:
        """Reset counters at start"""
        self.sound_count = 0
        self.total_duration = 0

    def on_execution_end(self, vm) -> None:
        """Report summary at end"""
        print(f"\n[{self.name}] Summary: Recorded {self.sound_count} sound(s)")

    def _handle_sound_play(self, sound_data):
        """
        Handle sound playback event

        Args:
            sound_data: Sound data (could be path, URL, or audio info)
        """
        self.sound_count += 1

        # Parse duration if it's a dict with duration info
        duration = 0
        if isinstance(sound_data, dict):
            duration = sound_data.get('duration', 0)
            sound_source = sound_data.get('source', str(sound_data))
        else:
            sound_source = str(sound_data)

        self.total_duration += duration

        data = {
            'type': 'sound',
            'source': sound_source,
            'duration': duration,
            'timestamp': datetime.now().isoformat(),
            'index': self.sound_count
        }
        self.collect_data(data)
        print(f"[{self.name}] Recorded sound #{self.sound_count}: {sound_source}")

    def get_all_sounds(self) -> list:
        """
        Get all recorded sound sources

        Returns:
            List of sound sources
        """
        return [item['source'] for item in self.data_collected]

    def get_statistics(self) -> dict:
        """
        Get recording statistics

        Returns:
            Dictionary with statistics
        """
        return {
            'total_sounds': self.sound_count,
            'total_duration': self.total_duration,
            'sounds': self.data_collected.copy()
        }
