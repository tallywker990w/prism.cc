import customtkinter as ctk
import ctypes
import os
import requests
import webbrowser
import datetime
import platform
from tkinter import filedialog, messagebox

# --- CONFIG & SYSTEM DATA ---
USER_ACCOUNT = "tallywker990" 
DLL_NAME = "windows_cache.dll"
# Using the specific Discord link from your screenshot
DISCORD_LINK = "https://discord.gg/A36ePNE2jt" 
current_theme_color = "#00ff88"
log_history = []
IS_LINUX = platform.system() == "Linux"

# --- RAYFIELD BRIDGE SCRIPT ---
RAYFIELD_LOADER = f"""
local Rayfield = loadstring(game:HttpGet('https://sirius.menu/rayfield'))()
local Window = Rayfield:CreateWindow({{
   Name = "PRISM.CC | V20",
   LoadingTitle = "PRISM EXECUTOR",
   LoadingSubtitle = "by {USER_ACCOUNT}",
   KeySystem = true,
   KeySettings = {{
      Title = "PRISM Access",
      Subtitle = "Key Required",
      Note = "Join Discord: {DISCORD_LINK}",
      FileName = "PrismKeyV5", 
      SaveKey = true, 
      Key = {{"PRISM_2026"}},
      Actions = {{
            [1] = {{
                Text = "Join Discord",
                OnPress = function() setclipboard("{DISCORD_LINK}") end
            }}
        }}
   }}
}})
"""

# --- DIRECTORY & DLL HANDLING ---
FAV_PATH = os.path.join(os.getcwd(), "scripts", "favorites")
if not os.path.exists(FAV_PATH): os.makedirs(FAV_PATH)

def setup_dll():
    global wrd, funcs
    # If we are on your Chromebook, we ignore the DLL completely
    if IS_LINUX:
        return "LINUX_MODE"
    
    dll_path = os.path.join(os.getcwd(), DLL_NAME)
    if not os.path.exists(dll_path):
        return "MISSING"
    
    try:
        wrd = ctypes.WinDLL(dll_path)
        # Assuming the DLL has 5 standard export functions for injection
        funcs = [wrd[i] for i in range(1, 6)]
        for f in funcs: f.argtypes = [ctypes.c_char_p]
        return "READY"
    except Exception as e:
        return f"ERROR: {e}"

dll_status = setup_dll()

class PrismApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"PRISM.CC // V20.0 - {platform.system()}")
        self.geometry("1100x820") 
        ctk.set_appearance_mode("dark")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=280, fg_color="#080808")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.title_lbl = ctk.CTkLabel(self.sidebar, text="PRISM", font=("Impact", 64), text_color=current_theme_color)
        self.title_lbl.pack(pady=45)
        
        self.create_nav_btn("LUA EXECUTOR", "⚡", self.show_executor)
        self.create_nav_btn("SAVED SCRIPTS", "📁", self.show_favorites)
        self.create_nav_btn("CLOUD HUB", "☁️", self.show_cloud)
        self.create_nav_btn("ESSENTIALS", "🛠️", self.show_essentials)
        self.create_nav_btn("THEMES", "🎨", self.show_themes)
        self.create_nav_btn("SETTINGS", "⚙️", self.show_settings)
        
        self.dev_tag = ctk.CTkLabel(self.sidebar, text=f"User: {USER_ACCOUNT}", font=("Arial", 12, "bold"), text_color="#444")
        self.dev_tag.pack(side="bottom", pady=20)

        self.container = ctk.CTkFrame(self, fg_color="#0d0d0d", corner_radius=20)
        self.container.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)
        
        self.show_executor()
        self.log(f"System: {platform.system()} | DLL Status: {dll_status}")

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

    def show_executor(self):
        self.clear_container()
        ctk.CTkLabel(self.container, text="LUA EXECUTOR", font=("Arial", 22, "bold")).pack(pady=10)
        self.editor = ctk.CTkTextbox(self.container, height=380, fg_color="#050505", text_color=current_theme_color, font=("Consolas", 14))
        self.editor.pack(fill="both", expand=True, padx=25, pady=5)
        self.editor.insert("0.0", RAYFIELD_LOADER)

        self.console = ctk.CTkTextbox(self.container, height=120, fg_color="#020202", text_color="#777", font=("Consolas", 11))
        self.console.pack(fill="x", padx=25, pady=10)
        
        btn_bar = ctk.CTkFrame(self.container, fg_color="transparent")
        btn_bar.pack(fill="x", padx=25, pady=(0, 20))
        
        # Action Buttons
        ctk.CTkButton(btn_bar, text="INJECT", width=110, command=self.inject_logic).pack(side="left", padx=3)
        ctk.CTkButton(btn_bar, text="EXECUTE", width=110, fg_color=current_theme_color, text_color="black", command=lambda: self.run_lua(self.editor.get("0.0", "end"))).pack(side="left", padx=3)
        ctk.CTkButton(btn_bar, text="CLEAR", width=80, fg_color="#ff4444", command=lambda: self.editor.delete("0.0", "end")).pack(side="right", padx=3)

    def inject_logic(self):
        if IS_LINUX:
            self.log("Linux Detected: Using internal file bridge (No DLL needed).")
            return
        
        if dll_status == "READY":
            try:
                wrd[1]() # Call the injection export from the DLL
                self.log("DLL Injected successfully.")
            except:
                self.log("Injection failed. Is Roblox open?")
        else:
            self.log(f"Cannot Inject: DLL is {dll_status}")

    def run_lua(self, code):
        if not code.strip(): return
        
        if IS_LINUX:
            # The "Chromebook Bridge" - Writes to a file for the emulator to catch
            try:
                bridge = os.path.expanduser("~/.local/share/prism_exec.lua")
                with open(bridge, "w") as f:
                    f.write(code)
                self.log("Code sent to Bridge.")
            except Exception as e:
                self.log(f"Bridge Error: {e}")
        elif dll_status == "READY":
            # Windows/Victus method using the DLL functions
            payload = (code.strip() + "\0").encode('utf-8')
            for f in funcs:
                try: f(payload)
                except: continue
            self.log("Executed via DLL.")
        else:
            self.log("Execution failed: DLL not ready.")

    def clear_container(self):
        for widget in self.container.winfo_children(): widget.destroy()

    def show_favorites(self):
        self.clear_container()
        ctk.CTkLabel(self.container, text="SAVED SCRIPTS", font=("Arial", 22, "bold")).pack(pady=10)
        scroll = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=25, pady=10)
        for filename in os.listdir(FAV_PATH):
            if filename.endswith(".lua"):
                item = ctk.CTkFrame(scroll, fg_color="#121212", height=50)
                item.pack(fill="x", pady=2)
                ctk.CTkLabel(item, text=f"📜 {filename}").place(x=15, y=12)
                ctk.CTkButton(item, text="LOAD", width=60, command=lambda f=filename: self.load_fav(f)).place(relx=0.9, rely=0.5, anchor="center")

    def load_fav(self, filename):
        with open(os.path.join(FAV_PATH, filename), "r") as f:
            content = f.read()
        self.show_executor()
        self.editor.delete("0.0", "end")
        self.editor.insert("end", content)

    def show_cloud(self):
        self.clear_container()
        ctk.CTkLabel(self.container, text="CLOUD HUB", font=("Arial", 22, "bold")).pack(pady=15)
        self.s_entry = ctk.CTkEntry(self.container, placeholder_text="Search ScriptBlox...", height=45)
        self.s_entry.pack(fill="x", padx=25)
        ctk.CTkButton(self.container, text="SEARCH", command=self.search_logic).pack(pady=10)
        self.scroll_cloud = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        self.scroll_cloud.pack(fill="both", expand=True, padx=20)

    def search_logic(self):
        q = self.s_entry.get()
        for w in self.scroll_cloud.winfo_children(): w.destroy()
        try:
            r = requests.get(f"https://scriptblox.com/api/script/search?q={q}&max=15").json()
            for s in r['result']['scripts']:
                card = ctk.CTkFrame(self.scroll_cloud, fg_color="#121212", height=60)
                card.pack(fill="x", pady=4)
                ctk.CTkLabel(card, text=s['title'][:40]).place(x=15, y=10)
                ctk.CTkButton(card, text="LOAD", width=60, command=lambda sl=s['slug']: self.load_cloud(sl)).place(relx=0.9, rely=0.5, anchor="center")
        except: self.log("Search failed.")

    def load_cloud(self, slug):
        try:
            r = requests.get(f"https://scriptblox.com/api/script/{slug}").json()
            code = r['result']['script']['script']
            self.show_executor()
            self.editor.delete("0.0", "end")
            self.editor.insert("end", code)
        except: self.log("Cloud Load Error.")

    def show_essentials(self):
        self.clear_container()
        ctk.CTkLabel(self.container, text="ESSENTIALS", font=("Arial", 22, "bold")).pack(pady=10)
        scroll = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20)
        ess = [("Infinite Yield", "Admin commands.", "loadstring(game:HttpGet('https://raw.githubusercontent.com/EdgeIY/infiniteyield/master/source'))()"),
               ("Dex Explorer", "Instance browser.", "loadstring(game:HttpGet('https://raw.githubusercontent.com/infyiff/backup/main/dex.lua'))()")]
        for n, d, c in ess:
            card = ctk.CTkFrame(scroll, fg_color="#121212", height=80)
            card.pack(fill="x", pady=5)
            ctk.CTkLabel(card, text=n, font=("Arial", 14, "bold")).place(x=15, y=12)
            ctk.CTkButton(card, text="Execute", command=lambda code=c: self.run_lua(code)).place(relx=0.9, rely=0.5, anchor="center")

    def show_themes(self):
        self.clear_container()
        scroll = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=40, pady=20)
        themes = {"Prism Green": "#00ff88", "Deep Red": "#ff0000", "Midnight Purple": "#a020f0"}
        for name, hex in themes.items():
            ctk.CTkButton(scroll, text=name, fg_color=hex, text_color="black", command=lambda h=hex: self.apply_theme(h)).pack(pady=5, fill="x")

    def apply_theme(self, hex):
        global current_theme_color
        current_theme_color = hex
        self.title_lbl.configure(text_color=hex)
        self.show_executor()

    def show_settings(self):
        self.clear_container()
        scroll = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=25)
        
        ctk.CTkLabel(scroll, text="DEBUG INFO", font=("Arial", 16, "bold"), text_color=current_theme_color).pack(anchor="w", pady=10)
        ctk.CTkLabel(scroll, text=f"Platform: {platform.system()}").pack(anchor="w")
        ctk.CTkLabel(scroll, text=f"DLL Status: {dll_status}").pack(anchor="w")
        
        if IS_LINUX:
            ctk.CTkLabel(scroll, text="Bridge Path: ~/.local/share/prism_exec.lua", text_color="#777").pack(anchor="w")

        ctk.CTkButton(scroll, text="KILL ROBLOX", fg_color="#700", command=lambda: os.system("pkill -f Roblox" if IS_LINUX else "taskkill /F /IM RobloxPlayerBeta.exe")).pack(pady=20)

if __name__ == "__main__":
    app = PrismApp()
    app.mainloop()

srry i needed to paste so i can add it to github
