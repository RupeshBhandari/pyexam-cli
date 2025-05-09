from src.interface.navigation import Navigation
from src.utils.database_setup import setup_database


def main():
    # Set up the database if needed
    setup_database()

    # Initialize the Navigation class
    navigation = Navigation()
    navigation.start()


if __name__ == "__main__":
    main()
