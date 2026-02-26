import asyncio
import os
from dotenv import load_dotenv
from hume import AsyncHumeClient, MicrophoneInterface, Stream
from hume.empathic_voice.types import SubscribeEvent

load_dotenv()

async def main():
    api_key = os.getenv("HUME_API_KEY")
    client = AsyncHumeClient(api_key=api_key)

    print("\nConnecting to Lumi...")

    try:
        # 1. Connect to the Empathic Voice Interface
        async with client.empathic_voice.chat.connect() as socket:
            print("✨ LUMI IS ONLINE! ✨")
            print(">>> Talk to Lumi. (Press Ctrl+C to stop)\n")

            # 2. Define how to handle incoming messages (Emotions + Audio)
            async def on_message(message: SubscribeEvent):
                if message.type == "user_message":
                    print(f"🎤 You: {message.message.content}")
                    
                    # Extract Emotional Prosody
                    if hasattr(message.models, "prosody") and message.models.prosody:
                        scores = message.models.prosody.scores
                        top_3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
                        emotion_display = " | ".join([f"{k}: {v:.2f}" for k, v in top_3])
                        print(f"💙 Lumi Senses: {emotion_display}\n")
                
                elif message.type == "assistant_message":
                    print(f"🌸 Lumi: {message.message.content}")

            # 3. Start the NEW Stream interface (2026 standard)
            # This handles both sending your mic and playing Lumi's voice
            await Stream.consume(
                socket,
                handle_message=on_message,
                user_input=MicrophoneInterface()
            )

    except Exception as e:
        print(f"\n❌ Connection Error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nLumi is resting now. Bye!")
