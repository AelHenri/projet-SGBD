var counter = 1;
function addInput(){
	counter++;
	var newFields = document.getElementById('dynamicInput').cloneNode(true);
	newFields.id = '';
	var newField = newFields.childNodes;
	var insertHere = document.getElementById('writeroot');
	insertHere.parentNode.insertBefore(newFields,insertHere);
}