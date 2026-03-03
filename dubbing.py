import os
import torch
import asyncio
from moviepy.editor import VideoFileClip, AudioFileClip
from faster_whisper import WhisperModel

class RTX_Dubber:
    def __init__(self):
        # Sprawdzanie CUDA
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🚀 Silnik RTX: {self.device.upper()} (Model: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'})")
        
        # Inicjalizacja Whisper Large-v3 (na RTX 5070 Ti to będzie śmigać)
        print("⏳ Ładowanie modelu Whisper Large-v3...")
        self.whisper = WhisperModel("large-v3", device=self.device, compute_type="float16")
        
    async def run_lip_sync(self, video_path, audio_path):
        output_sync = os.path.join("outputs", "synced_video.mp4")
        checkpoint = os.path.join("checkpoints", "wav2lip_gan.pth")
        
        # Komenda z poprawionymi ścieżkami dla Windows
        cmd = (
            f"python Wav2Lip\\inference.py "
            f"--checkpoint_path {checkpoint} "
            f"--face \"{video_path}\" "
            f"--audio \"{audio_path}\" "
            f"--outfile \"{output_sync}\" "
            f"--nosmooth" # RTX jest na tyle szybki, że nosmooth często daje ostrzejszy detal
        )
        
        print("👄 [Wav2Lip] Generowanie ruchu ust...")
        os.system(cmd)
        return output_sync

    def enhance_faces(self, synced_video):
        print("✨ [GFPGAN] Podbijanie jakości twarzy do HD...")
        # Ważne: GFPGAN tworzy folder z wynikami, musimy podać ścieżkę do pliku wejściowego
        # Używamy wersji 1.4, którą pobrałeś
        cmd = (
            f"python GFPGAN\\inference_gfpgan.py "
            f"-i {synced_video} "
            f"-o outputs\\final_hd "
            f"-v 1.4 -s 2 --only_center_face --bg_upsampler None"
        )
        os.system(cmd)
        return "outputs\\final_hd\\restored_videos\\synced_video.mp4"

async def main():
    # Upewnij się, że foldery istnieją
    for folder in ["inputs", "outputs", "checkpoints"]:
        if not os.path.exists(folder): os.makedirs(folder)

    dubber = RTX_Dubber()
    
    # TWOJE PLIKI WEJŚCIOWE (Upewnij się, że tam są!)
    input_video = "inputs\\test_clip.mp4"
    input_audio = "inputs\\polski_dubbing.wav" 

    if not os.path.exists(input_video) or not os.path.exists(input_audio):
        print("❌ BŁĄD: Brak pliku wideo lub audio w folderze inputs!")
        return

    # 1. Lip-Sync
    synced_v = await dubber.run_lip_sync(input_video, input_audio)
    
    # 2. Upscaling (GFPGAN)
    if os.path.exists(synced_v):
        final_v = dubber.enhance_faces(synced_v)
        print(f"🏁 SUKCES! Finalny film: {final_v}")
    else:
        print("❌ Lip-sync nie wygenerował pliku. Sprawdź błędy w konsoli.")

if __name__ == "__main__":
    asyncio.run(main())