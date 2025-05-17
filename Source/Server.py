from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
import hashlib
import os, random, string
import chardet
import sqlite3
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Nhập tên của bạn rồi bắt đầu chat!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def encrypt_challenge_RSA(message, public_key):
    rsa_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    encrypted_message = cipher.encrypt(message.encode())
    return encrypted_message

def generate_random_challenge(length=50):
    # Tạo chuỗi ngẫu nhiên có độ dài length
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def handle_client(client):  # Takes client socket as argument.
    global indexP
    global indexG
    global indexAto
    global indexBto
    global tester
    global DS_users_online
    global loop
    global batmotlan
    global rangbuoc_deluu4giatri
    global firstauthenuser
    name = client.recv(BUFSIZ).decode("utf8") # nhận tên client
    if name in DS_users_online:
        welcome = 'Bạn đã đăng nhập rồi !!!'
        client.send(bytes(welcome, "utf8"))
        time.sleep(0.25)
        welcome1 = "Cửa sổ sẽ bị đóng trong {} giây."
        # Gửi thông điệp từ 3 xuống 1
        for i in range(3, 0, -1):
            client.send(bytes(welcome1.format(i), "utf8"))
            time.sleep(1)  # Tạm dừng 1 giây trước khi gửi thông điệp tiếp theo
        client.send(bytes("{quit}", "utf8"))
        client.close()
    else:
        conn = sqlite3.connect('./instance/Database.db')
        c = conn.cursor()
        # Kiểm tra User có trong database không ?

        c.execute('SELECT username FROM users WHERE username = ?', (name,))
        result = c.fetchall()
        conn.close()
    
        if result:
            conn = sqlite3.connect('./instance/Database.db')
            c = conn.cursor()
            # Tạo tin nhắn ngẫu nhiên rồi mã hoá bằng PublicKey của Client
            c.execute('SELECT publicKey_RSA FROM users WHERE username = ?', (name,))
            takefirstone = c.fetchone()
            publicKey_RSA_fromDB = takefirstone[0]
            # Publickey_RSA_fromDB là kiểu bytes khi lấy từ DB
            random_challenge = generate_random_challenge()
            encrypted_challenge = encrypt_challenge_RSA(random_challenge, publicKey_RSA_fromDB)

            
            # Gửi challenge cho Client
            client.send(b"xThUc"+encrypted_challenge)

            # Nhận Hash của Challenge sau khi Client đã giải mã xong
            Hashed_Challenge_From_Client = client.recv(BUFSIZ)

            #  Chuyển đổi tin nhắn thành dạng byte trước khi băm
            message_bytes = random_challenge.encode('utf-8')
                    
            # Sử dụng SHA-256 để băm tin nhắn
            hash_object = hashlib.sha256(message_bytes)
                    
            # Lấy giá trị băm dưới dạng chuỗi hex
            hashed_message = hash_object.hexdigest()

            # Xác thực, so sánh hai chuỗi băm có giống nhau không, nếu giống thì xác thực thành công
            if hashed_message == Hashed_Challenge_From_Client.decode("utf-8"):
                

                welcome = 'Xin chào %s! Nếu bạn muốn thoát gõ, {quit} để thoát.' % name
                client.send(bytes(welcome, "utf8"))

                # Truy vấn các Users có trong DB để hiện lên cho Client chọn để nhắn tin
                c.execute('SELECT username FROM users')
                danh_sach_users = c.fetchall()

                for user in danh_sach_users:
                    if user[0] != name:
                        
                        client.send(bytes("DSuser:"+user[0],"utf8"))
                        time.sleep(0.25)

                
                #broadcast(bytes(msg, "utf8")) #
                rangbuoc[name] = None
                clients[client] = name # dict
                DS_users_online.append(name)
                
                conn.close()
                while True:
                    msg = client.recv(BUFSIZ)
                    
                    if msg != bytes("{quit}", "utf8"):
                            if b"LayTN:" in msg:
                                
                                msg = msg[6:]
                                rangbuoc[clients[client]] = msg.decode("utf8")
                                # Lấy các message từ DB vào để đồng bộ
                                conn = sqlite3.connect('./instance/Database.db')
                                c = conn.cursor()
                                c.execute('SELECT username_send, message, username_receive,nguoixacthuctruoc, p, Ato, Bto, g FROM messages WHERE (username_send = ? and username_receive = ? ) or (username_send = ? and username_receive = ?) ',(name, msg.decode("utf8"),msg.decode("utf8"),name))
                                result1 = c.fetchall()
                                if result1:                                           
                                    indexP="p0FInDEx" + str(result1[0][4]) # p
                                    indexG="g0FInDEx" + str(result1[0][7]) # g
                                    indexAto1 = "A0FInDEx" + str(result1[0][5]) # Ato
                                    indexBto1 = "B0FInDEx" + str(result1[0][6]) # Bto
                                    userxacthuctruoc = result1[0][3]
                                    # Gửi P, G cho client
                                    client.send(indexP.encode("utf8"))
                                    time.sleep(0.25)
                                    client.send(indexG.encode("utf8"))
                                    time.sleep(0.25)
                                    if result1[0][3] == clients[client]: # Nếu người xác thực trước thì gửi Bto để tính s
                                        # gửi Bto
                                        client.send(indexBto1.encode("utf8"))
                                        
                                        time.sleep(0.25)
                                    else:
                                        # Gửi Ato
                                        client.send(indexAto1.encode("utf8"))  
                                        time.sleep(0.25)
                                    
                                    for i in result1:
                                        broadcast(i[1],client,i[0]+": ")
                                        batmotlan = 1
                                        time.sleep(0.25)
                                    rangbuoc_deluu4giatri[name+" - "+msg.decode("utf8")] = [indexG[8:],indexAto1[8:],indexBto1[8:],indexP[8:],userxacthuctruoc]
                                    
                                    conn.close()
                                # elif kiểm tra xem rangbuoc_deluu4giatri
                                elif name + " - " + msg.decode("utf8") in rangbuoc_deluu4giatri:
                                    indexP_taiday="p0FInDEx" + str(rangbuoc_deluu4giatri[name+" - "+msg.decode("utf8")][3]) # p
                                    indexG_taiday="g0FInDEx" + str(rangbuoc_deluu4giatri[name+" - "+msg.decode("utf8")][0]) # g
                                    indexAto1_taiday = "A0FInDEx" + str(rangbuoc_deluu4giatri[name+" - "+msg.decode("utf8")][1]) # Ato
                                    indexBto1_taiday = "B0FInDEx" + str(rangbuoc_deluu4giatri[name+" - "+msg.decode("utf8")][2]) # Bto

                                    client.send(indexP_taiday.encode("utf8"))
                                    time.sleep(0.25)
                                    client.send(indexG_taiday.encode("utf8"))
                                    time.sleep(0.25)
                                    if rangbuoc_deluu4giatri[name+" - "+msg.decode("utf8")][4] == name : # Nếu người xác thực trước thì gửi Bto để tính s
                                        # gửi Bto
                                        client.send(indexBto1_taiday.encode("utf8"))
                                        time.sleep(0.25)
                                    else:
                                        # Gửi Ato
                                        client.send(indexAto1_taiday.encode("utf8"))  
                                        time.sleep(0.25)
                                        
                                else:
                                    user_ban_muon_nhan = msg.decode("utf8")
                                    
                                    if (msg.decode("utf8") in DS_users_online):
                                        if rangbuoc[user_ban_muon_nhan] == name:
                                            
                                            # tester = provider = client 1
                                            tester=client
                                            firstauthenuser = clients[client]
                                            client.send("Start Pr@tocol".encode("utf-8")) # Bắt đầu protocol

                                            # Chờ P, G, Ato
                                            indexP=client.recv(BUFSIZ).decode("utf8")
                                            indexG=client.recv(BUFSIZ).decode("utf8")
                                            indexAto=client.recv(BUFSIZ).decode("utf8")


                                            # khởi tạo, thêm header
                                            indexP="p,FInDEx" + indexP
                                            indexG="g,FInDEx" + indexG
                                            indexAto = "A,FInDEx" + indexAto

                                        

                                            # Hoán vị để gửi Bto *
                                            search_value = user_ban_muon_nhan
                                            
                                            # Duyệt qua từng cặp khóa-giá trị trong từ điển
                                            for key, value in clients.items():
                                                # Nếu giá trị trùng khớp với giá trị tìm kiếm
                                                if value == search_value:
                                                    # In ra khóa tương ứng
                                                    client = key
                                                    # Dừng vòng lặp nếu bạn chỉ muốn in ra một khóa duy nhất
                                                    break
                                            
                                            # Gửi P, G cho client 2
                                            client.send(indexP.encode("utf8"))
                                            time.sleep(0.25)
                                            client.send(indexG.encode("utf8"))
                                            time.sleep(0.25)

                                            
                                            client.send(indexAto.encode("utf8"))
                                            time.sleep(0.25)
                                            
                                    
                                            
                                            # Thử hoán vị
                                            
                                            while (indexBto == ""):
                                                si = "0"

                                            
                                        
                                            
                                            indexBto = "B,FInDEx" + indexBto
                                            # Hoán vị lần nữa
                                           

                                            search_value = name
                                            
                                            for key, value in clients.items():
                                                # Nếu giá trị trùng khớp với giá trị tìm kiếm
                                                if value == search_value:
                                                    # In ra khóa tương ứng
                                                    client = key
                                                    # Dừng vòng lặp nếu bạn chỉ muốn in ra một khóa duy nhất
                                                    break

                                            client.send(indexBto.encode("utf8"))

                                                                                                                     
                                            rangbuoc_deluu4giatri[name+" - "+user_ban_muon_nhan] = [indexG[8:],indexAto[8:],indexBto[8:],indexP[8:],firstauthenuser]
                                            rangbuoc_deluu4giatri[user_ban_muon_nhan + " - "+name] = [indexG[8:],indexAto[8:],indexBto[8:],indexP[8:],firstauthenuser]
                                            
                                            # Đoạn này để trả về thông tin cả hai đã trao đổi khoá thành công
                                            tukhoa1 = name
                                            tukhoa2 = user_ban_muon_nhan
                                            new_dict = {key: value for key, value in clients.items() if value in (tukhoa1, tukhoa2)}
                                            information = 'Bạn và người này đã trao khoá thành công.'
                                            for sock in new_dict:
                                                sock.send(bytes(information, "utf8"))
                                                time.sleep(0.25)
                                        else:
                                            error = 'Bạn và người này cần cùng phòng để trao khoá.'
                                            client.send(bytes(error, "utf8"))
                                    else:
                                        error = "User đang không Online nên không thể trao đổi khoá."
                                        client.send(bytes(error, "utf8"))

                            elif rangbuoc[clients[client]] == None:
                                error = "Xin hãy chọn người bạn muốn nhắn."
                                client.send(bytes(error, "utf8"))
                                
                            # elif loop == 1: # cách giải quyết: elfi rangbuoc[clients[client]] not in DS_user_online
                            elif rangbuoc[clients[client]] not in DS_users_online and name+" - "+rangbuoc[clients[client]] not in rangbuoc_deluu4giatri:
                                            # and rangbuoc_deluu4giatri[name+" - "+rangbuoc[clients[client]]] == rỗng
                                            # thì nghĩa là thằng mà thg client hiện tại muốn nhắn ko online và cũng chưa trao đổi khoá
                                error = "User đang không Online nên không thể trao đổi khoá."
                                client.send(bytes(error, "utf8"))
                            elif b"BIndex:" not in msg and rangbuoc[clients[client]] in DS_users_online and name+" - "+rangbuoc[clients[client]] not in rangbuoc_deluu4giatri: # TH2: cách giải quyết: elfi rangbuoc[clients[client]] in DS_user_online
                                            # and rangbuoc_deluu4giatri[name+" - "+rangbuoc[clients[client]]] == rỗng
                                            # thì nghĩa là thằng mà thg client hiện tại muốn nhắn đang online nhưng chưa trao đổi khoá
                                error = 'Bạn và người này cần cùng phòng để trao khoá.'
                                client.send(bytes(error, "utf8"))
                               
                            else:
                                
                                if b"BIndex:" in msg:
                                        msg = msg[7:]
                                        indexBto = msg.decode("utf8")
                                        
                                else:
                                    broadcast(msg, client,name + ": ")
                                    
                                    if b"M@C:" not in msg:                     
                                        conn = sqlite3.connect('./instance/Database.db')
                                        c = conn.cursor()
                                        c.execute("INSERT INTO messages (username_send, username_receive, message,nguoixacthuctruoc,g,Ato,Bto,p) VALUES (?,?,?,?,?,?,?,?)", (clients[client], rangbuoc[clients[client]],msg, rangbuoc_deluu4giatri[clients[client]+" - "+rangbuoc[clients[client]]][4], rangbuoc_deluu4giatri[clients[client]+" - "+rangbuoc[clients[client]]][0],rangbuoc_deluu4giatri[clients[client]+" - "+rangbuoc[clients[client]]][1],rangbuoc_deluu4giatri[clients[client]+" - "+rangbuoc[clients[client]]][2],rangbuoc_deluu4giatri[clients[client]+" - "+rangbuoc[clients[client]]][3]))
                                        conn.commit()
                                        conn.close()
                                        
                                    
                            
                            
                    else:
                        client.send(bytes("{quit}", "utf8"))
                        client.close()
                        del clients[client]
                        
                        break
            else:
                welcome = 'Xin chào ! Có vẻ như bạn không phải là %s.' % name
                client.send(bytes(welcome, "utf8"))
                
                welcome1 = "Cửa sổ sẽ bị đóng trong {} giây."

                # Gửi thông điệp từ 3 xuống 1
                for i in range(3, 0, -1):
                    client.send(bytes(welcome1.format(i), "utf8"))
                    time.sleep(1)  # Tạm dừng 1 giây trước khi gửi thông điệp tiếp theo
                
                client.send(bytes("{quit}", "utf8"))
                client.close()   
        else:
            conn = sqlite3.connect('./instance/Database.db')
            c = conn.cursor()
            client.send(bytes("YOurFirSTtImE", "utf8"))
            public_key_luuDB = client.recv(BUFSIZ)
            
            c.execute("INSERT INTO users (username, publicKey_RSA) VALUES (?, ?)", (name, public_key_luuDB))
            conn.commit()
            conn.close()
            

            welcome = 'Xin chào ! Đây là lần đầu xác thực của bạn.'
            client.send(bytes(welcome, "utf8"))
            time.sleep(0.25)
            welcome = 'Vui lòng mở lại cửa sổ để đăng nhập.'
            client.send(bytes(welcome, "utf8"))
            time.sleep(0.25)
            welcome1 = "Cửa sổ sẽ bị đóng trong {} giây."
            # Gửi thông điệp từ 3 xuống 1
            for i in range(3, 0, -1):
                client.send(bytes(welcome1.format(i), "utf8"))
                time.sleep(1)  # Tạm dừng 1 giây trước khi gửi thông điệp tiếp theo
            client.send(bytes("{quit}", "utf8"))
            client.close()
    

def broadcast(msg,indexclient, prefix=""):  # prefix is for name identification.  
    global batmotlan
    prefix = "N,FInDEx$" + prefix
    
    the_encoding = chardet.detect(msg)['encoding']
    
    if batmotlan == 1:
        tukhoa1 = clients[indexclient]
        new_dict = {key: value for key, value in clients.items() if value in (tukhoa1)}
        for sock in new_dict:
            sock.send(prefix.encode("utf8"))
            sock.send(msg)
        batmotlan = 0
    elif the_encoding == "ascii" and len(msg)==68: # không cần gửi prefix
        if (msg.decode("utf8")[0]=="M" and msg.decode("utf8")[1]=="@"): # ??? gui di chu ki
            if rangbuoc[clients[indexclient]] in DS_users_online: # nếu client 2 trong ds online
                if rangbuoc[rangbuoc[clients[indexclient]]] == clients[indexclient]:# nếu ràng buộc của client2 có tên client\
                    tukhoa1 = clients[indexclient]
                    tukhoa2 = rangbuoc[clients[indexclient]]

                    new_dict = {key: value for key, value in clients.items() if value in (tukhoa1, tukhoa2)}

                    for sock in new_dict:
                        sock.send(prefix.encode("utf8"))
                        time.sleep(0.25)
                        sock.send(msg)
                else:
                    tukhoa1 = clients[indexclient]
                    new_dict = {key: value for key, value in clients.items() if value in (tukhoa1)}
                    for sock in new_dict:
                        sock.send(prefix.encode("utf8"))
                        time.sleep(0.25)
                        sock.send(msg)
            
        time.sleep(0.1)
    else:
        # Ràng buộc là từ điển rangbuoc = {tenc_client1 : "ten_client1 - ten_client2"}
        if rangbuoc[clients[indexclient]] in DS_users_online: # nếu client 2 trong ds online
            if rangbuoc[rangbuoc[clients[indexclient]]] == clients[indexclient]:# nếu ràng buộc của client2 có tên client\
                tukhoa1 = clients[indexclient]
                tukhoa2 = rangbuoc[clients[indexclient]]
                
                new_dict = {key: value for key, value in clients.items() if value in (tukhoa1, tukhoa2)}
                
                for sock in new_dict:
                    sock.send(prefix.encode("utf8"))
                    time.sleep(0.25)
                    sock.send(msg)

            else:
                
                tukhoa1 = clients[indexclient]
                new_dict = {key: value for key, value in clients.items() if value in (tukhoa1)}
                for sock in new_dict:
                    sock.send(prefix.encode("utf8"))
                    time.sleep(0.25)
                    sock.send(msg)
        else:
            
            tukhoa1 = clients[indexclient]
            new_dict = {key: value for key, value in clients.items() if value in (tukhoa1)}
            for sock in new_dict:
                sock.send(prefix.encode("utf8"))
                time.sleep(0.25)
                sock.send(msg)

indexP = ""
indexG = ""
indexAto = ""
indexBto = ""
firstauthenuser = ""
batmotlan = 0
DS_users_online = []
rangbuoc = {}
rangbuoc_deluu4giatri = {}
clients = {}
addresses = {}
loop = 0

HOST = '127.0.0.1'
PORT = 33000
BUFSIZ = 8092 
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def database_exists():
    return os.path.exists('./instance/Database.db')

def create_database():
    
    conn = sqlite3.connect('./instance/Database.db')
    c = conn.cursor()
    # Tạo bảng users
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username STRING NOT NULL,
                 publicKey_RSA BLOB NOT NULL)''')

    # Tạo bảng messages
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username_send STRING NOT NULL,
                 username_receive STRING NOT NULL,
                 message BLOB NOT NULL,
                 nguoixacthuctruoc STRING NOT NULL,
                 g STRING NOT NULL,
                 Ato STRING NOT NULL,
                 Bto STRING NOT NULL,
                 p STRING NOT NULL,
                 FOREIGN KEY (username_send) REFERENCES users (username))''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    if not database_exists():
        create_database()
    SERVER.listen(2)
    print("Chờ kết nối từ các client...")
    
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()