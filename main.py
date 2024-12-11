import win32print
import time
import requests
import tkinter as tk
from tkinter import simpledialog, messagebox


class PasswordDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("А ты точно профсоюз?")
        self.geometry("300x100")
        self.resizable(False, False)

        self.label = tk.Label(self, text="Введите код для печати:")
        self.label.pack(pady=5)

        self.entry = tk.Entry(self)
        self.entry.pack(pady=5)
        self.entry.focus_set()

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=5)

        self.ok_button = tk.Button(self.button_frame, text="OK", command=self.on_ok)
        self.ok_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = tk.Button(self.button_frame, text="Отмена", command=self.on_cancel)
        self.cancel_button.pack(side=tk.LEFT, padx=5)

        self.result = None

        # Bind Ctrl+V for pasting
        self.bind_all("<Control-v>", self.paste_clipboard)

        # Center the window and make it topmost
        self.center_window()
        self.attributes('-topmost', True)

    def paste_clipboard(self, event):
        try:
            self.entry.insert(tk.END, self.clipboard_get())
        except tk.TclError:
            pass

    def center_window(self):
        self.update_idletasks()  # Update geometry information
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = screen_width // 2 - size[0] // 2
        y = screen_height // 2 - size[1] // 2
        self.geometry(f"{size[0]}x{size[1]}+{x}+{y}")

    def on_ok(self):
        self.result = self.entry.get()
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()


def get_daily_password_from_server():
    """Получает ежедневный пароль от бота через API."""
    try:
        response = requests.get('http://79.133.183.89:5000/daily-password', timeout=5)
        if response.status_code == 200:
            return response.json().get('password')
        else:
            print("Error fetching password from server.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to server: {e}")
        messagebox.showerror("Ошибка подключения", "Не удалось подключиться к серверу. Проверьте интернет-соединение.")
        return None


def prompt_for_password():
    """Графический интерфейс для ввода пароля."""
    root = tk.Tk()
    root.withdraw()  # Скрыть главное окно

    dialog = PasswordDialog(root)
    root.wait_window(dialog)

    if dialog.result is None:
        messagebox.showwarning("Отмена", "Вы отменили ввод кода.")
        return None

    return dialog.result


def show_result_message(success):
    """Показывает сообщение о результате проверки кода."""
    if success:
        messagebox.showinfo("Результат", "Пароль верный. Печать началась.")
    else:
        messagebox.showerror("Результат", "Пароль неверный. Печать отменена.")


def monitor_print_jobs():
    """Отслеживает печать и блокирует задания до проверки кода."""
    printer_name = win32print.GetDefaultPrinter()  # Получаем принтер по умолчанию
    print(f"Monitoring printer: {printer_name}")
    processed_jobs = {}  # Словарь для отслеживания обработанных заданий

    while True:
        # Получаем список заданий на печать
        printer_handle = win32print.OpenPrinter(printer_name)
        jobs = win32print.EnumJobs(printer_handle, 0, -1, 1)

        if jobs:
            for job in jobs:
                job_id = job['JobId']
                job_status = job.get('Status', 0)

                # Проверяем, обрабатывалось ли задание ранее
                if job_id in processed_jobs:
                    if processed_jobs[job_id] == "completed":
                        continue  # Пропускаем завершенные задания

                # Если задание не обработано или его статус изменился, работаем с ним
                print(f"Pausing job {job_id} for document: {job.get('pDocument', 'Unknown Document')}")
                win32print.SetJob(printer_handle, job_id, 0, None, win32print.JOB_CONTROL_PAUSE)

                # Выводим информацию о задании
                document_name = job.get('pDocument', 'Unknown Document')
                user_name = job.get('pUserName', 'Unknown User')
                print(f"Job detected: {document_name}")
                print(f"User: {user_name}, Status: {job_status}")

                # Запрашиваем код у пользователя
                code = get_daily_password_from_server()
                if code:
                    user_code = prompt_for_password()
                    if user_code == code:
                        print("Code accepted. Resuming the print job...")
                        win32print.SetJob(printer_handle, job_id, 0, None, win32print.JOB_CONTROL_RESUME)
                        processed_jobs[job_id] = "completed"
                        show_result_message(True)
                    else:
                        print("Invalid code. Canceling the print job...")
                        win32print.SetJob(printer_handle, job_id, 0, None, win32print.JOB_CONTROL_DELETE)
                        processed_jobs[job_id] = "completed"
                        show_result_message(False)

        win32print.ClosePrinter(printer_handle)


if __name__ == "__main__":
    try:
        monitor_print_jobs()
    except KeyboardInterrupt:
        print("Monitoring stopped.")
