import asyncio
import os
from dotenv import load_dotenv
from hume import AsyncHumeClient, MicrophoneInterface
from hume.empathic_voice.chat.socket_client import ChatConnectOptions

load_dotenv()

async def main():
    # 1. Initialize the client with your NEW keys
    client = AsyncHumeClient(
        api_key=os.getenv("HUME_API_KEY"),
        secret_key=os.getenv("HUME_SECRET_KEY")
    )

    # 2. Connect to Lumi's Voice Interface
    # We use a context manager (async with) to ensure the mic closes properly
    async with client.empathic_voice.chat.connect(ChatConnectOptions(config_id=None)) as socket:
        print("\n✨ LUMI IS AWAKE! ✨")
        print(">>> Talk to Lumi now (Press Ctrl+C to stop)\n")

        async def handle_messages():
            async for message in socket:
                # We only care about the moment YOU finish speaking
                if message.type == "user_message":
                    # Get the 'Prosody' (vocal emotion) scores
                    emotions = message.models.prosody.scores
                    
                    # Sort them to find the 'Top 3' strongest feelings
                    top_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:3]
                    
                    print(f"🎤 You said: '{message.message.content}'")
                    
                    emotion_str = ", ".join([f"{emo}: {score:.2f}" for emo, score in top_emotions])
                    print(f"💙 Lumi senses: {emotion_str}\n")

        # Start sending audio from mic and receiving data at the same time
        await asyncio.gather(
            MicrophoneInterface.start_sending(socket),
            handle_messages()
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nLumi is resting now. See you later!")
