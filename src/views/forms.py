from src.views.style import prompt


class Forms:
    @staticmethod
    def inputCredentials() -> tuple:
        """Credentials entry."""
        print()
        user = input(prompt("[Usuario] "))
        password = input(prompt("[Contraseña] "))
        return (user, password)

    @staticmethod
    def inputOption() -> int:
        """Options entry."""
        try:
            option = int(input(prompt("[Opción] ")))
        except ValueError:
            print("Data type error: el valor debe ser numérico")
            return -1
        return option

    @staticmethod
    def formcategoryInsert() -> str:
        """Input form for inserting a new category."""
        category = input(prompt("Categoría ")).strip().capitalize()
        return category
    
    @staticmethod
    def formInsert() -> tuple:
        """Input form for inserting new data into the safe."""
        try:
            site_name = input(prompt("Nombre del sitio")).strip().upper()
            category = input(prompt("Categoría ")).strip().capitalize()
            url = input(prompt("URL ")).strip()
            username = input(prompt("Usuario ")).strip()
            email = input(prompt("Email ")).strip().lower()
            password = input(prompt("Contraseña ")).strip()
            expiry_days = int(input(prompt("Días de expiración ")).strip())
            security_level = int(input(prompt("Nivel de seguridad ")).strip())
        except ValueError as v:
            print(f"Error: {v}")
    
        return (site_name, category, url, username, email, password,
            expiry_days, security_level)
    
    @staticmethod
    def formUpdate() -> tuple:
        "Form to update existing data in the safe."""
        try:
            site_name = input(prompt("Nombre del sitio ")).strip().upper()
            password = input(prompt("Nueva contraseña ")).strip()
            expiry_days = int(input(prompt("Días de expiración ")).strip())
            security_level = int(input(prompt("Nivel de seguridad ")).strip())
        except ValueError as v:
            print(f"Error: {v}")
        except UnboundLocalError as ul:
            print(f"Error: {ul}")
    
        return (site_name, password, expiry_days, security_level)
    
    @staticmethod
    def formID() -> int:
        """Input form for entering on iD."""
        try:
            id = int(input(prompt("ID del registro ")).strip())
        except (ValueError, SyntaxError) as ve:
            print(f"Error: {ve}")
    
        return id
    
    @staticmethod
    def formSitename() -> str:
        """Form for entering a site name."""
        category = input(prompt("Nombre del sitio ")).strip().upper()
        return category
    
    @staticmethod
    def ask(message="¿Desea continuar [S/N]?") -> str:
        """Asks the user if they want to continue with a specific action."""
        value = input(f"\n{message}: ").upper()
        return value

    @staticmethod
    def form_yearmonth() -> tuple:
        """Form for entering a year and month."""
        try:
            year = int(input(prompt("Año ")))
            month = int(input(prompt("Mes (1-12) ")))
        except (ValueError, SyntaxError) as ve:
            print(f"Error: {ve}")
    
        return (year, month)
    
    @staticmethod
    def form_yearyear() -> tuple:
        """Form for entering a data range of year and month."""
        try:
            year1 = input(prompt("Fecha inicial (YYYY-MM-DD) "))
            year2 = input(prompt("Fecha final (YYYY-MM-DD) "))
        except ValueError as ve:
            print(f"Error: {ve}")
    
        return (year1, year2)

    @staticmethod
    def form_login():
        email = input(prompt("[Email] "))
        password = input(prompt("[Contraseña] "))
        confirm_password = input(prompt("[Confirmar contraseña] "))

        return {"email": email, "password": password, "confirm_password": confirm_password}
