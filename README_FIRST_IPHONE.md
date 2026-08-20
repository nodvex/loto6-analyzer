# iPhoneだけで公開する手順
1. GitHubで `loto6-analyzer` というPublic Repositoryを作成。
2. このZIPをiPhoneの「ファイル」で展開し、フォルダ構造を保ってGitHubへアップロード。
3. GitHub → Actions → `Bootstrap / Update Loto6 Data` → Run workflow → `第1回から全データを再構築` をON。
4. 完了後、Settings → Pages → Sourceを `GitHub Actions` にする。
5. `Deploy GitHub Pages` 完了後、表示URLをSafariで開く。
6. Safari共有 → 「ホーム画面に追加」。

以後、月曜・木曜20:30/22:30（Asia/Tokyo）に自動更新します。
必要ならActionsから手動更新できます。
