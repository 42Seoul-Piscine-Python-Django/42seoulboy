function handle_up() {
  document.getElementById("btn-up").click();
}

function handle_down() {
  document.getElementById("btn-down").click();
}

function handle_left() {
  document.getElementById("btn-left").click();
}

function handle_right() {
  document.getElementById("btn-right").click();
}

function handle_a() {
  document.getElementById("btn-a").click();
}
function handle_left() {
  document.getElementById("btn-b").click();
}

function handle_start() {
  document.getElementById("btn-start").click();
}

function handle_select() {
  document.getElementById("btn-select").click();
}

window.addEventListener("keydown", (event) => {
  if (event.key === "w" || event.key === "ArrowUp") {
    return handle_up();
  }
  if (event.key === "s" || event.key === "ArrowDown") {
    return handle_down();
  }
  if (event.key === "a" || event.key === "ArrowLeft") {
    return handle_left();
  }
  if (event.key === "d" || event.key === "ArrowRight") {
    return handle_up();
  }
  if (event.key === "n") {
    return handle_a();
  }
  if (event.key === "m") {
    return handle_b();
  }
  if (event.key === "o") {
    return handle_select();
  }
  if (event.key === "p") {
    return handle_start();
  }
});
