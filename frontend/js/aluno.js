 const apiUrl = 'http://127.0.0.1:8000/aluno/'

fetch(apiUrl)
  .then(res => res.json())
  .then(dados => {
    const tbody = document.getElementById("tabela-alunos");

    dados.forEach(item => {
      const tr = document.createElement("tr");

      tr.innerHTML = `
        <td>${item.id}</td>
        <td>${item.nome}</td>
        <td>${item.curso}</td>
        <td>${item.email}</td>
        <td>${item.endereco}</td>
        <td>${item.telefone}</td>
        }
      `;

      tbody.appendChild(tr);
    });
  });
