let currentStep = 1;
let sgaStep = 0;
let sgaValues = { SGA: null, IK: null, PP: null };

function nextStep() {
  const current = document.getElementById(`step-${currentStep}`);
  const inputs = current.querySelectorAll('input[required]');
  for (let input of inputs) {
    if (!input.value.trim()) {
      alert("Please fill all required fields before proceeding.");
      input.focus();
      return;
    }
    if (input.type === "number" && isNaN(parseFloat(input.value))) {
      alert("Please enter valid numbers.");
      input.focus();
      return;
    }
  }
  const next = document.getElementById(`step-${currentStep + 1}`);
  if (current && next) {
    current.style.display = 'none';
    next.style.display = 'block';
    currentStep++;
  }
}

function prevStep() {
  // Special handling for SGA/IK/PP dynamic input step
  if (currentStep === 6 && sgaStep > 0) {
    const input = document.getElementById("inputField");
    sgaStep--;

    if (sgaStep === 1) {
      document.getElementById("label").innerHTML = "<h2>IK</h2>";
      input.placeholder = "Enter IK Target";
      input.value = sgaValues.IK ?? "";
      input.focus();
    } else if (sgaStep === 0) {
      document.getElementById("label").innerHTML = "<h2>SGA</h2>";
      input.placeholder = "Enter SGA Target";
      input.value = sgaValues.SGA ?? "";
      input.focus();
    }
    return;
  }

  // Default behavior for other steps
  if (currentStep > 1) {
    const current = document.getElementById(`step-${currentStep}`);
    const prev = document.getElementById(`step-${currentStep - 1}`);
    if (current && prev) {
      current.style.display = 'none';
      prev.style.display = 'block';
      currentStep--;
    }
  }
}


function nextSGAIKPP() {
  const input = document.getElementById("inputField");
  let value = input.value.trim();
  if (value === "") {
    alert("Please enter a value.");
    return;
  }
  const intVal = parseInt(value, 10);
  if (isNaN(intVal)) {
    alert("Please enter a valid integer.");
    return;
  }
  if (sgaStep === 0) {
    sgaValues.SGA = intVal;
    document.getElementById("label").innerHTML = "<h2>IK</h2>";
    input.placeholder = "Enter IK Target";
    input.value = "";
    input.focus();
    sgaStep++;
  } else if (sgaStep === 1) {
    sgaValues.IK = intVal;
    document.getElementById("label").innerHTML = "<h2>PP</h2>";
    input.placeholder = "Enter PP Target";
    input.value = "";
    input.focus();
    sgaStep++;
  } else if (sgaStep === 2) {
    sgaValues.PP = intVal;
    document.getElementById("sgaInput").value = sgaValues.SGA;
    document.getElementById("ikInput").value = sgaValues.IK;
    document.getElementById("ppInput").value = sgaValues.PP;
    console.log("✅ Submitting form:", sgaValues);
    document.getElementById("multiStepForm").submit();
  }
}
