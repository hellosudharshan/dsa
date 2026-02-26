import asyncio
import os
import base64
import sounddevice as sd
from dotenv import load_dotenv
from hume import AsyncHumeClient
# Import the specific model the SDK expects
from hume.empathic_voice.types import AudioInput

load_dotenv()

# Audio settings
RATE = 16000 
CHANNELS = 1

async def main():
    client = AsyncHumeClient(api_key=os.getenv("HUME_API_KEY"))

    try:
        async with client.empathic_voice.chat.connect() as socket:
            print("✨ LUMI IS ONLINE (v2026.2 Stable) ✨")

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

            async def send_audio():
                loop = asyncio.get_event_loop()
                queue = asyncio.Queue()

                def callback(indata, frames, time, status):
                    loop.call_soon_threadsafe(queue.put_nowait, indata.copy())

                with sd.InputStream(samplerate=RATE, channels=CHANNELS, callback=callback, dtype='int16', device=1):
                    while True:
                        data = await queue.get()
                        # 1. Convert to Base64
                        b64_data = base64.b64encode(data.tobytes()).decode("utf-8")
                        
                        # 2. Wrap in the AudioInput OBJECT (The Fix)
                        # We pass the b64 string to the 'data' field of the model
                        audio_obj = AudioInput(data=b64_data)
                        
                        # 3. Send the object, not raw bytes
                        await socket.send_audio_input(audio_obj)

            await asyncio.gather(handle_messages(), send_audio())

    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
