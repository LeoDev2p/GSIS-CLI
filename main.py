import time

from src.controllers.auth_controller import Authentication
from src.controllers.handler import Handler_Contorller
from src.controllers.safe_controllers import Safe
from src.models.safe_models import SafeSQL
from src.models.category_models import CategorySQL
from src.models.database import CreateTable
from src.views.app import App
from src.views.components import ShowConsole

safe = Safe(table=CreateTable(), safe=SafeSQL(), category=CategorySQL())
controller = Handler_Contorller(safe=safe, auth=Authentication())

if __name__ == "__main__":
    try:
        data = App(controller)
        if data.status:
            data.run()
    except KeyboardInterrupt:
        ShowConsole.show_message("\nleaving  .....")
        time.sleep(0.5)
