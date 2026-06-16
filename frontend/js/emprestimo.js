 const apiUrl = 'http://127.0.0.1:8000/emprestimos/'

fetch(apiUrl)
  .then(res => res.json())
  .then(dados => {
    const tbody = document.getElementById("tabela-alunos");

    dados.forEach(item => {
      const tr = document.createElement("tr");

      tr.innerHTML = `
        <td>${item.id}</td>
        <td>${item.aluno}</td>
        <td>${item.livro}</td>
      `;

      tbody.appendChild(tr);
    });
  });
