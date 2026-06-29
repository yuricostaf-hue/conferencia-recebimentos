#!/usr/bin/env python3
"""Main application entry point."""

import sys
from gui.main_window import MainWindow


def main() -> int:
    """Run the application.

    Returns:
        Exit code.
    """
    try:
        app = MainWindow()
        app.mainloop()
        return 0
    except Exception as e:
        print(f"Fatal error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
