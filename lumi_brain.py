import asyncio
import os
from dotenv import load_dotenv
from hume import AsyncHumeClient, MicrophoneInterface

# Load environment variables
load_dotenv()

async def main():
    # THE FIX: Only pass the api_key here.
    # The SDK handles the rest.
    api_key = os.getenv("HUME_API_KEY")
    if not api_key:
        print("ERROR: HUME_API_KEY not found in .env file!")
        return

    client = AsyncHumeClient(api_key=api_key)

    print("\nConnecting to Lumi...")

    try:
        # Use config_id=None to use the default EVI settings
        async with client.empathic_voice.chat.connect() as socket:
            print("✨ LUMI IS ONLINE! ✨")
            print(">>> Talk to Lumi. I'll show you what she senses.\n")

            async def handle_messages():
                async for message in socket:
                    # Look for the moment the AI transcribes your voice
                    if message.type == "user_message":
                        print(f"🎤 You: {message.message.content}")
                        
                        # Extract the emotional 'vibe' (Prosody)
                        if hasattr(message.models, "prosody") and message.models.prosody:
                            scores = message.models.prosody.scores
                            # Sort and get top 3 emotions
                            top_3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
                            
                            emotion_display = " | ".join([f"{k}: {v:.2f}" for k, v in top_3])
                            print(f"💙 Lumi Senses: {emotion_display}\n")
                    
                    # Also print what Lumi says back to you
                    elif message.type == "assistant_message":
                        print(f"🌸 Lumi: {message.message.content}")

            # Start recording and listening simultaneously
            await asyncio.gather(
                MicrophoneInterface.start_sending(socket),
                handle_messages()
            )

    except Exception as e:
        print(f"\n❌ Connection Error: {e}")
        print("Hint: Check if another app is using your microphone or if your API key is correct.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nLumi is going to sleep. Bye!")
