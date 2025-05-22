function updateTotals() {
    const agri = parseFloat(document.querySelector('[name="agriculture"]').value) || 0;
    const swas = parseFloat(document.querySelector('[name="swastham"]').value) || 0;
    const ayur = parseFloat(document.querySelector('[name="ayurman"]').value) || 0;
    const pari = parseFloat(document.querySelector('[name="paridhan"]').value) || 0;
  
    const total = agri + swas + ayur + pari;
    const remaining = Math.max(0, 100 - total);
  
    const totalEl = document.getElementById("total");
    totalEl.textContent = total.toFixed(2) + "%";
    document.getElementById("remaining").textContent = remaining.toFixed(2); 
  
    // Reset status color
    totalEl.classList.remove("status-blue", "status-green", "status-red");
  
    if (Math.abs(total - 100) < 0.01) {
      totalEl.classList.add("status-blue");
    } else if (total < 100) {
      totalEl.classList.add("status-green");
    } else {
      totalEl.classList.add("status-red");
    }
  }
  
  document.addEventListener("DOMContentLoaded", () => {
    updateTotals();
  
    document.querySelectorAll('[name="agriculture"], [name="swastham"], [name="ayurman"], [name="paridhan"]').forEach(input => {
      input.addEventListener("input", updateTotals);
    });
  
    document.getElementById("sectorForm")?.addEventListener("submit", (e) => {
      const total = parseFloat(document.getElementById("total").textContent);
      if (Math.abs(total - 100) > 0.01) {
        e.preventDefault();
        alert("Total must be exactly 100%");
      }
    });
  });
  