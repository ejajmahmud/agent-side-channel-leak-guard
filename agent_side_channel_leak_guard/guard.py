"""Core Side-Channel Leak Guard implementation."""
import os
import random
import time
from dataclasses import dataclass
from typing import Tuple

@dataclass
class ProtectedResponse:
    padded_payload: bytes
    total_elapsed_ms: float
    bucket_ms: float
    padding_bytes_added: int

class SideChannelLeakGuard:
    """Masks execution timing differences and pads payloads to constant bucket sizes."""
    
    def __init__(self, bucket_granularity_ms: float = 50.0, size_bucket_bytes: int = 128):
        self.bucket_granularity_ms = bucket_granularity_ms
        self.size_bucket_bytes = size_bucket_bytes

    def pad_payload(self, raw_data: bytes) -> Tuple[bytes, int]:
        orig_len = len(raw_data)
        remainder = orig_len % self.size_bucket_bytes
        pad_len = self.size_bucket_bytes - remainder if remainder != 0 else 0
        # Add PKCS-style or random padding
        padded = raw_data + os.urandom(pad_len)
        return padded, pad_len

    def guard_execution(self, start_time: float, raw_data: bytes) -> ProtectedResponse:
        elapsed_ms = (time.time() - start_time) * 1000.0
        # Compute target quantized bucket time
        bucket_count = int(elapsed_ms // self.bucket_granularity_ms) + 1
        target_time_ms = bucket_count * self.bucket_granularity_ms
        sleep_ms = target_time_ms - elapsed_ms
        if sleep_ms > 0:
            time.sleep(sleep_ms / 1000.0)

        padded, pad_len = self.pad_payload(raw_data)
        final_elapsed = (time.time() - start_time) * 1000.0

        return ProtectedResponse(
            padded_payload=padded,
            total_elapsed_ms=round(final_elapsed, 2),
            bucket_ms=target_time_ms,
            padding_bytes_added=pad_len
        )
