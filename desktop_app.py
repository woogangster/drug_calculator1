# -*- coding: utf-8 -*-
"""
약물 용량 계산기 - 데스크탑 GUI (CustomTkinter)
실행: python desktop_app.py
필요 패키지: customtkinter  (pip install customtkinter)
"""
import customtkinter as ctk
from drug_data import get_drug_names, calculate, DISCLAIMER

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

NAVY = "#1F4E78"
BLUE = "#2E75B6"
BLUE_DARK = "#163A5C"
BG_SOFT = "#F5F9FC"
TEXT_MUTE = "#5B7A9C"
TEXT_FAINT = "#9AA7B2"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("약물 용량 계산기 (교육용)")
        self.geometry("580x760")
        self.configure(fg_color="#FFFFFF")

        ctk.CTkLabel(self, text="💊 약물 용량 계산기", font=ctk.CTkFont(size=22, weight="bold"),
                     text_color=NAVY).pack(pady=(20, 4))
        ctk.CTkLabel(self, text="소아·노인 맞춤 용량 참고 프로그램 (교육용)", font=ctk.CTkFont(size=13),
                     text_color=TEXT_MUTE).pack(pady=(0, 16))

        form = ctk.CTkFrame(self, fg_color=BG_SOFT, corner_radius=14)
        form.pack(padx=24, pady=8, fill="x")

        ctk.CTkLabel(form, text="약물 선택", text_color=NAVY,
                     font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=16, pady=(16, 4))
        self.drug_var = ctk.StringVar(value=get_drug_names()[0])
        ctk.CTkOptionMenu(form, values=get_drug_names(), variable=self.drug_var,
                          fg_color=BLUE, button_color=NAVY, button_hover_color=BLUE_DARK
                          ).pack(fill="x", padx=16, pady=(0, 12))

        row = ctk.CTkFrame(form, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=(0, 12))
        row.grid_columnconfigure((0, 1), weight=1)

        age_box = ctk.CTkFrame(row, fg_color="transparent")
        age_box.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ctk.CTkLabel(age_box, text="나이 (세)", text_color=NAVY).pack(anchor="w")
        self.age_entry = ctk.CTkEntry(age_box, placeholder_text="예: 70")
        self.age_entry.pack(fill="x")

        weight_box = ctk.CTkFrame(row, fg_color="transparent")
        weight_box.grid(row=0, column=1, sticky="ew", padx=(8, 0))
        ctk.CTkLabel(weight_box, text="체중 (kg)", text_color=NAVY).pack(anchor="w")
        self.weight_entry = ctk.CTkEntry(weight_box, placeholder_text="예: 60")
        self.weight_entry.pack(fill="x")

        ctk.CTkLabel(form, text="혈청 크레아티닌 (mg/dL) — 선택 입력", text_color=NAVY
                     ).pack(anchor="w", padx=16, pady=(4, 2))
        self.creat_entry = ctk.CTkEntry(form, placeholder_text="신장기능 이상이 있다면 입력을 권장합니다")
        self.creat_entry.pack(fill="x", padx=16, pady=(0, 4))
        ctk.CTkLabel(form, text="※ 신장으로 배설되는 약물은 크레아티닌을 입력하면 더 정확한 결과를 제공합니다.",
                     font=ctk.CTkFont(size=11), text_color=TEXT_FAINT, wraplength=470,
                     justify="left").pack(anchor="w", padx=16, pady=(0, 8))

        self.sex_var = ctk.StringVar(value="남성")
        sex_frame = ctk.CTkFrame(form, fg_color="transparent")
        sex_frame.pack(fill="x", padx=16, pady=(0, 16))
        ctk.CTkLabel(sex_frame, text="성별", text_color=NAVY).pack(side="left", padx=(0, 12))
        ctk.CTkRadioButton(sex_frame, text="남성", variable=self.sex_var, value="남성",
                           fg_color=BLUE).pack(side="left", padx=(0, 12))
        ctk.CTkRadioButton(sex_frame, text="여성", variable=self.sex_var, value="여성",
                           fg_color=BLUE).pack(side="left")

        ctk.CTkButton(self, text="용량 계산하기", command=self.on_calculate,
                      fg_color=NAVY, hover_color=BLUE_DARK, height=42,
                      font=ctk.CTkFont(size=15, weight="bold")).pack(pady=16, padx=24, fill="x")

        self.result_box = ctk.CTkTextbox(self, height=260, fg_color=BG_SOFT, text_color="#1F2D3A",
                                          corner_radius=14, font=ctk.CTkFont(size=13))
        self.result_box.pack(padx=24, pady=(0, 12), fill="both", expand=True)
        self.result_box.configure(state="disabled")

        ctk.CTkLabel(self, text=DISCLAIMER, font=ctk.CTkFont(size=10.5),
                     text_color=TEXT_FAINT, wraplength=520, justify="left").pack(padx=24, pady=(0, 16))

    def on_calculate(self):
        drug = self.drug_var.get()
        age_text = self.age_entry.get().strip()
        weight_text = self.weight_entry.get().strip()
        creat_text = self.creat_entry.get().strip()

        if not age_text or not weight_text:
            self._show_result(["나이와 체중을 모두 입력해주세요."], [])
            return
        try:
            age = int(age_text)
            weight = float(weight_text)
        except ValueError:
            self._show_result(["나이는 정수, 체중은 숫자로 입력해주세요."], [])
            return

        creatinine = None
        if creat_text:
            try:
                creatinine = float(creat_text)
            except ValueError:
                self._show_result(["크레아티닌 수치는 숫자로 입력해주세요."], [])
                return

        sex = "F" if self.sex_var.get() == "여성" else "M"
        result = calculate(drug, age, weight, creatinine, sex)
        self._show_result(result["lines"], result["warnings"])

    def _show_result(self, lines, warnings):
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", "end")
        for l in lines:
            self.result_box.insert("end", f"{l}\n\n")
        for w in warnings:
            self.result_box.insert("end", f"{w}\n\n")
        self.result_box.configure(state="disabled")


if __name__ == "__main__":
    App().mainloop()
