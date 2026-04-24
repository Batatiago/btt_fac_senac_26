const form = document.getElementById("myForm");
const nameInput = document.getElementById("name");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");

form.addEventListener("submit", (e) => {
  e.preventDefault();

  const name = nameInput.value.trim();
  const email = emailInput.value.trim();
  const password = passwordInput.value.trim();

  if (name === "" || email === "" || password === "") {
    alert("Por favor, preencha todos os campos.");
    return;
  }

  // Aqui você pode adicionar código para enviar os dados para um servidor ou processá-los de outra forma
  console.log("Nome:", name);
  console.log("Email:", email);
  console.log("Senha:", password);

  alert("Formulário enviado com sucesso!");

  // Limpa os campos do formulário após o envio
  nameInput.value = "";
  emailInput.value = "";
  passwordInput.value = "";
});
