"""Module responsible for managing the command-line user interface of the application."""

from utils.utils import lengthText


class Views:
    """Manages the command-line user interface.

    Provides static methods for displaying menus, banners, input forms, error messages, and data tables in the console.

    This class is stateless, and all its methods are static, acting as a collection of UI utilities.
    """

    @staticmethod
    def Banner():
        """Displays the application banner in the console."""
        print(
            r"""
          ______    ______   ______   ______            ______   __        ______ 
         /      \  /      \ /      | /      \           /      \ /  |      /      |
        /$$$$$$  |/$$$$$$  |$$$$$$/ /$$$$$$  |        /$$$$$$  |$$ |      $$$$$$/ 
        $$ | _$$/ $$ \__$$/   $$ |  $$ \__$$/  ______ $$ |  $$/ $$ |        $$ |  
        $$ |/    |$$      \   $$ |  $$      \ /      |$$ |      $$ |        $$ |  
        $$ |$$$$ | $$$$$$  |  $$ |   $$$$$$  |$$$$$$/ $$ |   __ $$ |        $$ |  
        $$ \__$$ |/  \__$$ | _$$ |_ /  \__$$ |        $$ \__/  |$$ |_____  _$$ |_ 
        $$    $$/ $$    $$/ / $$   |$$    $$/         $$    $$/ $$       |/ $$   |
         $$$$$$/   $$$$$$/  $$$$$$/  $$$$$$/           $$$$$$/  $$$$$$$$/ $$$$$$/ 
                                                                By LeoDev2p                        
        """
        )

    @staticmethod
    def Menu():
        """Displays the main menu options in the console."""
        print(
            """
        [1] Create data base
        [2] Add categories
        [3] Delete categories
        [4] Add data
        [5] Filter data
        [6] Update data
        [7] Delete data
        [8] Exit
        """
        )

    @staticmethod
    def inputCredentials() -> tuple:
        """Credentials entry."""
        user = input("[User]: ")
        password = input("[Password]: ")
        return (user, password)

    @staticmethod
    def inputOption() -> str:
        """Options entry."""
        try:
            option = int(input("[Option]: "))
        except ValueError as v:
            return f"Data type error:  {v}"

        else:
            return option

    @staticmethod
    def formcategoryInsert() -> str:
        """Input form for inserting a new category."""
        category = input("[:] Category: ").capitalize()
        return category

    @staticmethod
    def formInsert() -> tuple:
        """Input form for inserting new data into the safe."""
        try:
            site_name = input("[:] Site name: ").upper()
            category = input("[:] Category: ").capitalize()
            url = input("[:] Url: ")
            username = input("[:] Username: ")
            email = input("[:] Email: ").lower()
            password = input("[:] Password: ")
            expiry_days = int(input("[:] Expiry days: "))
            security_level = int(input("[:] Security Level: "))
        except ValueError as v:
            print(f"Error: {v}")

        return (
            site_name,
            category,
            url,
            username,
            email,
            password,
            expiry_days,
            security_level,
        )

    @staticmethod
    def formUpdate() -> tuple:
        """Form to update existing data in the safe."""
        try:
            site_name = input("[:] Site name: ").upper()
            password = input("[:] Password: ")
            expiry_days = int(input("[:] Expiry days: "))
            security_level = int(input("[:] Security Level: "))
        except ValueError as v:
            print(f"Error: {v}")
        except UnboundLocalError as ul:
            print(f"Error: {ul}")

        return (site_name, password, expiry_days, security_level)

    @staticmethod
    def formID() -> int:
        """Input form for entering on iD."""
        try:
            id = int(input("[:] id: "))
        except (ValueError, SyntaxError) as ve:
            print(f"Error: {ve}")

        return id

    @staticmethod
    def formSitename() -> str:
        """Form for entering a site name."""
        category = input("[:] Site name: ").upper()
        return category

    @staticmethod
    def ask(message="Do you want to continue [S/N]") -> str:
        """Asks the user if they want to continue with a specific actino."""
        value = input(f"\n{message}: ").upper()
        return value

    @staticmethod
    def show_message(message: str):
        """Print a message to the console."""
        print(message, end="\n")

    @staticmethod
    def show_error(message):
        """Print an error message to the console."""
        try:
            if message.code:
                print(f"Error {message.code}: {str(message)}\n")
            else:
                print(f"Error: {message}\n")
        except AttributeError as at:
            print(f"Error: {at}\n")

    @staticmethod
    def show_data(row_data: list[tuple], title="RESULTS"):
        """Display data in a formatted table in the console."""
        len_category, len_siteweb, len_email = (
            lengthText(row_data, 1),
            lengthText(row_data, 2),
            lengthText(row_data, 3),
        )
        total = 19 + len_category + len_siteweb + len_email

        len_category = (
            len_category if len_category >= len("category") else len("category")
        )

        print(" " + "-" * (total - 1))
        print("|" + f"{title.center (total-1, " ")}" + "|")
        print(" " + "-" * (total - 1))
        print(
            f"| Id | {'Category':^{len_category}} | {'Site Web':^{len_siteweb}} | {'Email':^{len_email}} |"
        )

        for row in range(len(row_data)):
            print(
                f"| {row_data[row][0]:02d} | {row_data[row][1]:^{len_category}} | {row_data[row][2]:^{len_siteweb}} | {row_data[row][3]:^{len_email}} |"
            )

        print(" " + "-" * (total - 1))


class Filters:
    """Filters class responsible for managing the user interface related to data filtering and display of filtered results in the console."""

    @staticmethod
    def Menu_filter():
        """Displays the filter menu options in the console."""
        print(
            """
        [1] View All
        [2] Filter by site name
        [3] Filter by category
        [4] Filter by year and month
        [5] Filter by date range of modification
        [6] Exit
        """
        )

    @staticmethod
    def show_dataFilter(row_data: list[tuple], title="RESULTS"):
        """Display filtered data in a formatted table in the console."""
        len_category, len_siteweb, len_email = (
            lengthText(row_data, 1),
            lengthText(row_data, 2),
            lengthText(row_data, 3),
        )
        len_expiry = len("Expiry days")

        total = 21 + len_category + len_siteweb + len_email + len_expiry

        print(" " + "-" * (total - 1))
        print("|" + f"{title.center (total-1, " ")}" + "|")
        print(" " + "-" * (total - 1))
        print(
            f"| Id | {'Category':^{len_category}} | {'Site Web':^{len_siteweb}} | {'Email':^{len_email}} | {'Expiry days':^{len_expiry}} |"
        )

        len_category = (
            len_category if len_category >= len("category") else len("category")
        )

        for row in range(len(row_data)):
            """
            :< Alinea a la izquierda.
            :^ Centra el texto.
            :> Alinea a la derecha.
            """
            # row[0]:02d -> Número con 2 dígitos
            # row[1]:^{len_category} -> Centra el texto en un bloque de tamaño len_category
            print(
                f"| {row_data[row][0]:02d} | {row_data[row][1]:^{len_category}} | {row_data[row][2]:^{len_siteweb}} | {row_data[row][3]:^{len_email}} | {row_data[row][4]:^{len_expiry}} |"
            )

        print(" " + "-" * (total - 1))

    @staticmethod
    def form_yearmonth() -> tuple:
        """Form for entering a year and month."""
        try:
            year = int(input("[:] Year: "))
            month = int(input("[:] Month (1-12): "))
        except (ValueError, SyntaxError) as ve:
            print(f"Error: {ve}")

        return (year, month)

    @staticmethod
    def form_yearyear() -> tuple:
        """Form for entering a data range of year and month."""
        try:
            year1 = input("[:] Year [Y-m-d]: ")
            year2 = input("[:] year [Y-m-d]: ")
        except ValueError as ve:
            print(f"Error: {ve}")

        return (year1, year2)
