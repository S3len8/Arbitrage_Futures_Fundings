"""
Funding Scanner GUI
Запуск: python main.py
Зависимости: pip install customtkinter pillow
"""

import customtkinter as ctk
import subprocess
import threading
import ast
import json
import csv
import os
import sys
from datetime import datetime
from tkinter import messagebox, filedialog


# ─── Настройки темы ────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ─── Путь к сканеру (main.py должен лежать рядом с gui.py) ────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCANNER_SCRIPT = os.path.join(BASE_DIR, "main.py")


# ─── Цвета ─────────────────────────────────────────────────────────────────────
COLORS = {
    "bg":        "#0f1117",
    "surface":   "#1a1d2e",
    "card":      "#1e2235",
    "border":    "#2a2d3e",
    "accent":    "#6366f1",        # индиго
    "accent2":   "#22d3ee",        # циан
    "success":   "#10b981",
    "warning":   "#f59e0b",
    "danger":    "#ef4444",
    "text":      "#e2e8f0",
    "muted":     "#64748b",
    "row_odd":   "#1e2235",
    "row_even":  "#181b2c",
    "header_row":"#252840",
}

COLUMNS = [
    ("Пара",          "pair",         120, "w"),
    ("Малая биржа",   "small_ex",     110, "center"),
    ("Ask (мал.)",    "small_ask",     90, "center"),
    ("Bid (мал.)",    "small_bid",     90, "center"),
    ("Большая биржа", "big_ex",       110, "center"),
    ("Ask (бол.)",    "big_ask",       90, "center"),
    ("Bid (бол.)",    "big_bid",       90, "center"),
    ("Funding Spread","spread",       130, "center"),
    ("Profit %",      "profit",       100, "center"),
]


def profit_color(profit: float) -> str:
    """Возвращает цвет в зависимости от значения Profit."""
    if profit >= 2.0:
        return "#10b981"   # зелёный
    elif profit >= 1.0:
        return "#22d3ee"   # циан
    elif profit >= 0.5:
        return "#f59e0b"   # жёлтый
    else:
        return "#ef4444"   # красный


class TableRow(ctk.CTkFrame):
    def __init__(self, master, row_data: dict, index: int, **kwargs):
        bg = COLORS["row_odd"] if index % 2 == 0 else COLORS["row_even"]
        super().__init__(master, fg_color=bg, corner_radius=0, **kwargs)

        profit = row_data.get("profit", 0)
        p_color = profit_color(profit)

        values = [
            row_data.get("pair", ""),
            row_data.get("small_ex", "").upper(),
            f"{row_data.get('small_ask', 0):.6g}",
            f"{row_data.get('small_bid', 0):.6g}",
            row_data.get("big_ex", "").upper(),
            f"{row_data.get('big_ask', 0):.6g}",
            f"{row_data.get('big_bid', 0):.6g}",
            f"{row_data.get('spread', 0):.4f}",
            f"{profit:.4f}%",
        ]

        for i, (col_def, val) in enumerate(zip(COLUMNS, values)):
            _, _, width, anchor = col_def
            is_profit = (i == len(COLUMNS) - 1)
            lbl = ctk.CTkLabel(
                self,
                text=val,
                width=width,
                text_color=p_color if is_profit else COLORS["text"],
                font=ctk.CTkFont(size=13, weight="bold" if is_profit else "normal"),
                anchor=anchor,
            )
            lbl.grid(row=0, column=i, padx=(8 if i == 0 else 4, 4), pady=6, sticky="ew")

        self.columnconfigure(list(range(len(COLUMNS))), weight=1)


class HeaderRow(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS["header_row"], corner_radius=6, **kwargs)
        for i, (title, _, width, anchor) in enumerate(COLUMNS):
            lbl = ctk.CTkLabel(
                self,
                text=title.upper(),
                width=width,
                text_color=COLORS["accent2"],
                font=ctk.CTkFont(size=11, weight="bold"),
                anchor=anchor,
            )
            lbl.grid(row=0, column=i, padx=(8 if i == 0 else 4, 4), pady=8, sticky="ew")
        self.columnconfigure(list(range(len(COLUMNS))), weight=1)


class FundingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("⚡ Funding Scanner")
        self.geometry("1300x780")
        self.minsize(900, 600)
        self.configure(fg_color=COLORS["bg"])

        self._last_data: list[dict] = []
        self._running = False

        self._build_ui()

    # ─── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Шапка ──────────────────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color=COLORS["surface"], corner_radius=0, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        title_lbl = ctk.CTkLabel(
            header,
            text="⚡  FUNDING SCANNER",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS["accent"],
        )
        title_lbl.pack(side="left", padx=24, pady=18)

        self.status_lbl = ctk.CTkLabel(
            header,
            text="● Готов к сканированию",
            font=ctk.CTkFont(size=13),
            text_color=COLORS["muted"],
        )
        self.status_lbl.pack(side="left", padx=12)

        self.time_lbl = ctk.CTkLabel(
            header,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["muted"],
        )
        self.time_lbl.pack(side="right", padx=24)

        # ── Панель управления ──────────────────────────────────────────────────
        ctrl = ctk.CTkFrame(self, fg_color=COLORS["surface"], corner_radius=0, height=60)
        ctrl.pack(fill="x", pady=(2, 0))
        ctrl.pack_propagate(False)

        self.scan_btn = ctk.CTkButton(
            ctrl,
            text="🔍  Сканировать",
            command=self._start_scan,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=COLORS["accent"],
            hover_color="#4f46e5",
            corner_radius=8,
            height=38,
            width=180,
        )
        self.scan_btn.pack(side="left", padx=16, pady=11)

        self.export_btn = ctk.CTkButton(
            ctrl,
            text="💾  Экспорт CSV",
            command=self._export_csv,
            font=ctk.CTkFont(size=13),
            fg_color=COLORS["card"],
            hover_color=COLORS["border"],
            border_color=COLORS["accent"],
            border_width=1,
            corner_radius=8,
            height=38,
            width=150,
        )
        self.export_btn.pack(side="left", padx=4)

        # Фильтр по минимальному Profit
        filter_lbl = ctk.CTkLabel(
            ctrl, text="Min Profit %:", text_color=COLORS["muted"],
            font=ctk.CTkFont(size=13),
        )
        filter_lbl.pack(side="left", padx=(24, 4))

        self.min_profit_var = ctk.StringVar(value="0")
        self.profit_entry = ctk.CTkEntry(
            ctrl, textvariable=self.min_profit_var, width=70,
            fg_color=COLORS["card"], border_color=COLORS["border"],
            text_color=COLORS["text"], font=ctk.CTkFont(size=13),
        )
        self.profit_entry.pack(side="left")

        apply_btn = ctk.CTkButton(
            ctrl, text="Применить", command=self._apply_filter,
            font=ctk.CTkFont(size=12),
            fg_color=COLORS["card"], hover_color=COLORS["border"],
            border_color=COLORS["accent2"], border_width=1,
            corner_radius=8, height=30, width=100,
        )
        apply_btn.pack(side="left", padx=8)

        # Счётчик результатов
        self.count_lbl = ctk.CTkLabel(
            ctrl, text="Результатов: —",
            font=ctk.CTkFont(size=13), text_color=COLORS["muted"],
        )
        self.count_lbl.pack(side="right", padx=20)

        # ── Прогресс-бар ───────────────────────────────────────────────────────
        self.progress = ctk.CTkProgressBar(self, fg_color=COLORS["border"], progress_color=COLORS["accent"])
        self.progress.pack(fill="x", padx=0)
        self.progress.set(0)

        # ── Таблица (скролл) ───────────────────────────────────────────────────
        self.table_frame = ctk.CTkScrollableFrame(
            self, fg_color=COLORS["bg"],
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["accent"],
        )
        self.table_frame.pack(fill="both", expand=True, padx=16, pady=(12, 0))

        # Заголовок таблицы
        self.header_row = HeaderRow(self.table_frame)
        self.header_row.pack(fill="x", pady=(0, 4))

        # Контейнер строк
        self.rows_container = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        self.rows_container.pack(fill="x")

        # ── Пустое состояние ───────────────────────────────────────────────────
        self.empty_lbl = ctk.CTkLabel(
            self.rows_container,
            text="Нажмите «Сканировать» для поиска лучшего фандинга",
            font=ctk.CTkFont(size=16),
            text_color=COLORS["muted"],
        )
        self.empty_lbl.pack(pady=80)

        # ── Подвал ─────────────────────────────────────────────────────────────
        footer = ctk.CTkFrame(self, fg_color=COLORS["surface"], corner_radius=0, height=32)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        ctk.CTkLabel(
            footer, text="Funding Scanner  •  данные в реальном времени",
            font=ctk.CTkFont(size=11), text_color=COLORS["muted"],
        ).pack(side="left", padx=16)

    # ─── Сканирование ──────────────────────────────────────────────────────────

    def _start_scan(self):
        if self._running:
            return
        self._running = True
        self.scan_btn.configure(state="disabled", text="⏳  Сканирую...")
        self.status_lbl.configure(text="● Сканирование...", text_color=COLORS["warning"])
        self.progress.configure(mode="indeterminate")
        self.progress.start()
        threading.Thread(target=self._run_scanner, daemon=True).start()

    def _run_scanner(self):
        try:
            process = subprocess.Popen(
                [sys.executable, "-u", SCANNER_SCRIPT],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )

            lines = []
            for line in process.stdout:
                line = line.strip()
                if line:
                    lines.append(line)
                    preview = line[:60] + "…" if len(line) > 60 else line
                    self.after(0, lambda t=preview: self.status_lbl.configure(
                        text=f"⏳ {t}", text_color=COLORS["warning"]
                    ))

            process.wait(timeout=600)
            stderr_out = process.stderr.read().strip()

            if not lines:
                raise ValueError(
                    stderr_out or
                    "Программа не вернула никаких данных.\n"
                    "Убедись что main.py делает print(словарь) в конце."
                )

            # Ищем строку-словарь начиная с последней
            data = None
            for candidate in reversed(lines):
                try:
                    data = ast.literal_eval(candidate)
                    if isinstance(data, dict):
                        break
                except Exception:
                    try:
                        data = json.loads(candidate)
                        if isinstance(data, dict):
                            break
                    except Exception:
                        data = None

            if not isinstance(data, dict):
                full_output = "\n".join(lines[-5:])
                raise ValueError(
                    f"Не удалось найти словарь в выводе программы.\n\n"
                    f"Последние строки вывода:\n{full_output}\n\n"
                    f"Убедись что main.py печатает словарь через print()."
                )

            rows = self._parse_data(data)
            self.after(0, self._display_results, rows)

        except subprocess.TimeoutExpired:
            process.kill()
            self.after(0, self._show_error, "Превышено время ожидания (10 мин).\nПроверь не завис ли main.py.")
        except Exception as e:
            self.after(0, self._show_error, str(e))

    def _parse_data(self, raw: dict) -> list[dict]:
        rows = []
        for pair, info in raw.items():
            rows.append({
                "pair":      pair,
                "small_ex":  info.get("Small_exchange", ""),
                "small_ask": info.get("Small_ask", 0),
                "small_bid": info.get("Small_bid", 0),
                "big_ex":    info.get("Big_exchange", ""),
                "big_ask":   info.get("Big_ask", 0),
                "big_bid":   info.get("Big_bid", 0),
                "spread":    info.get("Funding_spread", 0),
                "profit":    info.get("Profit", 0),
            })
        rows.sort(key=lambda x: x["profit"], reverse=True)
        return rows

    def _display_results(self, rows: list[dict]):
        self._last_data = rows
        self._stop_progress()
        self._render_rows(rows)
        ts = datetime.now().strftime("%H:%M:%S")
        self.time_lbl.configure(text=f"Обновлено: {ts}")
        self.status_lbl.configure(text=f"● Готово  —  найдено {len(rows)} пар", text_color=COLORS["success"])

    def _apply_filter(self):
        try:
            min_p = float(self.min_profit_var.get())
        except ValueError:
            min_p = 0.0
        filtered = [r for r in self._last_data if r["profit"] >= min_p]
        self._render_rows(filtered)

    def _render_rows(self, rows: list[dict]):
        # Очистка
        for widget in self.rows_container.winfo_children():
            widget.destroy()

        if not rows:
            ctk.CTkLabel(
                self.rows_container,
                text="Нет данных по заданному фильтру",
                font=ctk.CTkFont(size=15),
                text_color=COLORS["muted"],
            ).pack(pady=60)
            self.count_lbl.configure(text="Результатов: 0")
            return

        for i, row_data in enumerate(rows):
            row = TableRow(self.rows_container, row_data, i)
            row.pack(fill="x", pady=1)

        self.count_lbl.configure(text=f"Результатов: {len(rows)}")

    def _show_error(self, msg: str):
        self._stop_progress()
        self.status_lbl.configure(text="● Ошибка", text_color=COLORS["danger"])
        messagebox.showerror("Ошибка сканера", msg)

    def _stop_progress(self):
        self.progress.stop()
        self.progress.configure(mode="determinate")
        self.progress.set(1)
        self.scan_btn.configure(state="normal", text="🔍  Сканировать")
        self._running = False

    # ─── Экспорт ───────────────────────────────────────────────────────────────

    def _export_csv(self):
        if not self._last_data:
            messagebox.showinfo("Экспорт", "Нет данных для экспорта. Запустите сканирование.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV файлы", "*.csv")],
            initialfile=f"funding_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        )
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(self._last_data[0].keys()))
            writer.writeheader()
            writer.writerows(self._last_data)
        messagebox.showinfo("Экспорт", f"Сохранено: {path}")


# ─── Запуск ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = FundingApp()
    app.mainloop()