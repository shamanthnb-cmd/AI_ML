"""Environment Sanity & Diagnostic Script.

Author: Shamanth (DevOps)
Project: Team 1 AI/ML Subsystem
"""

import sys


def check_environment() -> bool:
    print("=" * 60)
    print(" Team 1 - AI/ML Subsystem Environment Verification ")
    print("=" * 60)

    # 1. Check Python version (Target: Python 3.12)
    py_ver = sys.version.split()[0]
    print(f"[✓] Python Version: {py_ver}")
    if sys.version_info < (3, 12) or sys.version_info >= (3, 13):
        print("    [WARNING] Expected Python 3.12.x for standard environment.")
    else:
        print("    [SUCCESS] Standard Python 3.12 runtime verified.")

    # 2. Check NumPy
    try:
        import numpy as np

        print(f"[✓] NumPy Version: {np.__version__}")
        if int(np.__version__.split(".")[0]) >= 2:
            print(
                "    [WARNING] NumPy >= 2.0 detected. "
                "May cause issues with older ONNX builds."
            )
    except ImportError as e:
        print(f"[FAILED] NumPy not installed: {e}")
        return False

    # 3. Check OpenCV
    try:
        import cv2

        print(f"[✓] OpenCV Version: {cv2.__version__}")
    except ImportError as e:
        print(
            "[FAILED] OpenCV not installed or missing system "
            f"libraries (libGL/libglib): {e}"
        )
        return False

    # 4. Check ONNX & ONNX Runtime
    try:
        import onnx
        import onnxruntime as ort

        print(f"[✓] ONNX Version: {onnx.__version__}")
        print(f"[✓] ONNX Runtime Version: {ort.__version__}")

        providers = ort.get_available_providers()
        print(f"[✓] Available Providers: {providers}")

        if "CPUExecutionProvider" in providers:
            print(
                "[SUCCESS] CPUExecutionProvider is active and ready for inference!"
            )
        else:
            print("[FAILED] CPUExecutionProvider not found.")
            return False

    except ImportError as e:
        print(f"[FAILED] ONNX Runtime not installed: {e}")
        return False

    print("=" * 60)
    print(" 🎉 ALL ENVIRONMENT CHECKS PASSED SUCCESSFULLY! ")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = check_environment()
    sys.exit(0 if success else 1)