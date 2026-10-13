"""NeuroFriend 2.0.0 — local desktop AI companion for Ollama."""
from __future__ import annotations
import json, os, queue, shutil, sqlite3, sys, threading, urllib.error, urllib.request
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

APP_NAME, APP_VERSION, DEFAULT_MODEL = "NeuroFriend", "2.0.0", "qwen2.5:3b"
DEFAULT_ENDPOINT = "http://127.0.0.1:11434"
BG, SIDEBAR, PANEL, CARD = "#0b1020", "#10182b", "#111d33", "#182640"
HOVER, TEXT, MUTED, ACCENT = "#223453", "#edf3ff", "#93a3c2", "#8b7cff"
GREEN, RED, BORDER, USER_BUBBLE = "#5de0b0", "#ff8494", "#293956", "#26365b"
STRINGS = {
"ru":{"subtitle":"Твой локальный ИИ-помощник","new":"+ Новый чат","history":"ТВОИ ЧАТЫ","settings":"Настройки","ready":"Готов к общению","working":"NeuroFriend думает…","placeholder":"Напиши сообщение…","send":"Отправить","stop":"Остановить","welcome":"Привет! Я NeuroFriend ✨","welcome_body":"Я работаю через Ollama прямо на твоём компьютере. Можно общаться, разбирать сложные темы, учиться и писать код.","tip":"Для начала установи Ollama и скачай модель:","model":"Модель","language":"Язык интерфейса","endpoint":"Адрес Ollama","save":"Сохранить","check":"Проверить соединение","connected":"Подключение работает","offline":"Ollama не отвечает. Проверь, что приложение запущено.","saved":"Настройки сохранены","rename":"Переименовать","delete":"Удалить чат","delete_q":"Удалить этот чат и все его сообщения?","you":"Ты","assistant":"NeuroFriend","error":"Не удалось получить ответ","empty":"Новый чат","model_missing":"Модель не найдена. Скачай её командой: ollama pull {model}","request_error":"Не удалось связаться с Ollama. Проверь адрес и запуск сервиса.\n\nПодробности: {detail}","thinking":"Думаю…","cancelled":"Генерация остановлена.","copied":"Ответ скопирован","local":"ЛОКАЛЬНЫЙ ИИ","input_hint":"Enter — отправить   ·   Shift+Enter — новая строка","rename_prompt":"Название чата","no_messages":"Пока пусто. Напиши первое сообщение ниже.","endpoint_hint":"Обычно: http://127.0.0.1:11434","theme_note":"История хранится на этом компьютере.","check_running":"Проверяю…","no_answer":"Модель вернула пустой ответ."},
"uk":{"subtitle":"Твій локальний ШІ-помічник","new":"+ Новий чат","history":"ТВОЇ ЧАТИ","settings":"Налаштування","ready":"Готовий до спілкування","working":"NeuroFriend думає…","placeholder":"Напиши повідомлення…","send":"Надіслати","stop":"Зупинити","welcome":"Привіт! Я NeuroFriend ✨","welcome_body":"Я працюю через Ollama прямо на твоєму комп’ютері. Можемо спілкуватися, вчитися, розбирати складні теми та писати код.","tip":"Спочатку встанови Ollama та завантаж модель:","model":"Модель","language":"Мова інтерфейсу","endpoint":"Адреса Ollama","save":"Зберегти","check":"Перевірити з’єднання","connected":"З’єднання працює","offline":"Ollama не відповідає. Перевір, чи запущено Ollama.","saved":"Налаштування збережено","rename":"Перейменувати","delete":"Видалити чат","delete_q":"Видалити цей чат і всі його повідомлення?","you":"Ти","assistant":"NeuroFriend","error":"Не вдалося отримати відповідь","empty":"Новий чат","model_missing":"Модель не знайдена. Завантаж її командою: ollama pull {model}","request_error":"Не вдалося зв’язатися з Ollama. Перевір адресу та сервіс.\n\nДеталі: {detail}","thinking":"Думаю…","cancelled":"Генерацію зупинено.","copied":"Відповідь скопійовано","local":"ЛОКАЛЬНИЙ ШІ","input_hint":"Enter — надіслати   ·   Shift+Enter — новий рядок","rename_prompt":"Назва чату","no_messages":"Поки порожньо. Напиши перше повідомлення нижче.","endpoint_hint":"Зазвичай: http://127.0.0.1:11434","theme_note":"Історія зберігається на цьому комп’ютері.","check_running":"Перевіряю…","no_answer":"Модель повернула порожню відповідь."},
"en":{"subtitle":"Your local AI companion","new":"+ New chat","history":"YOUR CHATS","settings":"Settings","ready":"Ready to chat","working":"NeuroFriend is thinking…","placeholder":"Message NeuroFriend…","send":"Send","stop":"Stop","welcome":"Hey! I'm NeuroFriend ✨","welcome_body":"I run through Ollama right on your computer. Chat with me, explore tricky topics, study, brainstorm, or work on code.","tip":"First install Ollama and download a model:","model":"Model","language":"Interface language","endpoint":"Ollama address","save":"Save settings","check":"Check connection","connected":"Connection is working","offline":"Ollama is not responding. Make sure it is running.","saved":"Settings saved","rename":"Rename chat","delete":"Delete chat","delete_q":"Delete this chat and all its messages?","you":"You","assistant":"NeuroFriend","error":"Could not get a response","empty":"New chat","model_missing":"Model not found. Download it with: ollama pull {model}","request_error":"Could not connect to Ollama. Check the address and service.\n\nDetails: {detail}","thinking":"Thinking…","cancelled":"Generation stopped.","copied":"Response copied","local":"LOCAL AI","input_hint":"Enter — send   ·   Shift+Enter — new line","rename_prompt":"Chat title","no_messages":"Nothing here yet. Send your first message below.","endpoint_hint":"Usually: http://127.0.0.1:11434","theme_note":"Chat history is stored on this computer.","check_running":"Checking…","no_answer":"The model returned an empty response."}
}

def data_directory():
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    target = base / APP_NAME
    target.mkdir(parents=True, exist_ok=True)
    legacy, destination = Path.cwd() / "neurofriend.db", target / "neurofriend.db"
    if legacy.exists() and not destination.exists():
        try: shutil.copy2(legacy, destination)
        except OSError: pass
    return target

DB_PATH = data_directory() / "neurofriend.db"

class Store:
    """SQLite access stays on the Tk main thread."""
    def __init__(self, path=DB_PATH):
        self.db = sqlite3.connect(str(path), timeout=10)
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.execute("CREATE TABLE IF NOT EXISTS chats(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,created_at TEXT NOT NULL,updated_at TEXT NOT NULL)")
        self.db.execute("CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY AUTOINCREMENT,chat_id INTEGER NOT NULL,role TEXT NOT NULL CHECK(role IN ('user','assistant','system')),content TEXT NOT NULL,created_at TEXT NOT NULL,FOREIGN KEY(chat_id) REFERENCES chats(id) ON DELETE CASCADE)")
        self.db.execute("CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY,value TEXT NOT NULL)")
        self.db.commit()
    def get(self,key,default):
        row=self.db.execute("SELECT value FROM settings WHERE key=?",(key,)).fetchone()
        return row[0] if row else default
    def set(self,key,value):
        self.db.execute("INSERT OR REPLACE INTO settings(key,value) VALUES(?,?)",(key,value)); self.db.commit()
    def chats(self):
        return self.db.execute("SELECT id,title,updated_at FROM chats ORDER BY updated_at DESC").fetchall()
    def create_chat(self,title):
        now=datetime.now().isoformat(timespec="seconds")
        cur=self.db.execute("INSERT INTO chats(title,created_at,updated_at) VALUES(?,?,?)",(title,now,now)); self.db.commit(); return cur.lastrowid
    def rename(self,cid,title):
        self.db.execute("UPDATE chats SET title=?,updated_at=? WHERE id=?",(title,datetime.now().isoformat(timespec="seconds"),cid)); self.db.commit()
    def delete(self,cid):
        self.db.execute("DELETE FROM messages WHERE chat_id=?",(cid,)); self.db.execute("DELETE FROM chats WHERE id=?",(cid,)); self.db.commit()
    def messages(self,cid):
        return self.db.execute("SELECT role,content FROM messages WHERE chat_id=? ORDER BY id",(cid,)).fetchall()
    def add_message(self,cid,role,content):
        now=datetime.now().isoformat(timespec="seconds")
        self.db.execute("INSERT INTO messages(chat_id,role,content,created_at) VALUES(?,?,?,?)",(cid,role,content,now))
        self.db.execute("UPDATE chats SET updated_at=? WHERE id=?",(now,cid)); self.db.commit()
    def close(self): self.db.close()

class NeuroFriendApp:
    def __init__(self,root):
        self.root=root; self.store=Store(); self.lang=self.store.get("language","ru")
        if self.lang not in STRINGS: self.lang="ru"
        self.model=self.store.get("model",DEFAULT_MODEL); self.endpoint=self.store.get("endpoint",DEFAULT_ENDPOINT).rstrip("/")
        self.current_chat=None; self.busy=False; self.cancel_event=threading.Event(); self.events=queue.Queue(); self.active_response=None
        self.root.title(f"{APP_NAME} {APP_VERSION}"); self.root.geometry("1240x820"); self.root.minsize(850,580); self.root.configure(bg=BG)
        self.root.protocol("WM_DELETE_WINDOW",self.close); self._build()
        chats=self.store.chats()
        self.open_chat(chats[0][0]) if chats else self.new_chat()
        self._set_status(self.t("ready")); self._poll_events()
    def t(self,key): return STRINGS.get(self.lang,STRINGS["ru"]).get(key,STRINGS["ru"].get(key,key))
    def _label(self,parent,text,*,bg=BG,fg=TEXT,size=10,bold=False,**kw):
        return tk.Label(parent,text=text,bg=bg,fg=fg,font=("Segoe UI",size,"bold" if bold else "normal"),**kw)
    def _button(self,parent,text,command,primary=False,**kw):
        return tk.Button(parent,text=text,command=command,bg=ACCENT if primary else CARD,fg="white" if primary else TEXT,
          activebackground="#a69aff" if primary else HOVER,activeforeground="white",relief="flat",bd=0,cursor="hand2",
          font=("Segoe UI",10,"bold" if primary else "normal"),padx=12,pady=8,highlightthickness=0,**kw)
    def _build(self):
        self.root.grid_rowconfigure(0,weight=1); self.root.grid_columnconfigure(1,weight=1)
        self.sidebar=tk.Frame(self.root,bg=SIDEBAR,width=264); self.sidebar.grid(row=0,column=0,sticky="ns"); self.sidebar.grid_propagate(False)
        brand=tk.Frame(self.sidebar,bg=SIDEBAR); brand.pack(fill="x",padx=19,pady=(22,5))
        logo=tk.Canvas(brand,width=36,height=36,bg=SIDEBAR,highlightthickness=0); logo.pack(side="left")
        logo.create_oval(2,2,34,34,fill=ACCENT,outline=""); logo.create_text(18,18,text="✦",fill="white",font=("Segoe UI",17,"bold"))
        self.brand_title=self._label(brand,"NeuroFriend",bg=SIDEBAR,size=16,bold=True); self.brand_title.pack(side="left",padx=9)
        self.subtitle=self._label(self.sidebar,self.t("subtitle"),bg=SIDEBAR,fg=MUTED,size=9); self.subtitle.pack(anchor="w",padx=21,pady=(0,19))
        self.new_btn=self._button(self.sidebar,self.t("new"),self.new_chat,True); self.new_btn.pack(fill="x",padx=14,pady=(0,23),ipady=5)
        self.history_label=self._label(self.sidebar,self.t("history"),bg=SIDEBAR,fg="#7485a6",size=8,bold=True); self.history_label.pack(anchor="w",padx=20,pady=(0,8))
        self.chat_list=tk.Frame(self.sidebar,bg=SIDEBAR); self.chat_list.pack(fill="both",expand=True,padx=9)
        bottom=tk.Frame(self.sidebar,bg=SIDEBAR); bottom.pack(fill="x",padx=14,pady=15)
        self.settings_btn=self._button(bottom,"⚙  "+self.t("settings"),self.open_settings); self.settings_btn.pack(fill="x",ipady=3)
        self.local_label=self._label(bottom,"●  "+self.t("local"),bg=SIDEBAR,fg=GREEN,size=8,bold=True); self.local_label.pack(anchor="w",padx=5,pady=(13,0))
        self.version_label=self._label(bottom,"v"+APP_VERSION,bg=SIDEBAR,fg="#657594",size=8); self.version_label.pack(anchor="w",padx=5,pady=(4,0))
        self.main=tk.Frame(self.root,bg=BG); self.main.grid(row=0,column=1,sticky="nsew"); self.main.grid_rowconfigure(1,weight=1); self.main.grid_columnconfigure(0,weight=1)
        header=tk.Frame(self.main,bg=BG); header.grid(row=0,column=0,sticky="ew",padx=28,pady=(21,13))
        self.header_title=self._label(header,"NeuroFriend",bg=BG,size=16,bold=True); self.header_title.pack(side="left")
        self.connection_dot=self._label(header,"●",bg=BG,fg=MUTED,size=10); self.connection_dot.pack(side="left",padx=(13,5))
        self.status_text=self._label(header,self.t("ready"),bg=BG,fg=MUTED,size=9); self.status_text.pack(side="left")
        self.model_badge=self._label(header,"  "+self.model+"  ",bg=PANEL,fg=MUTED,size=9); self.model_badge.pack(side="right",ipady=5)
        area=tk.Frame(self.main,bg=BG); area.grid(row=1,column=0,sticky="nsew",padx=(22,12)); area.grid_rowconfigure(0,weight=1); area.grid_columnconfigure(0,weight=1)
        self.canvas=tk.Canvas(area,bg=BG,highlightthickness=0,bd=0); self.canvas.grid(row=0,column=0,sticky="nsew")
        scroll=ttk.Scrollbar(area,orient="vertical",command=self.canvas.yview); scroll.grid(row=0,column=1,sticky="ns"); self.canvas.configure(yscrollcommand=scroll.set)
        self.messages_frame=tk.Frame(self.canvas,bg=BG); self.canvas_window=self.canvas.create_window((0,0),window=self.messages_frame,anchor="nw")
        self.messages_frame.bind("<Configure>",self._on_frame_configure); self.canvas.bind("<Configure>",self._on_canvas_configure); self.canvas.bind_all("<MouseWheel>",self._on_mousewheel)
        wrap=tk.Frame(self.main,bg=BG); wrap.grid(row=2,column=0,sticky="ew",padx=28,pady=(14,8)); wrap.grid_columnconfigure(0,weight=1)
        self.composer=tk.Frame(wrap,bg=PANEL,highlightbackground=BORDER,highlightthickness=1); self.composer.grid(row=0,column=0,sticky="ew"); self.composer.grid_columnconfigure(0,weight=1)
        self.entry=tk.Text(self.composer,height=3,wrap="word",bg=PANEL,fg=TEXT,insertbackground=TEXT,selectbackground=ACCENT,relief="flat",bd=0,font=("Segoe UI",11),padx=15,pady=13,undo=True,maxundo=30)
        self.entry.grid(row=0,column=0,sticky="nsew"); self.entry.bind("<Return>",self._enter_send); self.entry.bind("<Shift-Return>",lambda _e:None)
        controls=tk.Frame(self.composer,bg=PANEL); controls.grid(row=0,column=1,sticky="se",padx=10,pady=10)
        self.stop_btn=self._button(controls,self.t("stop"),self.stop_generation); self.send_btn=self._button(controls,self.t("send")+"  ➤",self.send_message,True); self.send_btn.pack()
        self.input_hint=self._label(wrap,self.t("input_hint"),bg=BG,fg="#657594",size=8); self.input_hint.grid(row=1,column=0,sticky="w",pady=(6,0))
        self.footer=self._label(self.main,self.t("theme_note"),bg=BG,fg="#657594",size=8); self.footer.grid(row=3,column=0,sticky="w",padx=30,pady=(0,12))
    def _on_frame_configure(self,_e=None): self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    def _on_canvas_configure(self,e): self.canvas.itemconfigure(self.canvas_window,width=e.width)
    def _on_mousewheel(self,e):
        try: self.canvas.yview_scroll(int(-e.delta/120),"units")
        except (tk.TclError,AttributeError): pass
    def _scroll_bottom(self):
        try: self.root.update_idletasks(); self.canvas.configure(scrollregion=self.canvas.bbox("all")); self.canvas.yview_moveto(1.0)
        except tk.TclError: pass
    def _set_status(self,text,connected=None):
        self.status_text.configure(text=text); self.connection_dot.configure(fg=GREEN if connected is True else RED if connected is False else MUTED)
    def _refresh_sidebar(self):
        for child in self.chat_list.winfo_children(): child.destroy()
        for cid,title,_ in self.store.chats():
            selected=cid==self.current_chat
            btn=tk.Button(self.chat_list,text=("▸  " if selected else "   ")+title[:26],anchor="w",command=lambda x=cid:self.open_chat(x),
              bg=CARD if selected else SIDEBAR,fg=TEXT if selected else MUTED,activebackground=HOVER,activeforeground=TEXT,
              relief="flat",bd=0,font=("Segoe UI",10),padx=10,pady=9,cursor="hand2",highlightthickness=0)
            btn.pack(fill="x",pady=2); btn.bind("<Button-3>",lambda e,x=cid:self._chat_menu(e,x))
    def _chat_menu(self,e,cid):
        menu=tk.Menu(self.root,tearoff=0,bg=PANEL,fg=TEXT,activebackground=ACCENT,activeforeground="white")
        menu.add_command(label=self.t("rename"),command=lambda:self.rename_chat(cid)); menu.add_command(label=self.t("delete"),command=lambda:self.delete_chat(cid))
        try: menu.tk_popup(e.x_root,e.y_root)
        finally: menu.grab_release()
    def new_chat(self):
        if self.busy: self.stop_generation()
        self.current_chat=self.store.create_chat(self.t("empty")); self._refresh_sidebar(); self._render_messages(); self._set_status(self.t("ready")); self.entry.focus_set()
    def open_chat(self,cid):
        if self.busy and cid!=self.current_chat: self.stop_generation()
        self.current_chat=cid; chat=next((c for c in self.store.chats() if c[0]==cid),None)
        self.header_title.configure(text=chat[1] if chat else "NeuroFriend"); self._refresh_sidebar(); self._render_messages(); self.entry.focus_set()
    def rename_chat(self,cid):
        current=next((c[1] for c in self.store.chats() if c[0]==cid),"")
        title=simpledialog.askstring(self.t("rename"),self.t("rename_prompt"),initialvalue=current,parent=self.root)
        if title and title.strip():
            self.store.rename(cid,title.strip()[:60]); self._refresh_sidebar()
            if cid==self.current_chat: self.header_title.configure(text=title.strip()[:60])
    def delete_chat(self,cid):
        if not messagebox.askyesno(self.t("delete"),self.t("delete_q"),parent=self.root): return
        if cid==self.current_chat and self.busy: self.stop_generation()
        self.store.delete(cid); chats=self.store.chats()
        self.current_chat=self.store.create_chat(self.t("empty")) if not chats else (chats[0][0] if cid==self.current_chat else self.current_chat)
        self.open_chat(self.current_chat)
    def _render_messages(self):
        for child in self.messages_frame.winfo_children(): child.destroy()
        if not self.current_chat or not self.store.messages(self.current_chat):
            outer=tk.Frame(self.messages_frame,bg=BG); outer.pack(fill="both",expand=True,pady=(65,20))
            logo=tk.Canvas(outer,width=68,height=68,bg=BG,highlightthickness=0); logo.pack(); logo.create_oval(4,4,64,64,fill=ACCENT,outline=""); logo.create_text(34,34,text="✦",fill="white",font=("Segoe UI",28,"bold"))
            self._label(outer,self.t("welcome"),bg=BG,size=20,bold=True).pack(pady=(17,9))
            self._label(outer,self.t("welcome_body"),bg=BG,fg=MUTED,size=10,justify="center",wraplength=560).pack(padx=35,pady=(0,18))
            tip=tk.Frame(outer,bg=PANEL,highlightbackground=BORDER,highlightthickness=1); tip.pack(padx=20,pady=5)
            self._label(tip,self.t("tip"),bg=PANEL,fg=MUTED,size=9).pack(anchor="w",padx=15,pady=(12,4))
            self._label(tip,"ollama pull "+self.model,bg=PANEL,fg=GREEN,size=10,bold=True).pack(anchor="w",padx=15,pady=(0,12))
        else:
            for role,content in self.store.messages(self.current_chat): self._add_message_widget(role,content,scroll=False)
        self.root.after(40,self._scroll_bottom)
    def _add_message_widget(self,role,content,scroll=True):
        user=role=="user"; row=tk.Frame(self.messages_frame,bg=BG); row.pack(fill="x",padx=10,pady=8)
        color=USER_BUBBLE if user else PANEL; card=tk.Frame(row,bg=color,highlightbackground=BORDER if not user else USER_BUBBLE,highlightthickness=1)
        card.pack(anchor="e" if user else "w",fill="x" if not user else "none")
        max_width=max(300,min(820,self.canvas.winfo_width()-100))
        head=tk.Frame(card,bg=color); head.pack(fill="x",padx=14,pady=(10,2))
        self._label(head,self.t("you") if user else self.t("assistant"),bg=color,fg="#c3b9ff" if user else GREEN,size=9,bold=True).pack(side="left")
        body=self._label(card,content,bg=color,fg=TEXT,size=10,justify="left",anchor="w",wraplength=max_width-45)
        body.pack(fill="x",padx=14,pady=(2,12))
        if not user:
            actions=tk.Frame(card,bg=color); actions.pack(anchor="w",padx=10,pady=(0,7))
            self._button(actions,"⧉",lambda value=content:self.copy_text(value)).pack(side="left")
        if scroll: self.root.after(35,self._scroll_bottom)
        return body
    def _append_stream_text(self,body,value):
        try: body.configure(text=value); self._scroll_bottom()
        except tk.TclError: pass
    def _enter_send(self,e):
        if e.state&0x1: return
        self.send_message(); return "break"
    def send_message(self):
        if self.busy: return
        text=self.entry.get("1.0","end-1c").strip()
        if not text: return
        if not self.current_chat: self.current_chat=self.store.create_chat(self.t("empty"))
        old=self.store.messages(self.current_chat); self.store.add_message(self.current_chat,"user",text)
        if not old: self.store.rename(self.current_chat," ".join(text.split())[:36] or self.t("empty"))
        cid=self.current_chat; self.entry.delete("1.0","end"); self._refresh_sidebar()
        self.header_title.configure(text=next((c[1] for c in self.store.chats() if c[0]==cid),"NeuroFriend"))
        self._render_messages(); body=self._add_message_widget("assistant",self.t("thinking"))
        self.busy=True; self.cancel_event.clear(); self.send_btn.configure(state="disabled"); self.stop_btn.pack()
        self._set_status(self.t("working"))
        history=self.store.messages(cid); lang_name={"ru":"Russian","uk":"Ukrainian","en":"English"}.get(self.lang,"Russian")
        system=("You are NeuroFriend, a helpful and friendly AI companion. Be warm, respectful, honest and useful. "
                "Do not pretend to be human. Reply in the user's language; interface language: "+lang_name+
                ". Give clear, age-appropriate explanations. Use Markdown when helpful.")
        payload={"model":self.model,"messages":[{"role":"system","content":system}]+[{"role":r,"content":c} for r,c in history if r in ("user","assistant")],"stream":True,"options":{"temperature":0.7}}
        threading.Thread(target=self._request_worker,args=(payload,cid,body),daemon=True).start()
    def _request_worker(self,payload,cid,body):
        answer=""; response=None
        try:
            req=urllib.request.Request(self.endpoint+"/api/chat",data=json.dumps(payload).encode("utf-8"),headers={"Content-Type":"application/json"},method="POST")
            response=urllib.request.urlopen(req,timeout=300); self.active_response=response
            for line in response:
                if self.cancel_event.is_set(): break
                if not line.strip(): continue
                packet=json.loads(line.decode("utf-8"))
                if packet.get("error"): raise RuntimeError(packet["error"])
                answer+=packet.get("message",{}).get("content","")
                if answer: self.events.put(("stream",cid,body,answer))
                if packet.get("done"): break
            self.events.put(("cancelled" if self.cancel_event.is_set() else "done",cid,body,answer.strip()))
        except urllib.error.HTTPError as exc:
            if self.cancel_event.is_set():
                self.events.put(("cancelled",cid,body,answer.strip()))
            else:
                detail=exc.read().decode("utf-8","replace")[:500]; self.events.put(("error",cid,body,detail))
        except Exception as exc:
            if self.cancel_event.is_set():
                self.events.put(("cancelled",cid,body,answer.strip()))
            else:
                self.events.put(("error",cid,body,str(exc)))
        finally:
            if response:
                try: response.close()
                except Exception: pass
            self.active_response=None
    def _poll_events(self):
        try:
            while True:
                kind,cid,body,value=self.events.get_nowait()
                if kind=="stream":
                    if cid==self.current_chat: self._append_stream_text(body,value)
                elif kind=="done":
                    if value: self.store.add_message(cid,"assistant",value)
                    self._append_stream_text(body,value or self.t("no_answer")); self._finish_generation(self.t("ready"),True)
                elif kind=="cancelled":
                    if value: self.store.add_message(cid,"assistant",value)
                    self._append_stream_text(body,value or self.t("cancelled")); self._finish_generation(self.t("ready"),None)
                elif kind=="error":
                    msg=self.t("model_missing").format(model=self.model) if "404" in value or "not found" in value.lower() else self.t("request_error").format(detail=value[:300])
                    self._append_stream_text(body,msg); self._finish_generation(self.t("error"),False)
        except queue.Empty: pass
        try: self.root.after(60,self._poll_events)
        except tk.TclError: pass
    def _finish_generation(self,status,connected):
        self.busy=False; self.active_response=None; self.send_btn.configure(state="normal"); self.stop_btn.pack_forget()
        self._set_status(status,connected); self._refresh_sidebar(); self._scroll_bottom()
    def stop_generation(self):
        if not self.busy: return
        self.cancel_event.set()
        if self.active_response:
            try: self.active_response.close()
            except Exception: pass
        self._set_status(self.t("cancelled"))
    def copy_text(self,text):
        self.root.clipboard_clear(); self.root.clipboard_append(text); self._set_status(self.t("copied"))
    def open_settings(self):
        win=tk.Toplevel(self.root); win.title(self.t("settings")); win.geometry("500x480"); win.minsize(500,480); win.configure(bg=BG); win.transient(self.root); win.grab_set()
        self._label(win,self.t("settings"),bg=BG,size=19,bold=True).pack(anchor="w",padx=26,pady=(24,20))
        self._label(win,self.t("language"),bg=BG,fg=MUTED,size=10).pack(anchor="w",padx=26)
        lang_var=tk.StringVar(value=self.lang); line=tk.Frame(win,bg=BG); line.pack(fill="x",padx=24,pady=(7,18))
        for code,label in [("ru","Русский"),("uk","Українська"),("en","English")]:
            tk.Radiobutton(line,text=label,value=code,variable=lang_var,bg=BG,fg=TEXT,selectcolor=CARD,activebackground=BG,activeforeground=TEXT,font=("Segoe UI",10)).pack(side="left",padx=(0,12))
        self._label(win,self.t("model"),bg=BG,fg=MUTED,size=10).pack(anchor="w",padx=26)
        model_var=tk.StringVar(value=self.model); model_entry=tk.Entry(win,textvariable=model_var,bg=PANEL,fg=TEXT,insertbackground=TEXT,relief="flat",font=("Segoe UI",11),bd=0)
        model_entry.pack(fill="x",padx=26,pady=(7,18),ipady=10)
        self._label(win,self.t("endpoint"),bg=BG,fg=MUTED,size=10).pack(anchor="w",padx=26)
        endpoint_var=tk.StringVar(value=self.endpoint); endpoint_entry=tk.Entry(win,textvariable=endpoint_var,bg=PANEL,fg=TEXT,insertbackground=TEXT,relief="flat",font=("Segoe UI",11),bd=0)
        endpoint_entry.pack(fill="x",padx=26,pady=(7,4),ipady=10)
        self._label(win,self.t("endpoint_hint"),bg=BG,fg="#657594",size=8).pack(anchor="w",padx=26)
        result=self._label(win,"",bg=BG,fg=GREEN,size=9); result.pack(anchor="w",padx=26,pady=(12,0))
        buttons=tk.Frame(win,bg=BG); buttons.pack(fill="x",padx=26,pady=22)
        def check():
            result.configure(text=self.t("check_running"),fg=MUTED); endpoint=endpoint_var.get().strip().rstrip("/")
            def worker():
                try:
                    with urllib.request.urlopen(endpoint+"/api/tags",timeout=4) as r: data=json.loads(r.read().decode("utf-8"))
                    names=[m.get("name","") for m in data.get("models",[])]
                    msg=self.t("connected")+(f" · {len(names)} models" if names else "")
                    self.root.after(0,lambda:result.configure(text=msg,fg=GREEN))
                except Exception: self.root.after(0,lambda:result.configure(text=self.t("offline"),fg=RED))
            threading.Thread(target=worker,daemon=True).start()
        def save():
            endpoint=endpoint_var.get().strip().rstrip("/")
            if not endpoint.startswith(("http://","https://")):
                messagebox.showerror(self.t("settings"),"URL must start with http:// or https://",parent=win); return
            self.lang=lang_var.get(); self.model=model_var.get().strip() or DEFAULT_MODEL; self.endpoint=endpoint
            self.store.set("language",self.lang); self.store.set("model",self.model); self.store.set("endpoint",self.endpoint)
            self._rebuild_ui_text(); win.destroy(); self._set_status(self.t("saved"))
        self._button(buttons,self.t("check"),check).pack(side="left"); self._button(buttons,self.t("save"),save,True).pack(side="right")
    def _rebuild_ui_text(self):
        self.subtitle.configure(text=self.t("subtitle")); self.new_btn.configure(text=self.t("new")); self.history_label.configure(text=self.t("history"))
        self.settings_btn.configure(text="⚙  "+self.t("settings")); self.local_label.configure(text="●  "+self.t("local"))
        self.model_badge.configure(text="  "+self.model+"  "); self.input_hint.configure(text=self.t("input_hint")); self.footer.configure(text=self.t("theme_note"))
        self.send_btn.configure(text=self.t("send")+"  ➤"); self._refresh_sidebar(); self._render_messages(); self._set_status(self.t("ready"))
    def close(self):
        self.cancel_event.set()
        try:
            if self.active_response: self.active_response.close()
        except Exception: pass
        try: self.store.close()
        except Exception: pass
        self.root.destroy()

def main():
    root=tk.Tk()
    try: root.tk.call("tk","scaling",1.1)
    except tk.TclError: pass
    NeuroFriendApp(root); root.mainloop()

if __name__=="__main__": main()
