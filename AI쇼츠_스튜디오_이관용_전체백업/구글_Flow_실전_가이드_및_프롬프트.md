# 🎬 Google Flow (Veo) × 내 PC 자동 편집기 실전 연결 가이드

맞습니다! 이미 구글 생태계를 쓰고 계시다면 클링(Kling)이나 하이루오(Hailuo)를 따로 결제하실 필요 없이 **Google Flow (`https://labs.google/fx/tools/flow`)**의 **Veo 모델(Text-to-Video / Frames-to-Video)**을 쓰시는 게 화질과 물리 엔진 면에서 가장 압도적입니다.

그리고 우리가 아까 뽑아둔 **초고화질 영화 스틸컷 10장(`D:\투자홈페이지\AI쇼츠_스튜디오_이관용_전체백업\ai_shorts_output\assets\`)**을 Google Flow의 **`Frames to Video` (시작 프레임 이미지 넣기)**에 넣으면, 그 사진 속 고대 로마 사람들과 뇌 시냅스, 빗길 포르쉐가 **그 화질 그대로 실제 영화처럼 움직이는 `.mp4` 비디오**로 변환됩니다!

---

## 🚀 방법 1: Antigravity `/browser` 기능으로 구글 Flow 자동 조작하기

크롬 브라우저에서 [Google Flow (labs.google/fx/tools/flow)](https://labs.google/fx/tools/flow)에 로그인해 두신 뒤, 이 채팅창에 **`/browser`** 명령어를 붙여 말씀해 주시면 에이전트가 직접 브라우저를 제어해 프롬프트를 입력하고 영상을 생성·다운로드할 수 있습니다.

```text
/browser https://labs.google/fx/tools/flow 에 접속해서 아래 4개 프롬프트로 9:16 세로형 영상을 생성하고 다운로드해줘.
```

---

## 🚀 방법 2: 내가 이미 만들어 둔 ‘고화질 시작 프레임 10장’을 Google Flow에 넣고 1분 만에 뽑기

`D:\투자홈페이지\AI쇼츠_스튜디오_이관용_전체백업\ai_shorts_output\assets\` 폴더에 이미 영화급 스틸컷 10장이 들어 있습니다.  
Google Flow에서 **`Frames to Video`**를 선택하고 아래 이미지와 **카메라 모션 프롬프트**를 넣으시면 됩니다.

### 🧠 1번 영상용 (미국 유튜브 1위: 3D 뇌과학 다큐)
1. **Cut 1 (`v1_shot1_eye.jpg` 첨부)**
   ```text
   Extreme macro cinematic shot. The tired human eye slowly blinks and the pupil dilates as blue smartphone light flickers across the iris in a dark room at 3 AM. Subtle handheld camera movement, 85mm macro lens.
   ```
2. **Cut 2 (`v1_shot2_brain_scan.jpg` 첨부)**
   ```text
   3D medical documentary animation. The camera slowly orbits around the translucent human head while glowing cyan and amber neural pathways pulse and fire rapidly across the cerebral cortex.
   ```
3. **Cut 3 (`v1_shot3_neurons.jpg` 첨부)**
   ```text
   Microscopic 3D scientific CGI. Camera pushes forward through a dense forest of brain neurons as bright bio-electrical action potentials shoot along axons and toxic red particles accumulate around synapses.
   ```
4. **Cut 4 (`v1_shot4_mri.jpg` 첨부)**
   ```text
   Handheld documentary shot inside a dark hospital neurology lab. A neurologist points at the glowing brain MRI scan on the monitor as the scan slices animate on screen.
   ```

---

### 📸 2번 영상용 (미국 인스타 릴스 1위: 다크 럭셔리 빗길)
1. **Cut 1 (`v2_shot1_porsche_rain.jpg` 첨부)**
   ```text
   35mm Kodak Portra night cinematography. Driver POV inside a Porsche driving smoothly through rainy Manhattan streets at night. Raindrops streak across the windshield and warm city neon bokeh lights glide past.
   ```
2. **Cut 2 (`v2_shot2_macbook_desk.jpg` 첨부)**
   ```text
   Slow cinematic dolly-in toward a sleek laptop on a dark walnut desk in a minimalist penthouse at night, while heavy rain streams down the floor-to-ceiling window overlooking the glowing city skyline.
   ```

---

### 🏛️ 3번 영상용 (미국 역사 다큐 1위: 고대 로마 24시간 생존)
1. **Cut 1 (`v3_shot1_rome_street.jpg` 첨부)**
   ```text
   Ridley Scott live-action movie shot on ARRI Alexa 65. The camera tracks forward through a crowded, muddy street in Ancient Rome's Subura district at dawn as citizens in linen tunics walk past and golden sunlight pierces through rising dust and smoke.
   ```
2. **Cut 2 (`v3_shot2_roman_coins.jpg` 첨부)**
   ```text
   Cinema close-up. Weathered hands slowly pour ancient silver Roman denarii coins onto a rough wooden tavern table while warm oil lamp flames flicker in the background.
   ```
3. **Cut 3 (`v3_shot3_thermae_bath.jpg` 첨부)**
   ```text
   Slow cinematic pan across an ancient Roman marble bathhouse as thick steam rises from the turquoise water and volumetric sunbeams shift through the high stone arches.
   ```
4. **Cut 4 (`v3_shot4_colosseum_dusk.jpg` 첨부)**
   ```text
   Epic dusk cinema shot of the Roman Colosseum in 80 AD. Burning torches flicker in the wind along the stone arches as crowds move across the plaza and dramatic storm clouds drift overhead.
   ```

---

## 🚀 마지막 단계: 다운받은 Flow 영상들을 ‘상단 상태창 없는 100% 클린 쇼츠’로 5초 만에 합치기

Google Flow에서 다운받은 `.mp4` 파일들을 **`D:\투자홈페이지\AI쇼츠_스튜디오_이관용_전체백업\ai_shorts_output\flow_clips\`** 폴더에 넣고 아래 명령어만 실행하면, **위쪽의 어색한 상태창/게이지 없이 100% 깔끔한 풀스크린 + AI 성우 + 하단 단어별 팝업 자막**으로 즉시 합쳐집니다!

```powershell
python "D:\투자홈페이지\AI쇼츠_스튜디오_이관용_전체백업\flow_shorts_merger.py"
```
