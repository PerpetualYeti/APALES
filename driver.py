from gcodeSender import Sender

def main():
    # Replace with actual COM port
    com_port = "COM6"
    print("Hello from driver")
    
    sender = Sender(com_port)
    sender.connect()
    sender.send_job()
    #sender.send_wakeup()
    sender.disconnect()

if __name__ == "__main__":
    main()