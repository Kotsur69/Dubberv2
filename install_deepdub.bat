@echo off
chcp 65001 >nul
echo 🛠️ NAPRAWA MODELI - PODEJŚCIE OSTATECZNE...
echo.

:: 1. Czyszczenie uszkodzonych plików
if exist checkpoints\s3fd.pth del /q checkpoints\s3fd.pth
if exist checkpoints\wav2lip_gan.pth del /q checkpoints\wav2lip_gan.pth

:: 2. Pobieranie - Proste, bezbłędne komendy PowerShell
echo 📥 Pobieranie wav2lip_gan.pth (414 MB)...
powershell -Command "Invoke-WebRequest -UserAgent 'Mozilla/5.0' -Uri 'https://huggingface.co/KadirNar/Wav2Lip/resolve/main/wav2lip_gan.pth?download=true' -OutFile 'checkpoints\wav2lip_gan.pth'"

echo 📥 Pobieranie s3fd.pth (85 MB)...
powershell -Command "Invoke-WebRequest -UserAgent 'Mozilla/5.0' -Uri 'https://huggingface.co/KadirNar/Wav2Lip/resolve/main/s3fd.pth?download=true' -OutFile 'checkpoints\s3fd.pth'"

echo.
echo 🔍 SPRAWDZANIE WYNIKÓW:
echo --------------------------------------------------
powershell -Command "Get-ChildItem checkpoints\*.pth | Select-Object Name, @{Name='Size(MB)';Expression={[math]::Round($_.Length / 1MB, 2)}} | Format-Table -AutoSize"
echo --------------------------------------------------
pause