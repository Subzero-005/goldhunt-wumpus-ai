let gridSize = 0;

function showError(data) {
  if (data.error) {
    document.getElementById('status').innerText = data.error;
    return true;
  }
  return false;
}

function startGame() {
  gridSize = document.getElementById('sizeInput').value;
  fetch('/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ size: gridSize })
  })
  .then(res => res.json())
  .then(data => { if (!showError(data)) updateGrid(data); });
}

function move(dir) {
  fetch('/move', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ direction: dir })
  })
  .then(res => res.json())
  .then(data => { if (!showError(data)) updateGrid(data); });
}

function runAI() {
  fetch('/ai')
    .then(res => res.json())
    .then(data => {
      if (showError(data)) return;
      let steps = data.steps;
      let i = 0;

      function step() {
        if (i < steps.length) {
          renderGrid({ grid: steps[i].grid });
          document.getElementById('status').innerText =
            steps[i].status || `AI Exploring: (${steps[i].pos[0]}, ${steps[i].pos[1]})`;
          i++;
          setTimeout(step, 500); // smoother & faster animation
        } else {
          const last = steps[steps.length - 1];
          document.getElementById('status').innerText =
            last.status && last.status !== 'Playing' ? last.status : 'AI Finished';
        }
      }

      step();
    });
}

function updateGrid(data) {
  renderGrid({ grid: data.grid });
  document.getElementById('status').innerText = data.status || 'Playing';
}
function renderGrid(data) {
  const grid = data.grid;
  const container = document.getElementById('grid');
  container.innerHTML = '';
  container.style.gridTemplateColumns = `repeat(${gridSize}, 48px)`; 

  grid.forEach(row => {
    row.forEach(cell => {
      const div = document.createElement('div');
      div.classList.add('grid-cell');

      if (cell === "danger") {
        div.classList.add('cell-danger');
        // Randomly add danger1 or danger2 class
        div.classList.add(Math.random() < 0.5 ? 'danger1' : 'danger2');
      } else {
        div.classList.add(`cell-${cell}`);
      }

      container.appendChild(div);
    });
  });
}

