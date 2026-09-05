import customtkinter as CTk
from tkinter import messagebox as mb
from lib import SocketHelper
from threading import Thread
import socket


class SocketGUI(CTk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sockets | Python App")
        self.geometry("380x550")
        self.poppins = CTk.CTkFont(family="Poppins")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.socket = SocketHelper()
        self.is_start = False
        self.is_receiving = False

        self.sender_ip_label = CTk.CTkLabel(
            self, text="Sender IP", font=(self.poppins, 12, "bold")
        )
        self.sender_ip_label.place(x=80, y=20, anchor="n")
        self.sender_ip_field = CTk.CTkEntry(
            self,
            placeholder_text="Enter IP",
            corner_radius=5,
            width=200,
            height=30,
            font=(self.poppins, 12, "bold"),
        )
        self.sender_ip_field.place(x=230, y=20, anchor="n")

        self.sender_port_label = CTk.CTkLabel(
            self, text="Sender PORT", font=(self.poppins, 12, "bold")
        )
        self.sender_port_label.place(x=80, y=70, anchor="n")
        self.sender_port_field = CTk.CTkEntry(
            self,
            placeholder_text="Enter PORT",
            corner_radius=5,
            width=200,
            height=30,
            font=(self.poppins, 12, "bold"),
        )
        self.sender_port_field.place(x=230, y=70, anchor="n")
        self.getLocalIP()

        self.receiver_ip_label = CTk.CTkLabel(
            self, text="Receiver IP", font=(self.poppins, 12, "bold")
        )
        self.receiver_ip_label.place(x=80, y=120, anchor="n")
        self.receiver_ip_field = CTk.CTkEntry(
            self,
            placeholder_text="ex. 192.168.100",
            corner_radius=5,
            width=200,
            height=30,
            font=(self.poppins, 12),
        )
        self.receiver_ip_field.place(x=230, y=120, anchor="n")

        self.receiver_port_label = CTk.CTkLabel(
            self, text="Receiver PORT", font=(self.poppins, 12, "bold")
        )
        self.receiver_port_label.place(x=80, y=170, anchor="n")
        self.receiver_port_field = CTk.CTkEntry(
            self,
            placeholder_text="ex. 5000",
            corner_radius=5,
            width=200,
            height=30,
            font=(self.poppins, 12),
        )
        self.receiver_port_field.place(x=230, y=170, anchor="n")
        self.setDummyIPAndPort()

        self.start_btn = CTk.CTkButton(
            self,
            text="Start",
            border_width=0,
            corner_radius=5,
            font=(self.poppins, 12),
            text_color="white",
            height=30,
            width=100,
            command=self.startStopServer,
        )
        self.start_btn.place(x=120, y=230, anchor="n")

        self.send_btn = CTk.CTkButton(
            self,
            text="Send",
            border_width=0,
            corner_radius=5,
            font=(self.poppins, 12),
            text_color="white",
            height=30,
            width=100,
            command=self.sendMessage,  #
        )
        self.send_btn.place(x=250, y=230, anchor="n")

        self.send_msg_label = CTk.CTkLabel(
            self, text="Send Message", font=(self.poppins, 12, "bold")
        )
        self.send_msg_label.place(x=80, y=295, anchor="n")
        self.send_msg_field = CTk.CTkEntry(
            self,
            placeholder_text="Enter Message",
            corner_radius=5,
            width=200,
            height=30,
            font=(self.poppins, 12),
        )
        self.send_msg_field.place(x=230, y=295, anchor="n")

        self.receiver_textbox = CTk.CTkTextbox(
            self, font=(self.poppins, 12), width=300, height=180, corner_radius=5
        )
        self.receiver_textbox.place(x=40, y=350)

    def startStopServer(self):
        if self.is_start:
            self.start_btn.configure(text="Start")
            self.is_start = False
            self.is_receiving = False  # Stop receiving loop
            self.sender_ip_field.configure(state="normal")
            self.sender_port_field.configure(state="normal")
        else:
            self.start_btn.configure(text="Stop")
            self.is_start = True
            self.is_receiving = True
            self.sender_ip_field.configure(state="disabled")
            self.sender_port_field.configure(state="disabled")
            receive_thread = Thread(target=self.receiveMessage, daemon=True)
            receive_thread.start()

    def receiveMessage(self):
        try:
            IP = self.receiver_ip_field.get()
            PORT = int(self.receiver_port_field.get())

            while self.is_receiving:
                try:
                    res = self.socket.UDPReceive(IP, PORT)
                    if res:
                        MSG, sender_ip, sender_port = res
                        txt = f"Server: {MSG} from {sender_ip}:{sender_port}\n"
                        mb(title="Message", message=txt)
                        self.receiver_textbox.insert("end", txt)
                        self.serverPlaceholder("Server:", "red")
                        self.send_msg_field.delete(0, "end")
                except socket.timeout:
                    continue
                except socket.error as e:
                    mb.showerror(title="Error", message=f"Error receiving message: {e}")
                    break

        except Exception as e:
            mb.showerror(title="Error", message=f"Server error: {e}")
        finally:
            self.is_receiving = False

    def sendMessage(self):
        TARGET_IP = self.sender_ip_field.get()
        TARGET_PORT = int(self.sender_port_field.get())
        MSG = self.send_msg_field.get()

        if not TARGET_IP or not TARGET_PORT or not MSG:
            mb.showwarning("Warning", "Please fill in all fields before sending.")
            return
        try:
            self.socket.UDPSend(MSG, TARGET_IP, TARGET_PORT)
        except Exception as e:
            mb.showerror(title="Error", message=f"Error sending message: {e}")

    def getLocalIP(self):
        LOCAL_IP = self.socket.get_local_ip_address()
        self.sender_ip_field.insert(0, LOCAL_IP)
        self.sender_port_field.insert(0, 60001)

    def serverPlaceholder(self, word, tag):
        self.receiver_textbox.tag_config(tag, foreground="red")
        start = "1.0"

        while True:
            pos = self.receiver_textbox.search(word, start, stopindex="end")
            if not pos:
                break
            end = f"{pos}+{len(word)}c"
            self.receiver_textbox.tag_add(tag, pos, end)
            start = end

    def setDummyIPAndPort(self):
        ip = "192.168.100.127"
        port = 6000
        self.receiver_ip_field.insert(0, ip)
        self.receiver_port_field.insert(0, port)


app = SocketGUI()
app.mainloop()
