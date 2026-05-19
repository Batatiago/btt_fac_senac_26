let alunos = JSON.parse(localStorage.getItem("alunos")) || [];

const formAluno = document.getElementById("formAluno");
const tabelaAlunos = document.getElementById("tabelaAlunos");

function atualizarTabela() {
  tabelaAlunos.innerHTML = "";

  alunos.forEach(aluno => {
    const linha = document.createElement("tr");
    
    linha.innerHTML = `
      <td>${aluno.nome}</td>
      <td>${aluno.nota1.toFixed(1)}</td>
      <td>${aluno.nota2.toFixed(1)}</td>
      <td>${aluno.media.toFixed(1)}</td>
      <td>${aluno.situacao}</td>
    `;
    
    tabelaAlunos.appendChild(linha);
  });
}

// Renderiza os dados salvos assim que a página carrega
atualizarTabela();

formAluno.addEventListener("submit", function(e) {
  e.preventDefault();

  const nomeValor = document.getElementById("nome").value.trim();
  const nota1Valor = parseFloat(document.getElementById("nota1").value);
  const nota2Valor = parseFloat(document.getElementById("nota2").value);

  if (nomeValor === "") {
    alert("É preciso digitar algum nome!");
    return;
  }

  if (isNaN(nota1Valor) || nota1Valor < 0 || nota1Valor > 10) {
    alert("É preciso digitar uma nota entre 0 e 10 no campo Nota 1!");
    return;
  }
  if (isNaN(nota2Valor) || nota2Valor < 0 || nota2Valor > 10) {
    alert("É preciso digitar uma nota entre 0 e 10 no campo Nota 2!");
    return;
  }

  const mediaCalculada = (nota1Valor + nota2Valor) / 2;
  let situacaoFinal = "";

  if (mediaCalculada >= 6) {
    situacaoFinal = "Aprovado";
  } else if (mediaCalculada >= 2) {
    situacaoFinal = "Exame Final";
  } else {
    situacaoFinal = "Reprovado";
  }

  const novoAluno = {
    nome: nomeValor,
    nota1: nota1Valor,
    nota2: nota2Valor,
    media: mediaCalculada,
    situacao: situacaoFinal
  };

  alunos.push(novoAluno);

  localStorage.setItem("alunos", JSON.stringify(alunos));
  atualizarTabela();
  formAluno.reset();
});