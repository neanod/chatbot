# chatbot

Simple cli-based chatbot using google.genai sdk and fasterwhisper.

#### How to use

* hold f13 to speak
* press ctrl+f13 to write message directly

from win10toast import ToastNotifier
import os
import sys

stderr_fileno = sys.stderr.fileno()
save_stderr = os.dup(stderr_fileno)
dev_null = os.open(os.devnull, os.O_WRONLY)
os.dup2(dev_null, stderr_fileno)
os.close(dev_null)
toaster = ToastNotifier()
toaster.show_toast("Test Title", "Test Message", duration=0)
print("Toast sent")
