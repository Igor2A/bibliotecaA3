 const apiUrl = 'http://127.0.0.1:8000/livro/'

fetch(apiUrl)
  .then(res => res.json())
  .then(dados => {
    const tbody = document.getElementById("tabela-livros");

    dados.forEach(item => {
      const tr = document.createElement("tr");

      tr.innerHTML = `
        <td>${item.id}</td>
        <td>${item.nome}</td>
        <td>${item.autor}</td>
        <td>${item.editora}</td>
        <td>${item.ano}</td>
        <td>${item.edicao}</td>
        <td>${item.numero_pags}</td>
        <td>${item.categoria}</td>
        <td>${item.idioma}</td>
      `;

      tbody.appendChild(tr);
    });
  });
