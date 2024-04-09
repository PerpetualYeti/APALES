from gcode_sender import gCodeSender

def main():
    print("Hello from driver")
    sender = gCodeSender('COM6')
    sender.connect()
    sender.send_job()
    #sender.send_wakeup()
    sender.disconnect()

if __name__ == "__main__":
    main()