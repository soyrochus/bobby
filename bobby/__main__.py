# part of Bobby, a GTK4 application for practicing English pronunciation with advanced phrases. | Copyright (c) 2025 | License: MIT

"""Bobby pronunciation practice application."""

__all__ = ["BobbyApp"]

from .app import BobbyApp

def main():
    app = BobbyApp()
    app.run()


if __name__ == "__main__":
    main()