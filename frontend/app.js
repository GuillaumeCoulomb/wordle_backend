async function init() {
  await fetch("/preinit", { credentials: "include" });
  const res = await fetch("/init", { credentials: "include" });
  const data = await res.json();
  renderGuesses(data.guesses);
}

async function submitGuess() {
  const word = document.getElementById("guessInput").value;
  if (word.length !== 5) return alert("Mot de 5 lettres requis !");
  const res = await fetch(`/guess?word=${word}`, {
    method: "POST",
    credentials: "include"
  });
  const data = await res.json();
  if (data.status === "ok") {
    refresh();
  }
}

async function refresh() {
  const res = await fetch("/state", { credentials: "include" });
  const data = await res.json();
  renderGuesses(data.guesses);
}