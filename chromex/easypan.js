const EIDS = [
  'ApplicantTitle',
  'firstname',
  'middlename',
  'lastname',
  'father_firstname',
  'father_middlename',
  'father_lastname',
  'cardname',
  'pan_state',
  'dob',
  'Aadhaar_No',
  'Aadhaar_name',
  'c_houseno',
  'c_village',
  'c_post',
  'c_District',
  'c_State',
  'c_PIN',
  'contactno',
];

const readFile = (file) =>
  new Promise((resolve, reject) => {
    var reader = new FileReader();
    reader.onload = (e) => {
      // Code.
      let data = JSON.parse(e.target.result);
      resolve(data);
    };
    reader.readAsText(file);
  });

const copy2clip = (text) => {
  const ELEMENT_ID = 'copy_el_id';
  // Add An Element To Dom;
  var textArea = document.createElement('textarea');
  textArea.value = text;
  textArea.id = ELEMENT_ID;
  // Avoid scrolling to bottom
  textArea.style.top = '0';
  textArea.style.left = '0';
  textArea.style.position = 'fixed';
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();
  // Actual Copy Command;
  document.execCommand('copy');
  // Remove That Element From Dom;
  document.getElementById(ELEMENT_ID).remove();
};

const download = (text, name, type) => {
  var file = new Blob([text], { type: type });
  var a = document.createElement('a');
  a.href = URL.createObjectURL(file);
  a.download = name;
  a.click();
};

const create_ui = () => {
  // Craete;
  const root = document.createElement('div');
  root.setAttribute('id', 'epan_ui_root');

  const getBtn = document.createElement('button');
  getBtn.setAttribute('class', 'button_jst');
  getBtn.setAttribute('id', 'dump_form');

  const setBtn = document.createElement('button');
  setBtn.setAttribute('class', 'button_jst');
  setBtn.setAttribute('id', 'load_form');

  const file_input = document.createElement('input');
  file_input.setAttribute('id', 'file_json');
  file_input.setAttribute('type', 'file');
  file_input.setAttribute('accept', '.json');

  getBtn.innerText = 'Dump';
  setBtn.innerText = 'Load';

  root.appendChild(getBtn);
  root.appendChild(setBtn);
  root.appendChild(file_input);
  document.body.appendChild(root);

  // Add Buttons Click Handler;
  getBtn.addEventListener('click', dump_form);
  setBtn.addEventListener('click', () => file_input.click());
  file_input.addEventListener('change', load_form);
};

/* Get Form Data As Json */
function dump_form() {
  formData = {}; // Empty Data Placeholder;
  EIDS.forEach((id) => (formData[id] = document.getElementById(id).value));
  // copy2clip(JSON.stringify(formData));
  download(
    JSON.stringify(formData),
    formData['cardname'] + '.json',
    'application/json'
  );
}

/* Fill Form Form Json File */
function load_form(e) {
  if (e.target.files.length < 1) return;
  const file = e.target.files[0];
  readFile(file).then((data) => {
    const event = new Event('change');
    EIDS.forEach((id) => {
      let el = document.getElementById(id);
      el.value = data[id];
      el.dispatchEvent(event);
    });
  });
}

create_ui();
