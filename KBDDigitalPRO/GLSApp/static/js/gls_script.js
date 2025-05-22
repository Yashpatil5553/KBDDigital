function showInput(base) {
    const label = document.getElementById("inputLabel");
    const inputField = document.getElementById("inputField");
    const inputDiv = document.getElementById("inputDiv");

    if (base === "income") {
        label.textContent = "";
        inputField.placeholder = "Enter Target Income";
    } else if (base === "sales") {
        label.textContent = "";
        inputField.placeholder = "Enter Target Sales";
    } else if (base === "team") {
        label.textContent = "";
        inputField.placeholder = "Enter Target Team";
    }

    inputDiv.style.display = "block";
    inputField.value = "";
    document.getElementById("calculateBtn").disabled = true;
}


function checkInputValue() {
    const value = document.getElementById("inputField").value;
    const calculateBtn = document.getElementById("calculateBtn");
    calculateBtn.disabled = !value;
}


document.addEventListener("DOMContentLoaded", () => {
    const sections = document.querySelectorAll(".section");
    const nextBtn = document.getElementById("nextBtn");
    const backBtn = document.getElementById("backBtn");
    const redirectBtn = document.getElementById("redirectBtn");
  
    let currentIndex = 0;
  
    function showSection(index) {
      sections.forEach((section, i) => {
        section.style.display = i === index ? "block" : "none";
        section.style.opacity = i === index ? "1" : "0";
      });
  
      backBtn.style.display = index > 0 ? "inline-block" : "none";
      nextBtn.style.display = index < sections.length - 1 ? "inline-block" : "none";
      redirectBtn.style.display = index === sections.length - 1 ? "inline-block" : "none";
    }
  
    nextBtn.onclick = () => {
      if (currentIndex < sections.length - 1) {
        currentIndex++;
        showSection(currentIndex);
      }
    };
  
    backBtn.onclick = () => {
      if (currentIndex > 0) {
        currentIndex--;
        showSection(currentIndex);
      }
    };
  
    showSection(currentIndex);
  });

 
  