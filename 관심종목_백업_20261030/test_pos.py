from engine.cleaner import RawDumpCleaner
from engine.extractor import FactExtractor

with open('raw_input_latest.txt', 'r', encoding='utf-8') as f:
    raw = f.read()

cleaner = RawDumpCleaner()
cleaned = cleaner.clean(raw)
extractor = FactExtractor()

m_06 = extractor.extract(cleaned, date_override='2026-10-06')
m_07 = extractor.extract(cleaned, date_override='2026-10-07')

print('=== 10-06 Interviews ===')
for sym, sheet in m_06.stocks.items():
    if sheet.interviews:
        print(f'{sym}:', [(i.speaker_name, i.source_media, i.source_url, i.core_quotes[:1]) for i in sheet.interviews])

print('\n=== 10-07 Interviews ===')
for sym, sheet in m_07.stocks.items():
    if sheet.interviews:
        print(f'{sym}:', [(i.speaker_name, i.source_media, i.source_url, i.core_quotes[:1]) for i in sheet.interviews])
