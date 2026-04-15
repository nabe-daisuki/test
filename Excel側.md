' ==================================================
' WebCapture VBAモジュール
' 事前作成したPowerShellスクリプトを呼び出して
' Webサイトのスクリーンショットを取得・貼り付け
' ==================================================
Option Explicit

' 設定定数
Private Const PS1_FILENAME As String = "WebCapture.ps1"
Private Const DEFAULT_WAIT_SEC As Long = 6
Private Const DEFAULT_BROWSER As String = "edge"
Private Const IMG_WIDTH As Long = 800
Private Const IMG_HEIGHT As Long = 600

' ==================================================
' 単一URLのスクリーンショット取得
' ==================================================
Public Sub CaptureWebsite()
    
    ' ===== 設定項目（ここを変更してください） =====
    Dim targetURL As String
    Dim pasteCell As String
    
    targetURL = "https://www.yahoo.co.jp"     ' 対象URL
    pasteCell = "B2"                          ' 貼り付け先セル
    ' =============================================
    
    Dim ps1Path As String
    Dim imgPath As String
    Dim success As Boolean
    
    ' PowerShellスクリプトのパス取得
    ps1Path = GetPowerShellScriptPath()
    If ps1Path = "" Then Exit Sub
    
    ' 一時画像ファイルパス
    imgPath = CreateTempImagePath()
    
    ' 画面更新停止
    Application.ScreenUpdating = False
    Application.StatusBar = "Webスクリーンショット取得中..."
    
    ' PowerShellスクリプト実行
    success = ExecuteWebCapture(ps1Path, targetURL, imgPath, DEFAULT_WAIT_SEC, DEFAULT_BROWSER)
    
    If success And FileExists(imgPath) Then
        ' 画像をシートに貼り付け
        Call PasteImageToSheet(ActiveSheet, imgPath, pasteCell)
        
        ' 一時ファイル削除
        DeleteFile imgPath
        
        MsgBox "スクリーンショットを取得しました！" & vbCrLf & _
               "セル " & pasteCell & " に貼り付けました。", vbInformation, "取得完了"
    Else
        MsgBox "スクリーンショットの取得に失敗しました。" & vbCrLf & _
               "URLやブラウザ設定を確認してください。", vbCritical, "取得失敗"
    End If
    
    Application.StatusBar = False
    Application.ScreenUpdating = True
    
End Sub

' ==================================================
' 複数URL一括処理
' シート構成:
'   A列: URL
'   B列: 貼り付け先セル（例: D5）
'   C列: 結果（自動記入）
'   D列: 実行日時（自動記入）
' ==================================================
Public Sub BatchCaptureWebsites()
    
    Dim ws As Worksheet
    Dim ps1Path As String
    Dim lastRow As Long
    Dim i As Long
    Dim url As String
    Dim cellAddr As String
    Dim imgPath As String
    Dim success As Boolean
    Dim successCount As Long
    Dim failCount As Long
    
    Set ws = ActiveSheet
    
    ' PowerShellスクリプトのパス取得
    ps1Path = GetPowerShellScriptPath()
    If ps1Path = "" Then Exit Sub
    
    ' データ範囲確認
    lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row
    If lastRow < 2 Then
        MsgBox "A列にURLを入力してください（2行目から開始）。", vbExclamation, "データなし"
        Exit Sub
    End If
    
    ' 初期化
    Application.ScreenUpdating = False
    successCount = 0
    failCount = 0
    
    ' ヘッダー設定
    ws.Range("A1:D1").Value = Array("URL", "貼り付けセル", "結果", "実行日時")
    ws.Range("A1:D1").Font.Bold = True
    
    ' 各URLを順次処理
    For i = 2 To lastRow
        url = Trim(ws.Cells(i, "A").Value)
        cellAddr = Trim(ws.Cells(i, "B").Value)
        
        ' 空行はスキップ
        If url = "" Then GoTo NextURL
        
        ' 貼り付け先が未指定の場合はデフォルト設定
        If cellAddr = "" Then cellAddr = "F" & i
        
        ' プログレス表示
        Application.StatusBar = _
            "処理中 " & (i - 1) & "/" & (lastRow - 1) & " : " & Left(url, 50) & "..."
        
        ' 一時画像ファイルパス
        imgPath = CreateTempImagePath("batch_" & i)
        
        ' スクリーンショット取得実行
        success = ExecuteWebCapture(ps1Path, url, imgPath, DEFAULT_WAIT_SEC, DEFAULT_BROWSER)
        
        If success And FileExists(imgPath) Then
            ' 成功: 画像を貼り付け
            Call PasteImageToSheet(ws, imgPath, cellAddr)
            ws.Cells(i, "C").Value = "✅ 成功"
            ws.Cells(i, "D").Value = Format(Now, "yyyy/mm/dd hh:mm:ss")
            DeleteFile imgPath
            successCount = successCount + 1
        Else
            ' 失敗
            ws.Cells(i, "C").Value = "❌ 失敗"
            ws.Cells(i, "D").Value = Format(Now, "yyyy/mm/dd hh:mm:ss")
            failCount = failCount + 1
        End If
        
        ' 次のURL処理前に少し待機（サーバー負荷軽減）
        Application.Wait Now + TimeValue("00:00:02")
        
NextURL:
    Next i
    
    Application.StatusBar = False
    Application.ScreenUpdating = True
    
    ' 結果表示
    MsgBox "一括処理が完了しました！" & vbCrLf & vbCrLf & _
           "✅ 成功: " & successCount & " 件" & vbCrLf & _
           "❌ 失敗: " & failCount & " 件", vbInformation, "処理完了"
    
End Sub

' ==================================================
' PowerShellスクリプト実行の共通関数
' ==================================================
Private Function ExecuteWebCapture( _
    ByVal ps1Path As String, _
    ByVal url As String, _
    ByVal imgPath As String, _
    ByVal waitSec As Long, _
    ByVal browser As String) As Boolean
    
    On Error GoTo ErrorHandler
    
    Dim wsh As Object
    Dim cmd As String
    Dim exitCode As Long
    
    ' PowerShell実行コマンド組み立て
    cmd = "powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden" & _
          " -File """ & ps1Path & """" & _
          " -url """ & url & """" & _
          " -outputPath """ & imgPath & """" & _
          " -waitSec " & waitSec & _
          " -browser """ & browser & """"
    
    ' WScript.Shellで実行
    Set wsh = CreateObject("WScript.Shell")
    exitCode = wsh.Run(cmd, 0, True)  ' 0=非表示, True=完了まで待機
    Set wsh = Nothing
    
    ExecuteWebCapture = (exitCode = 0)
    Exit Function
    
ErrorHandler:
    ExecuteWebCapture = False
    
End Function

' ==================================================
' 画像をシートの指定セルに貼り付け
' ==================================================
Private Sub PasteImageToSheet( _
    ByVal ws As Worksheet, _
    ByVal imgPath As String, _
    ByVal cellAddr As String)
    
    On Error GoTo ErrorHandler
    
    Dim targetCell As Range
    Dim pic As Shape
    
    Set targetCell = ws.Range(cellAddr)
    
    ' 既存の画像を削除（重複防止）
    Dim shp As Shape
    For Each shp In ws.Shapes
        If InStr(shp.Name, "WebCapture_") > 0 Then
            If Not Intersect(shp.TopLeftCell, targetCell) Is Nothing Then
                shp.Delete
            End If
        End If
    Next shp
    
    ' 画像挿入
    Set pic = ws.Shapes.AddPicture( _
        Filename:=imgPath, _
        LinkToFile:=msoFalse, _
        SaveWithDocument:=msoCTrue, _
        Left:=targetCell.Left, _
        Top:=targetCell.Top, _
        Width:=IMG_WIDTH, _
        Height:=IMG_HEIGHT)
    
    pic.Name = "WebCapture_" & Format(Now, "hhmmss")
    Exit Sub
    
ErrorHandler:
    MsgBox "画像の貼り付けに失敗しました: " & Err.Description, vbCritical
    
End Sub

' ==================================================
' ユーティリティ関数群
' ==================================================

' PowerShellスクリプトのパスを取得
Private Function GetPowerShellScriptPath() As String
    
    Dim ps1Path As String
    ps1Path = ThisWorkbook.Path & "\" & PS1_FILENAME
    
    If Dir(ps1Path) = "" Then
        MsgBox "PowerShellスクリプトが見つかりません。" & vbCrLf & vbCrLf & _
               "以下の場所に " & PS1_FILENAME & " を配置してください:" & vbCrLf & _
               ThisWorkbook.Path, vbCritical, "ファイルが見つかりません"
        GetPowerShellScriptPath = ""
    Else
        GetPowerShellScriptPath = ps1Path
    End If
    
End Function

' 一時画像ファイルパス生成
Private Function CreateTempImagePath(Optional prefix As String = "capture") As String
    CreateTempImagePath = Environ("TEMP") & "\" & prefix & "_" & Format(Now, "yyyymmdd_hhmmss") & ".png"
End Function

' ファイル存在確認
Private Function FileExists(ByVal filePath As String) As Boolean
    FileExists = (Dir(filePath) <> "")
End Function

' ファイル削除（エラー無視）
Private Sub DeleteFile(ByVal filePath As String)
    On Error Resume Next
    If FileExists(filePath) Then Kill filePath
    On Error GoTo 0
End Sub
