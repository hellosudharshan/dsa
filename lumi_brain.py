import asyncio
import os
from dotenv import load_dotenv
from hume import AsyncHumeClient, MicrophoneInterface, Stream

load_dotenv()

async def main():
    # 1. Initialize Client
    client = AsyncHumeClient(api_key=os.getenv("HUME_API_KEY"))

    try:
        # 2. Connect to the voice interface
        async with client.empathic_voice.chat.connect() as socket:
            print("✨ LUMI IS ONLINE! ✨")
            print(">>> I'm listening to your voice and your vibe...\n")

            # 3. Create a Stream to handle incoming data
            # This is the "brain" that processes what the socket sends back
            async def handle_messages():
                async for message in socket:
                    if message.type == "user_message":
                        print(f"🎤 You: {message.message.content}")
                        
                        # Extract the emotional vibe (Prosody)
                        if hasattr(message.models, "prosody") and message.models.prosody:
                            scores = message.models.prosody.scores
                            top_3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
                            
                            mood = " | ".join([f"{k}: {v:.2f}" for k, v in top_3])
                            print(f"💙 Lumi Senses: {mood}\n")
                    
                    elif message.type == "assistant_message":
                        print(f"🌸 Lumi: {message.message.content}")

            # 4. START THE MICROPHONE
            # In the 2026 SDK, we use .start() and pass the socket directly.
            # We also enable 'allow_user_interrupt' so you can talk over Lumi.
            message_task = asyncio.create_task(handle_messages())
            
            await MicrophoneInterface.start(
                socket, 
                allow_user_interrupt=True
            )
            
            await message_task

    except Exception as e:
        print(f"\n❌ Connection Error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nLumi is going to sleep. Bye!")
