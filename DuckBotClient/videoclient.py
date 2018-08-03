from rpistream.streamclient import Client


while True:
    try:
        client = Client(serverIp="18.111.67.233", port=5000, WriteFile=False) # Connects to the server
        client.startStream() # Starts recieving data and displaying the video
    except KeyboardInterrupt:
        break    
    except:
        pass
