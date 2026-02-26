import asyncio
import os
from dotenv import load_dotenv
# We are adding the 'HumeClient' for the authenticator
from hume import AsyncHumeClient, MicrophoneInterface
from hume.empathic_voice.chat.socket_client import ChatConnectOptions

load_dotenv()

async def main():
    # FIX: Initialize with ONLY api_key. 
    # The SDK will look for the secret if it needs to refresh tokens.
    client = AsyncHumeClient(api_key=os.getenv("HUME_API_KEY"))

    try:
        # Connect to Lumi's Voice Interface
        async with client.empathic_voice.chat.connect(config_id=None) as socket:
            print("\n✨ LUMI IS AWAKE! ✨")
            print(">>> Talk to Lumi now (Press Ctrl+C to stop)\n")

            async def handle_messages():
                async for message in socket:
                    if message.type == "user_message":
                        # Safety check to ensure prosody data exists
                        if hasattr(message.models, 'prosody') and message.models.prosody:
                            emotions = message.models.prosody.scores
                            top_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:3]
                            
                            print(f"🎤 You said: '{message.message.content}'")
                            emotion_str = ", ".join([f"{emo}: {score:.2f}" for emo, score in top_emotions])
                            print(f"💙 Lumi senses: {emotion_str}\n")

            await asyncio.gather(
                MicrophoneInterface.start_sending(socket),
                handle_messages()
            )
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nLumi is resting now. See you later!")
