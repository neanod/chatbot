from google import genai
from google.genai.types import Tool, GoogleSearchRetrieval, ToolCodeExecution
from win10toast import ToastNotifier


# Disabling stderr because for some reason
# win10toast prints TypeError while working perfectly
# stderr_fileno = sys.stderr.fileno()
# save_stderr = os.dup(stderr_fileno)
# dev_null = os.open(os.devnull, os.O_WRONLY)
# os.dup2(dev_null, stderr_fileno)
# os.close(dev_null)

with open("key", "r") as f:
    KEY = f.read()

client = genai.Client(api_key=KEY)


search_tool = Tool(
    google_search = GoogleSearchRetrieval
)
code_tool = Tool(
    code_execution = ToolCodeExecution
)

def send_notification(title: str, message: str) -> str:
    """Sends a notification to user.

    Args:
        title (str): The title of the notification.
        message (str): The message body of the notification.
    Returns:
        success indicator
    """
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=0)
    return "successfully send"


tools_list: list
# tools_list = [search_tool]
helper_tool_list = [search_tool]
tools_list = [send_notification]
# tools_list = [set_light_values, send_notification, search_tool]
print("FUNCTIONS INITIALISED")