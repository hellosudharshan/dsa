# 2. Sender: Custom Windows Mic Stream
            async def send_audio():
                loop = asyncio.get_event_loop()
                queue = asyncio.Queue()

                def callback(indata, frames, time, status):
                    if status: print(status)
                    loop.call_soon_threadsafe(queue.put_nowait, indata.copy())

                # Using Device 1 (Microphone Array) from your previous list
                with sd.InputStream(samplerate=RATE, channels=CHANNELS, callback=callback, dtype='int16', device=1):
                    while True:
                        data = await queue.get()
                        
                        # THE FIX: Convert bytes to Base64 string and wrap in the expected dict
                        import base64
                        encoded_data = base64.b64encode(data.tobytes()).decode("utf-8")
                        
                        # Use the modern 'send_audio_input' method with the correct payload
                        await socket.send_audio_input(data=encoded_data)
