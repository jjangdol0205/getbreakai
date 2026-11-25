let pwCurrentScreenJp = 0;
    let pwCurrentStepJp = 1;
    let pwAnswersJp = {
      objective: 'balanced',
      scale: 1800,
      comfort: 'dd18',
      techMix: 'tech_high'
    };

    function toggleJpTheme() {
      const cur = document.documentElement.getAttribute('data-jp-theme') || 'light';
      const next = cur === 'light' ? 'dark' : 'light';
      document.documentElement.setAttribute('data-jp-theme', next);
      try { localStorage.setItem('gb_jp_theme', next); } catch (_) {}
    }

    let gbaLiveTempScoreJp = 3.8;
    let gbaLiveTempDateJp = '2026-11-24';

    function hydrateGbaLiveTempBadgeJp() {
      const txtEl = document.getElementById('gbaLiveTempTextJp');
      if (!txtEl || typeof fetch !== 'function') return;
      const applyData = function(ov) {
        if (!ov || typeof ov !== 'object') return;
        const dt = String(ov.date || ov.as_of_date || '').trim();
        const rawSc = (ov.fg_score !== undefined) ? ov.fg_score : ((ov.fear_greed_score !== undefined) ? ov.fear_greed_score : ov.score);
        const numSc = Number(rawSc);
        if (!dt || isNaN(numSc)) return;
        const sc = Math.round(numSc * 10) / 10;
        gbaLiveTempScoreJp = sc;
        gbaLiveTempDateJp = dt;
        let reg = '中立圏';
        if (sc <= 25) reg = '極度の恐怖圏';
        else if (sc <= 44) reg = '慎重・警戒圏';
        else if (sc <= 55) reg = '中立圏';
        else if (sc <= 75) reg = '強気圏';
        else reg = '過熱注意圏';
        txtEl.textContent = '最新データ基準日：' + dt + ' ・ SMH恐怖と強欲指数：' + Number(sc).toFixed(1) + ' / 100（' + reg + '） →';
        renderGbaScreen4VaultJp();
      };
      fetch('/data/smh_fg_latest.json?v=' + Math.floor(Date.now() / 300000), { cache: 'no-cache' })
        .then(function(r) { return r.ok ? r.json() : Promise.reject(); })
        .then(applyData)
        .catch(function() {
          fetch('/static_api/semi_overview.json', { cache: 'no-cache' })
            .then(function(r2) { return r2.ok ? r2.json() : null; })
            .then(applyData)
            .catch(function() {});
        });
    }

    function loadPwSavedAnswersJp() {
      try {
        const raw = localStorage.getItem('gba_pw_stepup_answers_v1');
        if (raw) {
          const parsed = JSON.parse(raw);
          if (parsed && typeof parsed === 'object') {
            pwAnswersJp = Object.assign(pwAnswersJp, parsed);
          }
        }
      } catch (_) {}
    }

    function computePwBaselineJp() {
      const obj = pwAnswersJp.objective || 'balanced';
      const comfort = pwAnswersJp.comfort || 'dd18';
      const scale = Number(pwAnswersJp.scale) || 1800;

      let smh = 55;
      let xlv = 35;
      let cushion = 10;

      if (obj === 'growth') {
        smh = 68; xlv = 27; cushion = 5;
      } else if (obj === 'preservation') {
        smh = 35; xlv = 45; cushion = 20;
      }

      if (comfort === 'dd10') {
        smh = Math.max(25, smh - 12);
        xlv = xlv + 5;
        cushion = 100 - smh - xlv;
      } else if (comfort === 'dd25') {
        cushion = Math.max(0, cushion - 5);
        smh = smh + 8;
        xlv = 100 - smh - cushion;
      }

      const objLbl = obj === 'growth' ? '半導体成長統計ケース' : (obj === 'preservation' ? '安全クッション重視ケース' : '標準統計ケース');
      const scaleLbl = scale >= 5000 ? '5,000万円+' : (scale === 1800 ? '1,800万円（新NISA生涯枠）' : scale.toLocaleString() + '万円');
      const ddLbl = comfort === 'dd10' ? '穏やか変動レンジ' : (comfort === 'dd25' ? '長期成長レンジ' : '標準2本柱レンジ');

      const smhMan = Math.round(scale * smh / 100);
      const xlvMan = Math.round(scale * xlv / 100);
      const cushMan = Math.max(0, scale - smhMan - xlvMan);
      const estDd = comfort === 'dd10' ? '-17.8%（回復目安 約13ヶ月）' : (comfort === 'dd25' ? '-31.2%（回復目安 約22ヶ月）' : '-24.5%（回復目安 約18ヶ月）');

      return {
        smh: smh,
        xlv: xlv,
        cushion: cushion,
        smhMan: smhMan,
        xlvMan: xlvMan,
        cushMan: cushMan,
        estDd: estDd,
        headline: 'SMH ' + smh + '% ・ XLV ' + xlv + '% ・ 個人向け国債／SGOV ' + cushion + '%',
        summary: '比較条件：' + objLbl + ' ・ ' + scaleLbl + ' ・ ' + ddLbl
      };
    }

    function getSavedGbaEmailJp() {
      try {
        if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.getLocalMember === 'function') {
          const m = window.DreamCompanyCRM.getLocalMember('GBA');
          if (m && m.email) return String(m.email).trim().toLowerCase();
        }
        return String(localStorage.getItem('gba_jp_free_email') || localStorage.getItem('gb_free_member_email') || '').trim().toLowerCase();
      } catch (_) {
        return '';
      }
    }

    function syncPwStage2UiJp() {
      const b = computePwBaselineJp();
      const sumEl = document.getElementById('pwProfileSummaryJp');
      if (sumEl) sumEl.textContent = b.summary;
      const hlEl = document.getElementById('pwUnlockedRatioHeadlineJp');
      if (hlEl) hlEl.textContent = b.headline;

      const pSmh = document.getElementById('pwPctSmhJp');
      const pXlv = document.getElementById('pwPctXlvJp');
      const pCush = document.getElementById('pwPctCushionJp');
      if (pSmh) pSmh.textContent = b.smh + '%';
      if (pXlv) pXlv.textContent = b.xlv + '%';
      if (pCush) pCush.textContent = b.cushion + '%';

      const aSmh = document.getElementById('pwAmtSmhJp');
      const aXlv = document.getElementById('pwAmtXlvJp');
      const aCush = document.getElementById('pwAmtCushionJp');
      if (aSmh) aSmh.textContent = '米国半導体現物ETF（約' + b.smhMan.toLocaleString() + '万円）';
      if (aXlv) aXlv.textContent = '米国ヘルスケア現物ETF（約' + b.xlvMan.toLocaleString() + '万円）';
      if (aCush) aCush.textContent = '個人向け国債／特定口座SGOV（約' + b.cushMan.toLocaleString() + '万円）';

      const ddCmp = document.getElementById('pwHistDdCompareJp');
      if (ddCmp) ddCmp.textContent = b.estDd;

      const bar = document.getElementById('pwRatioVisualBarJp');
      if (bar) {
        bar.innerHTML =
          '<span style="width:' + b.smh + '%;background:#0F172A;"></span>' +
          '<span style="width:' + b.xlv + '%;background:#065F46;"></span>' +
          '<span style="width:' + b.cushion + '%;background:#94A3B8;"></span>';
      }

      const em = getSavedGbaEmailJp();
      const inp = document.getElementById('gba-jp-club-email');
      if (inp && em && !inp.value) inp.value = em;
    }

    function fmtManYenJp(n) {
      return Math.round(Number(n) || 0).toLocaleString('ja-JP') + '万円';
    }

    function renderGbaScreen4VaultJp() {
      const b = computePwBaselineJp();
      const inp = document.getElementById('gbaCustomManYenInput');
      const totalMan = Math.max(100, Number(inp && inp.value ? inp.value : pwAnswersJp.scale) || 1800);
      if (inp && Number(inp.value) !== totalMan) inp.value = String(totalMan);

      const smhMan = Math.round(totalMan * b.smh / 100);
      const xlvMan = Math.round(totalMan * b.xlv / 100);
      const cushMan = Math.max(0, totalMan - smhMan - xlvMan);

      const yenTbl = document.getElementById('gbaScreen4YenTable');
      if (yenTbl) {
        yenTbl.innerHTML =
          '<div class="pw-table-header"><span class="pw-table-title">第1章 — 円建て世帯規模ワークシート（想定総額：' + fmtManYenJp(totalMan) + '）</span><span class="pw-table-meta">現物1倍ETF・国債過去統計</span></div>' +
          '<div class="pw-table-scroll"><table class="pw-sim-table"><thead><tr><th>構成区分</th><th>過去統計比率</th><th>円建て目安金額</th><th>2000〜2025年統計における役割</th></tr></thead><tbody>' +
          '<tr><td><strong>SMH</strong>（米国半導体現物ETF）</td><td>' + b.smh + '%</td><td style="font-variant-numeric:tabular-nums;font-weight:700;">' + fmtManYenJp(smhMan) + '</td><td>AI・半導体技術革新による長期成長エンジン</td></tr>' +
          '<tr><td><strong>XLV</strong>（米国ヘルスケア現物ETF）</td><td>' + b.xlv + '%</td><td style="font-variant-numeric:tabular-nums;font-weight:700;">' + fmtManYenJp(xlvMan) + '</td><td>景気後退局面でも底堅い生活必須医療キャッシュフロー</td></tr>' +
          '<tr class="is-featured"><td><strong>個人向け国債（変動10年）／SGOV</strong></td><td>' + b.cushion + '%</td><td style="font-variant-numeric:tabular-nums;font-weight:700;">' + fmtManYenJp(cushMan) + '</td><td>暴落時に株式を売却せず生活費を守る安全クッション</td></tr>' +
          '</tbody></table></div>';
      }

      const tech49 = Math.round(totalMan * 0.49);
      const sp35 = Math.round(totalMan * 0.35);
      const studyPct = Math.round((0.46 * (b.smh / 100) + 0.16 * (b.xlv / 100)) * 1000) / 10;
      const studyLoss = Math.round(totalMan * (studyPct / 100));
      const stressEl = document.getElementById('gbaScreen4StressTest');
      if (stressEl) {
        stressEl.innerHTML =
          '<div class="pw-table-header"><span class="pw-table-title">第2章 — -35%暴落局面ストレステスト（' + fmtManYenJp(totalMan) + ' 基準）</span><span class="pw-table-meta">下落耐性比較</span></div>' +
          '<div class="pw-table-scroll"><table class="pw-sim-table"><thead><tr><th>比較ケース</th><th>想定下落幅</th><th>評価変動額</th><th>残存評価額＆安全資産クッション</th></tr></thead><tbody>' +
          '<tr><td>半導体単独（SMH 100%）</td><td class="pw-dd-neg">-49.0%</td><td class="pw-dd-neg">-' + fmtManYenJp(tech49) + '</td><td>' + fmtManYenJp(totalMan - tech49) + '（国債バッファ 0円）</td></tr>' +
          '<tr><td>S&amp;P 500単独</td><td class="pw-dd-neg">-35.0%</td><td class="pw-dd-neg">-' + fmtManYenJp(sp35) + '</td><td>' + fmtManYenJp(totalMan - sp35) + '（国債バッファ 0円）</td></tr>' +
          '<tr class="is-featured"><td><strong>選択中の SMH &times; XLV ＋ 安全資産ケース</strong></td><td class="pw-eff-pos">-' + studyPct.toFixed(1) + '%</td><td class="pw-eff-pos">-' + fmtManYenJp(studyLoss) + '</td><td><strong>' + fmtManYenJp(totalMan - studyLoss) + '（安全資産 ' + fmtManYenJp(cushMan) + ' 無傷）</strong></td></tr>' +
          '</tbody></table></div>' +
          '<p class="pw-table-note">※教育目的の過去統計シミュレーションです。個人向け国債（変動10年）や短期米国債ETF（SGOV）を別枠で確保しておくことで、市場回復までの約18ヶ月間も落ち着いて保有を継続しやすくなります。</p>';
      }

      const equityTotalMan = smhMan + xlvMan;
      const nisaGrowthSlot = Math.min(1200, equityTotalMan);
      const equityOverflowAfterGrowth = Math.max(0, equityTotalMan - nisaGrowthSlot);
      const nisaTsumitateSlot = Math.min(600, equityOverflowAfterGrowth);
      const overflowTaxableEquityMan = Math.max(0, equityOverflowAfterGrowth - nisaTsumitateSlot);
      const totalOverflowAndSafetyMan = cushMan + overflowTaxableEquityMan;
      const nisaEl = document.getElementById('gbaScreen4NisaRoadmap');
      if (nisaEl) {
        nisaEl.innerHTML =
          '<div class="pw-kicker" style="margin-bottom:6px;">第3章 — 新NISA 1,800万円法定上限完全準拠（合計一致検証：' + fmtManYenJp(nisaGrowthSlot + nisaTsumitateSlot + totalOverflowAndSafetyMan) + ' / ' + fmtManYenJp(totalMan) + '）</div>' +
          '<h3 style="margin:0 0 10px;font-size:1.15rem;color:#0F172A;">成長投資枠1,200万円＋つみたて枠600万円＋超過分の安全配置（1円も消失しない完全配分）</h3>' +
          '<div style="display:grid;gap:10px;font-size:0.94rem;color:#334155;">' +
          '<div style="padding:12px;background:#F8FAFC;border-left:3px solid #0F172A;border-radius:6px;"><strong>1. 新NISA 成長投資枠（年間上限240万円・生涯上限1,200万円 ／ 配置額：' + fmtManYenJp(nisaGrowthSlot) + '）：</strong> 現物1倍ETFである <strong>SMH × XLV</strong> を法定上限1,200万円まで優先配置します（3倍レバレッジETF・短期債SGOVは新NISA枠を使いません）。</div>' +
          '<div style="padding:12px;background:#F8FAFC;border-left:3px solid #065F46;border-radius:6px;"><strong>2. 新NISA つみたて投資枠（年間上限120万円・生涯上限600万円 ／ 配置額：' + fmtManYenJp(nisaTsumitateSlot) + '）：</strong> 成長枠1,200万円を超える長期株式分は、金融庁届出済みの低コスト広範インデックス投信で最大600万円の生涯非課税枠を5年計画で活用します。</div>' +
          '<div style="padding:12px;background:#F8FAFC;border-left:3px solid #64748B;border-radius:6px;"><strong>3. 生涯非課税枠超過分 ＆ 安全クッション（合計配置額：' + fmtManYenJp(totalOverflowAndSafetyMan) + ' ＝ 安全資産 ' + fmtManYenJp(cushMan) + ' ＋ 非課税枠超過分 ' + fmtManYenJp(overflowTaxableEquityMan) + '）：</strong> 新NISA対象外の安全バッファおよび1,800万円超過分は、<strong>個人向け国債（変動10年・元本割れなし）</strong>または<strong>特定口座（源泉徴収あり）内の SGOV・現物ETF</strong> に明確に分離配置します（米国ETF配当には米国10%源泉徴収＋日本課税の外国税額控除対象ルールを適用）。</div>' +
          '</div>';
      }

      const brokerEl = document.getElementById('gbaScreen4BrokerGuide');
      if (brokerEl) {
        brokerEl.innerHTML =
          '<div class="pw-kicker" style="margin-bottom:6px;">第4章 — 楽天証券・SBI証券 大きな文字（18px+）5分安全注文図解ガイド</div>' +
          '<h3 style="margin:0 0 10px;font-size:1.15rem;color:#0F172A;">見間違い・高値掴みを防ぐ4ステップ確認手順</h3>' +
          '<ol style="margin:0;padding-left:22px;font-size:1.02rem;line-height:1.85;color:#1E293B;">' +
          '<li><strong>注文時間帯の確認：</strong> 米国市場オープン直後15分間（日本時間23:30〜23:45／冬時間0:30〜0:45）のスプレッド拡大を避け、落ち着いた時間帯または事前の指値予約を利用します。</li>' +
          '<li><strong>ティッカーと現物1倍の確認：</strong> 楽天証券（iSPEED）またはSBI証券（米国株アプリ）で <strong>SMH</strong>・<strong>XLV</strong>・<strong>SGOV</strong> を検索し、レバレッジ型ではない現物ETFであることを確認します。</li>' +
          '<li><strong>「成行」ではなく必ず「指値（Limit）」を選択：</strong> 口座区分（「NISA成長投資枠」または「特定預り」）を確認のうえ、現在値付近の指値注文で安全に発注します。</li>' +
          '<li><strong>点検は年2回（1月・7月）のみ：</strong> 毎日の株価ニュースに振り回されず、半年ごとの比率確認だけで穏やかな老後時間を守ります。</li>' +
          '</ol>';
      }

      const rebalDue = (gbaLiveTempScoreJp >= 78 || gbaLiveTempScoreJp <= 22);
      const verdictTxt = rebalDue
        ? '【今月の1秒判定：過去データ比率の定期点検タイミング】'
        : '【今月の1秒判定：維持して安心してお休みください】';
      const monthlyEl = document.getElementById('gbaScreen4MonthlyCard');
      if (monthlyEl) {
        monthlyEl.innerHTML =
          '<div class="pw-kicker" style="margin-bottom:6px;">第5章 — 毎月1日『月次あんしん成績表』＆ 月1回『会員匿名Q&amp;A回報』</div>' +
          '<div style="padding:12px 16px;border-radius:8px;background:' + (rebalDue ? '#FEF3C7' : '#ECFDF5') + ';color:' + (rebalDue ? '#92400E' : '#065F46') + ';font-weight:800;font-size:1.02rem;margin-bottom:10px;">' + verdictTxt + ' ・ 市場温度 ' + gbaLiveTempScoreJp + ' / 100（' + gbaLiveTempDateJp + ' 基準）</div>' +
          '<p style="margin:0 0 8px;font-size:0.96rem;color:#334155;"><strong>先月の変動クッション要約：</strong> 半導体現物（SMH）にヘルスケア（XLV）と安全資産（' + fmtManYenJp(cushMan) + '）を組み合わせた2本柱ケースは、ハイテク単独保有と比べて穏やかな値動きを維持しました。</p>' +
          '<p style="margin:0;font-size:0.94rem;color:#475569;"><strong>今月の匿名Q&amp;A抜粋：</strong>「Q. 為替（円高・円安）が気になるときはどう考えればよいですか？」→「A. 米国株ETF（ドル資産）と日本円建ての個人向け国債（変動10年）を併用することで、通貨面でも自然な分散クッションが働きます（※教育目的の一般解説）。」</p>';
      }

      const satEl = document.getElementById('gbaSatisfactionMount');
      if (satEl && !satEl.__mounted && window.DreamCompanyCRM && typeof window.DreamCompanyCRM.mountSatisfactionBar === 'function') {
        satEl.__mounted = true;
        window.DreamCompanyCRM.mountSatisfactionBar(satEl, { div: 'GBA', context: 'screen4_paid_vault_jp', email: getSavedGbaEmailJp() });
      }
    }

    function onGbaManYenInput() {
      const inp = document.getElementById('gbaCustomManYenInput');
      pwAnswersJp.scale = Math.max(100, Number(inp ? inp.value : 1800) || 1800);
      renderGbaScreen4VaultJp();
    }

    function openGbaCustomPdfWindowJp() {
      renderGbaScreen4VaultJp();
      const s1 = (document.getElementById('gbaScreen4YenTable') || {}).innerHTML || '';
      const s2 = (document.getElementById('gbaScreen4StressTest') || {}).innerHTML || '';
      const s3 = (document.getElementById('gbaScreen4NisaRoadmap') || {}).innerHTML || '';
      const s4 = (document.getElementById('gbaScreen4BrokerGuide') || {}).innerHTML || '';
      const s5 = (document.getElementById('gbaScreen4MonthlyCard') || {}).innerHTML || '';
      const w = window.open('', '_blank');
      if (!w) { window.print(); return; }
      w.document.write(
        '<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><title>GetBreakAI セルフサービス自動計算統計ワークブックPDF</title>' +
        '<style>body{font-family:"Hiragino Kaku Gothic ProN",Meiryo,sans-serif;max-width:780px;margin:24px auto;padding:0 20px;color:#0f172a;font-size:16px;line-height:1.72;}table{width:100%;border-collapse:collapse;margin:12px 0;font-size:14px;}th,td{border:1px solid #cbd5e1;padding:9px 10px;text-align:left;}th{background:#f1f5f9;}.page-break{page-break-before:always;margin-top:26px;padding-top:18px;border-top:2px solid #0f172a;}@media print{.no-print{display:none;}}</style></head><body>' +
        '<div class="no-print" style="padding:12px;background:#ecfdf5;border:1px solid #059669;border-radius:8px;margin-bottom:18px;"><strong>PDF保存の準備が完了しました：</strong> 印刷画面で「PDFに保存」を選択してください。 <button onclick="window.print()" style="margin-left:12px;padding:8px 16px;background:#065f46;color:#fff;border:none;border-radius:6px;font-weight:700;cursor:pointer;">PDFとして保存・印刷</button></div>' +
        '<h1>GetBreakAI — 新NISA・SMH &times; XLV ＋ 安全資産 セルフサービス自動計算統計ワークブック</h1>' +
        '<p style="font-size:13px;color:#475569;">独立系リサーチ出版（教育目的データ・投資助言非該当 ・ お問い合わせ: support@getbreakai.com）</p>' +
        '<div>' + s1 + '</div><div style="margin-top:18px;">' + s2 + '</div>' +
        '<div class="page-break">' + s3 + '</div><div class="page-break">' + s4 + '</div><div class="page-break">' + s5 + '</div>' +
        '</body></html>'
      );
      w.document.close();
      setTimeout(function() { try { w.print(); } catch (_) {} }, 350);
    }

    function submitGbaPaidMagicEmailJp(ev) {
      if (ev && ev.preventDefault) ev.preventDefault();
      const inp = document.getElementById('gbaPaidMagicEmailInput');
      const st = document.getElementById('gbaPaidMagicStatus');
      const em = String(inp && inp.value ? inp.value : getSavedGbaEmailJp()).trim().toLowerCase();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(em)) {
        if (st) {
          st.style.display = 'block';
          st.style.color = '#991B1B';
          st.textContent = '正しいメールアドレスをご入力ください。';
        }
        return false;
      }
      if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.deliverPaidMagicPack === 'function') {
        window.DreamCompanyCRM.deliverPaidMagicPack({
          div: 'GBA',
          email: em,
          plan_tier: (localStorage.getItem('gb_vip_plan') === 'annual') ? '年間リサーチパス（¥29,800/年）' : '月額リサーチパス（¥4,400/月）',
          order_ref: localStorage.getItem('gb_vip_license_key') || 'GBA-MAGIC-LINK',
          base_url: 'https://getbreakai.com/jp/',
          hash_anchor: 'gbaPaidScreen4VaultJp',
          profile_state: pwAnswersJp
        }).then(function(res) {
          if (st) {
            st.style.display = 'block';
            st.style.color = '#065F46';
            st.textContent = em + ' 宛に永久復元マジックリンク（未閲覧7日返金・1クリック解約案内付き）を送信しました。';
          }
          const rf = document.getElementById('gbaOneClickRefundLink');
          if (rf && res && res.refund_support_url) rf.href = res.refund_support_url;
        });
      }
      return false;
    }

    function showPwScreenJp(screenNum) {
      pwCurrentScreenJp = screenNum;
      let isVipUnlocked = (screenNum === 4);
      try {
        if (localStorage.getItem('gb_vip_unlocked') === 'true') isVipUnlocked = true;
      } catch (_) {}
      const s0 = document.getElementById('pwScreen0Jp');
      const s1 = document.getElementById('pwScreen1Jp');
      const s2 = document.getElementById('gbaMorningClubJp');
      const s3 = document.getElementById('pricing');
      const s4 = document.getElementById('gbaPaidScreen4VaultJp');
      if (s0) s0.style.display = (screenNum === 0) ? 'block' : 'none';
      if (s1) s1.style.display = (screenNum === 1) ? 'block' : 'none';
      if (s2) s2.style.display = (screenNum >= 2) ? 'block' : 'none';
      if (s3) s3.style.display = (screenNum >= 2) ? 'block' : 'none';
      if (s4) s4.style.display = (screenNum === 4 || (screenNum >= 2 && isVipUnlocked)) ? 'block' : 'none';
      if (screenNum >= 2) {
        syncPwStage2UiJp();
        if (s4 && s4.style.display === 'block') renderGbaScreen4VaultJp();
      }
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function showPwQuestionStepJp(stepNum) {
      pwCurrentStepJp = Math.max(1, Math.min(4, stepNum));
      document.querySelectorAll('[data-pw-qpane-jp]').forEach(function(el) {
        el.style.display = (Number(el.getAttribute('data-pw-qpane-jp')) === pwCurrentStepJp) ? 'block' : 'none';
      });
      const cLbl = document.getElementById('pwStepCounterJp');
      if (cLbl) cLbl.textContent = 'STEP 0' + pwCurrentStepJp + ' OF 04';
      const fill = document.getElementById('pwStepProgressFillJp');
      if (fill) fill.style.width = (pwCurrentStepJp * 25) + '%';
      document.querySelectorAll('[data-pw-jfield]').forEach(function(btn) {
        const f = btn.getAttribute('data-pw-jfield');
        const v = btn.getAttribute('data-pw-jval');
        const act = String(pwAnswersJp[f]) === String(v);
        btn.classList.toggle('is-selected', act);
      });
    }

    function startPwStepUpJp() {
      showPwQuestionStepJp(1);
      showPwScreenJp(1);
    }

    function prevPwStepJp() {
      if (pwCurrentStepJp > 1) {
        showPwQuestionStepJp(pwCurrentStepJp - 1);
      } else {
        showPwScreenJp(0);
      }
    }

    function selectPwOptionJp(field, val) {
      pwAnswersJp[field] = val;
      try { localStorage.setItem('gba_pw_stepup_answers_v1', JSON.stringify(pwAnswersJp)); } catch (_) {}
      showPwQuestionStepJp(pwCurrentStepJp);
      if (pwCurrentStepJp < 4) {
        setTimeout(function() { showPwQuestionStepJp(pwCurrentStepJp + 1); }, 150);
      }
    }

    function submitPwAssessmentJp() {
      if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.trackFunnelEvent === 'function') {
        window.DreamCompanyCRM.trackFunnelEvent('GBA', 'quiz_complete');
      }
      showPwScreenJp(2);
    }

    function editPwInputsJp() {
      showPwQuestionStepJp(1);
      showPwScreenJp(1);
    }

    function submitPwFreeGateJp(ev) {
      if (ev && ev.preventDefault) ev.preventDefault();
      const hp = document.getElementById('gba-jp-club-hp');
      if (hp && hp.value) return false;
      const inp = document.getElementById('gba-jp-club-email');
      const st = document.getElementById('pwGateStatusJp');
      const btn = document.getElementById('gba-jp-club-submit');
      const email = String(inp ? inp.value : '').trim().toLowerCase();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
        if (st) {
          st.style.display = 'block';
          st.style.color = '#991B1B';
          st.textContent = '正しいメールアドレスをご入力ください。';
        }
        if (inp && inp.focus) inp.focus();
        return false;
      }
      if (btn) { btn.disabled = true; btn.textContent = '登録中...'; }

      const b = computePwBaselineJp();
      const noteStr = 'site=getbreakai.com/jp/ | study_ratio=' + b.headline + ' | ' + b.summary;
      try {
        const kst = new Date(Date.now() + 9 * 3600 * 1000).toISOString().slice(0, 10);
        localStorage.setItem('gba_jp_free_email', email);
        localStorage.setItem('gb_free_member_email', email);
        localStorage.setItem('gba_jp_free_since', kst);
        localStorage.setItem('dc_member_GBA', JSON.stringify({
          div: 'GBA', email: email, nickname: '', segment: 'nisa_wealth_defense', notes: noteStr, joined_at: new Date().toISOString()
        }));
        if (typeof window.trackGbaFreeSignup === 'function') window.trackGbaFreeSignup(email);
      } catch (_) {}

      const done = function(res) {
        if (btn) { btn.disabled = false; btn.innerHTML = (res && res.ok) ? '保存・購読登録済み' : '再試行する'; }
        if (st) {
          st.style.display = 'block';
          if (res && res.ok) {
            st.style.color = '#065F46';
            st.textContent = 'サーバー登録完了：毎朝の朝刊リサーチノートを ' + email + ' 宛にお届けします（いつでも1クリック解除OK）。';
          } else {
            st.style.color = '#991B1B';
            st.textContent = '一時的な通信エラーが発生しました。少し時間をおいて再度お試しください。';
          }
        }
        syncPwStage2UiJp();
      };

      if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.registerMember === 'function') {
        window.DreamCompanyCRM.registerMember({
          div: 'GBA', email: email, nickname: '', segment: 'nisa_wealth_defense', lang: 'ja-JP', notes: noteStr, message: noteStr
        }).then(done).catch(function() { done({ ok: false }); });
      } else {
        done({ ok: false });
      }
      return false;
    }

    function jumpFromManualToJpMail() {
      if (typeof window.closeGbaStarterManualModal === 'function') window.closeGbaStarterManualModal();
      showPwScreenJp(2);
    }

    function openPwRestoreModalJp() {
      const m = document.getElementById('pwRestoreModalJp');
      if (!m) return;
      const saved = getSavedGbaEmailJp();
      const inp = document.getElementById('pwRestoreEmailJp');
      if (inp && saved && !inp.value) inp.value = saved;
      m.classList.add('is-open');
    }

    function closePwRestoreModalJp() {
      const m = document.getElementById('pwRestoreModalJp');
      if (m) m.classList.remove('is-open');
    }

    function downloadProtectedGbaPdfJp() {
      var btn = document.getElementById('btnDownloadGbaMaster12pPdf');
      if (btn) { btn.dataset.origLabel = btn.dataset.origLabel || btn.textContent; btn.textContent = '12p PDFをダウンロード準備中...'; btn.disabled = true; }
      var resetBtn = function(msg) {
        if (!btn) return;
        btn.disabled = false;
        btn.textContent = msg || btn.dataset.origLabel || '12p 新NISA完全版ワークブックPDFをダウンロード →';
        if (msg) setTimeout(function() { btn.textContent = btn.dataset.origLabel || '12p 新NISA完全版ワークブックPDFをダウンロード →'; }, 3500);
      };
      if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.openProtectedPdfDownload === 'function') {
        return Promise.resolve(window.DreamCompanyCRM.openProtectedPdfDownload('GBA', 'gba_jp_nisa_12p', function() {
          resetBtn();
          openPwRestoreModalJp();
        })).then(function(res) {
          if (res && res.ok) resetBtn('✓ 12p 完全版PDFのダウンロードを開始しました');
          else resetBtn();
          return res;
        }).catch(function() {
          resetBtn();
          openPwRestoreModalJp();
          return false;
        });
      }
      resetBtn();
      openPwRestoreModalJp();
      return false;
    }
    window.downloadProtectedGbaPdfJp = downloadProtectedGbaPdfJp;

    function requestGbaOtpJp() {
      const emInp = document.getElementById('pwRestoreEmailJp');
      const st = document.getElementById('jpHubVipStatus');
      const em = String(emInp ? emInp.value : '').trim().toLowerCase();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(em)) {
        if (st) {
          st.style.display = 'block';
          st.style.color = '#991B1B';
          st.textContent = '先にWhop決済時のメールアドレスをご入力ください。';
        }
        return false;
      }
      if (st) {
        st.style.display = 'block';
        st.style.color = '#334155';
        st.textContent = '6桁ワンタイム認証コードを送信しています...';
      }
      if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.requestAuthOtp === 'function') {
        window.DreamCompanyCRM.requestAuthOtp({ div: 'GBA', email: em }).then(function() {
          if (st) {
            st.style.display = 'block';
            st.style.color = '#065F46';
            st.textContent = '有効なご購入履歴が確認された場合、6桁認証コードをメール送信しました（10分間有効）。上の欄へ入力して認証してください。';
          }
        });
      }
      return false;
    }

    function syncStoredVipKeysOnHub() {
      // Client-only key length checks disabled for Zero-Bypass security; active sessions verify server-side.
      return;
    }

    function submitPwRestoreJp(ev) {
      if (ev && ev.preventDefault) ev.preventDefault();
      const emInp = document.getElementById('pwRestoreEmailJp');
      const licInp = document.getElementById('jpHubLicenseInput');
      const st = document.getElementById('jpHubVipStatus');
      const em = String(emInp ? emInp.value : '').trim().toLowerCase();
      const lic = String(licInp ? licInp.value : '').trim();

      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(em)) {
        if (st) {
          st.style.display = 'block';
          st.style.color = '#991B1B';
          st.textContent = 'Whop決済時にご使用されたメールアドレスをご入力ください。';
        }
        return false;
      }
      const isSixDigitOtp = /^\d{6}$/.test(lic);
      if (!lic || (!isSixDigitOtp && lic.length < 6)) {
        if (st) {
          st.style.display = 'block';
          st.style.color = '#991B1B';
          st.textContent = 'アクセスコード・領収書IDを入力するか、「6桁コードを送信」ボタンを押してください。';
        }
        return false;
      }
      if (st) {
        st.style.display = 'block';
        st.style.color = '#334155';
        st.textContent = 'サーバーでWhop会員権限を照合しています...';
      }
      const reqPayload = isSixDigitOtp
        ? { div: 'GBA', email: em, otp: lic }
        : { div: 'GBA', email: em, access_code: lic };
      const vp = (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.verifyEntitlement === 'function')
        ? window.DreamCompanyCRM.verifyEntitlement(reqPayload)
        : Promise.resolve({ authorized: false });
      vp.then(function(vres) {
        try {
          localStorage.setItem('gba_jp_free_email', em);
          localStorage.setItem('gb_free_member_email', em);
        } catch (_) {}
        if (vres && vres.authorized) {
          try {
            localStorage.setItem('gb_vip_unlocked', 'true');
            localStorage.setItem('gb_vip_license_key', isSixDigitOtp ? 'OTP-VERIFIED' : lic);
            localStorage.setItem('gb_vip_key', isSixDigitOtp ? 'OTP-VERIFIED' : lic);
          } catch (_) {}
          if (st) {
            st.style.display = 'block';
            st.style.color = '#065F46';
            st.textContent = '有料会員パスが確認されました。12p完全版ワークブック画面を開きます。';
          }
          setTimeout(function() { closePwRestoreModalJp(); showPwScreenJp(4); }, 450);
        } else {
          try { localStorage.removeItem('gb_vip_unlocked'); } catch (_) {}
          if (st) {
            st.style.display = 'block';
            st.style.color = '#991B1B';
            st.textContent = '有効なWhop決済履歴が確認できませんでした。「6桁コードを送信」をお試しいただくか support@getbreakai.com へご連絡ください。';
          }
        }
      });
      return false;
    }

    function bindJpHubWhopCheckoutBridge() {
      if (window.__jpHubWhopMsgBound) return;
      window.__jpHubWhopMsgBound = true;
      window.addEventListener('message', function(msgEvt) {
        try {
          if (!msgEvt || !msgEvt.origin) return;
          const origHost = new URL(String(msgEvt.origin)).hostname.toLowerCase();
          if (origHost !== 'whop.com' && !origHost.endsWith('.whop.com')) return;
          const payload = typeof msgEvt.data === 'string' ? JSON.parse(msgEvt.data) : msgEvt.data;
          if (payload && (payload.event === 'checkout.complete' || payload.type === 'checkout.succeeded' || payload.status === 'succeeded')) {
            if (typeof window.closeGbaWhopCheckoutModal === 'function') window.closeGbaWhopCheckoutModal();
            openPwRestoreModalJp();
          }
        } catch (_) {}
      });
    }

    window.addEventListener('DOMContentLoaded', function() {
      try {
        const savedTheme = localStorage.getItem('gb_jp_theme');
        if (savedTheme === 'dark' || savedTheme === 'light') {
          document.documentElement.setAttribute('data-jp-theme', savedTheme);
        }
      } catch (_) {}

      window.GBA_COPY_MODE = (window.PAYMENT_CONFIG && window.PAYMENT_CONFIG.STORE_LIVE_READY) ? 'LIVE_SHARP' : 'UNDERWRITING_SAFE';
      loadPwSavedAnswersJp();
      showPwQuestionStepJp(1);
      syncStoredVipKeysOnHub();
      bindJpHubWhopCheckoutBridge();
      hydrateGbaLiveTempBadgeJp();

      try {
        if (window.DreamCompanyCRM && typeof window.DreamCompanyCRM.decodeMagicRestoreParam === 'function') {
          const mObj = window.DreamCompanyCRM.decodeMagicRestoreParam(window.location.search || '');
          if (mObj && typeof mObj === 'object' && mObj.email && mObj.access_code && typeof window.DreamCompanyCRM.verifyEntitlement === 'function') {
            if (mObj.objective) pwAnswersJp.objective = mObj.objective;
            if (mObj.scale) pwAnswersJp.scale = Number(mObj.scale) || 1800;
            if (mObj.comfort) pwAnswersJp.comfort = mObj.comfort;
            if (mObj.techMix) pwAnswersJp.techMix = mObj.techMix;
            localStorage.setItem('gba_pw_stepup_answers_v1', JSON.stringify(pwAnswersJp));
            localStorage.setItem('gba_jp_free_email', String(mObj.email).toLowerCase());
            window.DreamCompanyCRM.verifyEntitlement({
              div: 'GBA',
              email: mObj.email,
              access_code: mObj.access_code,
              magic_restore: true
            }).then(function(vr) {
              if (vr && vr.authorized) {
                localStorage.setItem('gb_vip_unlocked', 'true');
                showPwScreenJp(4);
              } else {
                openPwRestoreModalJp();
              }
            });
            return;
          }
        }
        const params = new URLSearchParams(window.location.search || '');
        const h = (window.location.hash || '').toLowerCase();
        if (params.get('payment') === 'success' || params.get('checkout_status') === 'succeeded') {
          openPwRestoreModalJp();
        } else if (h === '#pricing' || h === '#gbamorningclubjp') {
          showPwScreenJp(2);
        }
      } catch (_) {}
    });
