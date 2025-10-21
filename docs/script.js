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

    // ✅ 通常の日付別ランキング（先に表示）
    const sections = Object.keys(data).filter(key =>
      key !== '更新時刻' &&
      key !== '前日比増加率ランキング' &&
      key !== '週平均比増加率ランキング'
    );

    sections.forEach(section => {
      const block = document.createElement('section');
      block.innerHTML = `
        <h2>${section}</h2>
        <table class="ranking-table standard">
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

    // ✅ 特別セクション：前日比増加率ランキング（後ろに表示）
    if (data['前日比増加率ランキング']) {
      const block = document.createElement('section');
      block.innerHTML = `
        <h2>📈 前日比増加率ランキング</h2>
        <table class="ranking-table ratio">
          <thead>
            <tr><th>順位</th><th>記事タイトル</th><th>増加率</th><th>前日</th><th>最新</th></tr>
          </thead>
          <tbody>
            ${data['前日比増加率ランキング'].map((item, index) => `
              <tr>
                <td>${index + 1}</td>
                <td>${item.title}</td>
                <td>${(item.rate * 100).toFixed(2)}%</td>
                <td>${item.previous.toLocaleString()}</td>
                <td>${item.latest.toLocaleString()}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;
      content.appendChild(block);
    }

    // ✅ 特別セクション：週平均比増加率ランキング（後ろに表示）
    if (data['週平均比増加率ランキング']) {
      const block = document.createElement('section');
      block.innerHTML = `
        <h2>📈 週平均比増加率ランキング</h2>
        <table class="ranking-table ratio">
          <thead>
            <tr><th>順位</th><th>記事タイトル</th><th>増加率</th><th>週平均</th><th>最新</th></tr>
          </thead>
          <tbody>
            ${data['週平均比増加率ランキング'].map((item, index) => `
              <tr>
                <td>${index + 1}</td>
                <td>${item.title}</td>
                <td>${(item.rate * 100).toFixed(2)}%</td>
                <td>${Math.round(item.weekly_avg).toLocaleString()}</td>
                <td>${item.latest.toLocaleString()}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;
      content.appendChild(block);
    }
  })
  .catch(error => {
    document.getElementById('content').innerHTML = `<p>ランキングデータの読み込みに失敗しました。</p>`;
    console.error('読み込みエラー:', error);
  });
