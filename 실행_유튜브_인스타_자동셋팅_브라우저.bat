@echo off
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="%USERPROFILE%\.yt_ig_div3_profile" --remote-debugging-port=9223 --disable-blink-features=AutomationControlled --no-first-run --no-default-browser-check --start-maximized "%~dp0yt_ig_setup_studio.html" "https://studio.youtube.com" "https://www.instagram.com/accounts/edit/"
