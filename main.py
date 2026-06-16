import customtkinter as ctk
import threading
from functions import *
import numpy as np

class BallisticSimulatorApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title("Моделирование снаряда")
        self.geometry("1280x720")        
        
        # Единое хранилище для всех полей ввода
        self.inputs = {}
        
        # Запуск сборки интерфейса
        self._build_ui()

    def _build_ui(self):
        """Главный метод сборки всех панелей"""

        self.left_area = ctk.CTkFrame(self, width=380)
        self.left_area.pack(side="left", fill="both", expand=False, padx=10, pady=10)

        # отрисовка всех полей
        self._build_targeting_section()
        self._build_physics_section()
        self._build_controls_section()
        self._build_console_section()

    def input_except(self):
            self.text_box.configure(state="disabled")
            self.button_calc.configure(state="normal", text="РАССЧИТАТЬ ТРАЕКТОРИЮ")
            

    def _create_input_row(self, parent_frame, row_index, label_text, dictionary_key):
        """Фабрика: создает строчку с Label и Entry, и сохраняет Entry в словарь"""

        lbl = ctk.CTkLabel(parent_frame, text=label_text)
        lbl.grid(row=row_index, column=0, padx=10, pady=5, sticky="w")
        
        ent = ctk.CTkEntry(parent_frame)
        ent.grid(row=row_index, column=1, padx=10, pady=5, sticky="w")
        
        self.inputs[dictionary_key] = ent    # заносим все поля ctk.CTkEntry в словарь inputs

    def _build_targeting_section(self):
        """Сборка секции координат"""

        frame = ctk.CTkFrame(self.left_area)
        frame.pack(side="top", fill="x", padx=15, pady=10)
        
        title = ctk.CTkLabel(frame, text="Координаты цели")
        title.grid(row=0, column=0, columnspan=2)

        self._create_input_row(frame, 1, "Координата X (м):", "target_x")
        self._create_input_row(frame, 2, "Координата Y (м):", "target_y")
        self._create_input_row(frame, 3, "Координата Z (м):", "target_z")
        self.inputs["target_x"].insert(0, "15000")
        self.inputs["target_y"].insert(0, "3500")
        self.inputs["target_z"].insert(0, "300")

    def _build_physics_section(self):
        """Сборка секции физики"""

        frame = ctk.CTkFrame(self.left_area)
        frame.pack(side="top", fill="x", padx=15, pady=10)
        
        title = ctk.CTkLabel(frame, text="Параметры среды")
        title.grid(row=0, column=0, columnspan=2)

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

        frame = ctk.CTkFrame(self.left_area)
        frame.pack(side="top", fill="x", padx=15, pady=10)
        
        text_box = ctk.CTkTextbox(frame, width=40, height=200)
        text_box.pack(side="top", fill="x", padx=15, pady=10)
        text_box.configure(state=ctk.DISABLED)
        self.text_box = text_box

    def _build_controls_section(self):
        """Сборка секции вычислений"""
        frame = ctk.CTkFrame(self.left_area)
        frame.pack(side="top", fill="x", padx=15, pady=10)

        self.button_calc = ctk.CTkButton(
        frame, 
        text="РАССЧИТАТЬ ТРАЕКТОРИЮ",
        command = self.on_click,
        )

        self.button_calc.pack(side="top", fill="x", padx=15, pady=10)


    def on_click(self):
        """Эта функция срабатывает сразу при нажатии"""

        self.text_box.configure(state=ctk.NORMAL)
        self.text_box.insert(ctk.END, "Запуск вычислений\n")
        self.text_box.configure(state=ctk.DISABLED)

        self.button_calc.configure(state="disabled", text="Вычисление...")
        
        thread = threading.Thread(target=self.solve_pde)
        thread.daemon = True
        thread.start()


    def solve_pde(self):     
        """Решение самого диу в потоке и вывод этого в console"""

        start_coordinates = [0, 0, 0]

        self.text_box.configure(state=ctk.NORMAL)

        try:
                
            target_x = float(self.inputs["target_x"].get())
            target_y = float(self.inputs["target_y"].get())
            target_z = float(self.inputs["target_z"].get())
            target_coordinates = [target_x, target_y, target_z]       
            m = float(self.inputs["mass"].get())                       
            v0 = float(self.inputs["v0"].get())
            Wx = self.inputs["wind_x"].get()
            Wy = self.inputs["wind_y"].get()
            Wz = self.inputs["wind_z"].get()
        
            if m <= 0:
                self.text_box.insert("end", f"Масса не может быть отрицательной или нулевой, введите корректное значение\n\n")
                self.input_except()
                return

            if v0 <= 0:
                self.text_box.insert("end", f"Скорость не может быть отрицательной или нулевой, введите корректное значение\n\n")
                self.input_except()
                return
                
            Wx = text_replace(Wx)
            Wy = text_replace(Wy)
            Wz = text_replace(Wz)
            
        except Exception:
            self.text_box.insert("end", f"Введены некорректные значения\n\n")
            self.input_except()
            return
            
        W = [Wx, Wy, Wz]
        params = [m, v0, W]

        try:
            t_flying, teta, phi = find_angles(start_coordinates, target_coordinates, params)

        except SyntaxError:
            print("Проверьте правильность ввода")
            self.input_except()   
            return

        except Exception:
            print("Не получилось найти значения углов")
            self.input_except()
            return

        self.text_box.configure(state=ctk.NORMAL)
        self.text_box.insert(
            ctk.END, 
            f"\nНайденные углы:\n"
            f"    \u03B8: {np.degrees(teta):.2f}°\n"
            f"    \u03C6: {np.degrees(phi):.2f}°\n\n"
        )
        self.text_box.configure(state=ctk.DISABLED)
        self.button_calc.configure(state="normal", text="РАССЧИТАТЬ ТРАЕКТОРИЮ")

if __name__ == "__main__":
    app = BallisticSimulatorApp()
    app.mainloop()