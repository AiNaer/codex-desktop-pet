import os
import tkinter as tk

from PIL import Image, ImageTk


ASSET = os.path.join(os.path.dirname(__file__), "codex_pet_v2.png")
TRANSPARENT = "#ff00ff"


class DesktopPet:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg=TRANSPARENT)
        self.root.wm_attributes("-transparentcolor", TRANSPARENT)

        image = Image.open(ASSET).convert("RGBA")
        image = image.resize((image.width // 2, image.height // 2),
                             Image.Resampling.NEAREST)
        self.width, self.height = image.size
        self.split_y = int(self.height * 0.68)
        head = image.crop((0, 0, self.width, self.split_y))
        body = image.crop((0, self.split_y, self.width, self.height))
        self.head_photo = ImageTk.PhotoImage(head)
        self.body_photo = ImageTk.PhotoImage(body)

        self.canvas = tk.Canvas(root, width=self.width, height=self.height,
                                bg=TRANSPARENT, highlightthickness=0)
        self.canvas.pack()
        self.body_item = self.canvas.create_image(
            0, self.split_y, anchor="nw", image=self.body_photo)
        self.head_item = self.canvas.create_image(
            0, 0, anchor="nw", image=self.head_photo)

        self.drag_start = None
        self.x = 0
        self.y = 0
        self.frame = 0

        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.end_drag)
        self.canvas.bind("<Button-3>", self.menu)
        self.root.bind("<Escape>", lambda _event: root.destroy())

        self.root.update_idletasks()
        self.x = root.winfo_screenwidth() - self.width - 40
        self.y = root.winfo_screenheight() - self.height - 100
        self.root.geometry(f"+{self.x}+{self.y}")
        self.animate()

    def start_drag(self, event):
        self.x = self.root.winfo_x()
        self.y = self.root.winfo_y()
        self.drag_start = (event.x_root - self.x, event.y_root - self.y)

    def drag(self, event):
        if self.drag_start:
            self.x = event.x_root - self.drag_start[0]
            self.y = event.y_root - self.drag_start[1]
            self.root.geometry(f"+{int(self.x)}+{int(self.y)}")

    def end_drag(self, _event):
        self.drag_start = None

    def animate(self):
        # Keep only a small idle head sway; the pet no longer walks automatically.
        head_shift = (-2, -1, 0, 1, 2, 1, 0, -1)[self.frame % 8]
        self.canvas.coords(self.head_item, head_shift, 0)
        self.canvas.coords(self.body_item, 0, self.split_y)

        self.frame += 1
        self.root.after(120, self.animate)

    def menu(self, event):
        menu = tk.Menu(self.root, tearoff=False)
        menu.add_command(label="退出桌宠", command=self.root.destroy)
        menu.tk_popup(event.x_root, event.y_root)


if __name__ == "__main__":
    app = tk.Tk()
    DesktopPet(app)
    app.mainloop()
