import torch
import sys
import os

print("--- DIAGNOSTYKA RTX ---")
print(f"Wersja Pythona: {sys.version}")
print(f"Czy CUDA jest dostępna? {'✅ TAK' if torch.cuda.is_available() else '❌ NIE'}")

if torch.cuda.is_available():
    print(f"Twoja karta: {torch.cuda.get_device_name(0)}")
    print(f"Pamięć VRAM: {round(torch.cuda.get_device_properties(0).total_memory / 1024**3, 2)} GB")
    
    # Testowy ładunek dla karty
    print("\n⏳ Testuję ładowanie tensora na GPU...")
    x = torch.rand(10000, 10000).cuda()
    print("🚀 Sukces! Karta graficzna poprawnie przelicza dane.")
else:
    print("\n⚠️ UWAGA: Skrypt nie widzi karty NVIDIA. Lip-sync będzie trwał wieki.")

# Sprawdzenie plików modeli
models = ["checkpoints/wav2lip_gan.pth", "checkpoints/s3fd.pth", "checkpoints/GFPGANv1.4.pth"]
print("\n--- STATUS MODELI ---")
for m in models:
    if os.path.exists(m):
        size = os.path.getsize(m) / (1024*1024)
        print(f"✅ {m} ({round(size, 2)} MB)")
    else:
        print(f"❌ BRAK: {m}")