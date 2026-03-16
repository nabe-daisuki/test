VR酔い（VRシックネス）は「目は動いている映像を見ているのに、体（前庭感覚）は動いていない」などの感覚のズレや、遅延（レイテンシ）・低フレームレートなどで起きやすくなります VirtualSpeech VIVE Blog Unity

まず効きやすい「即効性の高い」対策（優先順）
1) 移動方式を「テレポート」系にする
滑らかにスティック移動（Smooth-move）するほど酔いやすく、Teleport-move（テレポート移動）やDash-move（ダッシュ移動）が楽になりやすいです Road to VR

2) 旋回は「スナップターン」にする（体で回るのも有効）
Snap-turn（段階的にカクッと回る）は「comfortable for most」とされ、Smooth-turn（滑らか回転）は「comfortable for least（最もしんどくなりがち）」と整理されています Road to VR

3) 視野を狭める設定（ビネット／ブラインダー／トンネル）をON
周辺視野の動きが強いほど酔いやすいので、Blinders（= vignette：視野をクロップして周辺の動きを減らす）を使うのが定番です Road to VR

体と環境で効く対策（わりと即効）
4) 扇風機を自分に当てる／涼しくする・座って遊ぶ
冷やす・座るのはよく効きます（姿勢の安定にも寄与）。VirtualSpeech は「Keep cool」「Sit down」を推奨しています VirtualSpeech

5) 休憩ルールを決める（“我慢しない”）
不快感が出たら押し切らずに中断。VIVEは20〜30分ごとの休憩も勧めています VIVE Blog

6) 空腹・満腹を避ける／水分補給
VIVEは「水分補給」「直前の重い食事を避ける」が効くと述べています VIVE Blog

機器・画質の“酔いに直結”ポイント（重要）
7) カクつき・遅延があるコンテンツは避ける（最重要）
レイテンシ（遅延）や低フレームレートは酔いを増やします。VIVEは「Low frame rates… amplifies latency」のように説明しています VIVE Blog  
Unityも、サイバーシックネス要因としてlag（遅延）や refresh rateなどを挙げています Unity

8) ヘッドセットの装着・IPD（瞳孔間距離）調整を見直す
VIVEはIPD調整やしっかり固定してブレを減らすことを挙げています VIVE Blog

9) 画面が強すぎるなら明るさを下げる
VirtualSpeechはヘッドセットの明るさを下げることも提案しています VirtualSpeech

慣らし（体質改善）：一番“長期的に効く”やり方
VirtualSpeech は、段階的にプレイ時間を増やす方法を具体的に提案しています（例：  
最初の週：数日おきに5分 → 次の週：週2回10分 → 数週間かけて15分を目標）VirtualSpeech

ポイントは「気持ち悪くなる前に切り上げて、良い状態で終える」です。

酔いを感じたら（その場のリカバリー手順）
1) すぐ停止（我慢しない） VIVE Blog  
2) ヘッドセットを外して、風に当たる（扇風機があると強い）VirtualSpeech  
3) 次回は「テレポート移動＋スナップターン＋ビネット強め」から再開 Road to VR

参考（図解・動画）
図解（原因のイメージが掴める）
- VirtualSpeechの記事内図（3DoF/6DoFなど）  
  VirtualSpeech: Degrees of Freedom  
  出典: VirtualSpeech

YouTube（日本語で手早く見たい場合）
- 「[VR] 7 tips to prevent VR sickness, even for beginners [Meta Quest]」(7:31)  
  https://www.youtube.com/watch?v=l3cHrb5XcZ8
- 「今すぐ試せる！…5つのVR酔い対策」(12:56)  
  https://www.youtube.com/watch?v=VzBKmSKs63E

あなた向けに最適化できます
使っている機器（Quest/PSVR2/PCVRなど）と、酔いやすい状況（VRChatの移動、FPS、車・ジェットコースター系、スティック移動など）を教えてください。そのタイトルの設定項目名に合わせて「どれをON/OFFにするか」を短く手順化します。