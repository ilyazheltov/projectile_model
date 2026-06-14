import tkinter as tk
import threading
import time
from functions import *

class BallisticSimulatorApp(tk.Tk):

    def __init__(self):
        super().__init__()
        
        self.title("Моделирование снаряда")
        self.geometry("1280x720+0+0")        
        self.configure(bg="#020202")
        self.resizable(False, False)
        
        self.label_opts = {"bg": "#151414", "fg": "white", "font": ("Arial", 12)}
        self.entry_opts = {"bg": "#151414", "fg": "white", "font": ("Arial", 12), "relief": "flat", "width": 20, "justify":"center"}
        
        # Единое хранилище для всех полей ввода
        self.inputs = {}
        
        # Запуск сборки интерфейса
        self._build_ui()

    def _build_ui(self):
        """Главный метод сборки всех панелей"""

        self.left_area = tk.Frame(self, width=380, bg="#020202")
        self.left_area.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        self.left_area.pack_propagate(False)

        # отрисовка всех полей
        self._build_targeting_section()
        self._build_physics_section()
        self._build_controls_section()
        self._build_console_section()

    def _create_input_row(self, parent_frame, row_index, label_text, dictionary_key):
        """Фабрика: создает строчку с Label и Entry, и сохраняет Entry в словарь"""

        lbl = tk.Label(parent_frame, text=label_text, **self.label_opts)
        lbl.grid(row=row_index, column=0, padx=10, pady=5, sticky="w")
        
        ent = tk.Entry(parent_frame, **self.entry_opts)
        ent.grid(row=row_index, column=1, padx=10, pady=5, sticky="w")
        
        self.inputs[dictionary_key] = ent    # заносим все поля tk.Entry в словарь inputs

    def _build_targeting_section(self):
        """Сборка секции координат"""

        frame = tk.Frame(self.left_area, bg="#020202", pady=10)
        frame.pack(side=tk.TOP, fill=tk.X)
        
        title = tk.Label(frame, text="Координаты цели", font=("Arial", 14, "bold"), bg="#020202", fg="white")
        title.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        self._create_input_row(frame, 1, "Координата X (м):", "target_x")
        self._create_input_row(frame, 2, "Координата Y (м):", "target_y")
        self._create_input_row(frame, 3, "Координата Z (м):", "target_z")
        self.inputs["target_x"].insert(0, "15000")
        self.inputs["target_y"].insert(0, "3500")
        self.inputs["target_z"].insert(0, "300")

    def _build_physics_section(self):
        """Сборка секции физики"""

        frame = tk.Frame(self.left_area, bg="#020202", pady=10)
        frame.pack(side=tk.TOP, fill=tk.X)
        
        title = tk.Label(frame, text="Параметры среды", font=("Arial", 14, "bold"), bg="#020202", fg="white")
        title.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        self._create_input_row(frame, 1, "Масса снаряда (кг):", "mass")
        self._create_input_row(frame, 2, "Скорость вылета (м/с):", "v0")
        self._create_input_row(frame, 3, "Ветер X (м/с):", "wind_x")
        self._create_input_row(frame, 4, "Ветер Y (м/с):", "wind_y")
        self._create_input_row(frame, 5, "Ветер z (м/с):", "wind_z")
        self.inputs["mass"].insert(0, "45")
        self.inputs["v0"].insert(0, "800")
        self.inputs["wind_x"].insert(0, "5*log(10*x+1)")
        self.inputs["wind_y"].insert(0, "2")
        self.inputs["wind_z"].insert(0, "0")

    
    def _build_console_section(self):
        """Сборка секции консоли"""

        frame = tk.Frame(self.left_area, bg="#020202", pady=10)
        frame.pack(side=tk.TOP, fill=tk.X, pady=(5, 0))
        
        text_box = tk.Text(frame, width=40, height=30)
        text_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        text_box.config(state=tk.DISABLED, font=('Arial', 16))
        self.text_box = text_box

    def _build_controls_section(self):
        """Сборка секции вычислений"""
        frame = tk.Frame(self.left_area, bg="#020202", pady=10)
        frame.pack(side=tk.TOP, fill=tk.X)

        self.button_calc = tk.Button(
        frame, 
        text="РАССЧИТАТЬ ТРАЕКТОРИЮ",
        command = self.on_click,
        bg="lightblue",
        fg="black", 
        font=("Arial", 14)
        )

        self.button_calc.pack(pady=10)


    def on_click(self):
        """Эта функция срабатывает сразу при нажатии"""

        self.text_box.config(state=tk.NORMAL)
        self.text_box.insert(tk.END, "Запуск вычислений\n")
        self.text_box.config(state=tk.DISABLED)

        self.button_calc.config(state="disabled", bg="#555555", text="Вычисление...")
        
        thread = threading.Thread(target=self.solve_pde)
        thread.daemon = True
        thread.start()


    def solve_pde(self):     
        """Решение самого диу в потоке и вывод этого в console"""

        start_coordinates = [0, 0, 0]

        

        while True:
            try:
                target_coordinates = [
                    float(self.inputs["target_x"].get()), 
                    float(self.inputs["target_y"].get()), 
                    float(self.inputs["target_z"].get())
                    ]
                m = float(self.inputs["mass"].get())
                v0 = float(self.inputs["v0"].get())
                Wx = self.inputs["wind_x"].get()
                Wy = self.inputs["wind_y"].get()
                Wz = self.inputs["wind_z"].get()
                break
            
            except (ValueError, SyntaxError):
                self.text_box.insert(tk.END, f"Введите корректные значения/n")
        
        W = [Wx, Wy, Wz]

        params = [m, v0, W]

        t_flying, teta, phi = find_angles(start_coordinates, target_coordinates, params)

        self.text_box.config(state=tk.NORMAL)
        self.text_box.insert(tk.END, f"\nНайденные углы:\n \u03B8: {np.degrees(teta):.2f}°\n \u03C6: {np.degrees(phi):.2f}°\n")
        self.text_box.config(state=tk.DISABLED)

        self.button_calc.config(state="normal", bg="#007acc", text="РАССЧИТАТЬ ТРАЕКТОРИЮ")


if __name__ == "__main__":
    app = BallisticSimulatorApp()
    app.mainloop()