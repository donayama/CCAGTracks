# LIMINAL ATLAS OST Bible - Common

このファイルは、シリーズ全体で共通して参照する方針・付録情報を集約したもの。
個別トラック仕様は `tracks.md` を参照。

# 架空ゲームサントラ OSTバイブル v4
## LIMINAL ATLAS シリーズ 全40作 設定資料集
### AceStep プロンプト制作用 内部資料

---

# CURATORIAL MANIFESTO / シリーズ編集方針

## このプロジェクトが「おいしい」と判断する音楽の基準

本Bibleの全タイトルの音楽設計・AceStepプロンプト生成・ライナーノーツ執筆において、以下の方針を常に最優先の判断軸とする。タイトルごとにジャンル・テンポ・編成は大きく異なるが、この方針はハイテンポのフュージョンにもスロウなバラードにも等しく適用される。

---

### 優先順位 1 ——「捕獲力」

**最初の数秒でリスナーの心拍が変わること。**

イントロなしでいきなりサビから始まる。あるいは最初の数音でもう「何かが起きている」と分からせる盛り上がりイントロ。バラードであれば1音目の音色・和音・余白が「これは普通ではない」と告げる。

どのトラックも「始まった瞬間に存在感を放つ」設計を優先する。ゆっくり本題に入るトラックは、その「ゆっくり」自体が掴みとして機能していなければならない。

**AceStep設計原則：** 冒頭の設計を必ず記述する。「○小節目から始まる」ではなく「1音目・1小節目に何が起きているか」を明示する。

---

### 優先順位 2 ——「疾走感」

**前に引っ張られる推進力・グルーヴがあること。**

BPMを速くするだけでは出ない。リフの食い込み方、ベースラインの推進力、次の小節への「引き」が連続して生まれる設計の問題だ。スロウなトラックでも「次の音への引力」は存在できる——テンポではなくグルーヴが疾走感を作る。

「乗れる」「前のめりになる」「止められない」という身体反応を引き出すことが目標。聴き手が能動的に音楽に引っ張られている状態。

**AceStep設計原則：** ベースライン・リフの「食い込み」「シンコペーション」「次への引き」を具体的に記述する。疾走感はドラムだけでもベースだけでも出ない——複数の声部が同じ方向に引っ張るときに生まれる。

---

### 優先順位 3 ——「スルメ感」

**何度聴いても耳に引っかかるものが残り続けること。**

1回目に全部聴こえる必要はない。2回目に気づくフック、10回目に発見するレイヤーがあっていい。しかし1回目でも「また聴きたい」と思わせる何かが必ず存在すること。

そのための設計として「耳に刺さるフレーズの繰り返し周期」「ゲームの外で聴いても意味を持つ音楽的完結性」「毎回わずかに違うソロ・ランダム要素」を積極的に使う。

**排除する設計：** 雰囲気だけで押す・フックを持たない環境音楽的処理・「悪くないが引っかからない」状態。

---

### 優先順位 4 ——「音圧・密度」

**音が物理的に身体に刺さってくること。**

BPMを速くするだけでは解決しない。何層が同時に鳴っているか、それぞれの音色が役割を持っているか、最大密度の「全部乗せ」がどれだけ圧力を持っているか。

アコースティック編成でもエレクトリック編成でも「物量で来る」感覚は設計できる。電気的音圧に頼れない場合は「全抜き→全部乗せ」の落差で物理的な衝撃を作る。

**AceStep設計原則：** 使用楽器の列挙ではなく「何が何層で、最大時に何が鳴っているか」を具体的に記述する。

---

### 優先順位 5 ——「メリハリ」

**動と静の落差が腕を掴むこと。**

静がなければ動は存在しない。全抜き・無音・単音への瞬間的な収縮が、次の爆発を2〜3倍の衝撃にする。この「抜き」の設計は全タイトルに必須で、その位置・長さ・深さを具体的に設計すること。

スロウなトラックでも「抜き」は存在する——音数を絞る・音色を変える・リズムを一瞬止める。「静かな曲」と「抜きのある曲」は別物だ。

---

### 排除する美学（このプロジェクトで「おいしくない」とする判断）

以下は架空ゲームサントラとして設計上「意図的に避ける」美学だ。ジャンルによっては存在してもよいが、それが「このタイトルのおいしい部分」として前面に出ることを避ける。

- **雰囲気内協・平和主義的BGM** ——場面の邪魔をしないだけの音楽。音楽がそこにいる理由がない状態。鳴っていても鳴っていなくても同じ、という設計は失敗だ。
- **小奇麗にまとめた仕上がり** ——尖りを削って万人向けにした結果、誰の記憶にも残らない音楽。「悪くない」は「おいしくない」と同義だ。

---

### このシリーズの音楽がめざす状態

1. **最初の数秒で「これは何か」と思わせる個性を持つ。**
2. **ゲームの外でも単体のサントラとして完結し成立する。**
3. **耳でなく脳に直接刺さるフレーズ・リフの到達感がある。**

---

### 冒頭設計チェックリスト（全タイトル共通）

AceStepプロンプト生成前に以下を確認する：

- [ ] **1音目・1小節目に何が起きているか**を一文で言えるか
- [ ] **最大密度時に何層が何の音色で鳴っているか**を具体的に書いたか
- [ ] **全抜きの位置・長さ・深さ**を設計したか
- [ ] **耳に残るフックが何で、何小節周期で来るか**を明示したか
- [ ] **「おいしくない美学」のいずれかに寄っていないか**を確認したか

---


---

## 付録A：両スタジオ 対照表

| 項目 | Pale Signal Games | Ironclad Sound AB |
|---|---|---|
| 本拠地 | テキサス州オースティン（USA） | ストックホルム（Sweden） |
| 設立 | 2015年 | 2017年 |
| スタッフ規模 | 約11名（インディー） | 約52名（AA） |
| 音楽ディレクター | Marcus Hale（元ジャズドラマー） | Eva Lindqvist（元メタルギタリスト） |
| 主要プラットフォーム | Steam / Xbox / Xbox Game Pass | PS5 / Steam / Xbox（後期） |
| 価格帯 | $9.99〜$14.99（Steam中価格帯） | $19.99〜$34.99（AA価格帯） |
| サントラ販売 | Bandcamp独立販売（ゲームより売れる） | 公式サイト＋SpotifyのみでBandcampなし |
| 受賞歴 | IGF Excellence in Audio 2勝 | BAFTA Games 音楽部門 3勝 |
| 海外認知度 | サントラ経由での発見が多い | PS Store / メディアレビュー経由 |
| 両スタジオの出会い | GDCにて Marcus Hale と Eva Lindqvist が初対面 | → 20番「Temporal Glitch: Hotfix」共同開発へ |

---

## 付録B：Series I ↔ Series II 音楽的対応関係

| Series I（Pale Signal） | Series II（Ironclad Sound） | 音楽的対応 |
|---|---|---|
| 01 深海都市（アクア・ファンク BPM112〜116） | 11 鋼鉄要塞（メタルコア×テクノ BPM180） | 水の揺らぎ vs 鋼鉄の衝撃 |
| 02 オートパイロット（アンビエント BPM128） | 12 オーバークロック（ニューロファンク BPM174→182） | AIの静寂 vs AIの暴走 |
| 03 蒸気都市（和ジャズ×ファンク BPM118〜120） | 13 竜騎士団（シンフォニックメタル BPM180） | 帝都の粋 vs 天空の咆哮 |
| 04 電脳ハイウェイ（テクノ×シティポップ BPM130〜134） | 14 地下闘技場（ジャングル×ハードベース BPM180） | 思考の高速道路 vs 肉体の激突 |
| 05 魔法学園（DnB×オーケストラ BPM170〜174） | 17 古代遺跡（DnB×民族音楽 BPM178〜182） | 学院の夜 vs 遺跡の崩壊 |
| 06 輸送船（スペースロック×ディスコ BPM118〜122） | 15 海賊艦橋（スペースメタル×DnB BPM176〜180） | 宇宙の孤独な航行 vs 宇宙の混乱した戦闘 |
| 07 グリッチ（IDM×ヴェイパー BPM140〜150） | 20 時間断層（マスコア×IDM BPM180） | デバッグの日常 vs 時間の崩壊 |
| 08 スカイウェイ（フレンチ×バレアリック BPM126〜128） | 18 反重力レース（電子×生楽器 BPM180） | 空の巡航 vs 空の激走 |
| 09 カジノ（エレクトロスウィング BPM128〜132） | 19 魔王軍（ブラックメタル×オーケストラ BPM180） | 死の享楽 vs 死の戦場 |
| 10 氷の惑星（ポストロック×シューゲ BPM100→140） | 16 光速列車（ハードコア×ストリングス BPM180） | 惑星の静かな熱 vs 列車の爆発的速度 |

---

## 付録C：AceStep プロンプト共通パラメータ

### Series I 共通指針（Pale Signal Games）
- **ムード：** immersive, deep focus, cinematic but restrained, indie atmospheric
- **避けるべき要素：** lo-fi, chill, relaxing, background music（これらはNG）
- **推奨する要素：** groove, pulse, texture, depth, subtle complexity
- **共通の音楽設計原則：**
  - メロディは断片化・着地させない
  - ベースラインで集中を維持
  - 展開はモルフィングのみ・突然の転換を避ける
  - 60〜90分版を想定したシームレスループ設計
  - 「なぜか飽きない」という体験を音楽工学的に設計する

### Series II 共通指針（Ironclad Sound AB）
- **ムード：** high-energy, adrenaline focus, zone state, nordic precision
- **避けるべき要素：** emotional catharsis, melodic resolution, lo-fi, relaxing
- **推奨する要素：** drive, momentum, precision, power, controlled aggression
- **共通の音楽設計原則：**
  - リズムで身体を支配する
  - 「命令音」モチーフ（2〜3音）が全曲を貫く
  - カウントダウン／カウントアップ構造
  - BPM180固定または意図的に加速する設計
  - コードはマイナー固定・感情の揺れを最小化しながら緊張感だけを維持

---
*LIMINAL ATLAS シリーズ 全20作 OSTバイブル v3 完*
*Pale Signal Games（テキサス州オースティン）× Ironclad Sound AB（ストックホルム）*
*AceStep プロンプト制作用 内部資料 v3.0*

---
---

# SERIES III：独立タイトル群

---

## 付録D：全40作 タイトル一覧（統合版）

| # | タイトル（日本語） | 英題 | スタジオ | ジャンル | 音楽系統 |
|---|---|---|---|---|---|
| 01 | 深海都市のネオン・ダイブ | Abyss Groove City | Pale Signal Games | ノワールADV | アシッド・ジャズ×ダブ |
| 02 | 終末世界のオートパイロット | Autopilot: End Protocol | Pale Signal Games | AI管理SLG | アンビエント×モジュラー |
| 03 | 蒸気都市のネオ・エド・クルーズ | Steam Samurai Cruise | Pale Signal Games | 策謀RPG | 和ジャズ×ファンク |
| 04 | 電脳世界のハイウェイ・パズル | Neural Highway | Pale Signal Games | 高速パズル | シティポップ×テクノ |
| 05 | 魔法学園のミッドナイト・フライ | Midnight Academy | Pale Signal Games | スニークアクション | DnB×オーケストラ |
| 06 | 銀河間輸送船のロング・ラン | Haul: Interstellar | Pale Signal Games | 宇宙SLG | クラウトロック×スペースディスコ |
| 07 | グリッチ・ホラーのデバッグ | Neon Exploit | Pale Signal Games | ハッキングパズル | IDM×ヴェイパー |
| 08 | 空島スカイウェイのサンセット | Skyway Sunset | Pale Signal Games | レーシング探索 | バレアリック×フレンチハウス |
| 09 | 死者の街の深夜ギャンブル | Dead City Casino | Pale Signal Games | ノワールADV | エレクトロスウィング |
| 10 | 氷の惑星のクリスタル・ラリー | Crystal Rally: Cryosphere | Pale Signal Games | 地形改造レース | ポストロック×シューゲイザー |
| 11 | 鋼鉄要塞の最終突破 | Iron Breach: Last Gate | Ironclad Sound AB | タクティカルシューター | メタルコア×テクノ |
| 12 | 神経回路のオーバークロック | Neural Overdrive | Ironclad Sound AB | AIハッキング | ニューロファンク×グリッチ |
| 13 | 天空竜騎士団の出撃 | Skydragon Scramble | Ironclad Sound AB | 空中戦略RPG | シンフォニックメタル×アニソン |
| 14 | 地下闘技場の覇者ルート | Underground Champion | Ironclad Sound AB | 格闘×RPG | ジャングル×ハードベース |
| 15 | 宇宙海賊旗艦の艦橋 | Corsair Bridge: Battle Stations | Ironclad Sound AB | 宇宙SLG | スペースメタル×DnB |
| 16 | 光速列車の緊急制御 | Emergency: Mach Line | Ironclad Sound AB | 緊急対応SIM | ハードコア×ストリングス |
| 17 | 古代遺跡のタイムアタック | Ruin Rush: Zero Second | Ironclad Sound AB | ダンジョン脱出 | DnB×民族音楽 |
| 18 | 反重力レースの最終ラップ | Anti-Grav: Final Lap | Ironclad Sound AB | 反重力レース | エレクトロ×ロック |
| 19 | 魔王軍総攻撃の前線 | Demon Vanguard: The Surge | Ironclad Sound AB | 大規模SLG | ブラックメタル×オーケストラ |
| 20 | 時間断層のバグ修正 | Temporal Glitch: Hotfix | 両社共同 | メタフィクションRPG | マスコア×IDM |
| 21 | 霓虹の格子都市 | Neon Grid Architect | Sublayer Works | 都市建設SIM | Progressive Trance |
| 22 | 魔法回路、侵蝕中 | Arcane Circuit: Runebreaker | Iron Glyph Studio | アクションRPG | オーケストラ→Gabber変容 |
| 23 | 理論値という名の幽霊 | Perfect Lap Standard | Threshold Lap Co. | タイムアタックレース | ハードバップ×精度 |
| 24 | 調性の迷宮 | Modulation Depths | Harmonic Rogue Lab | ローグライク | 和声ジャズ×音楽理論 |
| 25 | バリオ・ロホ 炎の回廊 | Barrio Rojo: Combate | Tablao Digital | 横スクアクション | フラメンコ×ブレリア |
| 26 | 対位法という遊び | Fugue Matrix | Contrapuntal Games | ライン消去パズル | 4声フーガ×チェンバロ |
| 27 | 霊魂は拳で語る | Soul Strike | Frequency Bout Studio | 1対1格闘 | スローテンポR&B |
| 28 | 黙示録は賛美歌の顔をしている | Neon Apocrypha | Vesper Code | シナリオ重視ADV | ダークR&B×賛美歌構造 |
| 29 | ループが割れる夜 | Loop Fracture | Null Frame Studio | 時間巻き戻しアクション | IDM×逆再生 |
| 30 | 息と息のあいだ | Echo Between Breaths | Tidal Silence Works | 短編時間干渉探索 | 尺八×ヴァイオリン対話 |

---
*Series III 完 / Series IV「J-RPGオマージュ戦闘曲系譜」へ続く*
*Pale Signal Games × Ironclad Sound AB × Independent Studios × Resonant Arc Studio*
*AceStep プロンプト制作用 内部資料 v4.0*
---
---

# SERIES IV：J-RPGオマージュ戦闘曲系譜

---

# SERIES IV 全体対照表

| No. | タイトル | 日本題 | 区分 | 音楽軸 | 主オマージュ | BPM（戦闘） |
|---|---|---|---|---|---|---|
| 31 | Banner of the Far Roads | 遠道の旗手たち | ストレート | 群像オーケストラ | DQ4 | 132〜168 |
| 32 | Ashen Throne Tactics | 灰色の玉座と戦記 | ストレート | 重厚戦記シンフォニック | ロマサガ2 | 144〜156 |
| 33 | Glass Circuit Testament | ガラス回路の遺言 | ストレート | 都市SFドラマ | FF7 | 132〜148 |
| 34 | Rune Breaker: Frontier Pulse | ルーンブレイカー：辺境の鼓動 | ストレート | 古典高速アクション | Ys I&II | 172〜188 |
| 35 | Sunwake on the Tidal Isle | 潮島の夜明け | ストレート | 漂流冒険ロック | Ys8 | 148〜172 |
| 36 | Rootgrave Atlas | 根墓回廊地図帳 | ストレート | 迷宮踏破 | 世界樹（無印） | 148〜184 |
| 37 | Blue Archive of Ragolight | 羅光の青い遺録 | ストレート | 未来惑星探索 | PSO | 132〜180 |
| 38 | Starwoven Cartography | 星織の地図誌 | ミックス | 迷宮×未来探索 | 世界樹×PSO | 148〜172 |
| 39 | Blazebanner | 炎旗の戦場 | ミックス | 戦記×高速ロック | ロマサガ2×Ys | 152〜184 |
| 40 | Crown of Null Beasts | 虚無の獣冠 | 無双 | ボス様式博覧会 | 系譜全般 | ボス別 |

*Series IV完 / LIMINAL ATLAS シリーズ 全40作*

