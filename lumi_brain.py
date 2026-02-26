import asyncio
import os
import numpy as np
import sounddevice as sd
from dotenv import load_dotenv
from hume import AsyncHumeClient

load_dotenv()

# Audio Settings for Lumi
CHANNELS = 1
RATE = 16000  # 16kHz is preferred by Hume
CHUNK = 1024

async def main():
    client = AsyncHumeClient(api_key=os.getenv("HUME_API_KEY"))

    try:
        async with client.empathic_voice.chat.connect() as socket:
            print("✨ LUMI IS ONLINE (Windows Bridge) ✨")

            # 1. Receiver: Handle Lumi's responses
            async def handle_messages():
                async for message in socket:
                    if message.type == "user_message":
                        print(f"🎤 You: {message.message.content}")
                        if hasattr(message.models, "prosody"):
                            scores = message.models.prosody.scores
                            top_3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
                            print(f"💙 Sensed: {', '.join([f'{k}: {v:.2f}' for k, v in top_3])}")
                    elif message.type == "assistant_message":
                        print(f"🌸 Lumi: {message.message.content}")

            # 2. Sender: Custom Windows Mic Stream
            async def send_audio():
                # We use a Queue to pass audio from the mic thread to the async socket
                loop = asyncio.get_event_loop()
                queue = asyncio.Queue()

                def callback(indata, frames, time, status):
                    if status: print(status)
                    loop.call_soon_threadsafe(queue.put_nowait, indata.copy())

                # Open the microphone (Device 1 from your list)
                with sd.InputStream(samplerate=RATE, channels=CHANNELS, callback=callback, dtype='int16'):
                    while True:
                        data = await queue.get()
                        # Convert audio to bytes and send to Hume
                        await socket.send_audio_input(data.tobytes())

            # Run both at the same time
            await asyncio.gather(handle_messages(), send_audio())

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
