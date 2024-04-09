from gcode_sender import gCodeSender

def main():
    # Replace with actual COM port
    com_port = "COM6"
    print("Hello from driver")
    
    sender = gCodeSender(com_port)
    sender.connect()
    sender.send_job()
    #sender.send_wakeup()
    sender.disconnect()

if __name__ == "__main__":
    main()