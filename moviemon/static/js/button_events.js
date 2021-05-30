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
function handle_b() {
  document.getElementById("btn-b").click();
}

function handle_start() {
  document.getElementById("btn-start").click();
}

function handle_select() {
  document.getElementById("btn-select").click();
}

window.addEventListener("keydown", (event) => {
  if (event.code === "KeyW" || event.code === "ArrowUp") {
    return handle_up();
  }
  if (event.code === "KeyS" || event.code === "ArrowDown") {
    return handle_down();
  }
  if (event.code === "KeyA" || event.code === "ArrowLeft") {
    return handle_left();
  }
  if (event.code === "KeyD" || event.code === "ArrowRight") {
    return handle_right();
  }
  if (event.code === "KeyN") {
    return handle_a();
  }
  if (event.code === "KeyM") {
    return handle_b();
  }
  if (event.code === "KeyO") {
    return handle_select();
  }
  if (event.code === "KeyP") {
    return handle_start();
  }
});
