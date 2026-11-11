"""CLI for agent-side-channel-leak-guard."""
import sys
import argparse
import time
from .guard import SideChannelLeakGuard

def main():
    parser = argparse.ArgumentParser(description="Agent Side-Channel Leak Guard CLI")
    parser.add_argument("--demo", action="store_true", help="Demonstrate constant-time and padding guard")
    args = parser.parse_args()

    if args.demo:
        guard = SideChannelLeakGuard(bucket_granularity_ms=20.0, size_bucket_bytes=64)
        t0 = time.time()
        time.sleep(0.005)  # 5ms internal task
        res = guard.guard_execution(t0, b"Secret user token 12345")
        print(f"Protected Response: Padded Length={len(res.padded_payload)}B (+{res.padding_bytes_added}B pad)")
        print(f"Elapsed: {res.total_elapsed_ms}ms (Target Bucket: {res.bucket_ms}ms)")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
