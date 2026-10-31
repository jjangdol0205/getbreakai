"""Raw Dump Text Automated Cleaning Pipeline.

Strips 8 distinct categories of web UI chrome, conversational chatter,
model artifacts, legal disclaimers, YouTube widget controls, and feedback buttons
while preserving 100% of underlying financial facts and URLs.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Pattern, Tuple


class RawDumpCleaner:
    """8-category deterministic regex cleaner for LLM / chatbot raw dumps."""

    # 1. UI Chrome & Navigation Elements
    RE_UI_CHROME: Pattern[str] = re.compile(
        r'^(?:Google\s+)?Gemini(?:\s+(?:Advanced|1\.5\s+Pro|1\.5\s+Flash|2\.0\s+Flash|Pro|Ultra))?\s*$'
        r'|^(?:새\s*대화|대화\s*시작|대화\s*내역|최근\s*대화|채팅창|고급|탐색|도움말|설정|업그레이드)\s*$'
        r'|^(?:Google\s*계정|프로필|로그인|앱\s*및\s*활동|메뉴|사이드바\s*(?:열기|닫기))\s*$'
        r'|^(?:Gemini에\s*질문하기|새로운\s*채팅|Gemini와의\s*대화|베타완료|알았음|실패)\s*$'
        r'|^(?:Google\s*アカウント|新しいチャット)\s*$'
        r'|^.*?(?:[-*•▶▪◆]\s*)?["\'“”‘’]?(?:Track|Summarize)\s+["\'“”‘’]?.*?developments["\'“”‘’]?\s+(?:is|are)\s+up\s+to\s+date\.?\s*$'
        # Resilient Gemini sidebar conversation history entries:
        r'|^(?:[-*•▶▪◆]\s*)?(?:(?:\d{4}[.\-/년]\s*\d{1,2}[.\-/월]\s*\d{1,2}[일.]?|\d{1,2}[.\-/월]\s*\d{1,2}[일.]?)\s*)?(?:'
        r'우버(?:의)?\s*(?:투자자\s*및\s*IB\s*시각\s*분석|투자\s*분석|기업\s*분석|주가\s*(?:흐름|동향|분석)|실적\s*(?:점검|분석)).*|'
        r'관심사\s*일기\s*정리.*|'
        r'모빌아이\s*(?:투자\s*분석\s*리포트.*|투자\s*분석|기업\s*분석|주가\s*(?:흐름|동향|분석)?|실적\s*(?:점검|분석)).*|'
        r'플루언스\s*에너지\s*(?:투자\s*분석|기업\s*분석|주가\s*(?:흐름|동향|분석)?|실적\s*(?:점검|분석|호조)?|.*?분석).*|'
        r'플루언스에너지(?:\([A-Z]+\))?\s*(?:투자\s*분석|기업\s*분석|주가\s*(?:흐름|동향|분석)?|실적\s*(?:점검|분석|호조)?|.*?분석).*|'
        r'업스타트\s*(?:홀딩스)?\s*(?:투자\s*분석|기업\s*분석|주가\s*(?:흐름|동향|분석)?|대출\s*실적.*?분석|실적\s*(?:점검|분석|호조)?|.*?분석).*|'
        r'업스타트홀딩스\s*(?:투자\s*분석|기업\s*분석|주가\s*(?:흐름|동향|분석)?|실적\s*(?:점검|분석|호조)?|.*?분석).*|'
        r'SK\s*스퀘어\s*(?:투자\s*분석|기업\s*분석|주가\s*(?:흐름|동향|분석)|실적\s*(?:점검|분석)).*|'
        r'인페이즈\s*에너지\s*(?:기업\s*분석|투자\s*분석|주가\s*(?:흐름|동향|분석)|실적\s*(?:점검|분석)).*|'
        r'주요\s*AI\s*리더\s*인터뷰\s*추적.*|'
        r'셀시우스\s*(?:홀딩스\s*)?(?:기업\s*분석|투자\s*분석|주가\s*(?:흐름|동향|분석)?|실적\s*(?:점검|분석|호조)?).*|'
        r'Ai\s*시대\s*이준이\s*교육.*|'
        r'인생조언.*|'
        r'자산\s*50억.*|'
        r'YouTube\s+Video\s+Content\s+Analysis.*|'
        r'SK\s*하이닉스\s*ADR\s*투자\s*분석.*|'
        r'.*?주가\s*(?:흐름|변동|마감).*?(?:분석함|완료함).*|'
        r'.*?Analyzed\s+(?:Celsius|Enphase|Wall\s*Street).*|'
        r'.*?Summarized\s+.*|'
        r'.*?Analyzing\s+recent\s+.*'
        r')\s*$'
        r'|^(?:[-*•▶▪◆]\s*)?["\'“”‘’]?(?:Summarize|Track)\s+.*?[•·]\s*\d{1,2}월\s*\d{1,2}[일]?,?\s*(?:오전|오후|\d{1,2}:\d{2}).*?$'
        r'|^(?:[-*•▶▪◆]\s*)?["\'“”‘’]?(?:Track|Summarize)\s+["\'“”‘’]?(?:Uber|SK\s*hynix|SK\s*하이닉스|Mobileye|모빌아이|Celsius|셀시우스|Enphase|엔페이즈|인페이즈|Fluence|플루언스|Upstart|업스타트|SK\s*Square|SK\s*스퀘어).*?$'
        r'|^(?:[-*•▶▪◆]\s*)?▶️?\s*(?:주요\s*)?(?:코멘트|Q&A)\s*$',
        re.IGNORECASE
    )

    # 2. Model Markers, Timestamps & Watermarks
    RE_TIMESTAMPS_MODEL: Pattern[str] = re.compile(
        r'^(?:수정됨|Edited|방금\s*전?|어제|오늘|\d+\s*(?:시간|분|초|일)\s*전)\s*$'
        r'|^(?:(?:오전|오후)\s*\d{1,2}:\d{2}(?::\d{2})?|\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM|오전|오후))\s*$'
        r'|^\d{4}[\.\-/]\s*\d{1,2}[\.\-/]\s*\d{1,2}\.?(?:\s*(?:오전|오후)?\s*\d{1,2}:\d{2}(?::\d{2})?)?\s*$'
        r'|^(?:답변|버전)\s*\d+(?:\s*/\s*\d+)?\s*$'
        r'|^다른\s*답안\s*보기\s*$',
        re.IGNORECASE
    )

    # 3. User Prompts & Conversational Chatter
    # Note: '질문' is deliberately excluded from prompts to protect interview questions (질문: ...)
    RE_USER_PROMPT: Pattern[str] = re.compile(
        r'^(?:나|User|You|사용자|프롬프트|System)\s*:\s*.*$'
        r'|^</?(?:USER_REQUEST|user_request|prompt)>\s*$'
        r'|^/[a-zA-Z0-9_\-]+(?:\s+.*)?$',
        re.IGNORECASE
    )
    RE_CONVERSATIONAL_PREAMBLE: Pattern[str] = re.compile(
        r'^(?:네[,\s]+)?(?:요청하신|문의하신|물어보신|질문해주신|다음은|\d{4}년)?.*?'
        r'(?:시황\s*브리핑|브리핑|마감\s*시황|시황|동향|요약)'
        r'.*?'
        r'(?:입니다|\s*정리해\s*드립니다|\s*안내해\s*드립니다|다음과\s*같습니다|알려드립니다|결과입니다)[:.]?\s*$'
        r'|^Here\s+is\s+(?:the\s+)?(?:daily\s+)?(?:market\s+)?(?:summary|report).*?:?\s*$'
        r'|^Hope\s+this\s+helps.*$'
        r'|^(?:도움이\s*되셨기를\s*(?:바랍니다|원합니다)?.*|'
        r'추가\s*(?:궁금하신\s*(?:점이나\s*)?|질문이나\s*문의사항이\s*|질문이\s*)(?:있으시면|있으시다면|있다면)?\s*언제든(?:지)?\s*(?:편하게\s*)?(?:말씀|문의).*|'
        r'언제든(?:지)?\s*(?:편하게\s*)?(?:말씀(?:해\s*주세요|해\s*주시기\s*바랍니다|하여\s*주세요)|문의(?:해\s*주세요|바랍니다)).*)$',
        re.IGNORECASE
    )

    # 4. Legal, Regulatory & Financial Disclaimers
    RE_DISCLAIMERS: Pattern[str] = re.compile(
        r'^Gemini(?:는|\s+may).*?(?:확인하세요|주의하세요|double-check|표시할\s*수\s*있습니다|실수를\s*할\s*수\s*있습니다).*?$'
        r'|^(?:[-*•▶▪◆]\s*)?(?:본\s*(?:자료|정보|리포트|내용|글)는|※\s*본\s*내용은)?\s*'
        r'(?:'
        r'.*?(?:정보\s*제공|투자\s*(?:권유|추천)|투자\s*판단|단순\s*참고).*?'
        r'(?:'
        r'투자\s*권유를\s*위한\s*것이\s*아닙니다|'
        r'투자\s*권유가\s*아닙니다|'
        r'권유를\s*위한\s*것이\s*아닙니다|'
        r'위한\s*것이\s*아닙니다|'
        r'단순\s*참고용입니다|'
        r'참고용입니다|'
        r'참고용으로만\s*활용|'
        r'(?:최종\s*)?책임(?:은)?\s*(?:투자자\s*)?본인에게\s*(?:있습니다|귀속됩니다)|'
        r'(?:어떠한\s*)?책임(?:도\s*)?지지\s*않습니다|'
        r'책임을\s*부담하지\s*않습니다|'
        r'보증하지\s*않습니다'
        r')'
        r')[.:]?\s*$'
        r'|^(?:[-*•▶▪◆]\s*)?.*?(?:'
        r'정보\s*제공만을\s*목적으로\s*하며|'
        r'특정\s*증권의\s*매수[·\s]*매도를\s*추천하거나|'
        r'투자\s*결과에\s*대한\s*최종적인\s*책임은\s*투자자\s*본인에게|'
        r'어떠한\s*경우에도\s*법적\s*책임\s*소재의\s*증빙\s*자료|'
        r'공개\s*실적발표\s*내용으로\s*별도의\s*승인절차\s*없이\s*제공'
        r').*?$'
        r'|^(?:Google\s*)?(?:개인정보처리방침|서비스\s*약관|약관\s*및\s*정책|라이선스)\s*$'
        r'|^YouTube\s+video\s+views\s+will\s+be\s+stored\s+in\s+your\s+YouTube\s+History.*?$',
        re.IGNORECASE
    )

    # 5. YouTube / Media Embed & Interactive Widget Noise
    RE_MEDIA_WIDGET: Pattern[str] = re.compile(
        r'^(?:동영상\s*시청\s*시\s*)?YouTube(?:\s*(?:서비스\s*약관(?:이\s*적용됩니다)?|약관이\s*적용됩니다|에서\s*시청))?[.:]?\s*$'
        r'|^(?:자막|음소거(?:\s*해제)?|재생|일시중지|전체화면|영화관\s*모드|동영상\s*더보기|재생목록)\s*$'
        r'|^(?:구독|구독중|알림\s*설정|클립|저장|오프라인\s*저장)\s*$'
        r'|^(?:댓글\s*[\d,]+\s*개|정렬\s*기준|답글(?:\s*[\d,]+\s*개)?|실시간\s*채팅|실시간\s*스트림)\s*$'
        r'|^@[\w\.\-]+(?:\s+\d+[일주월년초분시간]+\s*전)?\s*$',
        re.IGNORECASE
    )

    # 6. Feedback, Export & Action Button Tokens
    RE_ACTION_BUTTONS: Pattern[str] = re.compile(
        r'^(?:답변\s*)?(?:복사|복사됨|공유|공유하기|수정|수정하기|다시\s*생성|새로고침|더보기)\s*$'
        r'|^(?:더보기\s*)?예약은\s*지정된\s*시간\s*근처에\s*실행되며.*?$'
        r'|^(?:실행하는\s*경우|확인\s*사항|작업|스케줄\s*명칭)\s*:\s*$'
        r'|^(?:Whenever\s*new|Every\s*day).*?$'
        r'|^(?:Google\s*Docs로\s*내보내기|Gmail로\s*임시보관(?:\s*작성)?|스프레드시트로\s*내보내기|내보내기)\s*$'
        r'|^(?:좋아요|싫어요|좋은\s*답변|부정확한\s*답변|피드백\s*제출)\s*$'
        r'|^(?:자세히\s*알아보기|출처\s*확인|관련\s*콘텐츠|웹\s*검색\s*결과)\s*$'
        r'|^(?:共有|回答を再生成)\s*$',
        re.IGNORECASE
    )

    # 7. Inline Citations & Search Footnotes
    RE_INLINE_CITATIONS: Pattern[str] = re.compile(
        r'\[(?:\d+|출처|source|링크|G)\](?!\()',
        re.IGNORECASE
    )
    RE_SEARCH_CHIPS: Pattern[str] = re.compile(
        r'^(?:G\s+)?(?:검색어\s*:|출처\s*\d+\s*개|관련\s*검색어|Google\s*Search).*?$',
        re.IGNORECASE
    )

    # Date discovery regex
    RE_DATE_HINT: Pattern[str] = re.compile(
        r'(\d{4})[.\-/년]\s*(\d{1,2})[.\-/월]\s*(\d{1,2})[일]?'
    )

    def __init__(self) -> None:
        self.last_metadata: Dict[str, Any] = {}

    def extract_date_hint(self, text: str) -> str:
        """Attempts to extract the most prominent date (YYYY-MM-DD) from the text."""
        match = self.RE_DATE_HINT.search(text)
        if match:
            year, month, day = match.group(1), match.group(2).zfill(2), match.group(3).zfill(2)
            return f"{year}-{month}-{day}"
        return ""

    def clean(self, raw_text: str) -> str:
        """Cleans raw text and returns cleaned string."""
        cleaned_text, _ = self.clean_with_metadata(raw_text)
        return cleaned_text

    def clean_with_metadata(self, raw_text: str) -> Tuple[str, Dict[str, Any]]:
        """Cleans raw text and returns (cleaned_text, metadata)."""
        metadata: Dict[str, Any] = {
            "original_length": len(raw_text),
            "removed_categories": {
                "ui_chrome": 0,
                "timestamps": 0,
                "user_prompt": 0,
                "disclaimers": 0,
                "media_widgets": 0,
                "action_buttons": 0,
                "search_chips": 0,
                "inline_citations": 0,
            },
            "date_hint": self.extract_date_hint(raw_text),
        }

        # Step 8.1: Strip BOM, zero-width spaces, BiDi overrides/isolates (\u202A-\u202E, \u2066-\u2069), variation selectors (\uFE0E, \uFE0F), LRM/RLM/Word-joiner, normalize NBSP
        text = re.sub(r'[\u200B\u200C\u200E\u200F\u202A-\u202E\u2060\u2066-\u2069\uFE0E\uFE0F\uFEFF]', '', raw_text)
        text = text.replace('\u00A0', ' ')

        # Strip ZWJ (\u200D) unless connecting emoji characters in compound emoji sequences
        text = re.sub(r'(?<=[가-힣a-zA-Z0-9\s.,!?:;\'"()\[\]{}<>/\\|`~@#$%^&*+=_-])\u200D|\u200D(?=[가-힣a-zA-Z0-9\s.,!?:;\'"()\[\]{}<>/\\|`~@#$%^&*+=_-])', '', text)
        text = re.sub(r'^\u200D+|\u200D+$', '', text)
        text = re.sub(r'\u200D{2,}', '', text)

        # Peel YouTube terms preamble if concatenated at line start before media link
        text = re.sub(
            r'(?m)^(?:YouTube\s+동영상\s+조회\s+내역은\s+내\s+YouTube\s+기록에\s+저장되며[^\n]*?사용됩니다\.|'
            r'YouTube\s*(?:서비스\s*)?약관이\s*적용됩니다\.?)\s*',
            '',
            text
        )

        # Strip decorative emoji bullets from markdown headers
        text = re.sub(r'(?m)^(\s*#{1,6}\s*)[▶️◀️⏩⏪►]\s*', r'\1', text)

        # Step 8.2: Remove enclosing markdown document code fences (4-backtick and 3-backtick)
        text = re.sub(r'(?m)^[ \t]*`{4,}(?:markdown)?\s*$\n?', '', text, flags=re.IGNORECASE)
        text = re.sub(r'(?m)^[ \t]*`{3}(?:markdown)?\s*$\n?', '', text, flags=re.IGNORECASE)

        # Step 7.1: Remove inline citations like [1], [2], [출처] while preserving markdown links
        text, n_citations = self.RE_INLINE_CITATIONS.subn('', text)
        metadata["removed_categories"]["inline_citations"] = n_citations

        lines = text.splitlines()
        cleaned_lines: List[str] = []

        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                cleaned_lines.append("")
                continue

            # Peel off leading bullet markers to check content against noise rules
            content_stripped = re.sub(r'^[ \t]*[-*•▶▪◆]\s*', '', line_stripped)

            # Check 1: UI Chrome
            if self.RE_UI_CHROME.match(line_stripped) or self.RE_UI_CHROME.match(content_stripped):
                metadata["removed_categories"]["ui_chrome"] += 1
                continue

            # Check 2: Model Timestamps & Markers
            if self.RE_TIMESTAMPS_MODEL.match(line_stripped) or self.RE_TIMESTAMPS_MODEL.match(content_stripped):
                metadata["removed_categories"]["timestamps"] += 1
                continue

            # Check 3: User Prompts & Conversational Chatter
            if (self.RE_USER_PROMPT.match(line_stripped) or self.RE_CONVERSATIONAL_PREAMBLE.match(line_stripped)
                    or self.RE_USER_PROMPT.match(content_stripped) or self.RE_CONVERSATIONAL_PREAMBLE.match(content_stripped)):
                metadata["removed_categories"]["user_prompt"] += 1
                continue

            # Check 4: Disclaimers (evaluated on both raw and bullet-stripped candidate)
            if self.RE_DISCLAIMERS.match(line_stripped) or self.RE_DISCLAIMERS.match(content_stripped):
                metadata["removed_categories"]["disclaimers"] += 1
                continue

            # Check 5: Media Widgets (Unless line contains an actual URL)
            if "http://" not in line_stripped and "https://" not in line_stripped:
                if self.RE_MEDIA_WIDGET.match(line_stripped) or self.RE_MEDIA_WIDGET.match(content_stripped):
                    metadata["removed_categories"]["media_widgets"] += 1
                    continue

            # Check 6: Action Buttons
            if self.RE_ACTION_BUTTONS.match(line_stripped) or self.RE_ACTION_BUTTONS.match(content_stripped):
                metadata["removed_categories"]["action_buttons"] += 1
                continue

            # Check 7: Search Chips
            if self.RE_SEARCH_CHIPS.match(line_stripped) or self.RE_SEARCH_CHIPS.match(content_stripped):
                metadata["removed_categories"]["search_chips"] += 1
                continue

            # Step 8.3: Bullet normalization for preserved substantive content
            normalized_line = re.sub(r'^[ \t]*[•▶▪◆*]\s*', '- ', line)
            cleaned_lines.append(normalized_line)

        # Recombine and collapse 3+ consecutive newlines to 2 newlines
        result = "\n".join(cleaned_lines)
        result = re.sub(r'\n{3,}', '\n\n', result)
        result = result.strip()

        metadata["cleaned_length"] = len(result)
        self.last_metadata = metadata
        return result, metadata


def clean_raw_dump(raw_text: str) -> Tuple[str, Dict[str, Any]]:
    """Functional convenience wrapper for RawDumpCleaner."""
    cleaner = RawDumpCleaner()
    return cleaner.clean_with_metadata(raw_text)


def strip_markdown_links(text: str) -> str:
    """Converts markdown links [Anchor Text](URL) to plain Anchor Text."""
    if not text:
        return ""
    # 1. Replace [text](url) with text
    cleaned = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # 2. Remove parenthesized standalone URLs e.g. (https://...)
    cleaned = re.sub(r'\(\s*https?://[^\s)]+\s*\)', '', cleaned)
    # 3. Clean leftover parentheses wrapping only whitespace
    cleaned = re.sub(r'\s*\(\s*\)', '', cleaned)
    # 4. Strip leading punctuation artifacts like ". " or "- " while preserving negative numbers (-2.26%, -$5.00, -1,000원)
    if not re.match(r'^[+\-]\s*[\$₩\d]', cleaned):
        cleaned = re.sub(r'^[.\-–—*•\s]+', '', cleaned).strip()
    return cleaned

