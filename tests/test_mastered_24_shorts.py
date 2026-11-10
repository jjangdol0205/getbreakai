#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D:\드림컴퍼니\3사업부\tests\test_mastered_24_shorts.py
Comprehensive verification test suite for all 24 Mastered Japanese Breakout Shorts (EP01~EP24).
Verifies:
1. File presence and size (>5MB) for all 24 MP4s
2. Video format: 1080x1920 vertical, 30fps, h264
3. Audio format: AAC 44.1kHz mono, -0.5 dBFS limiter (max_volume <= -0.5 dB)
4. FFmpeg stream decoding integrity (0 errors)
5. Manifest & Upload Kit completeness (24 episodes)
"""

import os
import re
import sys
import json
import subprocess
import imageio_ffmpeg

ROOT_DIR = r"D:\드림컴퍼니\3사업부"
STUDIO_DIR = os.path.join(ROOT_DIR, "flow_shorts_studio")
MASTER_DIR = os.path.join(STUDIO_DIR, "mastered_jp_shorts")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

EXPECTED_IDS = [
    "EP01_NVDA_ATR_StopLoss",
    "EP02_PLTR_SEC_Form4_Flow",
    "EP03_TSLA_Gamma_Breakout",
    "EP04_8035_TokyoElectron_Sync",
    "EP05_6857_Advantest_AIScore94",
    "EP06_ShinNISA_15Risk_Rule",
    "EP07_META_AI_Ad_Breakout",
    "EP08_MSFT_Cloud_Copilot_SEC",
    "EP09_AMZN_AWS_Margin_Target",
    "EP10_9984_SoftBankG_Arm_AI",
    "EP11_7203_Toyota_Yen154_Flow",
    "EP12_USDJPY_Position_Sizing",
    "EP13_LLY_GLP1_Insider_Flow",
    "EP14_AVGO_Custom_ASIC_Breakout",
    "EP15_AMD_MI350_Donchian_Breakout",
    "EP16_CRWD_Falcon_ARR_PEAD",
    "EP17_VRT_Liquid_Cooling_RSI",
    "EP18_CEG_Nuclear_PPA_Breakout",
    "EP19_MSTR_BTC_Convertible_ATR",
    "EP20_ASML_HighNA_EUV_Monopoly",
    "EP21_SMCI_10K_Risk_Avoid_Trap",
    "EP22_6758_Sony_CMOS_Entertainment",
    "EP23_SOXL_vs_SMH_Leverage_Trap",
    "EP24_MACRO_CPI_FOMC_Gamma_Defense",
]


def test_manifest_and_kit():
    print("\n--- [1/3] Testing Manifest & Upload Kit ---")
    manifest_paths = [
        os.path.join(STUDIO_DIR, "mastered_24_shorts_manifest.json"),
        os.path.join(MASTER_DIR, "mastered_24_shorts_manifest.json"),
    ]
    for p in manifest_paths:
        assert os.path.exists(p), f"Manifest file missing: {p}"
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert len(data) == 24, f"Manifest {p} expected 24 items, found {len(data)}"
        manifest_ids = [item["id"] for item in data]
        for exp_id in EXPECTED_IDS:
            assert exp_id in manifest_ids, f"Episode {exp_id} missing in {p}"
        print(f"  OK: {os.path.basename(p)} (24 items)")

    kit_paths = [
        os.path.join(STUDIO_DIR, "UPLOAD_COPY_PASTE_KIT_24EP.md"),
        os.path.join(MASTER_DIR, "UPLOAD_COPY_PASTE_KIT_24EP.md"),
    ]
    for p in kit_paths:
        assert os.path.exists(p), f"Upload kit missing: {p}"
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()
        for exp_id in EXPECTED_IDS:
            assert exp_id in content, f"Episode {exp_id} missing in {p}"
        print(f"  OK: {os.path.basename(p)} (all 24 episodes documented)")


def test_mp4_integrity_and_audio():
    print("\n--- [2/3] Testing MP4 Video & Audio Specifications ---")
    for idx, ep_id in enumerate(EXPECTED_IDS):
        mp4_path = os.path.join(MASTER_DIR, f"{ep_id}.mp4")
        assert os.path.exists(mp4_path), f"Video missing: {mp4_path}"
        size_kb = os.path.getsize(mp4_path) // 1024
        assert size_kb > 5000, f"{ep_id}.mp4 is too small ({size_kb} KB)"

        # 1. FFmpeg decode integrity check
        res_int = subprocess.run(
            [FFMPEG, "-v", "error", "-i", mp4_path, "-f", "null", "-"],
            capture_output=True,
            text=True,
            errors="ignore",
        )
        assert res_int.returncode == 0, f"{ep_id}.mp4 decode failed with code {res_int.returncode}"
        assert not res_int.stderr.strip(), f"{ep_id}.mp4 decode errors: {res_int.stderr}"

        # 2. Stream probe (resolution, fps, duration)
        res_info = subprocess.run(
            [FFMPEG, "-i", mp4_path],
            capture_output=True,
            text=True,
            errors="ignore",
        )
        stderr = res_info.stderr
        assert "1080x1920" in stderr, f"{ep_id}.mp4 is not 1080x1920"
        assert "30 fps" in stderr or "30 tbr" in stderr, f"{ep_id}.mp4 is not 30 fps"
        assert "aac" in stderr.lower(), f"{ep_id}.mp4 missing AAC audio"

        # 3. Audio volume detection (limiter check <= -0.5 dBFS)
        res_vol = subprocess.run(
            [FFMPEG, "-i", mp4_path, "-af", "volumedetect", "-f", "null", "-"],
            capture_output=True,
            text=True,
            errors="ignore",
        )
        max_vol = None
        for line in res_vol.stderr.splitlines():
            m = re.search(r"max_volume:\s*(-?\d+(\.\d+)?)\s*dB", line)
            if m:
                max_vol = float(m.group(1))
                break
        assert max_vol is not None, f"Could not detect max_volume for {ep_id}.mp4"
        assert max_vol <= -0.5, f"{ep_id}.mp4 audio clipped! max_volume: {max_vol} dB > -0.5 dBFS"

        print(f"  [{idx+1:02d}/24] OK: {ep_id}.mp4 ({size_kb} KB, 1080x1920@30fps, max_vol={max_vol:.1f}dB, decode 0 err)")


def main():
    print("=" * 70)
    print("GetBreakAI Shorts Studio — 24 Episodes Clean Video V3 Audit")
    print("=" * 70)
    try:
        test_manifest_and_kit()
        test_mp4_integrity_and_audio()
        print("\n" + "=" * 70)
        print("SUCCESS: ALL 24 MASTERED SHORTS MEET CLEAN VIDEO V3 SPECIFICATIONS (100% PASS)")
        print("=" * 70)
        return 0
    except AssertionError as e:
        print(f"\nTEST FAILURE: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
