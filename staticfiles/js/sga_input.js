let currentStep = 1;
let sgaStep = 0;
let sgaValues = { SGA: null, IK: null, PP: null };

function nextStep() {
  const current = document.getElementById(`step-${currentStep}`);
  const next = document.getElementById(`step-${currentStep + 1}`);
  if (current && next) {
    current.style.display = 'none';
    next.style.display = 'block';
    currentStep++;
  }
}

function nextSGAIKPP() {
  const input = document.getElementById("inputField");
  let value = input.value.trim();

  console.log("Raw input:", value);

  if (value === "") {
    alert("Please enter a value.");
    return;
  }

  const intVal = parseInt(value, 10);
  console.log("Parsed integer:", intVal);

  if (isNaN(intVal)) {
    alert("Please a enter a valid integer.");
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
    console.log("Submitting form with:", sgaValues);
    document.getElementById("multiStepForm").submit();
  }
}
