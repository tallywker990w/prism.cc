#GEMINI IS A DUMBASS 

import customtkinter as ctk
import ctypes
import os
import requests
import webbrowser
import datetime
from tkinter import filedialog, messagebox

# --- CONFIG & SYSTEM DATA ---
USER_ACCOUNT = "tallywker990"
DLL_NAME = "wininet_cache.dll"
current_theme_color = "#00ff88"
log_history = []
current_font_size = 14
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}

# --- DIRECTORY SETUP ---
FAV_PATH = os.path.join(os.getcwd(), "scripts", "favorites")
if not os.path.exists(FAV_PATH):
    os.makedirs(FAV_PATH)

def load_dll(path=None):
    global wrd, funcs
    dll_path = path if path else os.path.join(os.getcwd(), DLL_NAME)
    try:
        wrd = ctypes.WinDLL(dll_path)
        funcs = [wrd[i] for i in range(1, 6)]
        for f in funcs: f.argtypes = [ctypes.c_char_p]
        return True
    except:
        wrd = None
        return False

load_dll()

class PrismApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PRISM.CC // V20.0")
        self.geometry("1150x850")
        ctk.set_appearance_mode("dark")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=280, fg_color="#080808")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.title_lbl = ctk.CTkLabel(self.sidebar, text="PRISM", font=("Impact", 64), text_color=current_theme_color)
        self.title_lbl.pack(pady=45)
        
        # Navigation
        self.create_nav_btn("LUA EXECUTOR", "⚡", self.show_executor)
        self.create_nav_btn("SAVED SCRIPTS", "📁", self.show_favorites)
        self.create_nav_btn("CLOUD HUB", "☁️", self.show_cloud)
        self.create_nav_btn("ESSENTIALS", "🛠️", self.show_essentials)
        self.create_nav_btn("THEMES", "🎨", self.show_themes)
        self.create_nav_btn("SETTINGS", "⚙️", self.show_settings)
        
        # Bottom Section
        self.dev_tag = ctk.CTkLabel(self.sidebar, text=f"Developed by: {USER_ACCOUNT}", font=("Arial", 12, "bold"), text_color="#444")
        self.dev_tag.pack(side="bottom", pady=20)

        # Discord Button
        self.discord_btn = ctk.CTkButton(self.sidebar, text="💬 JOIN DISCORD", 
                                        fg_color="#5865f2", hover_color="#4752c4", 
                                        height=40, font=("Arial", 13, "bold"), 
                                        command=lambda: webbrowser.open("https://discord.gg/2BSmXd8hKY"))
        self.discord_btn.pack(side="bottom", fill="x", padx=30, pady=5)
        
        self.container = ctk.CTkFrame(self, fg_color="#0d0d0d", corner_radius=20)
        self.container.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)
        
        self.show_executor()

    def create_nav_btn(self, text, icon, command):
        btn = ctk.CTkButton(self.sidebar, text=f"{icon} {text}", fg_color="transparent", height=55, anchor="w", font=("Arial", 14, "bold"), hover_color="#121212", command=command)
        btn.pack(fill="x", padx=20, pady=4)

    def log(self, msg):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        full_msg = f"[{ts}] {msg}"
        log_history.append(full_msg)
        if hasattr(self, 'console') and self.console.winfo_exists():
            self.console.configure(state="normal")
            self.console.insert("end", full_msg + "\n")
            self.console.see("end")
            self.console.configure(state="disabled")

    def clear_container(self):
        for widget in self.container.winfo_children(): widget.destroy()

    def show_favorites(self):
        self.clear_container()
        ctk.CTkLabel(self.container, text="SAVED SCRIPTS (FAVORITES)", font=("Arial", 22, "bold")).pack(pady=10)
        search_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        search_frame.pack(fill="x", padx=25, pady=5)
        self.fav_search = ctk.CTkEntry(search_frame, placeholder_text="Search local scripts...", height=35)
        self.fav_search.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.fav_search.bind("<KeyRelease>", lambda e: self.update_fav_list())
        self.fav_scroll = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        self.fav_scroll.pack(fill="both", expand=True, padx=25, pady=10)
        self.update_fav_list()

    def update_fav_list(self):
        for w in self.fav_scroll.winfo_children(): w.destroy()
        query = self.fav_search.get().lower() if hasattr(self, 'fav_search') else ""
        for filename in os.listdir(FAV_PATH):
            if filename.endswith(".lua") and query in filename.lower():
                item = ctk.CTkFrame(self.fav_scroll, fg_color="#121212", height=50)
                item.pack(fill="x", pady=2)
                ctk.CTkLabel(item, text=f"📜 {filename}", font=("Arial", 13)).place(x=15, y=12)
                ctk.CTkButton(item, text="LOAD", width=60, fg_color=current_theme_color, text_color="black", command=lambda f=filename: self.load_fav_to_editor(f)).place(relx=0.9, rely=0.5, anchor="center")
                ctk.CTkButton(item, text="DEL", width=40, fg_color="#700", command=lambda f=filename: self.delete_fav(f)).place(relx=0.8, rely=0.5, anchor="center")

    def load_fav_to_editor(self, filename):
        with open(os.path.join(FAV_PATH, filename), "r") as f: content = f.read()
        self.show_executor()
        self.editor.delete("0.0", "end")
        self.editor.insert("end", content)
        self.log(f"Loaded {filename}")

    def delete_fav(self, filename):
        if messagebox.askyesno("Prism", f"Delete {filename}?"):
            os.remove(os.path.join(FAV_PATH, filename))
            self.update_fav_list()

    def show_executor(self):
        self.clear_container()
        ctk.CTkLabel(self.container, text="LUA EXECUTOR", font=("Arial", 22, "bold")).pack(pady=10)
        self.editor = ctk.CTkTextbox(self.container, height=380, fg_color="#050505", text_color=current_theme_color, font=("Consolas", current_font_size))
        self.editor.pack(fill="both", expand=True, padx=25, pady=5)
        self.console = ctk.CTkTextbox(self.container, height=120, fg_color="#020202", text_color="#777", font=("Consolas", 11))
        self.console.pack(fill="x", padx=25, pady=10)
        self.console.configure(state="normal")
        if log_history: self.console.insert("end", "\n".join(log_history) + "\n")
        self.console.see("end")
        self.console.configure(state="disabled")
        btn_bar = ctk.CTkFrame(self.container, fg_color="transparent")
        btn_bar.pack(fill="x", padx=25, pady=(0, 20))
        ctk.CTkButton(btn_bar, text="INJECT", width=110, command=self.inject_logic).pack(side="left", padx=3)
        ctk.CTkButton(btn_bar, text="EXECUTE", width=110, fg_color=current_theme_color, text_color="black", command=lambda: self.run_lua(self.editor.get("0.0", "end"))).pack(side="left", padx=3)
        ctk.CTkButton(btn_bar, text="SAVE", width=80, fg_color="#3498db", command=self.save_script_dialog).pack(side="left", padx=3)
        ctk.CTkButton(btn_bar, text="P+E", width=80, fg_color="#ff8800", text_color="black", command=self.paste_and_execute).pack(side="left", padx=3)
        ctk.CTkButton(btn_bar, text="CLEAR", width=80, fg_color="#ff4444", command=lambda: self.editor.delete("0.0", "end")).pack(side="right", padx=3)

    def inject_logic(self):
        if wrd:
            try: wrd[1](); self.log("Injected.")
            except: self.log("Inject failed.")
        else: self.log("DLL missing.")

    def run_lua(self, code):
        if code and wrd:
            payload = (code.strip() + "\0").encode('utf-8')
            for f in funcs:
                try: f(payload)
                except: continue
            self.log("Executed.")

    def save_script_dialog(self):
        content = self.editor.get("0.0", "end-1c")
        if not content.strip(): return
        file_path = filedialog.asksaveasfilename(initialdir=FAV_PATH, defaultextension=".lua")
        if file_path:
            with open(file_path, "w") as f: f.write(content)
            self.log(f"Saved: {os.path.basename(file_path)}")

    def paste_and_execute(self):
        try:
            code = self.clipboard_get()
            if code:
                self.editor.delete("0.0", "end"); self.editor.insert("end", code)
                self.run_lua(code); self.log("P+E success.")
        except: self.log("Paste failed.")

    def show_cloud(self):
        self.clear_container()
        ctk.CTkLabel(self.container, text="CLOUD HUB", font=("Arial", 22, "bold")).pack(pady=15)
        sf = ctk.CTkFrame(self.container, fg_color="transparent")
        sf.pack(fill="x", padx=25)
        self.s_entry = ctk.CTkEntry(sf, placeholder_text="Search scripts...", height=45)
        self.s_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(sf, text="SEARCH", command=self.search_logic).pack(side="right")
        self.scroll_cloud = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        self.scroll_cloud.pack(fill="both", expand=True, padx=20, pady=15)

    def search_logic(self):
        q = self.s_entry.get()
        for w in self.scroll_cloud.winfo_children(): w.destroy()
        try:
            r = requests.get(f"https://scriptblox.com/api/script/search?q={q}&max=15", headers=headers, timeout=5).json()
            for s in r['result']['scripts']:
                card = ctk.CTkFrame(self.scroll_cloud, fg_color="#121212", height=60)
                card.pack(fill="x", pady=4, padx=5)
                ctk.CTkLabel(card, text=s['title'][:40], font=("Arial", 12, "bold")).place(x=15, y=10)
                slug = s['slug']
                ctk.CTkButton(card, text="LOAD", width=60, fg_color=current_theme_color, command=lambda sl=slug: self.load_cloud(sl)).place(relx=0.9, rely=0.5, anchor="center")
        except: self.log("Search error.")

    def load_cloud(self, slug):
        try:
            r = requests.get(f"https://scriptblox.com/api/script/{slug}", headers=headers, timeout=8).json()
            data = r.get('result', {}).get('script', {})
            code = data.get('script') or data.get('rawScript') or data.get('source')
            if code:
                self.editor.delete("0.0", "end"); self.editor.insert("end", code)
                self.show_executor(); self.log(f"Loaded: {slug}")
        except: self.log("Load failed.")

    def show_essentials(self):
        self.clear_container()
        ctk.CTkLabel(self.container, text="ESSENTIALS", font=("Arial", 22, "bold")).pack(pady=10)
        scroll = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20)
        ess = [
            ("Infinite Yield", "The #1 admin command script.", "loadstring(game:HttpGet('https://raw.githubusercontent.com/EdgeIY/infiniteyield/master/source'))()"),
            ("Invisible Fling", "Fling players while invisible.", "loadstring(game:HttpGet('https://raw.githubusercontent.com/0866/lua/main/InvisibleFling.lua'))()"),
            ("FPS Booster", "Optimizes game graphics for speed.", "loadstring(game:HttpGet('https://pastebin.com/raw/4CDTn6pd'))()"),
            ("Dex Explorer", "Browse game instances in-realtime.", "loadstring(game:HttpGet('https://raw.githubusercontent.com/infyiff/backup/main/dex.lua'))()"),
            ("CMD-X", "Powerful alternative admin script.", "loadstring(game:HttpGet('https://raw.githubusercontent.com/CMD-X/CMD-X/master/Source'))()"),
            ("Keyboard GUI", "On-screen keyboard for mobile users.", "loadstring(game:HttpGet('https://raw.githubusercontent.com/advxzivhsjjshsjuritixvisual/reall/main/key.lua'))()"),
            ("Rejoin Script", "Quickly rejoin the server.", "game:GetService('TeleportService'):Teleport(game.PlaceId, game.Players.LocalPlayer)"),
            ("Chat Bypasser", "See messages that would be tagged.", "loadstring(game:HttpGet('https://raw.githubusercontent.com/Synergy-Hub/Chat-Bypasser/main/ChatBypasser.lua'))()"),
            ("Remote Spy", "View all remote events firing.", "loadstring(game:HttpGet('https://raw.githubusercontent.com/ex-pve/VGG-Spy/main/VGG%20Spy.lua'))()"),
            ("SimpleSpy", "The industry standard remote spy.", "loadstring(game:HttpGet('https://raw.githubusercontent.com/74n0v/SimpleSpyV3/main/main.lua'))()"),
            ("Hydroxide", "Advanced debugging/spy toolset.", "loadstring(game:HttpGet('https://raw.githubusercontent.com/Upbolt/Hydroxide/revision/oh.lua'))()"),
            ("Unnamed ESP", "The most customizable ESP script.", "loadstring(game:HttpGet('https://raw.githubusercontent.com/ic3w01f22/Unnamed-ESP/master/UnnamedESP.lua'))()")]
        for n, d, c in ess:
            card = ctk.CTkFrame(scroll, fg_color="#121212", height=80)
            card.pack(fill="x", pady=5)
            ctk.CTkLabel(card, text=n, font=("Arial", 14, "bold")).place(x=15, y=12)
            ctk.CTkLabel(card, text=d, font=("Arial", 11), text_color="#aaa").place(x=15, y=38)
            ctk.CTkButton(card, text="Execute", width=80, fg_color=current_theme_color, text_color="black", command=lambda code=c: self.run_lua(code)).place(relx=0.9, rely=0.5, anchor="center")

    def show_themes(self):
        self.clear_container()
        scroll = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=40, pady=20)
        themes = {"Prism Green": "#00ff88", "Deep Red": "#ff0000", "Midnight Purple": "#a020f0", "Neon Red": "#ff3131", "Sky Blue": "#00d4ff"}
        for name, hex in themes.items():
            ctk.CTkButton(scroll, text=name, fg_color=hex, text_color="black", height=45, width=400, command=lambda h=hex: self.apply_theme(h)).pack(pady=5)

    def show_settings(self):
        self.clear_container()
        scroll = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=25)
        ctk.CTkLabel(scroll, text="VISUALS", font=("Arial", 14, "bold"), text_color=current_theme_color).pack(anchor="w", pady=5)
        ctk.CTkSwitch(scroll, text="ALWAYS ON TOP", command=lambda: self.attributes("-topmost", 1)).pack(anchor="w", pady=5)
        ctk.CTkSlider(scroll, from_=0.0, to=0.5, command=lambda v: self.attributes("-alpha", 1.0-float(v))).pack(fill="x", pady=5)
        ctk.CTkLabel(scroll, text="SYSTEM", font=("Arial", 14, "bold"), text_color=current_theme_color).pack(anchor="w", pady=(20, 5))
        ctk.CTkButton(scroll, text="HIDE CMD", command=lambda: ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)).pack(anchor="w", pady=5)
        ctk.CTkButton(scroll, text="KILL ROBLOX", fg_color="#700", command=lambda: os.system("taskkill /F /IM RobloxPlayerBeta.exe")).pack(anchor="w", pady=5)
        ctk.CTkButton(scroll, text="FLUSH RAM", command=lambda: ctypes.windll.psapi.EmptyWorkingSet(ctypes.windll.kernel32.GetCurrentProcess())).pack(anchor="w", pady=5)
        ctk.CTkButton(scroll, text="CLEAR LOGS", fg_color="#444", command=lambda: (log_history.clear(), self.log("Logs cleared."))).pack(anchor="w", pady=5)

    def apply_theme(self, hex):
        global current_theme_color; current_theme_color = hex
        self.title_lbl.configure(text_color=hex); self.show_executor()

if __name__ == "__main__":
    app = PrismApp()
    app.mainloop()
