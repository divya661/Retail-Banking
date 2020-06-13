var citiesByState = {
  Odisha: ["Bhubaneswar", "Puri", "Cuttack"],
  Maharashtra: ["Mumbai", "Pune", "Nagpur"],
  Kerala: ["kochi", "Kanpur"]
}
function makeSubmenu(value) {
  if (value.length == 0) document.getElementById("citySelect").innerHTML = "<option></option>";
  else {
    var citiesOptions = "";
    for (cityId in citiesByState[value]) {
      citiesOptions += "<option>" + citiesByState[value][cityId] + "</option>";
    }
    document.getElementById("citySelect").innerHTML = citiesOptions;
  }
}
function displaySelected() {
  var country = document.getElementById("countrySelect").value;
  var city = document.getElementById("citySelect").value;
  var id = document.getElementById("id").value;
  var name = document.getElementById("name").value;
  var age = document.getElementById("age").value;
  var address = document.getElementById("address").value;

  if (id.length == 9 && id.match(/^\d+/)) {
    if (age.match(/^\d+/)) {
      alert("SSN No. " + id + "\n" + "Name " + name + "\n" + "Age " + age + "\n" + "Address " + address + "\n" + "Country " + country + "\n" + "City " + city);
    }
    else {
      alert("Age must be numeric")
    }

  }
  else {
    alert("Customer SSN Id must be numeric & 9 characters long")
  }


}
function resetSelection() {
  document.getElementById("countrySelect").selectedIndex = 0;
  document.getElementById("citySelect").selectedIndex = 0;
}