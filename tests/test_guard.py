"""Unit tests for agent-side-channel-leak-guard."""
import time
import unittest
from agent_side_channel_leak_guard.guard import SideChannelLeakGuard

class TestSideChannelLeakGuard(unittest.TestCase):
    def setUp(self):
        self.guard = SideChannelLeakGuard(bucket_granularity_ms=10.0, size_bucket_bytes=32)

    def test_size_padding(self):
        raw = b"12345"  # 5 bytes
        padded, pad_len = self.guard.pad_payload(raw)
        self.assertEqual(len(padded), 32)
        self.assertEqual(pad_len, 27)

    def test_quantized_time_delay(self):
        t0 = time.time()
        time.sleep(0.002)
        res = self.guard.guard_execution(t0, b"data")
        self.assertGreaterEqual(res.total_elapsed_ms, 9.5)
        self.assertEqual(len(res.padded_payload) % 32, 0)
