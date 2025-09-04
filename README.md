# NEOS
The NEOS audiobook tool was built using Python as the core language, with Streamlit providing the interactive web interface for text input, file upload, playback, and session history. For text rewriting, it integrates Hugging Face models like Pegasus/Granite through API calls, while speech synthesis is handled using both the IBM Watson TTS API (online) and granite (offline) for flexible voice options. The Requests library is used to communicate with APIs, and os is used for temporary audio file handling. To enhance the user experience, base64 encoding enables custom wallpapers, while Streamlit session state manages history so users can revisit past narrations. Together, these components create a complete pipeline from text input to expressive, downloadable audio with full customization.
<h1>1️⃣ App Launch</h1>
<img width="1920" height="937" alt="Screenshot 2025-09-04 095737" src="https://github.com/user-attachments/assets/2f792c3d-50e6-4557-b095-5e9851b698d2" />

You open the NeoSonic – AI Audiobook Creator app. It lets you either paste text or upload a file to turn into speech. Basic settings like TTS Engine, Tone, and Voice are shown.
<h1>2️⃣ Default Interface</h1>
<img width="1920" height="988" alt="Screenshot 2025-09-04 095841" src="https://github.com/user-attachments/assets/79e7e4fb-6c02-4928-822e-1f989e7814a0" />

At first, the interface is plain with a default purple background. Nothing is uploaded yet, so only the input and options are visible.
<h1>3️⃣ Generating Audio</h1>
<img width="1920" height="922" alt="Screenshot 2025-09-04 100229" src="https://github.com/user-attachments/assets/a133725a-13a3-4dc5-9535-871687968b83" />

You test it by typing “I am human.” The engine is set to Granite (Offline) with a Neutral tone. The app generates audio and shows a play bar plus a small history log in reverse chronological order.
<h1>4️⃣ File Upload</h1>
<img width="1920" height="932" alt="Screenshot 2025-09-04 100646" src="https://github.com/user-attachments/assets/f7690f6c-1a9f-4a32-9562-75f520a04b5a" />

Next, you try uploading a file from your computer. The file explorer opens, showing your Downloads folder where you can pick a text file or background image.
<h1>5️⃣ Custom Background</h1>
<img width="1920" height="932" alt="Screenshot 2025-09-04 101625" src="https://github.com/user-attachments/assets/1a20148c-1bda-46e1-9488-b5f377d800f4" />

You upload a custom background — a pastel beach scene. The app background changes to this image, giving it a personalized look.

<img width="1920" height="930" alt="Screenshot 2025-09-04 101732" src="https://github.com/user-attachments/assets/09471b84-21ea-486d-bb13-a435c3b2dbb3" />

The app also highlights the Browse files button, showing how users can replace the background or upload text files easily.
<h1>6️⃣ Collapsed Panel View</h1>
<img width="1920" height="926" alt="Screenshot 2025-09-04 101829" src="https://github.com/user-attachments/assets/646eecdb-0153-4c01-aecb-90be822391a6" />

Finally, you collapse the side panel for a clean view. The beach wallpaper stays in the background, and the main controls for TTS and playback remain in the center.

