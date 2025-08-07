document.getElementById('queryForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const pdfFile = document.getElementById('pdf').files[0];
  const query = document.getElementById('query').value;

  if (!pdfFile || !query) {
    alert('Please upload a PDF and enter your query.');
    return;
  }

  const formData = new FormData();
  formData.append('pdf', pdfFile);
  formData.append('query', query);

  const response = await fetch('http://127.0.0.1:5000/query', {
    method: 'POST',
    body: formData,
  });

  const data = await response.json();

  document.getElementById('output').classList.remove('hidden');
  document.getElementById('metadata').textContent = JSON.stringify(data.metadata, null, 2);

  const clausesEl = document.getElementById('clauses');
  clausesEl.innerHTML = '';
  data.top_matches.forEach((match, i) => {
    const p = document.createElement('p');
    p.textContent = `${i + 1}. ${match.clause} (score: ${match.score.toFixed(4)})`;
    clausesEl.appendChild(p);
  });

  document.getElementById('answer').textContent = data.answer;
});

