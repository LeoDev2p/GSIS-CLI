from utils.view_utils import lengthText
from math import ceil

class Views:
    def __init__(self):
        pass
    
    @staticmethod
    def Banner ():
        print (r"""
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
        """)
    
    @staticmethod
    def Menu ():
        print ("""
        [1] Create data base
        [2] Add categories
        [3] Add data
        [4] Filter data
        [5] Update data
        [6] Delete data
        [7] Exit
        """)

    @staticmethod
    def inputCredentials ():
        user = input ("[User]: ")
        password = input ("[Password]: ")
        return (user, password)

    @staticmethod
    def inputOption ():
        try:
            option = int (input ("[Option]: "))
        except ValueError as v:
            return f"Error tipo de dato:  {v}"

        else: return option

    @staticmethod
    def formcategoryInsert ():
        category = input ("[:] Category: ").capitalize ()
        return category

    @staticmethod
    def formInsert ():
        try:
            site_name = input ("[:] Site name: ").upper ()
            category = input ("[:] Category: ").capitalize ()
            url = input ("[:] Url: ")
            username = input ("[:] Username: ")
            email = input ("[:] Email: ").lower ()
            password = input ("[:] Password: ")
            expiry_days = int (input ("[:] Expiry days: "))
            security_level = int (input ("[:] Security Level: "))
        except ValueError as v:
            print (f"Error: {v}")
        
        return (site_name, category, url, username, email, password, expiry_days, security_level)

    @staticmethod
    def formUpdate ():
        try:
            site_name = input ("[:] Site name: ").upper ()
            password = input ("[:] Password: ")
            expiry_days = int (input ("[:] Expiry days: "))
            security_level = int (input ("[:] Security Level: "))
        except ValueError as v:
            print (f"Error: {v}")
        except UnboundLocalError as ul:
            print (f"Error: {v}")

        return (site_name, password, expiry_days, security_level)

    @staticmethod
    def formID ():
        try:
            id = int (input ("[:] id: "))
        except ValueError as ve:
            print (f"Error: {ve}")
        
        return id
    
    @staticmethod
    def formSitename ():
        category = input ("[:] Site name: ").upper ()
        return category

    @staticmethod
    def ask ():
        value = input ("\nDo you want to continue [S/N]: ").upper ()
        return value

    @staticmethod
    def show_message (message):
        print (message, end='\n')
    
    @staticmethod
    def show_error (message):
        if message.code:
            print (f"Error {message.code}: {str(message)}\n")
        else:
            print (f"Error: {message}\n")
    
    @staticmethod
    def show_data (row_data, title = "RESULTADOS"):
        len_category, len_siteweb, len_email = lengthText (row_data, 1), lengthText (row_data, 2), lengthText (row_data, 3)
        total = 19 + len_category + len_siteweb + len_email

        print (" " + "-"*(total-1))
        print ("|" + f"{title.center (total-1, " ")}" + "|")
        print (" " + "-"*(total-1))
        print (f"| Id | {'Category':^{len_category}} | {'Site Web':^{len_siteweb}} | {'Email':^{len_email}} |")

        len_category = len_category if len_category >= len ('category') else len ('category')
        for row in range (len (row_data)):
            print (f"| {row_data[row][0]:02d} | {row_data[row][1]:^{len_category}} | {row_data[row][2]:^{len_siteweb}} | {row_data[row][3]:^{len_email}} |")
            # for item in row_data[row]:
            #     print (f"| {item} ")
        
        print (" " + "-"*(total-1))

class Filters:
    @staticmethod
    def Menu_filter ():
        print ("""
        [1] Traer todo
        [2] Filtrar por nombre de sitio
        [3] Filtrar por categoria
        [4] Filtrar por año y mes
        [5] Filtrar por rango de fecha de modificacion
        [6] Exit
        """)
    
    @staticmethod
    def show_dataFilter (row_data, title = "RESULTADOS"):
        # print (f"[DEBUG]: {row_data}")
        len_category, len_siteweb, len_email = lengthText (row_data, 1), lengthText (row_data, 2), lengthText (row_data, 3)
        len_expiry = len ('Expiry days')

        total = 21 + len_category + len_siteweb + len_email + len_expiry

        print (" " + "-"*(total-1))
        print ("|" + f"{title.center (total-1, " ")}" + "|")
        print (" " + "-"*(total-1))
        print (f"| Id | {'Category':^{len_category}} | {'Site Web':^{len_siteweb}} | {'Email':^{len_email}} | {'Expiry days':^{len_expiry}} |")

        len_category = len_category if len_category >= len ('category') else len ('category')
    
        for row in range (len (row_data)):
            """
            :< Alinea a la izquierda.
            :^ Centra el texto.
            :> Alinea a la derecha.
            """
            # row[0]:02d -> Número con 2 dígitos
            # row[1]:^{len_category} -> Centra el texto en un bloque de tamaño len_category
            print(f"| {row_data[row][0]:02d} | {row_data[row][1]:^{len_category}} | {row_data[row][2]:^{len_siteweb}} | {row_data[row][3]:^{len_email}} | {row_data[row][4]:^{len_expiry}} |")
                
        print (" " + "-"*(total-1))
    
    @staticmethod
    def form_yearmonth ():
        try:
            year = int (input ("[:] Year: "))
            month = int (input ("[:] Month (1-12): "))
        except ValueError as ve:
            print (f"Error: {ve}")
        
        return (year, month)

    @staticmethod
    def form_yearyear ():
        try:
            year1 = (input ("[:] Year [Y-m-d]: "))
            year2 = (input ("[:] year [Y-m-d]: "))
        except ValueError as ve:
            print (f"Error: {ve}")
        
        return (year1, year2)
    
    
    

