# 📦 [집 컴퓨터 이관용 올인원 패키지] 미국 떡상 AI 쇼츠·릴스 × Google Flow(Veo) 스튜디오

> **💡 이관 방법 (2가지 중 편한 것 하나만 가져가세요!)**
> 1. **가장 간단한 방법**: 이 파일 딱 1개(**`집컴퓨터_이관용_AI쇼츠_GoogleFlow_마스터패키지.md`**)만 카카오톡 '나에게 보내기'로 집 PC에 보낸 뒤, 아래 **[STEP 1]** 명령어를 집 PC Antigravity 채팅창에 붙여넣으세요!
> 2. **이미지·코드까지 통째로 가져가는 방법**: 같은 폴더에 생성된 **`AI쇼츠_스튜디오_이관용_전체백업.zip`** 압축 파일 1개를 카카오톡/구글 드라이브로 보내서 집 PC에 압축만 푸시면 오늘 만든 고화질 시작 프레임 14장과 파이썬 엔진 4종이 그대로 복원됩니다!

---

## 🚀 [집 PC 도착 후 실행] Antigravity 복붙용 원클릭 명령어

### 🔧 사전 준비 (집 PC 크롬에서 딱 1번만 체크 — 10초 소요)
집 PC에서 에이전트가 직접 **Google Flow (`https://labs.google/fx/tools/flow`)** 화면을 클릭하고 영상을 자동 생성·다운로드하게 하려면:
1. 크롬에서 **[Google Flow (`labs.google/fx/tools/flow`)](https://labs.google/fx/tools/flow)** 에 로그인해 둡니다.
2. 크롬 새 탭 주소창에 **`chrome://inspect/#remote-debugging`** 을 입력해 이동한 뒤, **`Enable remote debugging` (원격 디버깅 허용)** 체크박스를 켭니다.

---

### [STEP 1] 집 PC에 스튜디오 환경 + 고화질 시작 프레임 + 클린 합본 엔진 일괄 세팅 명령어
*(집 PC Antigravity 채팅창에 아래 블록을 복사해 붙여넣으세요)*
```text
/goal 현재 폴더의 집컴퓨터_이관용_AI쇼츠_GoogleFlow_마스터패키지.md 파일을 읽고, 미국 유튜브 쇼츠 & 인스타 릴스 제작 스튜디오 환경을 완벽하게 세팅해줘.

필수 작업:
1. 필요한 파이썬 패키지(edge-tts, imageio, imageio-ffmpeg, numpy, pillow)를 설치하고 Windows SSL 인증서(load_default_certs) 호환을 적용할 것.
2. 문서에 포함된 `flow_shorts_merger.py`와 `us_viral_studio.py`를 생성하여, 상단의 어색한 상태창(HUD/게이지)이 전혀 없는 '100% 클린 풀스크린 영상 + 원테이크 자연 호흡 성우(AndrewMultilingualNeural / BrianMultilingualNeural) + 단어 단위(WordBoundary 0.01초 싱크) Active-Word 팝업 자막 + 컷 전환 우쉬(Whoosh) 사운드 디자인' 파이프라인을 구축할 것.
3. 만약 assets/ 폴더에 시작 프레임 이미지 10종(뇌과학 4컷, 인스타 릴스 빗길 2컷, 고대 로마 4컷)이 없다면 image-generator 서브에이전트로 초고화질 시네마틱 스틸컷 10종을 생성해 둘 것.
4. 준비가 끝나면 크롬의 Google Flow(https://labs.google/fx/tools/flow)와 연동해 첫 번째 쇼츠 영상을 바로 생성할 수 있게 안내해줘.
```

---

### [STEP 2] Google Flow에서 받은 영상들을 5초 만에 ‘100% 클린 인기 쇼츠’로 합치는 명령어
*(Google Flow에서 클립 4개를 다운로드한 뒤 채팅창에 입력하거나 터미널에서 실행)*
```text
방금 Google Flow에서 다운받은 mp4 클립들을 다운로드(Downloads) 폴더에서 자동으로 가져와서, 상단 상태창 없이 100% 깔끔한 풀스크린 + 원테이크 영어 성우 + 하단 단어별(Word-by-Word) 팝업 자막과 효과음을 입혀 최종 쇼츠 mp4로 합쳐줘.
```

---

## 📊 1. 오늘 분석한 미국(US) 유튜브 쇼츠 vs 인스타 릴스 핵심 공식 요약

### ① 왜 일반 AI 영상은 어색하고 안 팔리는가? (절대 피해야 할 3가지)
1. **정지된 사진만 확대(Ken Burns)하는 영상**: 사물이나 인물이 실제로 움직이지 않으면 시청자가 2초 만에 스와이프합니다. → **해결책: 고화질 시작 프레임 이미지를 Google Flow(Veo)의 `Frames to Video`에 넣어 실제 움직이는 5~8초 시네마틱 비디오로 변환!**
2. **화면 상단의 기계적인 상태창(HUD, 게이지, 그래프, 점선)**: 실제 인기 유튜버들은 절대 넣지 않는 요소로, 프로그램이 찍어낸 티가 납니다. → **해결책: 상단 장식을 100% 제거한 클린 풀스크린(Clean Full-Screen) 유지!**
3. **문장 단위로 끊어 녹음한 로봇 억양 & 반투명 사각형 자막 박스**: → **해결책: 전체 대본을 원테이크(One-Take)로 한 번에 녹음하고, `boundary="WordBoundary"`로 지금 발음하는 단어만 색상이 켜지며 커지는 박스 없는 단어별(Active-Word) 자막 적용!**

### ② 미국 시장을 휩쓰는 3대 떡상 포맷
| 순번 | 포맷명 | 플랫폼 | 핵심 특징 및 수익화 구조 |
| :--- | :--- | :--- | :--- |
| **1호** | **3D 인체·뇌과학 호기심 다큐**<br>(*"What Happens to Your Brain If..."*) | 미국 유튜브 쇼츠 | *"잠을 6시간 미만 자면 뇌가 스스로를 먹어치운다"* 등 내 몸에 일어나는 변화로 **초반 3초 유지율 80%+ 달성** |
| **2호** | **다크 럭셔리 ‘저장 폭탄’ 리스트**<br>(*"5 Websites That Feel Illegal to Know"*) | 미국 인스타 릴스 | 비 내리는 야간 포르쉐·펜트하우스 영상 위에 5개 꿀팁 리스트 카드를 띄워 **반복 재생(200%) + 보관함 저장(Save) + `"Comment LIST"` 자동 DM 제휴 수익화** |
| **3호** | **역사·미스터리 ‘What-If’ 시나리오**<br>(*"Could You Survive 24 Hours in Ancient Rome?"*) | 미국 유튜브 쇼츠 | 리들리 스콧 영화 같은 35mm 필름 질감의 시대극 영상 + 묵직한 다큐 내레이션으로 **시청 지속시간 극대화** |

---

## 🎬 2. Google Flow (`labs.google/fx/tools/flow`) 전용 모션 프롬프트 & 대본 3종 세트

Google Flow에서 **세로 비율(`9:16`)** 및 **`Frames to Video`**(또는 `Text to Video`)를 선택하고 아래 프롬프트를 순서대로 넣으시면 됩니다.

### 🧠 [포맷 1] 미국 유튜브 1위: 뇌과학 다큐 쇼츠
* **원테이크 성우 대본 (`en-US-AndrewMultilingualNeural`)**:
  > *"If you sleep less than six hours tonight, your brain literally begins to eat itself. While you are awake, your neurons produce toxic metabolic waste every single second. Normally, during deep sleep, spinal fluid flushes those toxins right out. But when you skip sleep, microglial cells go into overdrive and start destroying healthy synapses. Even worse, just five nights of poor sleep drops your memory retention by forty percent."*
* **Google Flow 컷별 모션 프롬프트 (4컷)**:
  1. **Cut 1 (`v1_shot1_eye.jpg`)**:
     `Extreme macro cinematic shot. The tired human eye slowly blinks and the pupil dilates as blue smartphone light flickers across the iris in a dark room at 3 AM. Subtle handheld camera movement, 85mm macro lens.`
  2. **Cut 2 (`v1_shot2_brain_scan.jpg`)**:
     `3D medical documentary animation. The camera slowly orbits around the translucent human head while glowing cyan and amber neural pathways pulse and fire rapidly across the cerebral cortex.`
  3. **Cut 3 (`v1_shot3_neurons.jpg`)**:
     `Microscopic 3D scientific CGI. Camera pushes forward through a dense forest of brain neurons as bright bio-electrical action potentials shoot along axons and toxic red particles accumulate around synapses.`
  4. **Cut 4 (`v1_shot4_mri.jpg`)**:
     `Handheld documentary shot inside a dark hospital neurology lab. A neurologist points at the glowing brain MRI scan on the monitor as the scan slices animate on screen.`

---

### 📸 [포맷 2] 미국 인스타 릴스 1위: 다크 럭셔리 리스트 릴스
* **원테이크 성우 대본 (`en-US-AndrewMultilingualNeural`)**:
  > *"Save this before you scroll. Here are five websites so powerful, they actually feel illegal to know in twenty twenty-six."*
* **Google Flow 컷별 모션 프롬프트 (2컷)**:
  1. **Cut 1 (`v2_shot1_porsche_rain.jpg`)**:
     `35mm Kodak Portra night cinematography. Driver POV inside a Porsche driving smoothly through rainy Manhattan streets at night. Raindrops streak across the windshield and warm city neon bokeh lights glide past.`
  2. **Cut 2 (`v2_shot2_macbook_desk.jpg`)**:
     `Slow cinematic dolly-in toward a sleek laptop on a dark walnut desk in a minimalist penthouse at night, while heavy rain streams down the floor-to-ceiling window overlooking the glowing city skyline.`

---

### 🏛️ [포맷 3] 미국 역사 다큐 1위: 고대 로마 24시간 생존 쇼츠
* **원테이크 성우 대본 (`en-US-BrianMultilingualNeural`)**:
  > *"Could you actually survive twenty-four hours in Ancient Rome? First, forget sleeping in. By dawn, a million people pack into muddy streets narrower than your hallway. If you get sick, doctors might prescribe crushed gladiator sweat as medicine. Need to brush your teeth? Romans used aged human urine to whiten their smiles. And if your apartment catches fire at night, there is no public fire department, unless you pay them on the spot."*
* **Google Flow 컷별 모션 프롬프트 (4컷)**:
  1. **Cut 1 (`v3_shot1_rome_street.jpg`)**:
     `Ridley Scott live-action movie shot on ARRI Alexa 65. The camera tracks forward through a crowded, muddy street in Ancient Rome's Subura district at dawn as citizens in linen tunics walk past and golden sunlight pierces through rising dust and smoke.`
  2. **Cut 2 (`v3_shot2_roman_coins.jpg`)**:
     `Cinema close-up. Weathered hands slowly pour ancient silver Roman denarii coins onto a rough wooden tavern table while warm oil lamp flames flicker in the background.`
  3. **Cut 3 (`v3_shot3_thermae_bath.jpg`)**:
     `Slow cinematic pan across an ancient Roman marble bathhouse as thick steam rises from the turquoise water and volumetric sunbeams shift through the high stone arches.`
  4. **Cut 4 (`v3_shot4_colosseum_dusk.jpg`)**:
     `Epic dusk cinema shot of the Roman Colosseum in 80 AD. Burning torches flicker in the wind along the stone arches as crowds move across the plaza and dramatic storm clouds drift overhead.`

---

## 💻 3. 내장 핵심 코드 (`flow_shorts_merger.py` V2 — 문장 호흡 컷 동기화 & 미국 2대 엔딩 지원)

집 PC에 이 문서 파일만 가져가셨을 때도 즉시 실행할 수 있는 V2 마스터링 명령어입니다:

* **미국 상위 1% 엔딩 2종 동시 렌더링 (기본값)**:
  * **버전 A (`punchline`)**: 묵직한 한 줄 결론(Takeaway) + 극장판 서브베이스 드롭(`Sub-Bass Boom`) + 1초 여운 페이드아웃 (`US_1A_Punchline_Ending_Shorts.mp4`)
  * **버전 B (`loop`)**: 끝문장이 0초 첫 문장으로 끊김 없이 이어지는 무한 루프 편집 (`US_1B_Seamless_Loop_Shorts.mp4`)

```powershell
# 두 가지 엔딩 버전(A: 펀치라인 여운 / B: 무한 루프) 동시 생성
python flow_shorts_merger.py --ending both

# 펀치라인 엔딩만 생성
python flow_shorts_merger.py --ending punchline

# 무한 루프 엔딩만 생성
python flow_shorts_merger.py --ending loop
```
*(전체 실행 파일, 사이트 2종, Flow 원본 클립 및 완성본 영상은 백업 압축 파일 안에 모두 들어 있습니다.)*
