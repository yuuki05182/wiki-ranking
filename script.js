// script.js

// 表示する順番（ranking.jsonのキー）
const sections = [
  '一昨日',
  '3日前',
  '過去7日間',
  '9日前〜15日前',
  '過去30日間'
];

// JSONを読み込んで表示
fetch('ranking.json')
  .then(response => response.json())
  .then(data => {
    const content = document.getElementById('content');

    sections.forEach(section => {
      const block = document.createElement('section');
      block.innerHTML = `
        <h2>${section}</h2>
        <p><strong>${data[section].日付 || `${data[section].開始日}〜${data[section].終了日}`}</strong></p>
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
