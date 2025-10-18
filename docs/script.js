function formatDate(dateStr) {
  const date = new Date(dateStr);
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  return `${year}年${month}月${day}日`;
}

fetch('ranking.json')
  .then(response => response.json())
  .then(data => {
    if (data['更新時刻']) {
      const updatedTime = document.getElementById('updated-time');
      updatedTime.textContent = `最終更新：${data['更新時刻']}`;
    }

    const content = document.getElementById('content');
    const sections = Object.keys(data).filter(key => key !== '更新時刻');

    sections.forEach(section => {
      const block = document.createElement('section');

      // ラベル生成（日付 or 開始日〜終了日）
      let label = '';
      if (data[section].日付) {
        label = data[section].日付 + 'のランキング';
      } else if (data[section].開始日 && data[section].終了日) {
        label = `${data[section].開始日}9時00分から${data[section].終了日}8時59分の累計ランキング`;
      } else {
        label = section; // フォールバック
      }

      block.innerHTML = `
        <h2>${section}</h2>
        <p><strong>${label}</strong></p>
        <table>
          <thead>
            <tr><th>順位</th><th>記事タイトル</th><th>閲覧数</th></tr>
          </thead>
          <tbody>
            ${data[section].ランキング.map((item, index) => `
              <tr>
                <td>${index + 1}</td>
                <td>${item.title}</td>
                <td>${item.views.toLocaleString()}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;
      content.appendChild(block);
    });
  })
  .catch(error => {
    document.getElementById('content').innerHTML = `<p>ランキングデータの読み込みに失敗しました。</p>`;
    console.error('読み込みエラー:', error);
  });
