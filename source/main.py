import tkinter as tk
from tkinter import messagebox, scrolledtext
import random

# txt 파일 읽기
with open('leaders.txt', encoding='utf-8') as f:
    leaders = [name.strip() for name in f.read().split(',') if name.strip()]

root = tk.Tk()
root.title("문명6 지도자 추첨")
root.geometry("700x500")  # 창 크기

# 왼쪽 프레임 (입력 + 체크박스)
left_frame = tk.Frame(root)
left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

tk.Label(left_frame, text="뽑을 인원 수:", font=("Arial", 14)).pack(anchor='w')
count_entry = tk.Entry(left_frame, width=5, font=("Arial", 14))
count_entry.insert(0, "10")
count_entry.pack(anchor='w', pady=5)

# 스크롤 가능한 체크박스 프레임
canvas = tk.Canvas(left_frame)
scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0,0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

check_vars = []
for leader in leaders:
    var = tk.BooleanVar()
    chk = tk.Checkbutton(scrollable_frame, text=leader, variable=var, anchor='w', font=("Arial", 14))
    chk.pack(fill='x', anchor='w')
    check_vars.append(var)

# 마우스 휠로 스크롤 가능하도록 바인딩
def _on_mousewheel(event):
    # Windows
    canvas.yview_scroll(-1 * int(event.delta / 120), "units")
canvas.bind_all("<MouseWheel>", _on_mousewheel)

# 오른쪽 프레임 (결과 표시)
right_frame = tk.Frame(root)
right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

tk.Label(right_frame, text="추첨 결과:", font=("Arial", 14)).pack(anchor='w')
result_box = scrolledtext.ScrolledText(right_frame, width=30, height=25, font=("Arial", 14))
result_box.pack(fill='both', expand=True)

# 추첨 함수
def pick():
    try:
        count = int(count_entry.get())
    except ValueError:
        messagebox.showerror("오류", "뽑을 인원 수를 숫자로 입력하세요.")
        return

    excluded = [leaders[i] for i, var in enumerate(check_vars) if var.get()]
    available = [l for l in leaders if l not in excluded]

    if count > len(available):
        count = len(available)

    picked = random.sample(available, count)
    result_box.delete('1.0', tk.END)  # 이전 결과 삭제
    result_box.insert(tk.END, "\n".join(picked))

# 추첨 버튼
tk.Button(left_frame, text="추첨", command=pick, font=("Arial", 14)).pack(pady=10)

root.mainloop()
