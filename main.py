"""
GTI Tracker - GET-THAT-INTERNSHIP Tracker
Main application entry point
"""
import sys
import logging
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt
from db.session import init_database
from ui.main_window import MainWindow


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_stylesheet(app: QApplication) -> None:
    """Load and apply the application stylesheet"""
    try:
        # Try dark professional theme first (new Bloomberg-inspired design)
        dark_theme_path = Path(__file__).parent / 'styles' / 'dark_professional.qss'

        if dark_theme_path.exists():
            with open(dark_theme_path, 'r', encoding='utf-8') as f:
                stylesheet = f.read()
                app.setStyleSheet(stylesheet)
                logger.info("Dark professional stylesheet loaded successfully")
                return

        # Fallback to main.qss if dark theme not found
        main_stylesheet_path = Path(__file__).parent / 'styles' / 'main.qss'
        if main_stylesheet_path.exists():
            with open(main_stylesheet_path, 'r', encoding='utf-8') as f:
                stylesheet = f.read()
                app.setStyleSheet(stylesheet)
                logger.info("Main stylesheet loaded successfully")
        else:
            logger.warning(f"No stylesheet found")

    except Exception as e:
        logger.error(f"Failed to load stylesheet: {e}")


def main():
    """Main application entry point"""
    try:
        # Enable high DPI scaling BEFORE creating QApplication
        # For Qt6, use the new method
        if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
            QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        # High DPI policy for Qt6
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )

        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("GTI Tracker")
        app.setOrganizationName("GTI_Tracker")

        logger.info("Starting GTI Tracker application")

        # Initialize database
        logger.info("Initializing database...")
        init_database()
        logger.info("Database initialized successfully")

        # Load stylesheet
        load_stylesheet(app)

        # Create and show main window
        window = MainWindow()
        window.show()

        logger.info("Application started successfully")

        # Run event loop
        sys.exit(app.exec())

    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)

        # Show error dialog if possible
        try:
            error_app = QApplication.instance()
            if error_app is None:
                error_app = QApplication(sys.argv)

            QMessageBox.critical(
                None,
                "Fatal Error",
                f"An error occurred while starting the application:\n\n{str(e)}\n\n"
                "Please check the logs for more details."
            )
        except:
            pass

        sys.exit(1)


if __name__ == "__main__":
    main()

