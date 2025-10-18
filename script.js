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
    // ✅ 更新時刻の表示
    if (data['更新時刻']) {
      const updatedTime = document.getElementById('updated-time');
      updatedTime.textContent = `更新日時：${data['更新時刻']}`;
    }

    const content = document.getElementById('content');

    // ✅ 期間ラベルを動的に取得（更新時刻を除外）
    const sections = Object.keys(data).filter(key => key !== '更新時刻');

    sections.forEach(section => {
      const block = document.createElement('section');
      block.innerHTML = `
        <h2>${section}</h2>
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
